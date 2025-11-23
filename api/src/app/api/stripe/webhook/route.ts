import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { query } from '@/lib/db';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-11-17.clover',
});

const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

// Type extension for Stripe Subscription with period properties
// These properties exist in the API response but aren't in TypeScript definitions for this API version
type SubscriptionWithPeriod = Stripe.Subscription & {
  current_period_start: number;
  current_period_end: number;
};

export async function POST(request: NextRequest) {
  try {
    const body = await request.text();
    const signature = request.headers.get('stripe-signature')!;

    let event: Stripe.Event;

    try {
      event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
    } catch (err: any) {
      console.error('Webhook signature verification failed:', err.message);
      return NextResponse.json(
        { error: 'Invalid signature' },
        { status: 400 }
      );
    }

    // Handle the event
    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session;

        // Update order with payment success
        const orderId = session.metadata?.orderId;
        if (orderId) {
          await query(
            `UPDATE evaluation_orders
            SET
              payment_status = 'paid',
              stripe_payment_intent_id = $1,
              paid_at = NOW()
            WHERE id = $2`,
            [session.payment_intent as string, orderId]
          );

          // TODO: Trigger evaluation job (Redis queue, email notification, etc.)
          console.log(`Payment successful for order ${orderId}`);
          console.log(`Model: ${session.metadata?.modelName}`);
          console.log(`HuggingFace: ${session.metadata?.huggingfaceUrl}`);
          console.log(`Email: ${session.customer_email}`);
        }
        break;
      }

      case 'checkout.session.expired': {
        const session = event.data.object as Stripe.Checkout.Session;
        const orderId = session.metadata?.orderId;

        if (orderId) {
          await query(
            `UPDATE evaluation_orders
            SET payment_status = 'failed'
            WHERE id = $1`,
            [orderId]
          );
        }
        break;
      }

      case 'customer.subscription.created':
      case 'customer.subscription.updated': {
        const subscription = event.data.object as SubscriptionWithPeriod;

        // Handle enterprise subscription
        const session = await stripe.checkout.sessions.list({
          subscription: subscription.id,
          limit: 1,
        });

        if (session.data.length > 0) {
          const orderId = session.data[0].metadata?.orderId;
          const email = session.data[0].customer_email;

          if (orderId && email) {
            // Create or update enterprise subscription
            await query(
              `INSERT INTO enterprise_subscriptions (
                id,
                stripe_subscription_id,
                stripe_customer_id,
                email,
                status,
                current_period_start,
                current_period_end
              ) VALUES ($1, $2, $3, $4, $5, to_timestamp($6), to_timestamp($7))
              ON CONFLICT (stripe_subscription_id)
              DO UPDATE SET
                status = $8,
                current_period_start = to_timestamp($9),
                current_period_end = to_timestamp($10),
                updated_at = NOW()`,
              [
                orderId,
                subscription.id,
                subscription.customer as string,
                email,
                subscription.status,
                subscription.current_period_start,
                subscription.current_period_end,
                subscription.status,
                subscription.current_period_start,
                subscription.current_period_end,
              ]
            );
          }
        }
        break;
      }

      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription;

        await query(
          `UPDATE enterprise_subscriptions
          SET status = 'canceled', updated_at = NOW()
          WHERE stripe_subscription_id = $1`,
          [subscription.id]
        );
        break;
      }

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    return NextResponse.json({ received: true });
  } catch (error: any) {
    console.error('Webhook error:', error);
    return NextResponse.json(
      { error: error.message || 'Webhook processing failed' },
      { status: 500 }
    );
  }
}

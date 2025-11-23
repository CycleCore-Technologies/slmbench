import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { sql } from '@vercel/postgres';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-11-17.clover',
});

const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

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
          await sql`
            UPDATE evaluation_orders
            SET
              payment_status = 'paid',
              stripe_payment_intent_id = ${session.payment_intent as string},
              paid_at = NOW()
            WHERE id = ${orderId}
          `;

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
          await sql`
            UPDATE evaluation_orders
            SET payment_status = 'failed'
            WHERE id = ${orderId}
          `;
        }
        break;
      }

      case 'customer.subscription.created':
      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription;

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
            await sql`
              INSERT INTO enterprise_subscriptions (
                id,
                stripe_subscription_id,
                stripe_customer_id,
                email,
                status,
                current_period_start,
                current_period_end
              ) VALUES (
                ${orderId},
                ${subscription.id},
                ${subscription.customer as string},
                ${email},
                ${subscription.status},
                to_timestamp(${subscription.currentPeriodStart}),
                to_timestamp(${subscription.currentPeriodEnd})
              )
              ON CONFLICT (stripe_subscription_id)
              DO UPDATE SET
                status = ${subscription.status},
                current_period_start = to_timestamp(${subscription.currentPeriodStart}),
                current_period_end = to_timestamp(${subscription.currentPeriodEnd}),
                updated_at = NOW()
            `;
          }
        }
        break;
      }

      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription;

        await sql`
          UPDATE enterprise_subscriptions
          SET status = 'canceled', updated_at = NOW()
          WHERE stripe_subscription_id = ${subscription.id}
        `;
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

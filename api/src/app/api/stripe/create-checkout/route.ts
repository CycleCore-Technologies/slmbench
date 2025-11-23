import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { sql } from '@vercel/postgres';
import { v4 as uuidv4 } from 'uuid';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-11-17.clover',
});

// CORS headers for cross-origin requests
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export async function OPTIONS() {
  return NextResponse.json({}, { headers: corsHeaders });
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, modelName, huggingfaceUrl, productType } = body;

    // Validate input
    if (!email || !modelName || !huggingfaceUrl || !productType) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400, headers: corsHeaders }
      );
    }

    // Determine pricing based on product type
    const prices = {
      single: {
        amount: 2000, // $20.00 in cents
        name: 'Single Model Verification',
        description: 'Official verification for 1 model',
        recurring: false,
      },
      pack: {
        amount: 7900, // $79.00 in cents
        name: 'Verification Pack (5 Models)',
        description: 'Verify up to 5 models and save 21%',
        recurring: false,
      },
      enterprise: {
        amount: 49900, // $499.00 in cents (monthly)
        name: 'Enterprise Evaluation Service',
        description: 'Unlimited verifications + API access',
        recurring: true,
      },
    };

    const selectedPrice = prices[productType as keyof typeof prices];
    if (!selectedPrice) {
      return NextResponse.json(
        { error: 'Invalid product type' },
        { status: 400, headers: corsHeaders }
      );
    }

    // Create order ID
    const orderId = uuidv4();

    // Create Stripe checkout session
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price_data: {
            currency: 'usd',
            product_data: {
              name: selectedPrice.name,
              description: selectedPrice.description,
            },
            unit_amount: selectedPrice.amount,
            ...(selectedPrice.recurring && {
              recurring: {
                interval: 'month',
              },
            }),
          },
          quantity: 1,
        },
      ],
      mode: selectedPrice.recurring ? 'subscription' : 'payment',
      success_url: `${process.env.NEXT_PUBLIC_BASE_URL}/api/orders/${orderId}?success=true`,
      cancel_url: `${process.env.NEXT_PUBLIC_BASE_URL}/evaluation?canceled=true`,
      customer_email: email,
      metadata: {
        orderId,
        modelName,
        huggingfaceUrl,
        productType,
      },
    });

    // Store order in database
    await sql`
      INSERT INTO evaluation_orders (
        id,
        stripe_session_id,
        email,
        model_name,
        huggingface_url,
        product_type,
        amount_cents,
        payment_status,
        evaluation_status
      ) VALUES (
        ${orderId},
        ${session.id},
        ${email},
        ${modelName},
        ${huggingfaceUrl},
        ${productType},
        ${selectedPrice.amount},
        'pending',
        'queued'
      )
    `;

    return NextResponse.json({
      sessionId: session.id,
      url: session.url,
    }, { headers: corsHeaders });
  } catch (error: any) {
    console.error('Checkout error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500, headers: corsHeaders }
    );
  }
}

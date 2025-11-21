import { NextRequest, NextResponse } from 'next/server';
import { sql } from '@vercel/postgres';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const orderId = params.id;

    // Fetch order from database
    const result = await sql`
      SELECT
        id,
        email,
        model_name,
        huggingface_url,
        product_type,
        amount_cents,
        payment_status,
        evaluation_status,
        results_json,
        report_url,
        certificate_url,
        created_at,
        paid_at,
        completed_at
      FROM evaluation_orders
      WHERE id = ${orderId}
    `;

    if (result.rows.length === 0) {
      return NextResponse.json(
        { error: 'Order not found' },
        { status: 404 }
      );
    }

    const order = result.rows[0];

    // Check if this is a success redirect from Stripe
    const success = request.nextUrl.searchParams.get('success');

    if (success === 'true' && order.payment_status === 'paid') {
      // Redirect to thank you page with order details
      return NextResponse.redirect(
        `${process.env.NEXT_PUBLIC_BASE_URL}/thank-you?orderId=${orderId}`
      );
    }

    return NextResponse.json({
      order: {
        id: order.id,
        modelName: order.model_name,
        huggingfaceUrl: order.huggingface_url,
        productType: order.product_type,
        paymentStatus: order.payment_status,
        evaluationStatus: order.evaluation_status,
        results: order.results_json,
        reportUrl: order.report_url,
        certificateUrl: order.certificate_url,
        createdAt: order.created_at,
        paidAt: order.paid_at,
        completedAt: order.completed_at,
      },
    });
  } catch (error: any) {
    console.error('Order fetch error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

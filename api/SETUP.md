# SLMBench Payment Integration Setup Guide

This guide walks you through setting up the Stripe payment integration for SLMBench using DigitalOcean PostgreSQL and Vercel hosting.

## Architecture

- **Frontend/API**: Vercel (Next.js 14 with API routes)
- **Database**: DigitalOcean Managed PostgreSQL
- **Payments**: Stripe ($20, $79, $499/month)

---

## Step 1: DigitalOcean PostgreSQL Setup (15 mins)

### Create Database

1. Log into **DigitalOcean Dashboard**
2. Go to **Databases** → **Create Database**
3. Choose:
   - **Engine**: PostgreSQL 16
   - **Plan**: Development ($0/month with App Platform)
   - **Region**: Choose closest to your users
   - **Name**: `slmbench-db`
4. Click **Create Database**

### Run Schema

1. Wait for database to provision (~3 minutes)
2. Click **Users & Databases** tab
3. Create new database: `slmbench`
4. Click **Connection Details** → Copy connection string
5. Click **Console** tab (or use `psql` locally)
6. Run the schema from `database/schema.sql`:

```bash
# From your local machine
psql "postgresql://user:password@host:port/slmbench?sslmode=require" < database/schema.sql
```

Or copy/paste the SQL directly into the console.

### Verify Tables Created

```sql
\dt
-- Should show: evaluation_orders, enterprise_subscriptions
```

---

## Step 2: Stripe Configuration (20 mins)

### Create Products in Stripe Dashboard

1. Log into **Stripe Dashboard**
2. Go to **Products** → **Add Product**

#### Product 1: Single Model Verification

- **Name**: Official Model Verification
- **Description**: Get your model verified by CycleCore and earn a CCT✓ badge
- **Pricing**: One-time payment
- **Price**: $20.00 USD
- **Tax Code**: Software services (optional)
- Click **Save**
- Copy the **Price ID** (starts with `price_...`)

#### Product 2: Verification Pack

- **Name**: Verification Pack (5 Models)
- **Description**: Verify up to 5 models and save 21%
- **Pricing**: One-time payment
- **Price**: $79.00 USD
- Click **Save**
- Copy the **Price ID**

#### Product 3: Enterprise

- **Name**: Enterprise Evaluation Service
- **Description**: Unlimited verifications + API access + private leaderboard
- **Pricing**: Recurring
- **Billing Period**: Monthly
- **Price**: $499.00 USD
- Click **Save**
- Copy the **Price ID**

### Get API Keys

1. Go to **Developers** → **API Keys**
2. Copy **Publishable Key** (starts with `pk_test_...` or `pk_live_...`)
3. Copy **Secret Key** (starts with `sk_test_...` or `sk_live_...`)

**Important**: Use test keys during development, switch to live keys before launch.

---

## Step 3: Vercel Deployment (10 mins)

### Connect GitHub Repository

1. Log into **Vercel Dashboard**
2. Click **Add New** → **Project**
3. Import the `SLMBench` repository
4. Set **Root Directory**: `api`
5. **Framework Preset**: Next.js
6. Click **Deploy** (will fail first time - need environment variables)

### Add Environment Variables

In Vercel project settings → **Environment Variables**:

```env
# Stripe
STRIPE_SECRET_KEY=sk_test_... (from Step 2)
STRIPE_PUBLISHABLE_KEY=pk_test_... (from Step 2)
STRIPE_WEBHOOK_SECRET=(leave blank for now, add after webhook setup)

# Database (from Step 1)
POSTGRES_URL=postgres://user:password@host:port/slmbench?sslmode=require
POSTGRES_PRISMA_URL=postgres://user:password@host:port/slmbench?sslmode=require&pgbouncer=true
POSTGRES_URL_NO_SSL=postgres://user:password@host:port/slmbench
POSTGRES_URL_NON_POOLING=postgres://user:password@host:port/slmbench?sslmode=require
POSTGRES_USER=doadmin
POSTGRES_HOST=your-db-host.db.ondigitalocean.com
POSTGRES_PASSWORD=your-password
POSTGRES_DATABASE=slmbench

# Application
NEXT_PUBLIC_BASE_URL=https://api-slmbench.vercel.app (update with your actual URL)
NODE_ENV=production
```

Click **Save** → **Redeploy**

### Get Deployment URL

After deployment completes:
- Copy the deployment URL (e.g., `https://api-slmbench.vercel.app`)
- Update `NEXT_PUBLIC_BASE_URL` environment variable with this URL
- Redeploy one more time

---

## Step 4: Stripe Webhook Setup (5 mins)

### Create Webhook Endpoint

1. Go to **Stripe Dashboard** → **Developers** → **Webhooks**
2. Click **Add Endpoint**
3. **Endpoint URL**: `https://api-slmbench.vercel.app/api/stripe/webhook`
4. **Events to send**: Select these events:
   - `checkout.session.completed`
   - `checkout.session.expired`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
5. Click **Add Endpoint**
6. Copy the **Signing Secret** (starts with `whsec_...`)

### Add Webhook Secret to Vercel

1. Go back to Vercel → **Environment Variables**
2. Add: `STRIPE_WEBHOOK_SECRET=whsec_...`
3. **Redeploy**

### Test Webhook

1. In Stripe Dashboard → **Webhooks** → Your endpoint
2. Click **Send test webhook**
3. Choose `checkout.session.completed`
4. Check that endpoint returns `200 OK`

---

## Step 5: Test Payment Flow (10 mins)

### Using Stripe Test Mode

1. Make sure you're using **test** API keys (`sk_test_...`, `pk_test_...`)
2. Visit your submission form
3. Fill out model details
4. Use Stripe test card: `4242 4242 4242 4242`
   - Expiry: Any future date
   - CVC: Any 3 digits
   - ZIP: Any 5 digits
5. Complete checkout
6. Verify order appears in database:

```sql
SELECT id, model_name, payment_status, evaluation_status, paid_at
FROM evaluation_orders
ORDER BY created_at DESC
LIMIT 5;
```

Should show `payment_status = 'paid'`.

---

## Step 6: Go Live (5 mins)

### Switch to Live Mode

1. **Stripe Dashboard** → Toggle from **Test Mode** to **Live Mode** (top right)
2. Get your **live API keys** (Developers → API Keys)
3. Update Vercel environment variables:
   - `STRIPE_SECRET_KEY=sk_live_...`
   - `STRIPE_PUBLISHABLE_KEY=pk_live_...`
4. Recreate webhook endpoint with live mode URL
   - Update `STRIPE_WEBHOOK_SECRET` with new signing secret
5. **Redeploy** on Vercel

### Enable Live Payments

- Update submission form to use live Stripe publishable key
- Test with real payment (refund after testing)
- Monitor Stripe Dashboard for incoming payments

---

## Manual Processing Workflow

Since evaluation is manual initially:

### When Payment Succeeds

1. **You receive email notification** (optional: set up email alerts in Stripe)
2. **Check database** for new paid order:

```sql
SELECT id, model_name, huggingface_url, email
FROM evaluation_orders
WHERE payment_status = 'paid' AND evaluation_status = 'queued'
ORDER BY paid_at DESC;
```

3. **Run evaluation manually**:

```bash
cd /home/rain/SLMBench
python benchmarks/edge_json/scripts/eval.py \
  --model_url <huggingface_url> \
  --output results/<order_id>.json
```

4. **Update order with results**:

```sql
UPDATE evaluation_orders
SET
  evaluation_status = 'completed',
  results_json = '<paste JSON results>',
  completed_at = NOW()
WHERE id = '<order_id>';
```

5. **Email customer** with results:
   - Attach report PDF
   - Include leaderboard link
   - Thank them for supporting SLMBench

---

## Automation (Phase 2)

Later, automate this workflow:

1. **Webhook triggers job** (Redis queue or Vercel background functions)
2. **Worker picks up job** (Docker container runs `eval.py`)
3. **Results auto-uploaded** (S3 or DO Spaces)
4. **Customer auto-emailed** (SendGrid integration)
5. **Leaderboard auto-updated** (database write + cache invalidation)

For now, manual processing gets you to revenue faster.

---

## Costs Summary

### During Free Credits (Months 1-13)

- **Vercel**: $0 (free tier) → $20/month when commercial (Month 4+)
- **DO PostgreSQL**: $0 (covered by $200 credits, $15/month)
- **Total**: $0/month (Months 1-3), $20/month (Months 4-13)

### After Free Credits (Month 14+)

- **Vercel Pro**: $20/month
- **DO PostgreSQL**: $15/month
- **Total**: $35/month

**Projected Monthly Revenue** (Conservative):
- 10 evaluations × $20 = $200
- 1 pack × $79 = $79
- 1 enterprise × $499 = $499
- **Total**: ~$778/month

**ROI**: $778 revenue / $35 cost = 22x

---

## Troubleshooting

### Database Connection Fails

- Check connection string has `?sslmode=require`
- Verify database firewall allows Vercel IPs (DO auto-configures this)
- Test connection locally: `psql "connection_string"`

### Webhook Not Receiving Events

- Check endpoint URL is correct in Stripe Dashboard
- Verify `STRIPE_WEBHOOK_SECRET` matches signing secret
- Check Vercel logs for errors
- Ensure webhook endpoint returns 200 OK within 30 seconds

### Payment Succeeds but Order Not Updated

- Check webhook endpoint logs in Vercel
- Verify `stripe_session_id` matches between Stripe and database
- Check webhook signature verification isn't failing

### API Route 500 Error

- Check environment variables are set correctly
- Check database tables exist (`\dt` in psql)
- Check Vercel function logs for error details

---

## Support

- **Stripe Docs**: https://stripe.com/docs/payments/checkout
- **Vercel Docs**: https://vercel.com/docs
- **DO Database Docs**: https://docs.digitalocean.com/products/databases/

---

**Ready to accept your first payment?** 🚀

Once you complete Steps 1-4, you're live! Test in Step 5, then flip to production in Step 6.

Total setup time: ~1 hour

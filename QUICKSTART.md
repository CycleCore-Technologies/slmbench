# SLMBench Payment Integration - Quick Start

Get your payment system live in under 1 hour!

## Quick Links

- **Setup Guide**: `api/SETUP.md` (full details)
- **API Docs**: `api/README.md`
- **Form Template**: `api/FORM_EXAMPLE.html`

---

## 🚀 Fast Track (3 Steps)

### Step 1: Create Database (10 mins)

**DigitalOcean Dashboard** → https://cloud.digitalocean.com/databases

1. Click **Create** → **Databases**
2. Select **PostgreSQL 16**
3. Choose **Development** ($0 with App Platform)
4. Region: **New York** (or closest to you)
5. Database Name: `slmbench-db`
6. Click **Create Database Cluster**

**Wait 3 minutes for provisioning...**

7. Click **Users & Databases** tab
8. Click **Add Database** → Name: `slmbench` → **Save**
9. Click **Connection Details** → Copy **Connection String**

**Run Schema**:
```bash
# Replace <CONNECTION_STRING> with your actual connection string
psql "<CONNECTION_STRING>" -c "\i /home/rain/SLMBench/api/database/schema.sql"

# Or if you prefer, copy/paste the SQL directly in DO Console tab
```

**Verify**:
```bash
psql "<CONNECTION_STRING>" -c "\dt"
# Should show: evaluation_orders, enterprise_subscriptions
```

✅ **Database ready!**

---

### Step 2: Configure Stripe (15 mins)

**Stripe Dashboard** → https://dashboard.stripe.com

#### Get API Keys (5 mins)

1. **Developers** → **API Keys**
2. **Copy** these keys (keep in a text file temporarily):
   ```
   Publishable Key: pk_test_...
   Secret Key: sk_test_...
   ```

#### Create Webhook (10 mins)

1. **Developers** → **Webhooks** → **Add Endpoint**
2. **Endpoint URL**: `https://api-slmbench.vercel.app/api/stripe/webhook`
   - (Use your actual Vercel URL after deployment)
3. **Description**: SLMBench Payment Events
4. **Events to send**: Click **Select events**
   - ✅ `checkout.session.completed`
   - ✅ `checkout.session.expired`
   - ✅ `customer.subscription.created`
   - ✅ `customer.subscription.updated`
   - ✅ `customer.subscription.deleted`
5. **Add Endpoint**
6. **Copy Signing Secret**: `whsec_...`

✅ **Stripe configured!**

---

### Step 3: Deploy to Vercel (10 mins)

**Vercel Dashboard** → https://vercel.com/new

#### Import Project (2 mins)

1. Click **Import Project**
2. Import **CycleCore-Technologies/slmbench** from GitHub
3. **Root Directory**: `api`
4. **Framework Preset**: Next.js (should auto-detect)
5. **Don't click Deploy yet!** → Go to **Environment Variables**

#### Add Environment Variables (5 mins)

Click **Environment Variables** and add these:

```bash
# Stripe (from Step 2)
STRIPE_SECRET_KEY=sk_test_51...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Database (from Step 1 - use your actual connection string)
POSTGRES_URL=postgresql://doadmin:password@host-do-user-123-0.db.ondigitalocean.com:25060/slmbench?sslmode=require

# These are derived from POSTGRES_URL (copy same value for now)
POSTGRES_PRISMA_URL=postgresql://doadmin:password@host-do-user-123-0.db.ondigitalocean.com:25060/slmbench?sslmode=require&pgbouncer=true
POSTGRES_URL_NO_SSL=postgresql://doadmin:password@host-do-user-123-0.db.ondigitalocean.com:25060/slmbench
POSTGRES_URL_NON_POOLING=postgresql://doadmin:password@host-do-user-123-0.db.ondigitalocean.com:25060/slmbench?sslmode=require

# Extract these from your connection string:
POSTGRES_USER=doadmin
POSTGRES_HOST=host-do-user-123-0.db.ondigitalocean.com
POSTGRES_PASSWORD=your-password
POSTGRES_DATABASE=slmbench

# Application URL (update after first deploy with actual URL)
NEXT_PUBLIC_BASE_URL=https://api-slmbench.vercel.app
NODE_ENV=production
```

**Tip**: For the `POSTGRES_*` variables, parse your connection string:
```
postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

#### Deploy (3 mins)

1. Click **Deploy**
2. Wait for build to complete (~2 minutes)
3. **Copy your deployment URL**: `https://api-slmbench-abc123.vercel.app`

#### Update Environment Variables

4. Go to **Settings** → **Environment Variables**
5. Update `NEXT_PUBLIC_BASE_URL` with your actual URL
6. Click **Redeploy** (top right)

#### Update Stripe Webhook URL

7. Go back to **Stripe Dashboard** → **Webhooks**
8. Edit your webhook endpoint
9. Update URL to: `https://your-actual-url.vercel.app/api/stripe/webhook`
10. **Save**

✅ **Deployed and live!**

---

## ✅ Test Your Setup (5 mins)

### Test Payment Flow

1. Open `api/FORM_EXAMPLE.html` in a browser
2. Update API URL in the JavaScript:
   ```javascript
   // Line ~143
   const response = await fetch('https://YOUR-ACTUAL-URL.vercel.app/api/stripe/create-checkout', {
   ```
3. Fill out the form with test data:
   - Model Name: `Test-Model-v1`
   - HuggingFace URL: `https://huggingface.co/test/model`
   - Email: `test@example.com`
   - Choose: **Single Verification** ($20)
4. Click **Proceed to Payment**
5. Use Stripe test card: `4242 4242 4242 4242`
   - Expiry: `12/34`
   - CVC: `123`
   - ZIP: `12345`
6. Complete payment

### Verify in Database

```bash
psql "<CONNECTION_STRING>" -c "SELECT id, model_name, payment_status, evaluation_status, paid_at FROM evaluation_orders ORDER BY created_at DESC LIMIT 5;"
```

Should show:
```
payment_status = 'paid'
evaluation_status = 'queued'
```

✅ **Payment system working!**

---

## 🎉 You're Live!

**What's working**:
- ✅ Payments accepted (Stripe test mode)
- ✅ Orders tracked in database
- ✅ Webhook receiving events
- ✅ API responding correctly

**Next steps**:
1. Integrate submission form into slmbench.com
2. Process first test order manually
3. Switch to Stripe live mode when ready
4. Start accepting real payments!

**When you get a payment**:
```bash
# 1. Check for paid orders
psql "<CONNECTION_STRING>" -c "SELECT * FROM evaluation_orders WHERE payment_status='paid' AND evaluation_status='queued';"

# 2. Run evaluation
python benchmarks/edge_json/scripts/eval.py --model_url <url> --output results/<order_id>.json

# 3. Update database
psql "<CONNECTION_STRING>" -c "UPDATE evaluation_orders SET evaluation_status='completed', completed_at=NOW() WHERE id='<order_id>';"

# 4. Email customer with results
```

---

## 🆘 Troubleshooting

**Database connection fails**:
```bash
# Test connection
psql "<CONNECTION_STRING>" -c "SELECT version();"
```

**Vercel deployment fails**:
- Check build logs in Vercel dashboard
- Verify all environment variables are set
- Make sure `POSTGRES_URL` includes `?sslmode=require`

**Webhook not receiving events**:
- Check URL in Stripe dashboard matches Vercel deployment
- Verify `STRIPE_WEBHOOK_SECRET` is set correctly
- Check Vercel function logs

**Payment succeeds but order not updating**:
- Check webhook endpoint in Vercel logs
- Verify webhook secret matches
- Check database connection is working

---

## 📊 Monitoring

**View recent orders**:
```sql
SELECT
  id,
  model_name,
  email,
  product_type,
  amount_cents / 100 as amount_usd,
  payment_status,
  evaluation_status,
  created_at
FROM evaluation_orders
ORDER BY created_at DESC
LIMIT 10;
```

**Revenue this month**:
```sql
SELECT
  COUNT(*) as orders,
  SUM(amount_cents) / 100 as total_usd
FROM evaluation_orders
WHERE
  payment_status = 'paid'
  AND paid_at >= date_trunc('month', CURRENT_DATE);
```

---

**Ready to make money?** 🚀

Follow the 3 steps above and you'll be accepting payments in under an hour!

**Need help?** Check `api/SETUP.md` for detailed explanations.

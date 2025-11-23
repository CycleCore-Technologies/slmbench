# SLMBench.com Business Logic & Monetization - CC-WEB Implementation Guide

**Date**: 2025-11-21
**Purpose**: Technical implementation guide for revenue streams and business logic
**Status**: Planning phase - ready for implementation

---

## 🎯 Business Model Overview

### Open Core Strategy

**Free Tier (Open Source)**:
- ✅ Benchmark datasets (EdgeJSON v3)
- ✅ Evaluation harness (open source)
- ✅ Public leaderboard
- ✅ Model downloads (HuggingFace)
- ✅ Documentation and guides

**Paid Tier (Evaluation Service)**:
- 💰 Custom model evaluation
- 💰 Private leaderboard entries
- 💰 Detailed performance reports
- 💰 Priority support
- 💰 API access for automated evaluation

---

## 💳 Payment Integration (Stripe)

### Stripe Setup Requirements

**Account Details**:
- **Business Name**: CycleCore Technologies
- **Email**: hi@cyclecore.ai
- **Tax ID**: (TBD - need to provide)
- **Business Type**: Technology / SaaS
- **Country**: (TBD - need to confirm)

### Products to Create in Stripe

#### 1. Single Model Evaluation
```yaml
Product Name: "Single Model Evaluation"
Price: $49 USD
Type: One-time payment
Description: "Evaluate one model on EdgeJSON benchmark with detailed report"
Features:
  - Full EdgeJSON v3 evaluation (158 test cases)
  - Detailed performance report (PDF + JSON)
  - Per-schema breakdown
  - Latency analysis
  - 48-hour turnaround
  - Email delivery
```

#### 2. Model Evaluation Pack (5 Models)
```yaml
Product Name: "Model Evaluation Pack (5 Models)"
Price: $199 USD ($39.80 per model)
Type: One-time payment
Savings: 19% vs single evaluations
Description: "Evaluate up to 5 models with detailed reports"
Features:
  - All Single Evaluation features × 5
  - Comparison report (multi-model)
  - Priority queue
  - 72-hour turnaround for all 5
  - Bulk discount
```

#### 3. Enterprise Evaluation Service
```yaml
Product Name: "Enterprise Evaluation Service"
Price: $999 USD/month
Type: Subscription (monthly)
Description: "Unlimited evaluations + private leaderboard + API access"
Features:
  - Unlimited model evaluations
  - Private leaderboard (internal only)
  - API access (automated evaluation)
  - Custom benchmarks (upon request)
  - Priority support (24-hour response)
  - Dedicated account manager
  - White-label reports
```

#### 4. Custom Benchmark Creation
```yaml
Product Name: "Custom Benchmark Creation"
Price: $2,499 USD
Type: One-time payment
Description: "Create a custom benchmark for your specific use case"
Features:
  - Custom schema design (up to 10 schemas)
  - Synthetic data generation (500+ examples)
  - Validation and quality assurance
  - Private or public release option
  - 2-week delivery
  - Evaluation harness included
```

---

## 🔧 Technical Implementation

### Stripe Integration Flow

#### Payment Flow (Single/Pack Evaluations)

```
User Journey:
1. User clicks "Evaluate My Model" on slmbench.com
2. Form: Upload model (HF link or file) + email
3. Stripe Checkout (redirect to Stripe hosted page)
4. Payment success → Webhook to our backend
5. Backend: Queue evaluation job
6. Backend: Run evaluation (eval.py)
7. Backend: Generate report (PDF + JSON)
8. Backend: Email report to user
9. Backend: Update order status in database
```

**Stripe Checkout Implementation**:
```javascript
// Frontend (Next.js/React example)
const handleEvaluateClick = async () => {
  const response = await fetch('/api/create-checkout-session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      productId: 'single_evaluation', // or 'pack_5'
      modelInfo: {
        huggingface_url: userInput.hfUrl,
        model_name: userInput.modelName,
        email: userInput.email
      }
    })
  });
  
  const { sessionId } = await response.json();
  
  // Redirect to Stripe Checkout
  const stripe = await loadStripe(process.env.NEXT_PUBLIC_STRIPE_KEY);
  await stripe.redirectToCheckout({ sessionId });
};
```

**Backend API (create-checkout-session)**:
```javascript
// Backend (Next.js API route or Express)
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export default async function handler(req, res) {
  const { productId, modelInfo } = req.body;
  
  // Price IDs from Stripe Dashboard
  const prices = {
    single_evaluation: 'price_xxxxxxxxxxxxx', // $49
    pack_5: 'price_xxxxxxxxxxxxx'             // $199
  };
  
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{
      price: prices[productId],
      quantity: 1,
    }],
    mode: 'payment',
    success_url: `${process.env.DOMAIN}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.DOMAIN}/evaluate`,
    metadata: {
      model_name: modelInfo.model_name,
      huggingface_url: modelInfo.huggingface_url,
      email: modelInfo.email,
      product_type: productId
    }
  });
  
  res.json({ sessionId: session.id });
}
```

#### Webhook Handler (Payment Confirmation)

```javascript
// Backend webhook endpoint
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export default async function handler(req, res) {
  const sig = req.headers['stripe-signature'];
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
  
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, webhookSecret);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }
  
  // Handle the event
  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object;
      
      // Extract metadata
      const { model_name, huggingface_url, email, product_type } = session.metadata;
      
      // Create evaluation job in database
      await createEvaluationJob({
        orderId: session.id,
        modelName: model_name,
        modelUrl: huggingface_url,
        userEmail: email,
        productType: product_type,
        status: 'pending',
        createdAt: new Date()
      });
      
      // Trigger evaluation worker (queue system)
      await queueEvaluation({
        orderId: session.id,
        modelUrl: huggingface_url
      });
      
      // Send confirmation email
      await sendEmail({
        to: email,
        subject: 'SLMBench Evaluation - Payment Confirmed',
        body: `Your evaluation for ${model_name} has been queued. You'll receive results within 48 hours.`
      });
      
      break;
      
    case 'customer.subscription.created':
      // Handle enterprise subscription
      const subscription = event.data.object;
      await createEnterpriseAccount(subscription);
      break;
      
    default:
      console.log(`Unhandled event type ${event.type}`);
  }
  
  res.json({ received: true });
}
```

---

## 🗄️ Database Schema

### Evaluation Orders Table

```sql
CREATE TABLE evaluation_orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id VARCHAR(255) UNIQUE NOT NULL, -- Stripe session ID
  user_email VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_url TEXT NOT NULL, -- HuggingFace URL or upload path
  product_type VARCHAR(50) NOT NULL, -- 'single', 'pack_5', 'enterprise'
  status VARCHAR(50) NOT NULL, -- 'pending', 'running', 'completed', 'failed'
  payment_amount INTEGER NOT NULL, -- in cents
  payment_status VARCHAR(50) NOT NULL, -- 'paid', 'refunded'
  
  -- Evaluation results
  json_exact_score DECIMAL(5,2),
  field_f1_score DECIMAL(5,4),
  report_url TEXT, -- S3/storage URL for PDF report
  results_json JSONB, -- Full evaluation results
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  
  -- Metadata
  evaluation_time_seconds INTEGER,
  error_message TEXT,
  
  INDEX idx_user_email (user_email),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
);
```

### Enterprise Accounts Table

```sql
CREATE TABLE enterprise_accounts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_name VARCHAR(255) NOT NULL,
  contact_email VARCHAR(255) NOT NULL,
  stripe_customer_id VARCHAR(255) UNIQUE NOT NULL,
  stripe_subscription_id VARCHAR(255) UNIQUE NOT NULL,
  subscription_status VARCHAR(50) NOT NULL, -- 'active', 'canceled', 'past_due'
  
  -- API access
  api_key VARCHAR(255) UNIQUE NOT NULL,
  api_calls_this_month INTEGER DEFAULT 0,
  
  -- Private leaderboard
  private_leaderboard_enabled BOOLEAN DEFAULT TRUE,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  subscription_start TIMESTAMP,
  subscription_end TIMESTAMP,
  
  INDEX idx_api_key (api_key),
  INDEX idx_stripe_customer (stripe_customer_id)
);
```

### Evaluation Queue Table

```sql
CREATE TABLE evaluation_queue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id VARCHAR(255) NOT NULL,
  priority INTEGER DEFAULT 0, -- Higher = more urgent (enterprise = 10, pack = 5, single = 1)
  status VARCHAR(50) NOT NULL, -- 'queued', 'processing', 'completed', 'failed'
  worker_id VARCHAR(255), -- Which worker is processing this
  
  created_at TIMESTAMP DEFAULT NOW(),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  
  INDEX idx_status_priority (status, priority DESC),
  INDEX idx_order_id (order_id)
);
```

---

## 🤖 Evaluation Worker System

### Worker Architecture

```
┌─────────────────┐
│   User Payment  │
│   (Stripe)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Webhook       │
│   Handler       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Queue System   │
│  (Redis/RabbitMQ)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Worker Pool    │
│  (Docker)       │
│  - eval.py      │
│  - report gen   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Storage (S3)   │
│  - Reports      │
│  - Results      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Email Service  │
│  (SendGrid)     │
└─────────────────┘
```

### Worker Implementation (Python)

```python
# worker.py
import os
import json
import redis
from pathlib import Path
import subprocess
from datetime import datetime

# Connect to queue
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=6379,
    decode_responses=True
)

def process_evaluation(order_id, model_url):
    """Process a single evaluation job"""
    
    # Update status
    update_order_status(order_id, 'running')
    
    try:
        # Download model from HuggingFace
        model_path = download_model(model_url)
        
        # Run evaluation
        start_time = datetime.now()
        result = subprocess.run([
            'python3',
            '/app/benchmarks/edge_json/scripts/eval.py',
            '--model', model_path,
            '--data', '/app/benchmarks/edge_json/data/edgejson_test_v3.jsonl',
            '--output', f'/tmp/{order_id}_results.json'
        ], capture_output=True, text=True, timeout=3600)
        
        end_time = datetime.now()
        eval_time = (end_time - start_time).total_seconds()
        
        if result.returncode != 0:
            raise Exception(f"Evaluation failed: {result.stderr}")
        
        # Load results
        with open(f'/tmp/{order_id}_results.json') as f:
            results = json.load(f)
        
        # Generate PDF report
        report_path = generate_pdf_report(order_id, results)
        
        # Upload to S3
        report_url = upload_to_s3(report_path, f'reports/{order_id}.pdf')
        results_url = upload_to_s3(f'/tmp/{order_id}_results.json', f'results/{order_id}.json')
        
        # Update database
        update_order_results(order_id, {
            'status': 'completed',
            'json_exact_score': results['overall']['json_exact_match'],
            'field_f1_score': results['overall']['field_f1'],
            'report_url': report_url,
            'results_json': results,
            'evaluation_time_seconds': eval_time,
            'completed_at': datetime.now()
        })
        
        # Send email with results
        send_results_email(order_id, report_url, results)
        
        return True
        
    except Exception as e:
        # Handle failure
        update_order_status(order_id, 'failed', error=str(e))
        send_error_email(order_id, str(e))
        return False

def worker_loop():
    """Main worker loop"""
    print("Worker started, waiting for jobs...")
    
    while True:
        # Pop job from queue (blocking, 5 second timeout)
        job = redis_client.blpop('evaluation_queue', timeout=5)
        
        if job:
            _, job_data = job
            job_info = json.loads(job_data)
            
            order_id = job_info['order_id']
            model_url = job_info['model_url']
            
            print(f"Processing evaluation: {order_id}")
            process_evaluation(order_id, model_url)
            print(f"Completed evaluation: {order_id}")

if __name__ == '__main__':
    worker_loop()
```

---

## 📧 Email Templates (SendGrid)

### Payment Confirmation Email

```html
Subject: SLMBench Evaluation - Payment Confirmed

Hi there,

Thank you for your payment! Your model evaluation has been queued.

Order Details:
- Model: {{model_name}}
- Product: {{product_type}}
- Order ID: {{order_id}}
- Amount: ${{amount}}

What's Next:
1. Your model will be evaluated on the EdgeJSON v3 benchmark
2. You'll receive a detailed report within 48 hours
3. Report will include JSONExact score, Field F1, and per-schema breakdown

Questions? Reply to this email or contact us at hi@cyclecore.ai

Best,
CycleCore Technologies Team
```

### Results Ready Email

```html
Subject: SLMBench Evaluation - Results Ready!

Hi there,

Your model evaluation is complete! 🎉

Model: {{model_name}}
Overall Performance:
- JSONExact: {{json_exact}}%
- Field F1: {{field_f1}}

Download Your Report:
[Download PDF Report]({{report_url}})
[Download JSON Results]({{results_url}})

View on Leaderboard:
{{#if public_leaderboard}}
Your model has been added to the public leaderboard: {{leaderboard_url}}
{{/if}}

Questions? Reply to this email or contact us at hi@cyclecore.ai

Best,
CycleCore Technologies Team
```

---

## 🔐 API Access (Enterprise)

### API Endpoint Design

```
POST /api/v1/evaluate
Authorization: Bearer <api_key>
Content-Type: application/json

{
  "model_url": "https://huggingface.co/user/model",
  "model_name": "My Custom Model",
  "benchmark": "edgejson_v3",
  "private": true,  // Don't add to public leaderboard
  "callback_url": "https://myapp.com/webhook"  // Optional webhook
}

Response:
{
  "evaluation_id": "eval_abc123",
  "status": "queued",
  "estimated_completion": "2025-11-21T15:30:00Z"
}
```

### API Status Check

```
GET /api/v1/evaluate/{evaluation_id}
Authorization: Bearer <api_key>

Response:
{
  "evaluation_id": "eval_abc123",
  "status": "completed",
  "results": {
    "json_exact": 55.1,
    "field_f1": 0.780,
    "by_complexity": {
      "simple": 75.0,
      "medium": 50.0,
      "complex": 35.0
    }
  },
  "report_url": "https://s3.../report.pdf",
  "results_url": "https://s3.../results.json"
}
```

---

## 💰 Pricing Strategy

### Rationale

**Single Evaluation ($49)**:
- Cost to us: ~$2 (compute) + ~$3 (support/overhead) = $5
- Margin: $44 (88%)
- Target: Individual researchers, small teams

**Pack of 5 ($199)**:
- Cost to us: ~$10 (compute) + ~$10 (support) = $20
- Margin: $179 (90%)
- Savings for customer: $46 (19% discount)
- Target: Teams iterating on models

**Enterprise ($999/month)**:
- Unlimited evaluations (assume 20/month average)
- Cost to us: ~$40 (compute) + ~$200 (support/infra) = $240
- Margin: $759 (76%)
- Target: Companies with continuous evaluation needs

**Custom Benchmark ($2,499)**:
- Cost to us: ~$500 (labor: 20 hours @ $25/hr) + ~$100 (compute/overhead) = $600
- Margin: $1,899 (76%)
- Target: Enterprises with specific use cases

### Competitive Analysis

| Service | Our Price | Competitor | Notes |
|---------|-----------|------------|-------|
| Single Eval | $49 | N/A | No direct competitor |
| Enterprise | $999/mo | Hugging Face Pro: $9/mo | Different value prop (evaluation vs hosting) |
| Custom Benchmark | $2,499 | Consulting: $5k-20k | Significantly cheaper |

---

## 📊 Revenue Projections

### Conservative Estimates (Year 1)

```
Month 1-3 (Launch):
- Single Evals: 10/month × $49 = $490/month
- Packs: 2/month × $199 = $398/month
- Enterprise: 0 customers = $0/month
Total: ~$900/month

Month 4-6 (Growth):
- Single Evals: 25/month × $49 = $1,225/month
- Packs: 5/month × $199 = $995/month
- Enterprise: 1 customer × $999 = $999/month
Total: ~$3,200/month

Month 7-12 (Established):
- Single Evals: 50/month × $49 = $2,450/month
- Packs: 10/month × $199 = $1,990/month
- Enterprise: 3 customers × $999 = $2,997/month
- Custom: 1/quarter × $2,499 = $833/month
Total: ~$8,270/month

Year 1 Total Revenue: ~$50,000
```

### Optimistic Estimates (Year 1)

```
With successful launch, academic paper, and community adoption:

Year 1 Total Revenue: $150,000 - $250,000
- 100+ single evaluations/month
- 20+ packs/month
- 10+ enterprise customers
- 5+ custom benchmarks
```

---

## 🚀 Launch Strategy

### Phase 1: Soft Launch (Week 1-2)
- ✅ Website live with free features
- ✅ Public leaderboard (4 models)
- ✅ Documentation and guides
- 🔄 Payment integration (Stripe test mode)
- 🔄 Manual evaluation processing (no automation yet)

### Phase 2: Beta Launch (Week 3-4)
- 🔄 Stripe live mode
- 🔄 Automated evaluation pipeline
- 🔄 Email notifications
- 🔄 Beta pricing (20% discount)
- 🔄 Invite 10-20 beta testers

### Phase 3: Public Launch (Week 5-6)
- 🚀 Full automation
- 🚀 API access (enterprise)
- 🚀 Marketing push (X, LinkedIn, HN)
- 🚀 Academic paper on arXiv
- 🚀 Full pricing

---

## 🔒 Security & Compliance

### Data Privacy
- **User Data**: Email, payment info (Stripe handles PCI compliance)
- **Model Data**: Temporary storage only, deleted after evaluation
- **Results**: Stored encrypted (S3 with encryption at rest)
- **GDPR**: Right to deletion (delete results on request)

### API Security
- **Authentication**: Bearer tokens (API keys)
- **Rate Limiting**: 100 requests/hour (enterprise)
- **HTTPS Only**: All endpoints
- **Webhook Verification**: Stripe signature validation

### Terms of Service (Key Points)
- Models evaluated are not stored permanently
- Results may be added to public leaderboard (unless private)
- No refunds after evaluation starts
- Fair use policy (no abuse of unlimited enterprise)

---

## 📞 Support & Operations

### Support Channels
- **Email**: hi@cyclecore.ai (primary)
- **Response Time**: 
  - Free users: 48 hours
  - Paid users: 24 hours
  - Enterprise: 24 hours (priority)

### Refund Policy
- **Before Evaluation**: Full refund
- **After Evaluation**: No refund (service delivered)
- **Failed Evaluation**: Full refund or free retry

---

## 🛠️ Technical Stack Recommendations

### Frontend
- **Framework**: Next.js 14 (React)
- **Styling**: Tailwind CSS
- **Hosting**: Vercel or Netlify
- **Domain**: slmbench.com

### Backend
- **API**: Next.js API routes or Express.js
- **Database**: PostgreSQL (Supabase or RDS)
- **Queue**: Redis or RabbitMQ
- **Workers**: Docker containers (ECS or DigitalOcean)

### Payment
- **Processor**: Stripe
- **Mode**: Live (after beta)

### Storage
- **Reports**: AWS S3 or DigitalOcean Spaces
- **Models**: Temporary (local disk, deleted after eval)

### Email
- **Service**: SendGrid or Resend
- **Templates**: HTML with variables

### Monitoring
- **Errors**: Sentry
- **Analytics**: Plausible or PostHog
- **Uptime**: UptimeRobot

---

## 📋 Implementation Checklist for CC-WEB

### Stripe Setup
- [ ] Create Stripe account (CycleCore Technologies)
- [ ] Create products (Single, Pack, Enterprise, Custom)
- [ ] Get API keys (test + live)
- [ ] Set up webhook endpoint
- [ ] Test payment flow (test mode)

### Database
- [ ] Set up PostgreSQL database
- [ ] Create tables (orders, accounts, queue)
- [ ] Set up backups
- [ ] Create indexes

### Evaluation Pipeline
- [ ] Containerize eval.py (Docker)
- [ ] Set up queue system (Redis)
- [ ] Implement worker (Python)
- [ ] Test end-to-end flow

### Email
- [ ] Set up SendGrid account
- [ ] Create email templates
- [ ] Test email delivery

### Storage
- [ ] Set up S3 bucket (or equivalent)
- [ ] Configure access policies
- [ ] Test upload/download

### API (Enterprise)
- [ ] Implement API endpoints
- [ ] API key generation
- [ ] Rate limiting
- [ ] Documentation

### Frontend
- [ ] Payment form (Stripe Checkout)
- [ ] Order status page
- [ ] API key management (enterprise)
- [ ] Private leaderboard (enterprise)

---

## 📝 Environment Variables

```bash
# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Database
DATABASE_URL=postgresql://user:pass@host:5432/slmbench

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# AWS S3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=slmbench-reports
AWS_REGION=us-east-1

# SendGrid
SENDGRID_API_KEY=SG...
FROM_EMAIL=hi@cyclecore.ai

# App
DOMAIN=https://slmbench.com
NODE_ENV=production
```

---

## 🎯 Success Metrics

### KPIs to Track
- **Revenue**: Monthly recurring revenue (MRR)
- **Conversions**: Free → Paid conversion rate
- **Retention**: Enterprise churn rate
- **Usage**: Evaluations per month
- **Growth**: New customers per month
- **Support**: Average response time

### Goals (Year 1)
- 500+ total evaluations
- 10+ enterprise customers
- $50k+ revenue
- <5% churn rate
- <24hr support response time

---

**Document Version**: 1.0
**Last Updated**: 2025-11-21
**Status**: Ready for implementation
**Contact**: hi@cyclecore.ai


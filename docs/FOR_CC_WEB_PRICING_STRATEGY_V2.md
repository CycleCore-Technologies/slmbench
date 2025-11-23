# SLMBench.com Pricing & Leaderboard Strategy v2.0

**Date**: 2025-11-21
**Status**: REVISED - User feedback incorporated
**Key Changes**: Lower pricing ($20), dual leaderboard system

---

## 🎯 Core Strategy: Freemium + Certification

### The Model

**FREE**:
- ✅ Self-submit results to **Community Leaderboard**
- ✅ Run eval.py yourself (open source)
- ✅ Download benchmark datasets
- ✅ View all leaderboards
- ✅ Documentation and guides

**PAID ($20 - Certification)**:
- ✅ CycleCore runs evaluation (verified environment)
- ✅ **Verified Badge** on leaderboard
- ✅ Official performance certificate
- ✅ Detailed PDF report
- ✅ 48-hour turnaround
- ✅ Email support

**PAID ($999/mo - Enterprise)**:
- ✅ Unlimited verifications
- ✅ API access (automated evaluation)
- ✅ Private leaderboard (internal only)
- ✅ Priority support
- ✅ Custom benchmarks (upon request)

---

## 📊 Dual Leaderboard System

### Community Leaderboard (Free, Self-Reported)

**How It Works**:
1. User runs `eval.py` on their own hardware
2. User submits results JSON via web form
3. Results appear on **Community Leaderboard** with ⚪ badge
4. No verification, honor system

**Badge**: ⚪ **Community** (white/gray badge)

**Pros**:
- Zero friction for researchers
- Encourages participation
- Builds community
- Shows all models

**Cons**:
- Results not verified
- Potential for gaming/cheating
- No standardized environment

**Example Entry**:
```
⚪ My-Custom-Model-7B    | 62.3% | 0.815 | Self-reported | [JSON]
```

---

### Verified Leaderboard (Paid, CycleCore Certified)

**How It Works**:
1. User pays $20 for verification
2. CycleCore runs evaluation in standardized environment
3. Results appear on **Verified Leaderboard** with ✅ badge
4. Official certificate issued

**Badge**: ✅ **Verified by CycleCore** (green checkmark)

**Pros**:
- Trusted results
- Standardized environment
- Fair comparison
- Revenue stream

**Value Proposition**:
- "Official" status (credibility)
- Standardized hardware (fair comparison)
- Professional report (for papers/blogs)
- Certificate (for marketing)

**Example Entry**:
```
✅ Maaza-SLM-360M-JSON   | 55.1% | 0.780 | Verified | [Report] [Certificate]
```

---

## 💰 Revised Pricing

### 1. Single Verification: $20 USD

**What You Get**:
- ✅ CycleCore runs eval.py in standardized environment
- ✅ Verified badge (✅) on leaderboard
- ✅ Official performance certificate (PDF)
- ✅ Detailed evaluation report (PDF + JSON)
- ✅ 48-hour turnaround
- ✅ Email delivery

**Why $20?**:
- Impulse buy range (low friction)
- Covers compute + overhead (~$5 cost)
- Amazing advertising (users promote their verified badge)
- Fair price for "official" status
- Lower barrier = more volume

**Target**: Individual researchers, students, hobbyists

---

### 2. Verification Pack (5 Models): $79 USD

**What You Get**:
- All Single Verification features × 5
- Multi-model comparison report
- 21% savings ($15.80 per model vs $20)
- Priority queue

**Why $79?**:
- Volume discount (encourages bulk)
- Still affordable for teams
- ~$16/model (sweet spot)

**Target**: Teams iterating on models, research labs

---

### 3. Enterprise: $499/month USD

**What You Get**:
- ✅ Unlimited verifications
- ✅ API access (automated evaluation)
- ✅ Private leaderboard (internal team only)
- ✅ Priority support (24-hour response)
- ✅ Custom benchmarks (1 per quarter included)
- ✅ White-label reports (your branding)
- ✅ Dedicated account manager

**Why $499?** (down from $999):
- More accessible for startups
- Still premium tier
- Unlimited = predictable costs
- API access = real value

**Target**: AI companies, research labs, enterprises

---

### 4. Custom Benchmark: $1,999 USD

**What You Get**:
- Custom schema design (up to 10 schemas)
- Synthetic data generation (500+ examples)
- Validation and quality assurance
- Private or public release option
- 2-week delivery
- Evaluation harness included

**Why $1,999?** (down from $2,499):
- More competitive
- Still premium service
- Requires significant labor (~20 hours)

**Target**: Enterprises with specific use cases

---

## 🏆 Leaderboard UI Mockup

### Unified View (Default)

```
EdgeJSON Benchmark Leaderboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Filters: All | Verified Only | Community Only | <500M params | Open Source]

Rank | Model                      | Size  | JSONExact | Field F1 | Status        | Links
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🥇 1  | ✅ Maaza-SLM-360M-JSON v1  | 360M  | 55.1%     | 0.780    | Verified      | [HF] [Report] [Cert]
🥈 2  | ⚪ CustomModel-7B          | 7B    | 58.3%     | 0.795    | Community     | [JSON] [Get Verified]
🥉 3  | ✅ Maaza-MLM-135M-JSON v1  | 135M  | 24.7%     | 0.520    | Verified      | [HF] [Report] [Cert]
   4  | ⚪ MyModel-1B              | 1B    | 32.1%     | 0.612    | Community     | [JSON] [Get Verified]
   5  | ⚪ SmolLM2-360M (base)     | 360M  | ~5%       | ~0.15    | Community     | [HF]

[Submit Your Results (Free)] [Get Verified ($20)] [View Methodology]
```

**Key Features**:
- ✅ = Verified by CycleCore (green, trustworthy)
- ⚪ = Community (gray, self-reported)
- "Get Verified" button on community entries → $20 checkout
- Filter to show only verified or only community

---

## 🎯 Value Proposition: Why Pay $20?

### For Researchers
- **Credibility**: "Verified by CycleCore" badge for papers/blogs
- **Fairness**: Standardized environment (not your laptop vs someone's GPU)
- **Professional**: PDF report for publications
- **Certificate**: Official document for CV/portfolio

### For Companies
- **Marketing**: Verified badge = trust signal
- **Competitive**: Compare apples-to-apples
- **Proof**: Official certificate for customers/investors
- **Low Risk**: $20 is negligible for validation

### For Students
- **Affordable**: $20 is in student budget range
- **Portfolio**: Official certificate for job applications
- **Learning**: Detailed report shows where model fails

---

## 📈 Revenue Model

### Year 1 Projections (Conservative)

**Community Leaderboard** (Free):
- 500+ submissions (no revenue, but builds community)
- Drives awareness and traffic

**Verified Submissions** ($20):
- Month 1-3: 10/month = $200/month
- Month 4-6: 30/month = $600/month
- Month 7-12: 60/month = $1,200/month
- **Year 1 Total**: ~$8,000

**Verification Packs** ($79):
- Month 1-3: 2/month = $158/month
- Month 4-6: 5/month = $395/month
- Month 7-12: 10/month = $790/month
- **Year 1 Total**: ~$5,000

**Enterprise** ($499/month):
- Month 1-6: 0 customers
- Month 7-12: 2 customers = $998/month × 6 = $5,988
- **Year 1 Total**: ~$6,000

**Custom Benchmarks** ($1,999):
- 2 projects in Year 1
- **Year 1 Total**: ~$4,000

**Total Year 1 Revenue**: ~$23,000 (conservative)

---

### Year 1 Projections (Optimistic)

With successful academic paper, community adoption, and marketing:

- Verified: 100/month avg = $24,000
- Packs: 20/month avg = $18,960
- Enterprise: 5 customers × $499 × 8 months avg = $19,960
- Custom: 5 projects = $9,995

**Total Year 1 Revenue**: ~$73,000 (optimistic)

---

## 🚀 Launch Strategy

### Phase 1: Community First (Week 1-2)
- ✅ Launch with Community Leaderboard (free)
- ✅ Seed with 4 models (2 Maaza + 2 base)
- ✅ Encourage self-submissions
- ✅ Build traffic and awareness
- 🎯 Goal: 50+ community submissions

### Phase 2: Verification Launch (Week 3-4)
- 🚀 Launch $20 verification service
- 🚀 Offer 50% discount to first 20 verifications ($10)
- 🚀 Promote on X, HN, Reddit
- 🎯 Goal: 20+ verified models

### Phase 3: Enterprise (Month 2-3)
- 🚀 Launch $499/month enterprise tier
- 🚀 Reach out to 10 target companies
- 🚀 Offer 1-month free trial
- 🎯 Goal: 2+ enterprise customers

---

## 🎨 Badge Design Suggestions

### Verified Badge (✅)
```
┌─────────────────────────┐
│   ✅ VERIFIED           │
│   CycleCore Certified   │
│   EdgeJSON v3           │
│   2025-11-21            │
└─────────────────────────┘
```
- Green checkmark
- Official look
- Date stamp
- Benchmark version

### Community Badge (⚪)
```
┌─────────────────────────┐
│   ⚪ COMMUNITY          │
│   Self-Reported         │
│   EdgeJSON v3           │
│   [Get Verified →]      │
└─────────────────────────┘
```
- Gray/white circle
- Neutral look
- CTA to verify

---

## 📜 Certificate Design

### Official Performance Certificate

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              CYCLECORE TECHNOLOGIES                       ║
║           Official Performance Certificate                ║
║                                                           ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Model: Maaza-SLM-360M-JSON v1.0.0                       ║
║  Benchmark: EdgeJSON v3                                   ║
║  Date: November 21, 2025                                  ║
║                                                           ║
║  PERFORMANCE METRICS:                                     ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║  JSONExact Score:    55.1%                               ║
║  Field F1 Score:     0.780                               ║
║  Schema Compliance:  87.3%                               ║
║                                                           ║
║  LEADERBOARD RANK: #1 (Verified)                         ║
║                                                           ║
║  This certificate verifies that the above model was      ║
║  evaluated by CycleCore Technologies in a standardized   ║
║  environment using the EdgeJSON v3 benchmark.            ║
║                                                           ║
║  Certificate ID: CERT-2025-11-21-ABC123                  ║
║  Verification URL: slmbench.com/verify/ABC123            ║
║                                                           ║
║  ✅ Verified by CycleCore Technologies                   ║
║     hi@cyclecore.ai | slmbench.com                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

**Features**:
- Professional design
- Unique certificate ID
- Verification URL (public proof)
- Shareable on social media
- Printable (PDF)

---

## 🔄 User Flow: Community → Verified

### Step 1: User Runs Evaluation (Free)
```bash
python3 eval.py --model my_model --data edgejson_test_v3.jsonl --output results.json
```

### Step 2: User Submits to Community Leaderboard
- Upload `results.json` via web form
- Enter model name, size, HF link (optional)
- Appears on Community Leaderboard with ⚪ badge

### Step 3: User Sees "Get Verified" CTA
- "Want a verified badge? Get official certification for $20"
- Click → Stripe checkout
- Enter HF link or upload model

### Step 4: CycleCore Verifies
- Run evaluation in standardized environment
- Generate report + certificate
- Email results

### Step 5: Verified Badge Added
- Model moves to Verified Leaderboard (or gets ✅ badge)
- Certificate available for download
- User shares on social media

---

## 🎯 Marketing Angle

### Tagline
**"Trust, but verify. Get your model officially certified."**

### Messaging
- **Community**: "Free to submit, free to compare"
- **Verified**: "Official certification for $20"
- **Enterprise**: "Unlimited verification for your team"

### Social Proof
- "Join 500+ models on the leaderboard"
- "Trusted by researchers at [University], [Company]"
- "Official benchmark for edge AI"

---

## 🛡️ Anti-Gaming Measures

### Community Leaderboard
- **Require**: results.json with full details
- **Check**: JSON structure validity
- **Flag**: Suspicious scores (>90% JSONExact)
- **Moderate**: Review flagged submissions
- **Ban**: Repeat offenders

### Verified Leaderboard
- **Standardized**: Same hardware, same software
- **Reproducible**: Save all evaluation logs
- **Transparent**: Publish methodology
- **Auditable**: Results.json available for download

---

## 📊 Comparison: Community vs Verified

| Feature | Community (Free) | Verified ($20) |
|---------|------------------|----------------|
| **Leaderboard Entry** | ✅ Yes (⚪ badge) | ✅ Yes (✅ badge) |
| **Results JSON** | ✅ Self-provided | ✅ CycleCore-generated |
| **Environment** | ❌ Your hardware | ✅ Standardized |
| **Trust Level** | ⚠️ Self-reported | ✅ Verified |
| **Report** | ❌ No | ✅ Detailed PDF |
| **Certificate** | ❌ No | ✅ Official PDF |
| **Support** | ❌ No | ✅ Email support |
| **Marketing Value** | ⚠️ Low | ✅ High |

---

## 🚀 Implementation for CC-WEB

### Database Schema Updates

```sql
-- Add to evaluation_orders table
ALTER TABLE evaluation_orders ADD COLUMN leaderboard_type VARCHAR(20) DEFAULT 'verified';
-- 'verified' or 'community'

-- New table for community submissions
CREATE TABLE community_submissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  model_name VARCHAR(255) NOT NULL,
  model_size VARCHAR(50),
  huggingface_url TEXT,
  submitter_email VARCHAR(255) NOT NULL,
  
  -- Results
  json_exact_score DECIMAL(5,2) NOT NULL,
  field_f1_score DECIMAL(5,4) NOT NULL,
  results_json JSONB NOT NULL,
  
  -- Metadata
  submitted_at TIMESTAMP DEFAULT NOW(),
  status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'approved', 'flagged', 'rejected'
  flagged_reason TEXT,
  
  -- Verification
  verified BOOLEAN DEFAULT FALSE,
  verification_order_id UUID, -- Link to paid verification if upgraded
  
  INDEX idx_status (status),
  INDEX idx_verified (verified),
  INDEX idx_submitted_at (submitted_at)
);
```

### Frontend Components

1. **Community Submission Form**
   - Upload results.json
   - Enter model details
   - Email for notifications
   - "Submit to Community Leaderboard" button

2. **Leaderboard Toggle**
   - "All" | "Verified Only" | "Community Only"
   - Filter by size, license, etc.

3. **Get Verified CTA**
   - On community entries: "Get Verified ($20) →"
   - On landing page: "Submit Free or Get Verified"

4. **Certificate Viewer**
   - Public URL: slmbench.com/verify/{cert_id}
   - Shareable, embeddable

---

## 📝 Updated Stripe Products

### Product 1: Model Verification
- **Price**: $20 USD (down from $49)
- **Name**: "Official Model Verification"
- **Description**: "Get your model verified by CycleCore and earn a verified badge on the leaderboard"

### Product 2: Verification Pack (5 Models)
- **Price**: $79 USD (down from $199)
- **Name**: "Verification Pack (5 Models)"
- **Description**: "Verify up to 5 models and save 21%"

### Product 3: Enterprise
- **Price**: $499/month USD (down from $999)
- **Name**: "Enterprise Evaluation Service"
- **Description**: "Unlimited verifications + API access + private leaderboard"

---

## 🎯 Success Metrics

### Community Leaderboard
- 500+ submissions in Year 1
- 10% conversion to verified (50+ verifications)
- 50+ unique submitters

### Verified Leaderboard
- 100+ verified models in Year 1
- 20% repeat customers (packs or enterprise)
- <5% refund rate

### Revenue
- $20k+ in Year 1 (conservative)
- $70k+ in Year 1 (optimistic)
- Break-even: ~50 verifications ($1,000)

---

**Document Version**: 2.0
**Last Updated**: 2025-11-21
**Status**: REVISED - Ready for implementation
**Key Change**: $20 pricing + dual leaderboard system


# CC-WEB File Priority List for SLMBench.com

**Date**: 2025-11-21
**Purpose**: Prioritized list of files CC-WEB needs to build slmbench.com
**Status**: Ready for handoff

---

## 🚨 PRIORITY 1: MUST READ (Start Here)

These files contain critical information for building the website:

### 1. `/docs/FOR_CC_WEB_CLARIFICATIONS.md` ⭐⭐⭐⭐⭐
**Why**: Corrects all discrepancies and provides accurate numbers
**Contains**:
- ✅ Correct facts: 158 test cases, 24 schemas (not 25!)
- ✅ What to say vs what to avoid
- ✅ Website copy suggestions
- ✅ FAQ content
- ✅ Common mistakes to avoid

**Action**: Read this FIRST to avoid propagating errors

---

### 2. `/docs/FOR_CC_WEB_PRICING_STRATEGY_V2.md` ⭐⭐⭐⭐⭐
**Why**: Complete business model and monetization strategy
**Contains**:
- ✅ Final pricing: $20, $79, $499/month
- ✅ Dual leaderboard system (Community ⚪ + Verified ✅)
- ✅ User flows and conversion strategy
- ✅ Badge designs
- ✅ Certificate design
- ✅ Revenue projections

**Action**: Use this for all pricing and leaderboard implementation

---

### 3. `/docs/FOR_CC_WEB_SLMBENCH_DATA.md` ⭐⭐⭐⭐⭐
**Why**: All leaderboard data and model information
**Contains**:
- ✅ Current leaderboard (4 models with performance)
- ✅ Model profiles (MLM-135M, SLM-360M)
- ✅ Performance by complexity
- ✅ Benchmark details
- ✅ Website layout suggestions
- ✅ Branding guidelines

**Action**: Use this for leaderboard page and model profile pages

---

## 🔧 PRIORITY 2: TECHNICAL IMPLEMENTATION

These files are needed for backend/payment integration:

### 4. `/docs/FOR_CC_WEB_BUSINESS_LOGIC.md` ⭐⭐⭐⭐
**Why**: Complete technical implementation guide
**Contains**:
- ✅ Stripe integration (code examples)
- ✅ Database schema (SQL)
- ✅ Payment flow (webhooks)
- ✅ Worker architecture
- ✅ Email templates
- ✅ API design (enterprise)
- ✅ Environment variables

**Action**: Use this for Stripe setup and backend implementation

---

### 5. `/scripts/upload_to_huggingface.py` ⭐⭐⭐
**Why**: Reference for how models are structured
**Contains**:
- Model paths
- Repository naming
- Upload logic

**Action**: Reference only (understand model structure)

---

## 📊 PRIORITY 3: REFERENCE DATA

These files provide supporting data and context:

### 6. `/results/V3_VALIDATION_REPORT.md` ⭐⭐⭐
**Why**: Dataset quality assurance details
**Contains**:
- Dataset statistics (787 examples, 629 train, 158 test)
- Validation methodology
- Schema distribution
- Quality journey (v2 → v3)

**Action**: Use for "About the Benchmark" page

---

### 7. `/results/V3_VS_V2_VS_BASE_COMPARISON.md` ⭐⭐⭐
**Why**: Model performance analysis
**Contains**:
- Fine-tuning effectiveness (1.9% → 24.7%)
- Performance by complexity
- Capacity analysis
- Schema-level results

**Action**: Use for model comparison content

---

### 8. `/results/comparison_report.md` ⭐⭐
**Why**: Detailed comparison between models
**Contains**:
- Side-by-side metrics
- Improvement ratios
- Schema rankings

**Action**: Reference for detailed analysis pages

---

### 9. `/benchmarks/edge_json/README.md` ⭐⭐⭐
**Why**: Benchmark methodology and details
**Contains**:
- Task definition
- Evaluation metrics
- Dataset structure
- Usage instructions

**Action**: Use for "Benchmark Methodology" page

---

### 10. `/README.md` (main project) ⭐⭐
**Why**: Project overview
**Contains**:
- High-level description
- Quick start
- Repository structure

**Action**: Reference for overall project context

---

## 🎨 PRIORITY 4: ASSETS

These files are needed for branding and design:

### 11. `/assets/logos/cyclecore-logo-400x400.png` ⭐⭐⭐⭐
**Why**: Official logo for website and HuggingFace
**Contains**:
- 400×400px PNG
- Black background, white text
- "CycleCore Technologies"

**Action**: Use for website header, favicon, HuggingFace org profile

---

### 12. `/assets/logos/cyclecore-logo.svg` ⭐⭐
**Why**: Vector version of logo
**Contains**:
- SVG format (scalable)

**Action**: Use for high-res displays or print

---

## 📝 PRIORITY 5: DOCUMENTATION (Optional)

These files provide additional context but aren't critical for launch:

### 13. `/docs/NAMING_CONVENTIONS.md` ⭐⭐
**Why**: Official naming guidelines
**Contains**:
- Company name: CycleCore Technologies
- Product names: SLMBench, EdgeJSON, Maaza
- Branding consistency

**Action**: Reference for copy consistency

---

### 14. `/docs/DOMAIN_STRATEGY.md` ⭐
**Why**: Domain and email strategy
**Contains**:
- slmbench.com (product site)
- cyclecore.ai (company site)
- Email structure: hi@, support@, etc.

**Action**: Reference for domain setup

---

### 15. `/docs/LICENSING_STRATEGY.md` ⭐
**Why**: Legal and licensing details
**Contains**:
- Apache 2.0 rationale
- Open core strategy
- Revenue stream compatibility

**Action**: Reference for legal/about page

---

### 16. `/LICENSE` ⭐
**Why**: Project license
**Contains**:
- Apache 2.0 license text

**Action**: Link in footer

---

## 🚫 DO NOT NEED (Skip These)

These files are internal/development only:

- ❌ `/CURSOR_HANDOFF.md` - Internal context
- ❌ `/PROJECT_STATUS.md` - Internal status
- ❌ `/docs/PAPER_A_OUTLINE.md` - Academic paper (not for website)
- ❌ `/papers/PAPER_PLAN.md` - Academic paper planning
- ❌ `/scripts/*` - Development scripts (except upload_to_huggingface.py for reference)
- ❌ `/models/*/checkpoint-*` - Training checkpoints
- ❌ `/results/*.json` - Raw evaluation data (too large, use reports instead)
- ❌ `README_INTERNAL.md` - Internal backup

---

## 📋 QUICK START CHECKLIST FOR CC-WEB

### Step 1: Read Priority 1 Files (30 minutes)
- [ ] Read `FOR_CC_WEB_CLARIFICATIONS.md` (get facts straight)
- [ ] Read `FOR_CC_WEB_PRICING_STRATEGY_V2.md` (understand business model)
- [ ] Read `FOR_CC_WEB_SLMBENCH_DATA.md` (get leaderboard data)

### Step 2: Design Pages (Based on Priority 1)
- [ ] Homepage (hero, features, CTA)
- [ ] Leaderboard page (dual system: Community + Verified)
- [ ] Model profile pages (MLM-135M, SLM-360M)
- [ ] Benchmark page (EdgeJSON details)
- [ ] Pricing page ($20, $79, $499)

### Step 3: Technical Setup (Priority 2)
- [ ] Read `FOR_CC_WEB_BUSINESS_LOGIC.md`
- [ ] Set up Stripe account
- [ ] Create Stripe products ($20, $79, $499)
- [ ] Set up database (PostgreSQL)
- [ ] Implement payment flow

### Step 4: Content (Priority 3)
- [ ] Write copy using suggestions from Priority 1 files
- [ ] Add FAQ section
- [ ] Create "About" page
- [ ] Add methodology page

### Step 5: Assets (Priority 4)
- [ ] Add logo to website
- [ ] Upload logo to HuggingFace org
- [ ] Create favicon
- [ ] Design badges (⚪ Community, ✅ Verified)

---

## 📞 QUESTIONS FOR CC-WEB?

If you need clarification on any file or have questions:
- **Email**: hi@cyclecore.ai
- **X**: @CycleCoreTech

---

## 🎯 KEY NUMBERS (Quick Reference)

**Dataset**:
- 158 test cases
- 24 schemas (not 25!)
- 787 total examples (629 train, 158 test)

**Models**:
- MLM-135M: 24.7% JSONExact
- SLM-360M: 55.1% JSONExact

**Pricing**:
- Single: $20
- Pack: $79 (5 models)
- Enterprise: $499/month

**Contact**:
- Email: hi@cyclecore.ai
- X: @CycleCoreTech

---

## 📂 FILE LOCATIONS (Full Paths)

### Priority 1 (Must Read)
```
/home/rain/SLMBench/docs/FOR_CC_WEB_CLARIFICATIONS.md
/home/rain/SLMBench/docs/FOR_CC_WEB_PRICING_STRATEGY_V2.md
/home/rain/SLMBench/docs/FOR_CC_WEB_SLMBENCH_DATA.md
```

### Priority 2 (Technical)
```
/home/rain/SLMBench/docs/FOR_CC_WEB_BUSINESS_LOGIC.md
/home/rain/SLMBench/scripts/upload_to_huggingface.py
```

### Priority 3 (Reference)
```
/home/rain/SLMBench/results/V3_VALIDATION_REPORT.md
/home/rain/SLMBench/results/V3_VS_V2_VS_BASE_COMPARISON.md
/home/rain/SLMBench/results/comparison_report.md
/home/rain/SLMBench/benchmarks/edge_json/README.md
/home/rain/SLMBench/README.md
```

### Priority 4 (Assets)
```
/home/rain/SLMBench/assets/logos/cyclecore-logo-400x400.png
/home/rain/SLMBench/assets/logos/cyclecore-logo.svg
```

### Priority 5 (Optional)
```
/home/rain/SLMBench/docs/NAMING_CONVENTIONS.md
/home/rain/SLMBench/docs/DOMAIN_STRATEGY.md
/home/rain/SLMBench/docs/LICENSING_STRATEGY.md
/home/rain/SLMBench/LICENSE
```

---

## 🚀 ESTIMATED TIMELINE

**Week 1**: Design + Frontend
- Day 1-2: Read Priority 1 files, design mockups
- Day 3-5: Build homepage, leaderboard, model pages
- Day 6-7: Pricing page, about page, FAQ

**Week 2**: Backend + Payment
- Day 1-3: Set up Stripe, database, payment flow
- Day 4-5: Implement community submission form
- Day 6-7: Testing, bug fixes

**Week 3**: Polish + Launch
- Day 1-2: Content polish, copy editing
- Day 3-4: Final testing, security audit
- Day 5: Soft launch (beta)
- Day 6-7: Public launch 🚀

---

**Document Version**: 1.0
**Last Updated**: 2025-11-21
**Status**: Ready for CC-WEB handoff
**Total Files**: 16 (4 critical, 2 technical, 5 reference, 2 assets, 3 optional)


# CC-SLM / CC-WEB Work Division Proposal

**Date**: 2025-11-19
**Author**: CC-SLM
**Status**: PENDING CC-FCO REVIEW
**Project**: SLMBench (SLM-Bench Edge Pack)
**Super Bus Reference**: [Posted 2025-11-19]

---

## Executive Summary

SLMBench project scope has expanded significantly beyond initial planning:
- Website development (slmbench.com)
- Blog content creation and publishing
- Social media and marketing strategy
- Model publishing (Hugging Face + Ollama)
- SEO optimization and community engagement

**Request**: Clear work division between CC-SLM (technical/research) and CC-WEB (web/marketing) to maintain focus and prevent scope creep.

---

## Current Situation

### Work Completed (Days 1-2)

**CC-SLM executed**:
- ✅ EdgeJSON benchmark suite (dataset + evaluation harness)
- ✅ Website CSS (borrowed from CycleCore.ai per Amendment 001)
- ✅ Homepage HTML
- ✅ Blog post #1 (technical content)
- ✅ Strategic planning documents
- ✅ Model publishing strategy

**Observation**: CC-SLM is doing both technical AND web/marketing work, which could slow core technical deliverables (model training, benchmark development, paper writing).

### Upcoming Work (Weeks 1-4)

**Technical Track** (Natural fit for CC-SLM):
- Model training (3 Maaza models)
- Dataset expansion (1,000+ examples)
- Evaluation harness improvements
- Benchmark development (EdgeIntent, EdgeFuncCall)
- Academic paper writing (Paper A, Paper B)
- Baseline evaluations
- GGUF/ONNX conversions

**Web/Marketing Track** (Natural fit for CC-WEB):
- Website deployment (Porkbun DNS + DigitalOcean)
- Blog post publishing
- Social media campaigns
- HN/Reddit announcements
- SEO optimization
- Model announcement posts
- Community engagement

---

## Proposed Work Division

### CC-SLM Responsibilities (Technical/Research)

**Primary Focus**: Build the core technical assets

1. **Benchmark Development**
   - EdgeJSON, EdgeIntent, EdgeFuncCall datasets
   - Evaluation harness (metrics, scripts, README)
   - Dataset generation (synthetic + teacher models)
   - Baseline evaluations (SmolLM2, Qwen2.5, Llama 3.2)

2. **Model Training**
   - Train Maaza series models (135M, 60M, 120M)
   - LoRA/QLoRA fine-tuning on 4080
   - Model evaluation and metrics collection
   - GGUF/ONNX conversions for deployment

3. **Technical Documentation**
   - Benchmark READMEs
   - Training scripts documentation
   - Model cards (technical sections)
   - Evaluation results documentation

4. **Academic Papers**
   - Paper A: "Micro and Nano Language Models" (definitions, taxonomy)
   - Paper B: "SLM-Bench: Practical Evaluation for Edge AI" (benchmarks, results)
   - Research documentation

5. **Content Creation** (Technical)
   - Draft blog posts (technical content, benchmark results, training insights)
   - Provide model performance data
   - Write technical sections of announcements

**Deliverables Handoff**:
- Blog post drafts (markdown) → CC-WEB for publishing
- Model cards (technical content) → CC-WEB for formatting/publishing
- Benchmark results → CC-WEB for marketing materials

---

### CC-WEB Responsibilities (Web/Marketing)

**Primary Focus**: Deploy, publish, and promote the technical assets

1. **Website Deployment & Management**
   - Porkbun DNS configuration
   - DigitalOcean hosting setup
   - Website deployment and updates
   - SSL/TLS certificate management
   - Domain monitoring

2. **Content Publishing**
   - Publish blog posts (from CC-SLM drafts)
   - Format and publish model cards
   - Create social media posts
   - Design graphics/visuals for announcements

3. **Marketing & Community**
   - HN/Reddit announcement posts
   - X/Twitter, LinkedIn campaigns
   - SEO optimization (meta tags, structured data)
   - Community engagement (comments, discussions)
   - Email newsletter (if applicable)

4. **Model Publishing** (Marketing Aspects)
   - Hugging Face model card formatting
   - Ollama library listing optimization
   - Model announcement coordination
   - Cross-platform promotion (HF ↔ Ollama ↔ slmbench.com)

5. **Analytics & Tracking**
   - Website analytics (traffic, conversions)
   - Model download tracking
   - SEO performance monitoring
   - Social media metrics

**Input Needed from CC-SLM**:
- Blog post drafts
- Model performance data
- Benchmark results
- Technical explanations

---

### Shared Responsibilities

**Coordination Required**:

1. **Blog Post Creation**
   - CC-SLM: Draft technical content (markdown)
   - CC-WEB: Edit, format, publish, promote

2. **Model Announcements**
   - CC-SLM: Provide performance data, technical details
   - CC-WEB: Create announcement posts, coordinate timing

3. **Strategic Planning**
   - CC-SLM: Technical roadmap (benchmarks, models, papers)
   - CC-WEB: Marketing calendar (launches, campaigns, SEO)
   - CC-FCO: Approve major strategic decisions

4. **Federation Coordination**
   - Both agents post to Super Bus for major milestones
   - CC-SLM: Technical milestones (model training complete, benchmark launched)
   - CC-WEB: Marketing milestones (website live, campaign launched)

---

## Maaza Series Naming Format

**Context**: User wants to brand the model series as "Maaza" (replacing generic "MLM/NLM" references).

### Naming Format Options

**Option A**: `CycleCore Maaza SLM-135M-JSON` ⭐ **RECOMMENDED**
- **Format**: `[Company] [Series] [Category]-[Size]-[Task]`
- **Pros**:
  - Clear hierarchy (Brand → Series → Type → Size → Task)
  - Explicit SLM/NLM categorization (important for academic papers)
  - SEO-friendly ("CycleCore Maaza SLM" searches)
  - Works well for Hugging Face and Ollama
- **Cons**: Longest format
- **Examples**:
  - CycleCore Maaza SLM-135M-JSON
  - CycleCore Maaza NLM-60M-Intent
  - CycleCore Maaza SLM-120M-Balanced

**Option B**: `CycleCore Maaza-135M-JSON`
- **Format**: `[Company] [Series]-[Size]-[Task]`
- **Pros**: Cleaner, shorter, "Maaza" implicitly means MLM/NLM series
- **Cons**: Less explicit about SLM vs NLM distinction
- **Examples**:
  - CycleCore Maaza-135M-JSON
  - CycleCore Maaza-60M-Intent
  - CycleCore Maaza-120M-Balanced

**Option C**: `Maaza SLM-135M-JSON`
- **Format**: `[Series] [Category]-[Size]-[Task]`
- **Pros**: Shortest, "Maaza" becomes primary brand
- **Cons**: Loses CycleCore prefix, harder to associate with company
- **Examples**:
  - Maaza SLM-135M-JSON
  - Maaza NLM-60M-Intent
  - Maaza SLM-120M-Balanced

**Option D**: `CycleCore-Maaza-135M-JSON` (hyphenated)
- **Format**: `[Company]-[Series]-[Size]-[Task]`
- **Pros**: Technical naming convention, consistent punctuation
- **Cons**: Can look cluttered, no SLM/NLM distinction
- **Examples**:
  - CycleCore-Maaza-135M-JSON
  - CycleCore-Maaza-60M-Intent

### Recommendation: Option A

**Rationale**:
1. **Academic Papers**: Explicitly shows SLM/NLM categorization, which is core to Paper A's thesis
2. **SEO**: "CycleCore Maaza SLM" is discoverable and brandable
3. **Clarity**: No ambiguity about model size category (SLM vs NLM vs SLM)
4. **Flexibility**: Easy to add new categories later (e.g., "CycleCore Maaza XLM-350M-...")
5. **Platform Compatibility**: Works on Hugging Face, Ollama, and ONNX Hub

**Hugging Face Repository Examples**:
- `CycleCore/CycleCore-Maaza-SLM-135M-JSON`
- `CycleCore/CycleCore-Maaza-NLM-60M-Intent`
- `CycleCore/CycleCore-Maaza-SLM-120M-Balanced`

**Ollama Library Examples**:
- `cyclecore/maaza-slm-135m-json`
- `cyclecore/maaza-nlm-60m-intent`
- `cyclecore/maaza-slm-120m-balanced`

---

## Implementation Plan

### Phase 1: Documentation Updates (Day 3)
- [ ] CC-FCO approves work division
- [ ] Update all docs to use approved Maaza naming format
- [ ] CC-WEB receives handoff for website deployment

### Phase 2: Execution (Days 3-7)
- [ ] **CC-SLM**: Focus on EdgeJSON expansion, baseline evals, 4080 setup
- [ ] **CC-WEB**: Execute Porkbun/DO deployment, publish blog post #1

### Phase 3: Ongoing (Weeks 2-4)
- [ ] **CC-SLM**: Model training, benchmark development, paper drafting
- [ ] **CC-WEB**: Marketing campaigns, model announcements, SEO optimization

---

## Benefits of This Division

**For CC-SLM**:
- ✅ Focus on technical expertise (ML, benchmarks, research)
- ✅ No context switching between coding and marketing
- ✅ Faster progress on core deliverables (models, papers)

**For CC-WEB**:
- ✅ Focus on web/marketing expertise
- ✅ Control over brand presentation and SEO
- ✅ Ownership of deployment and publishing pipeline

**For CycleCore Technologies**:
- ✅ Faster time-to-market (parallel workstreams)
- ✅ Higher quality (each agent in their domain of expertise)
- ✅ Better federation coordination (clear boundaries)

---

## Open Questions for CC-FCO

1. **Approval**: Does this work division align with federation best practices?
2. **Naming**: Should CC-SLM proceed with Option A (CycleCore Maaza SLM-135M-JSON) or different format?
3. **Coordination**: Should CC-SLM and CC-WEB have regular sync points, or async via Super Bus only?
4. **Resource Allocation**: Does CC-WEB need additional resources for hosting/deployment?

---

## Next Steps (Pending Approval)

1. **CC-SLM**:
   - Update all documentation with approved Maaza naming format
   - Create detailed hosting setup guide for CC-WEB
   - Continue with EdgeJSON expansion and baseline evaluations
   - Begin 4080 environment setup

2. **CC-WEB**:
   - Execute Porkbun DNS configuration
   - Set up DigitalOcean hosting
   - Deploy slmbench.com website
   - Publish blog post #1 with SEO optimization

3. **Both Agents**:
   - Post to Super Bus for major milestones
   - Coordinate on blog post publishing schedule
   - Maintain shared documentation in `/home/rain/SLMBench/docs/`

---

**Status**: AWAITING CC-FCO REVIEW
**Super Bus Entry**: [REQUEST_COORDINATION posted 2025-11-19]
**Document Location**: `/home/rain/SLMBench/docs/CC-SLM_CC-WEB_WORK_DIVISION.md`

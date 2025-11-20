# CycleCore Technologies SLMBench: 30-Day MVP Strategic Plan

**Agent**: CC-SLM (SLM-Bench Edge Pack)
**Date**: 2025-11-19
**Status**: ACTIVE - Post-Investigation Planning Phase
**Domain**: slmbench.com (ACQUIRED)

---

## Executive Summary

CycleCore Technologies SLMBench is positioning to own the "practical edge AI evaluation" category through a three-pronged strategy:

1. **Build SLM-Bench Practical Suite**: Function calling, JSON extraction, and intent classification benchmarks (gaps in academic SLM-Bench)
2. **Train CycleCore Maaza Series**: Use idle 4080 GPU to distill/train baseline models while validating benchmarks
3. **Publish Academic Papers**: Define MLM (Micro Language Models) and NLM (Nano Language Models) categories, establish thought leadership

**30-Day Goal**: Launch slmbench.com with live leaderboard, 3+ CycleCore-trained models, and evaluation service offering.

---

## Strategic Positioning

### The Opportunity

**Market Timing** (November 2025):
- Academic SLM-Bench paper just published (Aug-Sep 2025) - validates market need
- Domain slmbench.com acquired - SEO/credibility advantage
- Function calling benchmarks underserved (academic SLM-Bench doesn't cover this)
- No standardized energy measurement for edge deployment
- Missing cross-platform validation (browser, Pi, laptop)

### CycleCore Differentiation

**vs Academic SLM-Bench**:
- **Them**: Comprehensive (15 models, 9 tasks, 23 datasets) - research-grade
- **Us**: Practical edge focus (JSON extraction, function calling, energy measurement)

**Brand Strategy**:
- **Primary**: "CycleCore Technologies SLMBench" (not just "SLMBench")
- **Positioning**: "Edge Pack - Practical benchmarks for production SLM deployment"
- **Future**: NLMBench.com (sub-10MB models, separate brand)

### The MLM/NLM Naming Play

**Strategic Goal**: Own category definitions through academic papers + slmbench.com

**MLM (Micro Language Models)**:
- Definition: 10M-250M parameters
- Target tasks: JSON extraction, intent classification, function calling
- Hardware: Edge devices (Pi, laptop CPU, browser WebGPU)
- Use cases: Structured tasks, not general chat

**NLM (Nano Language Models)**:
- Definition: <10MB footprint (3-10M params typical)
- Target tasks: Intent routing, spam filtering, PII detection
- Hardware: Embedded devices, ultra-low-power edge
- Use cases: Highly specialized, single-task models

**Academic Plan**:
- Paper A: Define MLM/NLM + introduce SLM-Bench (target: arXiv by Week 6)
- Paper B: Distillation methods for MLMs (after training pipeline proven)
- Paper C: NLM specialization (long-term, post-MVP)

---

## The 4080 Training Strategy

### Why This Matters

**Current State**: 4080 GPU idles frequently between other projects
**Opportunity**: Use downtime to train CycleCore MLM series
**Benefit**: Validate benchmarks with real models, create "CycleCore Certified" baselines

### Training Pipeline (Feedback Loop)

```
1. Build SLM-Bench benchmark
   ↓
2. Generate synthetic training data (via teacher model)
   ↓
3. Train CycleCore Maaza model on 4080 (24-48 hours)
   ↓
4. Evaluate on SLM-Bench
   ↓
5. Refine benchmark based on results
   ↓
6. Repeat
```

### Model Roadmap

**Week 1-2: CycleCore Maaza SLM-135M-JSON**
- Base: SmolLM2-135M (fine-tune) or distill from Qwen2.5-7B
- Task: JSON extraction specialist
- Size: ~250MB unquantized
- Training time: 24-48 hours on 4080
- Goal: Validate EdgeJSON benchmark

**Week 2-3: CycleCore Maaza NLM-60M-Intent**
- Base: Distill from Llama 3.2-3B
- Task: Intent classification (50-200 classes)
- Size: ~120MB unquantized
- Training time: 18-24 hours
- Goal: Ultra-compact intent router

**Week 3-4: CycleCore Maaza SLM-120M-Balanced**
- Base: Distill from Qwen2.5-7B
- Task: JSON + Intent (multi-task)
- Size: ~240MB unquantized
- Training time: 36-48 hours
- Goal: Balanced edge model

**Post-MVP: CycleCore-NLM-5M-Filter**
- Base: Distill from CycleCore Maaza NLM-60M-Intent
- Task: Spam/PII filtering
- Size: <10MB (heavy quantization)
- Training time: 12-18 hours
- Goal: Proof-of-concept NLM

### Model Naming Convention

```
CycleCore-{Category}-{Size}-{Specialty}

Examples:
- CycleCore Maaza SLM-135M-JSON
- CycleCore Maaza NLM-60M-Intent
- CycleCore Maaza SLM-120M-Balanced
- CycleCore-NLM-5M-Filter
```

**Branding Rationale**:
- "CycleCore" prefix: Brand ownership, differentiation
- Category (MLM/NLM): Reinforces category definitions
- Size: Transparency (parameter count)
- Specialty: Clear use case

---

## 30-Day Roadmap

### Week 1: Foundation + Content (Days 0-7)

**Domain & Site**:
- Point slmbench.com to hosting
- Deploy static site (CycleCore dark mode design)
- Homepage: "CycleCore Technologies SLMBench - Edge Pack"
- Blog setup (markdown-based)

**Content** (3 posts):
1. "Introducing CycleCore SLMBench: Practical Edge AI Evaluation"
2. "MLMs and NLMs: Defining Micro and Nano Language Models"
3. "EdgeJSON: Function Calling Benchmarks for SLMs"

**Research**:
- Digest GPT chat + ecosystem research
- Draft Paper A outline (MLM/NLM definitions + SLM-Bench)
- Identify benchmark gaps

**4080 Setup**:
- Training environment (venv, PyTorch, Transformers)
- Download teacher models (Qwen2.5-7B, Llama 3.2-3B)
- Test inference/training speed

**Deliverable**: Live site with content, training environment ready

---

### Week 2: EdgeJSON Benchmark + First Model (Days 8-14)

**Benchmark**:
- Generate 1,000 JSON extraction test cases (synthetic)
- Schema complexity levels (simple, medium, complex)
- Evaluation harness (Python script)
- Metrics: JSONExact, FieldF1, SchemaCompliance

**Model Training**:
- Train CycleCore Maaza SLM-135M-JSON on 4080
- Baseline comparisons: SmolLM2-135M, Qwen2.5-0.5B
- Publish to Hugging Face

**Content**:
- Post 4: "EdgeJSON Benchmark Results: Baseline Models"

**Deliverable**: EdgeJSON benchmark + first CycleCore model

---

### Week 3: EdgeIntent Benchmark + Leaderboard (Days 15-21)

**Benchmark**:
- EdgeIntent task: 50-200 class intent classification
- Synthetic dataset (diverse domains)
- Metrics: Accuracy, latency, energy estimate

**Model Training**:
- Train CycleCore Maaza NLM-60M-Intent on 4080
- Compare against baselines

**Leaderboard Launch**:
- Add results table to slmbench.com
- Baseline models: SmolLM2, Qwen2.5, CycleCore MLMs
- Methodology page (transparent, reproducible)
- Submit to HN, Reddit r/LocalLLaMA

**Deliverable**: Live leaderboard with 5+ models

---

### Week 4: EdgeFuncCall + Service Offering (Days 22-30)

**Benchmark**:
- EdgeFuncCall task: Multi-turn tool use scenarios
- Function parameter extraction accuracy
- Error recovery metrics

**Model Training**:
- Train CycleCore Maaza SLM-120M-Balanced on 4080
- Full SLM-Bench evaluation

**Service Launch**:
- Pricing page: $2.5K (basic), $5K (standard), $7.5K (premium)
- Request evaluation form
- Case study template
- First outreach: 5-10 SLM developers

**Paper A**:
- Complete first draft (Intro, Related Work, MLM Spec, SLM-Bench, Results)
- Target: arXiv submission Week 6

**Deliverable**: Evaluation service offering, Paper A draft

---

## Day 30 Success Metrics

**Website**:
- ✅ slmbench.com live with dark mode
- ✅ 4-5 blog posts published
- ✅ Leaderboard with 5+ models
- ✅ Evaluation service page

**Benchmark**:
- ✅ EdgeJSON complete (1,000 test cases)
- ✅ EdgeIntent complete (50-200 classes)
- ✅ EdgeFuncCall MVP
- ✅ Evaluation harness (reproducible)

**Models**:
- ✅ CycleCore Maaza SLM-135M-JSON trained & published
- ✅ CycleCore Maaza NLM-60M-Intent trained & published
- ✅ CycleCore Maaza SLM-120M-Balanced trained & published

**Academic**:
- ✅ Paper A first draft complete
- ✅ Ready for arXiv submission

**Business**:
- ✅ Pricing structure defined
- ✅ First outreach campaign launched
- ✅ 1-2 inbound leads

---

## Technology Stack

**Benchmarking**:
- Python 3.10+
- HuggingFace Transformers
- ONNX Runtime (cross-platform)
- Custom evaluation harness

**Model Training**:
- PyTorch 2.0+
- 4080 GPU (24GB VRAM)
- LoRA/QLoRA for efficient fine-tuning
- Distillation from Qwen2.5-7B, Llama 3.2-3B

**Website**:
- Static site (HTML/CSS/JS)
- CycleCore dark mode design (pure black #0a0a0a)
- Markdown for blog posts
- JSON for leaderboard data

**Energy Measurement** (Post-MVP):
- Joulescope JS110 power meter (when acquired)
- Standardized protocol for reproducibility

---

## NLMBench Future Expansion

**Timeline**: Post-MVP (Months 2-3)
**Domain**: nlmbench.com (to be acquired)

**Strategy**:
- Split off <10MB models into separate brand
- Different market: embedded devices, ultra-low-power
- Separate leaderboard, evaluation service
- Cross-link from slmbench.com

**First NLM**:
- CycleCore-NLM-5M-Filter
- Spam/PII filtering specialist
- <10MB footprint
- Proof-of-concept for category

---

## Business Model

**Evaluation-as-a-Service**:
- Basic: $2,500 (EdgeJSON only)
- Standard: $5,000 (EdgeJSON + EdgeIntent)
- Premium: $7,500 (Full SLM-Bench + energy measurement)

**Target Market**:
- SLM developers (Hugging Face community)
- Hardware vendors (Raspberry Pi, Jetson)
- Enterprises deploying edge AI

**Revenue Targets**:
- Month 1: 0-1 customers ($0-$7.5K)
- Month 3: 3-5 customers ($7.5K-$37.5K)
- Year 1: 10-20 evaluations ($50K-$100K)

**Marketing Funnel**:
- Free leaderboard → credibility
- Blog posts → SEO traffic
- Academic papers → thought leadership
- HN/Reddit → developer audience
- Paid evaluation service → revenue

---

## Code Sharing from Lexopoly

Per Constitutional Amendment 001 and DOCK-025, SLM-Bench can freely copy code from:
- Orchestra (deployment, GPU management)
- ComplianceLogger (web UI patterns)
- MCPBodega (if applicable)

**Process**: Direct copy + document source in commit message.

---

## Risk Mitigation

**Risk 1: Academic SLM-Bench conflict**
- Mitigation: Position as complement (practical vs research), cite their work

**Risk 2: 4080 training quality**
- Mitigation: Start with fine-tuning (easier), then distillation

**Risk 3: No evaluation customers**
- Mitigation: Free leaderboard drives traffic, build audience first

**Risk 4: MLM/NLM naming doesn't stick**
- Mitigation: Still valuable benchmarks, category naming is bonus

---

## Next Steps

See `ROADMAP_WEEK1.md` for detailed Day 0-7 action items.

**Immediate**:
1. Commit research updates
2. Create project structure
3. Draft website homepage
4. Outline Paper A
5. Set up 4080 training environment

---

**Status**: READY TO EXECUTE
**Spinup Date**: 2025-11-19
**Agent**: CC-SLM (Territory: CycleCore Technologies LLC)

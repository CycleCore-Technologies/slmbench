# GPT Assignment: Draft Introduction Section

**Date**: November 22, 2025  
**Status**: FOR GPT - Draft Introduction  
**Context**: Academic paper on Maaza MLMs and EdgeJSON benchmark

---

## 📋 **Your Assignment**

Draft the **Introduction section** (2-3 pages, ~1000-1500 words) for our academic paper.

**Target audience**: ML researchers, edge AI practitioners, NLP conference reviewers

**Tone**: Academic but accessible, clear narrative arc, strong empirical backing

---

## 🎯 **What We Need**

### Section Structure

**1.1 Motivation & Problem Statement** (~400 words)
- Open with edge AI deployment challenges
- Why structured data extraction matters (sensors, IoT, APIs)
- Current limitations: LLMs too big, SLMs struggle zero-shot
- The core tension: power vs capability

**1.2 Our Approach & Key Insight** (~300 words)
- Task specialization > parameter scaling (for structured tasks)
- Fine-tuning micro models beats deploying large zero-shot models
- Practical: 135M-360M models run on edge devices

**1.3 Contributions** (~300 words)
- EdgeJSON benchmark (787 examples, 24 schemas, validated)
- Maaza MLM series (135M, 360M, open-source)
- Empirical findings (fine-tuned 135M beats zero-shot 500M)
- Open methodology (reproducible, Apache 2.0)

**1.4 Key Results Preview** (~200 words)
- Main table: Maaza-MLM-135M (24.7%) vs Qwen2.5-0.5B (14.6%)
- Headline: 1.7× better performance, 3.7× smaller size
- Maaza-SLM-360M: 55.1% (3.8× better than Qwen)

**1.5 Paper Organization** (~100 words)
- Brief roadmap of remaining sections

---

## 📊 **Key Data to Incorporate**

### Verified Results (Use These Numbers)

**Main Comparison**:
| Model | Params | Type | JSONExact | Field F1 | Size (MB) |
|-------|--------|------|-----------|----------|-----------|
| SmolLM2-135M (base) | 135M | Zero-shot | 1.9% | 0.024 | 270 |
| **Maaza-MLM-135M** | 135M | Fine-tuned | **24.7%** | **0.520** | 270 |
| Qwen2.5-0.5B | 500M | Zero-shot | 14.6% | 0.195 | 954 |
| **Maaza-SLM-360M** | 360M | Fine-tuned | **55.1%** | **0.780** | 720 |

**Key Claims** (All Verified):
1. Fine-tuned 135M beats zero-shot 500M (24.7% vs 14.6%)
2. Fine-tuning gives 13× improvement (135M: 1.9% → 24.7%)
3. Zero-shot scaling gives only 7.7× improvement (135M: 1.9% → 500M: 14.6%)
4. **Task specialization > parameter scaling** (for structured tasks)

**EdgeJSON Benchmark**:
- 787 total examples (629 train, 158 test)
- 24 schema types (8 simple, 11 medium, 5 complex)
- 3 complexity bands
- 100% quality-validated (synthetic data from Qwen2.5-7B teacher)
- Reproducible evaluation (verified across 2 independent runs)

**Training Efficiency**:
- Maaza-MLM-135M: <1 minute training time
- Maaza-SLM-360M: <2 minutes training time
- LoRA fine-tuning (rank 8)
- Single RTX 3090

---

## 🎨 **Narrative Arc**

### Opening (Hook)
Start with a concrete scenario:
> "A Raspberry Pi monitoring sensor data needs to extract structured JSON from text logs. A cloud API call to GPT-4 adds 200ms latency and costs $0.01 per request. An on-device 7B model requires 14GB RAM the Pi doesn't have. What if a 270MB model could do the job—accurately, locally, in 50ms?"

### Build Tension
- Edge AI is exploding (IoT, mobile, privacy-sensitive apps)
- Structured data extraction is critical (APIs, sensors, forms)
- Current options are bad: cloud = expensive/slow, large SLMs = too big, small models = inaccurate

### Our Insight
- **Task specialization beats parameter scaling** (for structured tasks)
- We fine-tune 135M-360M models on JSON extraction
- They beat larger zero-shot models while being edge-deployable

### Contributions
- EdgeJSON: First benchmark for edge JSON extraction
- Maaza: First MLM series optimized for structured output
- Empirical evidence: Fine-tuned 135M > Zero-shot 500M
- Open source: Models, data, code (Apache 2.0)

### Preview Results
- Show the money table (Maaza-MLM-135M: 24.7% vs Qwen: 14.6%)
- Emphasize practical impact: smaller, faster, edge-ready

### Transition
- "The rest of this paper..."
- Roadmap to sections

---

## 📝 **Stylistic Notes**

### Do:
- ✅ Use concrete examples (Raspberry Pi, IoT sensors)
- ✅ Emphasize practical impact (size, latency, edge deployment)
- ✅ Lead with empirical findings (numbers early and often)
- ✅ Be precise about claims (fine-tuned vs zero-shot, 135M vs 500M)
- ✅ Use active voice ("We present...", "We demonstrate...")

### Don't:
- ❌ Overclaim (stick to verified results)
- ❌ Be vague ("small models work better" → "135M fine-tuned beats 500M zero-shot")
- ❌ Bury the lede (key result should appear in 1.4)
- ❌ Use jargon without definition ("MLM" needs one-sentence explanation)

---

## 🔗 **Context Documents**

You previously provided the Related Work section. Here's what you already know:

**Related Work Topics**:
- SLM evolution (DistilBERT → TinyLlama → SmolLM2)
- Benchmarks (GLUE, MMLU, SLM-Bench by Pham et al.)
- Edge AI frameworks (TFLite, ONNX, WebLLM)
- Fine-tuning methods (LoRA, distillation)

**Positioning**:
- SLM-Bench (Pham et al., 2025): General NLP tasks (MMLU, GSM8K)
- **Our EdgeJSON**: Specialized structured output tasks (JSON extraction)
- Complementary, not competing

**MLM Terminology**:
- MLM = Micro Language Model (10M-250M params, decoder-only)
- NOT "Masked Language Model" (BERT-era, encoder-only, legacy)
- Define clearly in Introduction: "We introduce the term Micro Language Model (MLM) for decoder-only models with 10M-250M parameters, distinct from the legacy 'Masked Language Model' used in encoder-only architectures [Devlin et al., 2019]."

---

## 🎯 **Success Criteria**

A successful Introduction should:
1. ✅ Hook the reader (concrete scenario, clear problem)
2. ✅ State the gap (structured tasks underexplored for edge AI)
3. ✅ Present our solution (Maaza MLMs + EdgeJSON)
4. ✅ Preview key results (24.7% vs 14.6%, 13× improvement)
5. ✅ List contributions (benchmark, models, findings, methodology)
6. ✅ Set up the rest of the paper (clear roadmap)
7. ✅ Be citation-ready (precise numbers, proper framing)

---

## 📤 **Deliverable**

Please draft:
1. **Full Introduction section** (1.1-1.5, ~1000-1500 words)
2. **Main results table** (formatted for LaTeX if possible)
3. **Opening paragraph** (hook + problem statement)

Use the structure above but feel free to adjust for better flow. We want this to be **compelling**, **precise**, and **empirically grounded**.

---

## 🚀 **Why This Matters**

The Introduction is where we:
- Hook reviewers ("fine-tuned 135M beats zero-shot 500M" is surprising!)
- Frame our contribution (not just "we built models", but "we show task specialization > scaling")
- Set expectations (this is empirical ML research, not just a benchmark paper)

Make it strong, clear, and impossible to ignore.

---

**Ready when you are!** 🥤

---

**Files for Reference**:
- `/home/rain/SLMBench/papers/PAPER_PLAN_V2_WITH_QWEN.md` (full paper plan)
- `/home/rain/SLMBench/papers/GPT_RELATED_WORK_DRAFT.md` (your previous work)
- `/home/rain/SLMBench/papers/MLM_TERMINOLOGY_POSITION.md` (official MLM definition)
- `/home/rain/SLMBench/results/BASELINE_QWEN_VERIFIED.md` (verified baseline results)


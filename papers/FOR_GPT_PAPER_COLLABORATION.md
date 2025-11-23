# For GPT: Academic Paper Collaboration Brief

**Date**: November 21, 2025  
**Project**: Maaza MLMs + EdgeJSON Benchmark  
**Your Role**: Background research, Related Work section, literature review

---

## 🎯 **What We're Writing**

### Paper Title (Working)
"Maaza: Task-Specialized Micro Language Models Outperform Larger Zero-Shot Models on Structured Data Extraction"

### Core Finding
**Fine-tuned 135M model beats zero-shot 500M model on JSON extraction**
- Maaza-MLM-135M (135M params): 24.7% accuracy
- Qwen2.5-0.5B (500M params): 14.6% accuracy
- **1.7× better despite being 3.7× smaller**

### Why This Matters
- Challenges "bigger is always better" narrative
- Validates edge AI / on-device ML approaches
- Shows task specialization > parameter scaling
- Practical for Raspberry Pi, browser, CPU-only laptops

---

## 📊 **Our Results (Verified, Reproducible)**

| Model | Params | JSONExact | Field F1 | Size | Type |
|-------|--------|-----------|----------|------|------|
| SmolLM2-135M (base) | 135M | 1.9% | 0.024 | 270MB | Zero-shot |
| **Maaza-MLM-135M** | 135M | **24.7%** | **0.520** | 270MB | Fine-tuned |
| Qwen2.5-0.5B | 500M | 14.6% | 0.195 | 954MB | Zero-shot |
| **Maaza-SLM-360M** | 360M | **55.1%** | **0.780** | 720MB | Fine-tuned |

**Key Points**:
1. Fine-tuning provides 13× improvement (135M: 1.9% → 24.7%)
2. Fine-tuned 135M beats zero-shot 500M (24.7% > 14.6%)
3. Fine-tuned 360M crushes zero-shot 500M (55.1% vs 14.6% = 3.8×)

---

## 🤝 **What We Need From You (GPT)**

### 1. **Related Work Section** (2-3 pages)

**Topics to Cover**:

#### A. Small Language Models (SLMs)
- **Recent models**: SmolLM2, Qwen2.5, Llama 3.2, Phi-3, Gemma
- **Evolution**: 2023 (TinyLlama 1.1B) → 2024 (SmolLM 135M) → 2025 (SmolLM2, Llama 3.2)
- **Key papers**: Find 10-15 recent SLM papers (2024-2025)
- **What to highlight**: Parameter counts, training data, performance on benchmarks

**Questions to Answer**:
- What's the current state-of-the-art for small models?
- How small have models gotten while maintaining quality?
- What tasks do SLMs excel at?

#### B. Benchmarks for Language Models
- **General**: MMLU, HellaSwag, GSM8K, HumanEval
- **SLM-specific**: SLM-Bench (Pham et al., 2025)
- **Gap**: No benchmarks for structured output (JSON, function calling) on edge

**Questions to Answer**:
- What benchmarks exist for evaluating small models?
- What's missing? (hint: structured output, edge deployment)
- How does our EdgeJSON benchmark fill the gap?

#### C. Edge AI and Deployment
- **Frameworks**: TensorFlow Lite, ONNX Runtime, WebLLM, Transformers.js
- **Hardware**: Raspberry Pi, mobile, browser (WebGPU)
- **Challenges**: Memory, latency, energy

**Questions to Answer**:
- What's the current state of edge AI deployment?
- What constraints do edge devices have?
- Why do we need smaller models?

#### D. Fine-Tuning and Adaptation
- **Methods**: LoRA, QLoRA, prompt tuning, prefix tuning
- **When it helps**: Task-specific data, structured output
- **Our approach**: LoRA fine-tuning on 629 examples

**Questions to Answer**:
- What fine-tuning methods exist?
- When does fine-tuning beat zero-shot?
- What's the trade-off (training cost vs deployment benefit)?

### 2. **Literature Review** (30-50 citations)

**Categories**:

#### SLM Papers (10-15 citations)
- SmolLM2 (Hugging Face, 2024)
- Qwen2.5 Technical Report (Alibaba, 2024)
- Llama 3.2 (Meta, 2024)
- Phi-3 (Microsoft, 2024)
- TinyLlama (Zhang et al., 2023)
- Gemma (Google, 2024)
- MobileBERT (Sun et al., 2020)
- DistilBERT (Sanh et al., 2019)
- TinyBERT (Jiao et al., 2020)
- [Find 5-6 more recent papers]

#### Benchmarks (5-10 citations)
- SLM-Bench (Pham et al., 2025)
- MMLU (Hendrycks et al., 2021)
- HellaSwag (Zellers et al., 2019)
- GSM8K (Cobbe et al., 2021)
- HumanEval (Chen et al., 2021)
- GLUE (Wang et al., 2018)
- SuperGLUE (Wang et al., 2019)

#### Fine-Tuning & Compression (5-10 citations)
- Knowledge Distillation (Hinton et al., 2015)
- LoRA (Hu et al., 2021)
- QLoRA (Dettmers et al., 2023)
- Quantization (Jacob et al., 2018)
- Pruning (Han et al., 2015)

#### Edge AI & Deployment (5-10 citations)
- TensorFlow Lite (Google, 2017)
- ONNX Runtime (Microsoft, 2018)
- WebLLM (MLC, 2023)
- Transformers.js (Hugging Face, 2023)
- Edge TPU (Google, 2019)

#### Transformers & Architecture (5-10 citations)
- Attention Is All You Need (Vaswani et al., 2017)
- BERT (Devlin et al., 2018)
- GPT-2 (Radford et al., 2019)
- GPT-3 (Brown et al., 2020)
- LLaMA (Touvron et al., 2023)

### 3. **BibTeX Entries**

**Format**: Create BibTeX entries for all citations

**Example**:
```bibtex
@article{hu2021lora,
  title={LoRA: Low-Rank Adaptation of Large Language Models},
  author={Hu, Edward J and Shen, Yelong and Wallis, Phillip and Allen-Zhu, Zeyuan and Li, Yuanzhi and Wang, Shean and Wang, Lu and Chen, Weizhu},
  journal={arXiv preprint arXiv:2106.09685},
  year={2021}
}
```

---

## 📝 **Writing Guidelines**

### Tone
- **Academic**: Formal, precise, evidence-based
- **Honest**: Acknowledge limitations, fair comparisons
- **Clear**: Accessible to ML practitioners, not just theorists

### What to Emphasize
- **Recency**: Focus on 2024-2025 papers (most relevant)
- **Relevance**: Connect to our work (edge AI, structured output, small models)
- **Gaps**: Highlight what's missing (benchmarks for edge JSON extraction)

### What to Avoid
- **Overclaiming**: Don't say "no one has done X" (be specific)
- **Unfair comparisons**: Acknowledge zero-shot vs fine-tuned difference
- **Jargon**: Explain technical terms (LoRA, quantization, etc.)

---

## 🎯 **Key Messages to Convey**

### 1. SLMs Are Getting Better
"Recent advances in small language models (SmolLM2, Qwen2.5, Llama 3.2) have demonstrated that models with 135M-3B parameters can achieve competitive performance on academic benchmarks while enabling edge deployment."

### 2. But Benchmarks Are Limited
"However, existing benchmarks (MMLU, HellaSwag) focus on academic tasks (multiple-choice QA, commonsense reasoning) rather than practical structured output tasks (JSON extraction, function calling) required for edge AI applications."

### 3. Fine-Tuning Matters
"While zero-shot and instruction-tuned models offer flexibility, task-specific fine-tuning has been shown to provide significant performance gains for specialized tasks, particularly with limited compute budgets."

### 4. Edge AI Is Growing
"The rise of edge AI frameworks (TensorFlow Lite, ONNX Runtime, WebLLM) and hardware (Raspberry Pi, mobile devices, browsers with WebGPU) has created demand for models that can run on-device with low latency and memory footprint."

### 5. Our Contribution Fills a Gap
"We address this gap by introducing EdgeJSON, a benchmark for structured JSON extraction on edge devices, and Maaza, a series of task-specialized micro models that outperform larger zero-shot models while being deployable on resource-constrained devices."

---

## 📚 **Specific Questions to Research**

### 1. What's the smallest effective LM?
- Find papers on ultra-small models (<500M params)
- What tasks can they handle?
- What are the limitations?

### 2. Has anyone compared fine-tuned small vs zero-shot large?
- Look for papers comparing fine-tuning vs scaling
- Especially for structured tasks
- What did they find?

### 3. What benchmarks exist for structured output?
- JSON extraction, function calling, schema compliance
- Are there any? (hint: probably not many)
- What's the closest?

### 4. What's the state of edge AI deployment?
- Recent papers on on-device LMs
- Browser-based LMs (WebLLM, Transformers.js)
- Raspberry Pi, mobile deployment

### 5. What are the latest SLM models (2024-2025)?
- SmolLM2, Qwen2.5, Llama 3.2, Phi-3, Gemma
- What are their specs? (params, training data, performance)
- How do they compare?

---

## 🔗 **Useful Resources**

### Paper Databases
- arXiv.org (search: "small language models", "edge AI", "LoRA")
- Papers with Code (leaderboards, benchmarks)
- Hugging Face Papers (recent model releases)
- Google Scholar (citation tracking)

### Keywords to Search
- "small language models"
- "micro language models"
- "edge AI deployment"
- "LoRA fine-tuning"
- "structured output generation"
- "JSON extraction"
- "on-device language models"
- "resource-constrained NLP"

### Recent Conferences/Workshops
- NeurIPS 2024 (Efficient ML workshop)
- ICLR 2025 (Tiny Papers track)
- MLSys 2024 (Systems for ML)
- TinyML Summit 2024

---

## 📊 **What We Already Have**

### Data
- ✅ EdgeJSON v3 benchmark (787 examples, 24 schemas)
- ✅ Maaza MLM-135M (24.7% JSONExact)
- ✅ Maaza SLM-360M (55.1% JSONExact)
- ✅ Qwen2.5-0.5B baseline (14.6% JSONExact, verified)
- ✅ All results reproducible (2 independent runs)

### Code
- ✅ Evaluation harness (eval.py)
- ✅ Training scripts (train_mlm_135m_json.py)
- ✅ Batch evaluation (batch_eval_qwen.sh)
- ✅ All open-source (Apache 2.0)

### Models
- ✅ HuggingFace Hub (CycleCoreTechnologies org)
- ✅ Model cards (documented, polished)
- ✅ Ready to cite

### Documentation
- ✅ Paper outline (PAPER_A_OUTLINE.md)
- ✅ Paper plan (PAPER_PLAN_V2_WITH_QWEN.md)
- ✅ Baseline results (BASELINE_QWEN_VERIFIED.md)

**What We Need**: Related Work section + references!

---

## 🎯 **Deliverables**

### 1. **Related Work Draft** (2-3 pages)
- 4 subsections (SLMs, Benchmarks, Edge AI, Fine-Tuning)
- Academic tone, clear structure
- Markdown or LaTeX format

### 2. **BibTeX File** (30-50 citations)
- All references in BibTeX format
- Organized by category
- Ready to import into LaTeX

### 3. **Summary Table** (optional but helpful)
- Recent SLM models (name, params, year, key contribution)
- Existing benchmarks (name, task, metrics)
- Edge AI frameworks (name, platform, features)

---

## 📅 **Timeline**

### Week 2 (Nov 25-Dec 1)
- **Your task**: Research + draft Related Work
- **Our task**: Draft Introduction, create figures
- **Goal**: Have Related Work section ready by Dec 1

### Week 3 (Dec 2-8)
- **Your task**: Finalize references, create BibTeX
- **Our task**: Draft Methods sections
- **Goal**: Have complete Related Work + references by Dec 8

---

## 🤝 **How to Collaborate**

### Communication
- Share drafts via markdown files
- Highlight areas needing clarification
- Ask questions if anything is unclear

### Iteration
- We'll review your draft
- Provide feedback
- You refine based on feedback

### Final Integration
- We'll integrate Related Work into full paper
- Ensure consistent tone and flow
- Credit you in acknowledgments (if desired)

---

## ✅ **Success Criteria**

### Quality
- ✅ Comprehensive coverage (SLMs, benchmarks, edge AI, fine-tuning)
- ✅ Recent papers (focus on 2024-2025)
- ✅ Clear connections to our work
- ✅ 30-50 high-quality citations

### Clarity
- ✅ Academic tone (formal, precise)
- ✅ Logical flow (background → gap → our contribution)
- ✅ Accessible (explain technical terms)

### Usefulness
- ✅ Establishes context for our work
- ✅ Highlights gaps we're filling
- ✅ Positions our contribution appropriately

---

**Ready to start?** Let us know if you have questions!

**Contact**: Share drafts via markdown files, we'll review and provide feedback.

**Timeline**: Aim for Related Work draft by Dec 1, 2025.

**Thank you for collaborating!** 🚀



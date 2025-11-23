# Academic Paper Plan - CycleCore SLMBench Research

**Date**: 2025-11-21
**Status**: Planning Phase
**Target**: arXiv preprint → Conference/Workshop submission

---

## 📋 Paper Overview

### Working Title
**"Maaza: Micro Language Models for Edge JSON Extraction"**

Alternative titles:
- "EdgeJSON Benchmark and Maaza MLMs: Practical Structured Output for Resource-Constrained Devices"
- "Micro Language Models (MLMs): Specialized Small Models for Edge AI Tasks"

### Core Story
We demonstrate that **task-specialized micro models (135M-360M params)** can achieve competitive performance on structured tasks (JSON extraction) while being deployable on edge devices (Raspberry Pi, browser, CPU-only laptops).

---

## 🎯 Key Contributions

### 1. **EdgeJSON v3 Benchmark** ✅ COMPLETE
- **Dataset**: 787 examples (629 train, 158 test)
- **Quality**: 100% validated, production-ready
- **Schemas**: 25 real-world schemas (3 complexity levels)
- **Metrics**: JSONExact, FieldF1, SchemaCompliance
- **Open Source**: Apache 2.0 license

### 2. **Maaza MLM Models** ✅ COMPLETE
- **MLM-135M-JSON**: 24.7% JSONExact (SmolLM2-135M base)
- **SLM-360M-JSON**: 55.1% JSONExact (SmolLM2-360M base)
- **Training**: LoRA fine-tuning, 629 examples
- **Deployment**: HuggingFace Hub (CycleCoreTechnologies org)

### 3. **Evaluation Framework** ✅ COMPLETE
- **Harness**: `eval.py` with comprehensive metrics
- **Reproducible**: Open source, documented methodology
- **Cross-platform**: Pi 5, laptop CPU, browser (future)

### 4. **Empirical Analysis** 🔄 IN PROGRESS
- **Baseline**: SmolLM2-135M (0% JSONExact on complex schemas)
- **Improvement**: Fine-tuning yields 24.7% → 55.1% (135M → 360M)
- **Efficiency**: 135M model runs on Pi 5, browser, CPU-only

---

## 📊 Current Results (From V3 Validation Report)

### Model Performance

| Model | Size | JSONExact | FieldF1 | Deployment |
|-------|------|-----------|---------|------------|
| **Maaza-MLM-135M** | 135M | 24.7% | ~0.65 | Pi 5, Browser, CPU |
| **Maaza-SLM-360M** | 360M | 55.1% | ~0.78 | Laptop CPU, Browser |
| SmolLM2-135M (base) | 135M | ~0% | ~0.20 | (unfine-tuned) |

### By Schema Complexity

| Complexity | Fields | Nesting | MLM-135M | SLM-360M |
|------------|--------|---------|----------|----------|
| Simple | 3-5 | Flat | ~45% | ~75% |
| Medium | 8-12 | 1-2 levels | ~20% | ~50% |
| Complex | 15+ | 3+ levels | ~5% | ~35% |

*(Note: Exact breakdown needs to be computed from eval results)*

---

## 📝 Paper Structure

### 1. **Abstract** (150-200 words)
- **Problem**: Edge AI needs structured output (JSON), existing SLMs too large or underperform
- **Gap**: No benchmark for edge JSON extraction, no specialized micro models
- **Contribution**: EdgeJSON v3 benchmark (787 examples, 25 schemas) + Maaza MLMs (135M-360M)
- **Results**: 55.1% JSONExact (360M model), deployable on Pi 5/browser
- **Impact**: Practical benchmark + models for edge AI deployment

### 2. **Introduction** (2 pages)
- **Motivation**: IoT, edge devices need structured data extraction (sensors, APIs, forms)
- **Challenge**: LLMs too large (cloud-only), SLMs (1B-3B) still too big for edge
- **Our Approach**: Task-specialized micro models (135M-360M) via fine-tuning
- **Contributions**: Benchmark + models + evaluation harness

### 3. **Related Work** (2 pages)
- **SLM Evolution**: SmolLM2, Qwen2.5, Llama 3.2, Phi-3
- **Benchmarks**: MMLU, HellaSwag, SLM-Bench (Pham et al., 2025)
- **Gap**: No structured output benchmarks for edge (JSON, function calling)
- **Edge AI**: TensorFlow Lite, ONNX Runtime, WebLLM, Transformers.js

### 4. **EdgeJSON Benchmark** (3 pages)
- **Task Definition**: Extract structured JSON from natural language prompts
- **Dataset**: 787 examples, 25 schemas, 3 complexity levels
- **Validation**: 100% mathematical consistency (v3 quality assurance)
- **Metrics**: JSONExact, FieldF1, SchemaCompliance, Latency
- **Methodology**: Synthetic generation via Qwen2.5-7B, human-validated schemas

### 5. **Maaza MLM Models** (2 pages)
- **Architecture**: LoRA fine-tuning on SmolLM2 base models
- **Training**: 629 examples, 48 checkpoints, 36-48 hours (RTX 4080)
- **Hyperparameters**: r=16, alpha=32, dropout=0.1, learning_rate=3e-4
- **Deployment**: HuggingFace Hub, ONNX export, browser-compatible

### 6. **Experiments** (3 pages)
- **Setup**: Hardware (Pi 5, laptop CPU), software (Transformers, ONNX Runtime)
- **Baselines**: SmolLM2-135M/360M (unfine-tuned), Qwen2.5-0.5B, Llama 3.2-1B
- **Results**: 24.7% (135M) → 55.1% (360M) JSONExact
- **Analysis**: By complexity, by schema, error analysis
- **Ablations**: Model size, training data size, LoRA rank

### 7. **Discussion** (2 pages)
- **When MLMs Excel**: Structured tasks, well-defined schemas, sufficient training data
- **Limitations**: Complex schemas (15+ fields), nested structures, creative tasks
- **Deployment**: Pi 5 feasibility, browser deployment, latency analysis
- **Future Work**: Multi-task training, quantization, energy measurement

### 8. **Conclusion** (1 page)
- **Summary**: EdgeJSON benchmark + Maaza MLMs enable edge JSON extraction
- **Impact**: Practical benchmark for edge AI, open-source models/harness
- **Call to Action**: Use SLMBench, contribute datasets, deploy Maaza models

### **Appendix**
- A. Full schema list (25 schemas)
- B. Prompt templates
- C. Hyperparameter details
- D. Error analysis (common failure modes)

---

## 🔬 Experiments Needed

### ✅ COMPLETE
1. EdgeJSON v3 dataset validation (100% pass rate)
2. Maaza MLM-135M training (24.7% JSONExact)
3. Maaza SLM-360M training (55.1% JSONExact)
4. Evaluation harness (`eval.py`)

### 🔄 IN PROGRESS
5. Detailed breakdown by schema complexity
6. Error analysis (common failure modes)
7. Ablation: Model size (135M vs 360M)

### ⏳ TODO
8. Baseline comparison: Qwen2.5-0.5B, Llama 3.2-1B (unfine-tuned)
9. Cross-platform evaluation: Pi 5, laptop CPU, browser
10. Latency measurement: Tokens/sec on each platform
11. Ablation: Training data size (100, 300, 629 examples)
12. Ablation: LoRA rank (r=8, 16, 32)
13. Energy measurement (future: Joulescope)

---

## 📐 Figures and Tables

### Figures Needed (8-10)
1. **Figure 1**: EdgeJSON task overview (input → model → JSON output)
2. **Figure 2**: Schema complexity distribution (simple/medium/complex)
3. **Figure 3**: Model architecture (SmolLM2 + LoRA adapter)
4. **Figure 4**: Training curves (loss, JSONExact over checkpoints)
5. **Figure 5**: Results by complexity (bar chart: 135M vs 360M)
6. **Figure 6**: Pareto curve (JSONExact vs model size)
7. **Figure 7**: Latency comparison (Pi 5, laptop, browser)
8. **Figure 8**: Error analysis (failure modes: missing fields, wrong types, etc.)

### Tables Needed (6-8)
1. **Table 1**: EdgeJSON dataset statistics (train/test, schemas, complexity)
2. **Table 2**: Maaza MLM hyperparameters (LoRA config, training args)
3. **Table 3**: Main results (JSONExact, FieldF1 by model)
4. **Table 4**: Results by complexity (simple/medium/complex)
5. **Table 5**: Cross-platform latency (Pi 5, laptop, browser)
6. **Table 6**: Ablation: Model size (135M, 360M, 1.7B)
7. **Table 7**: Ablation: Training data size (100, 300, 629)
8. **Table 8**: Error analysis (failure modes, frequency)

---

## 📅 Timeline

### Week 1 (Current): Planning ✅
- ✅ Review existing documentation (PAPER_A_OUTLINE.md, V3_VALIDATION_REPORT.md)
- ✅ Define paper scope (focus on EdgeJSON + Maaza MLMs)
- ✅ Create PAPER_PLAN.md

### Week 2: Data Analysis & Experiments
- 🔄 Compute detailed breakdown by schema complexity
- 🔄 Run baseline comparisons (Qwen2.5-0.5B, Llama 3.2-1B)
- 🔄 Cross-platform evaluation (Pi 5, laptop CPU)
- 🔄 Error analysis (common failure modes)

### Week 3: Writing - Introduction & Related Work
- 📝 Draft Introduction (2 pages)
- 📝 Draft Related Work (2 pages)
- 📝 Create Figure 1 (task overview)

### Week 4: Writing - Benchmark & Models
- 📝 Draft EdgeJSON Benchmark section (3 pages)
- 📝 Draft Maaza MLM Models section (2 pages)
- 📝 Create Figure 2 (schema distribution), Figure 3 (architecture)

### Week 5: Writing - Experiments & Results
- 📝 Draft Experiments section (3 pages)
- 📝 Create all result tables (Tables 3-8)
- 📝 Create result figures (Figures 4-8)

### Week 6: Writing - Discussion & Conclusion
- 📝 Draft Discussion (2 pages)
- 📝 Draft Conclusion (1 page)
- 📝 Draft Abstract (150-200 words)
- 📝 Compile Appendix

### Week 7: Revision & Polishing
- 🔍 Full paper review (internal)
- 🔍 Proofread, fix typos, improve clarity
- 🔍 Finalize figures/tables
- 🔍 Check references (30-50 citations)

### Week 8: Submission
- 🚀 arXiv preprint submission
- 🚀 Share on X (@CycleCoreTech), LinkedIn
- 🚀 Submit to workshop (TinyML, MLSys, ICLR/NeurIPS workshop)

---

## 🎯 Target Venues

### Primary: arXiv Preprint
- **Timeline**: Week 8 (early December 2025)
- **Format**: 10-12 pages (arXiv format)
- **Goal**: Establish priority, get community feedback

### Secondary: Workshop Submission
**Option 1: TinyML Workshop** (co-located with MLSys 2026)
- **Deadline**: ~March 2026
- **Fit**: Edge AI, resource-constrained devices
- **Audience**: Embedded ML practitioners

**Option 2: ICLR 2026 Workshop** (Efficient ML)
- **Deadline**: ~February 2026
- **Fit**: Small models, efficiency, benchmarks
- **Audience**: Academic ML researchers

**Option 3: NeurIPS 2026 Workshop** (Datasets & Benchmarks)
- **Deadline**: ~August 2026
- **Fit**: New benchmark (EdgeJSON), evaluation methodology
- **Audience**: ML research community

### Tertiary: Conference (Long-Term)
**Option 4: MLSys 2027** (full paper)
- **Deadline**: ~October 2026
- **Fit**: Systems for ML, edge deployment, benchmarking
- **Audience**: ML systems researchers

---

## 📚 References to Include (30-50 citations)

### SLM Papers (10-15)
1. SmolLM2 (Hugging Face, 2024)
2. Qwen2.5 Technical Report (Alibaba, 2024)
3. Llama 3.2 (Meta, 2024)
4. Phi-3 (Microsoft, 2024)
5. TinyLlama (Zhang et al., 2023)
6. SmolLM3 (Hugging Face, 2025)
7. Gemma (Google, 2024)
8. MobileBERT (Sun et al., 2020)
9. DistilBERT (Sanh et al., 2019)
10. TinyBERT (Jiao et al., 2020)

### Benchmarks (5-10)
11. SLM-Bench (Pham et al., 2025)
12. MMLU (Hendrycks et al., 2021)
13. HellaSwag (Zellers et al., 2019)
14. GSM8K (Cobbe et al., 2021)
15. HumanEval (Chen et al., 2021)
16. GLUE (Wang et al., 2018)
17. SuperGLUE (Wang et al., 2019)

### Distillation & Compression (5-10)
18. Knowledge Distillation (Hinton et al., 2015)
19. LoRA (Hu et al., 2021)
20. QLoRA (Dettmers et al., 2023)
21. Quantization (Jacob et al., 2018)
22. Pruning (Han et al., 2015)

### Edge AI & Deployment (5-10)
23. TensorFlow Lite (Google, 2017)
24. ONNX Runtime (Microsoft, 2018)
25. WebLLM (MLC, 2023)
26. Transformers.js (Hugging Face, 2023)
27. Edge TPU (Google, 2019)
28. NVIDIA Jetson (NVIDIA, 2014)

### Transformers & Architecture (5-10)
29. Attention Is All You Need (Vaswani et al., 2017)
30. BERT (Devlin et al., 2018)
31. GPT-2 (Radford et al., 2019)
32. GPT-3 (Brown et al., 2020)
33. LLaMA (Touvron et al., 2023)

---

## 🔧 Tools & Infrastructure

### Writing
- **Format**: LaTeX (arXiv template)
- **Collaboration**: Overleaf or local LaTeX
- **Version Control**: Git (separate branch: `paper-a-mlm-edgebench`)

### Figures
- **Plots**: Python (matplotlib, seaborn)
- **Diagrams**: draw.io or TikZ (LaTeX)
- **Style**: IEEE/ACM conference style (clean, professional)

### Experiments
- **Harness**: `benchmarks/edge_json/scripts/eval.py`
- **Logging**: JSON output, CSV for tables
- **Reproducibility**: Document all hyperparameters, seeds, hardware

---

## 🚀 Next Steps (Immediate)

### 1. **Compute Detailed Breakdown** (Week 2)
Run `eval.py` on Maaza models and compute:
- JSONExact by schema complexity (simple/medium/complex)
- FieldF1 by schema
- Error analysis (missing fields, wrong types, malformed JSON)

### 2. **Baseline Comparisons** (Week 2)
Evaluate unfine-tuned models on EdgeJSON v3:
- SmolLM2-135M (base)
- SmolLM2-360M (base)
- Qwen2.5-0.5B (zero-shot)
- Llama 3.2-1B (zero-shot)

### 3. **Cross-Platform Evaluation** (Week 2)
Measure latency on:
- Raspberry Pi 5 (ARM CPU)
- Laptop (x86 CPU)
- Browser (WebGPU, Transformers.js)

### 4. **Start Writing** (Week 3)
- Draft Introduction (motivation, contributions)
- Draft Related Work (SLMs, benchmarks, edge AI)

---

## 📋 Open Questions

### 1. **Authorship**
- **Lead Author**: CycleCore Technologies Research Team (or specific names?)
- **Affiliation**: CycleCore Technologies (independent research lab)
- **Contact**: hi@cyclecore.ai

### 2. **Code Release**
- **GitHub**: Public repo (github.com/CycleCore/SLMBench)
- **Models**: HuggingFace Hub (CycleCoreTechnologies org) ✅ DONE
- **License**: Apache 2.0 ✅ DONE

### 3. **Dataset Release**
- **EdgeJSON v3**: Public (Apache 2.0) ✅ DONE
- **HuggingFace Datasets**: Upload to datasets hub?
- **Leaderboard**: slmbench.com (future)

### 4. **Broader Impact Statement**
- **Privacy**: On-device processing (no cloud API calls)
- **Bias**: Synthetic data inherits teacher model biases
- **Environmental**: Training emissions vs deployment savings
- **Accessibility**: Open-source, free to use

---

## 🎯 Success Metrics

### Paper Acceptance
- ✅ arXiv preprint published
- 🎯 Workshop acceptance (TinyML, ICLR, NeurIPS)
- 🎯 Conference acceptance (MLSys 2027, long-term)

### Community Impact
- 🎯 10+ citations within 6 months
- 🎯 100+ HuggingFace model downloads
- 🎯 5+ external evaluations on EdgeJSON benchmark
- 🎯 Integration into SLM-Bench leaderboard (Pham et al.)

### Commercial Impact
- 🎯 slmbench.com evaluation service launch
- 🎯 3+ enterprise customers (evaluation service)
- 🎯 Maaza models deployed in production (edge devices)

---

**Status**: PLAN COMPLETE - Ready to start experiments & writing
**Next Action**: Compute detailed breakdown by schema complexity (Week 2)
**Timeline**: arXiv submission by Week 8 (early December 2025)


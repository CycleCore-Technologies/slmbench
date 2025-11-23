# MLM Terminology & SLMBench Naming - Official Position

**Date**: November 21, 2025  
**Status**: Final Decision - Documented for Paper

---

## 🎯 **Official Position: Keep MLM Terminology**

### Rationale

**1. BERT-style MLM is Legacy Technology**
- ✅ BERT (2018) uses "Masked Language Model" (MLM)
- ✅ But encoder-only models are NO LONGER actively developed
- ✅ Industry moved to decoder-only (GPT-style) in 2020+
- ✅ Current SLMs (SmolLM2, Qwen2.5, Llama 3.2) are ALL decoder-only
- ✅ Our "MLM = Micro Language Model" is MORE RELEVANT for 2025+

**2. Our MLM Category is Important**
- ✅ Fills gap between encoder models (<500M, BERT-era) and SLMs (1B+)
- ✅ Defines ultra-small decoder-only models (10M-250M params)
- ✅ Practical for edge deployment (Raspberry Pi, browser, mobile)
- ✅ Task-specialized models at this scale are underexplored

**3. Acronym Reuse is Common in ML**
- ✅ "LM" = Language Model, Likelihood Model, Linear Model
- ✅ "RNN" = Recurrent Neural Network, Recursive Neural Network
- ✅ "GAN" = Generative Adversarial Network, Gated Attention Network
- ✅ Context disambiguates (we never discuss masked LMs)

---

## 📝 **Paper Positioning**

### In Abstract
> "We present Maaza, a series of **Micro Language Models (MLMs)** with 135M-360M parameters, fine-tuned for JSON extraction..."

### In Introduction (Footnote)
> "We use the term 'Micro Language Model' (MLM) to denote decoder-only models with 10M-250M parameters, distinct from the legacy 'Masked Language Model' term used in BERT-era encoder models [Devlin et al., 2019]. The decoder-only paradigm has since become dominant for generative tasks."

### In Related Work (When discussing BERT)
> "Early compact transformers focused on encoder-only architectures such as BERT [Devlin et al., 2019], which uses masked language modeling (MLM) for pretraining. However, the shift toward decoder-only models (GPT, LLaMA, etc.) has made encoder-only models largely obsolete for generative tasks. We adopt the term **MLM (Micro Language Model)** to describe ultra-small decoder-only models in this new paradigm."

---

## 🌐 **Website: SLMBench.com**

### Official Name
**SLMBench** (no rebranding needed)

### Tagline Options
1. "SLMBench: EdgeJSON Evaluation for Small Language Models"
2. "SLMBench: Structured Output Benchmarking for Edge AI"
3. "SLMBench: JSON Extraction Benchmark for Resource-Constrained Devices"

### Homepage Positioning
```
SLMBench provides specialized evaluation for small language models 
on structured output tasks (JSON extraction, schema compliance).

We focus on edge AI deployment scenarios, complementing general-purpose 
benchmarks like SLM-Bench [Pham et al., 2025] with task-specific 
evaluation for structured data extraction.
```

### Citation to Pham et al.
```
Our EdgeJSON benchmark complements SLM-Bench (Pham et al., 2025), 
which evaluates SLMs on general NLP tasks (MMLU, GSM8K, HellaSwag). 
While SLM-Bench measures broad language understanding and reasoning, 
SLMBench focuses specifically on structured output reliability—a 
critical requirement for edge AI applications.
```

---

## 🏷️ **Model Naming (HuggingFace)**

### Keep Current Names
- ✅ `Maaza-MLM-135M-JSON-v1` (already published)
- ✅ `Maaza-SLM-360M-JSON-v1` (already published)

### In Paper, Refer As
- "Maaza-MLM-135M" (Micro Language Model, 135M params)
- "Maaza-SLM-360M" (Small Language Model, 360M params)

### Consistent Usage
- **MLM**: 10M-250M parameters (micro-scale)
- **SLM**: 250M-3B parameters (small-scale)
- **LLM**: 3B+ parameters (large-scale)

---

## 📊 **Comparison: Our MLM vs BERT MLM**

| Aspect | BERT MLM (2018) | Our MLM (2025) |
|--------|-----------------|----------------|
| **Full Name** | Masked Language Model | Micro Language Model |
| **Architecture** | Encoder-only | Decoder-only |
| **Pretraining** | Masked token prediction | Causal language modeling |
| **Use Case** | Classification, NLU | Generation, structured output |
| **Status** | Legacy (not actively developed) | Current (edge AI focus) |
| **Relevance** | Historical | Practical for edge deployment |

**Key Point**: BERT-style MLM is encoder-only (2018 era), no longer state-of-the-art. Our MLM is decoder-only (2025), designed for edge AI.

---

## 🎯 **Strategic Positioning**

### Why This Matters
1. **Category Definition**: We're defining a new, useful category (Micro LMs)
2. **Edge AI Focus**: 10M-250M params is the sweet spot for edge devices
3. **Practical Impact**: These models can run on Raspberry Pi, browser, mobile
4. **Research Gap**: Underexplored in literature (most work on 1B+ models)

### How to Defend in Reviews
**If Reviewer Says**: "MLM already means Masked Language Model"

**We Respond**:
> "We acknowledge that 'MLM' historically referred to 'Masked Language Model' in encoder-only architectures (BERT, 2019). However, encoder-only models are no longer actively developed, having been superseded by decoder-only architectures for generative tasks. We repurpose this acronym to denote 'Micro Language Model'—a category of ultra-small decoder-only models (10M-250M parameters) optimized for edge deployment. We believe this is a more relevant use of the acronym for 2025 and beyond, and clarify this distinction in our paper (see Introduction, footnote 1)."

---

## ✅ **Final Decision**

### Paper
- ✅ Use "MLM (Micro Language Model)" terminology
- ✅ Define clearly once (Introduction + footnote)
- ✅ Acknowledge BERT-era usage briefly
- ✅ Focus on importance of ultra-small decoder-only models

### Website
- ✅ Keep "SLMBench.com"
- ✅ Add tagline: "EdgeJSON Evaluation for Small Language Models"
- ✅ Cite Pham et al. SLM-Bench
- ✅ Position as complementary (structured output focus)

### Models
- ✅ Keep HuggingFace names: `Maaza-MLM-135M`, `Maaza-SLM-360M`
- ✅ Consistent usage in paper
- ✅ Clear category hierarchy: MLM < SLM < LLM

---

## 📚 **References to Add**

### BERT (for context)
```bibtex
@article{devlin2019bert,
  title={BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding},
  author={Devlin, Jacob and Chang, Ming-Wei and Lee, Kenton and Toutanova, Kristina},
  journal={NAACL-HLT},
  year={2019},
  note={Introduced Masked Language Model (MLM) pretraining for encoder-only architectures}
}
```

### SLM-Bench (for proper citation)
```bibtex
@article{pham2025slmbench,
  title={SLM-Bench: A Comprehensive Benchmark of Small Language Models on Environmental and Efficiency Impacts},
  author={Pham, Nguyen Thai and others},
  journal={Findings of EMNLP},
  year={2025},
  note={General-purpose benchmark for SLMs on academic tasks}
}
```

---

## 🚀 **Confidence Level**

**HIGH** - This positioning is:
- ✅ Academically sound (legacy tech vs new category)
- ✅ Practically important (edge AI gap)
- ✅ Defensible in reviews (clear distinction, footnote)
- ✅ Consistent with our branding (HuggingFace models)

**Proceed with MLM terminology and SLMBench.com!**

---

**Document Version**: 1.0 (Final)  
**Last Updated**: November 21, 2025  
**Status**: ✅ APPROVED - Use in paper and website


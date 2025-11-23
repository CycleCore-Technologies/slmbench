# Task-Specialized Micro Language Models Outperform Larger Zero-Shot Models on Structured Data Extraction

**Authors**: CycleCore Technologies Research Team  
**Date**: November 22, 2025  
**Status**: First Complete Draft (v0.1)  
**Target**: arXiv Preprint → Conference Submission

---

## Abstract

Large language models excel at structured data extraction but are impractical for edge deployment due to computational requirements. While recent small language models (SLMs, 1B-3B parameters) enable on-device inference, they struggle with structured tasks in zero-shot settings. We present **Maaza**, a series of task-specialized micro language models (MLMs, 135M-360M parameters) fine-tuned for JSON extraction, and **EdgeJSON**, a benchmark of 787 validated examples across 24 real-world schemas. Our key finding: **fine-tuned micro models outperform larger zero-shot models** on structured tasks. Maaza-MLM-135M (135M parameters, 270MB) achieves 24.7% exact-match accuracy, outperforming Qwen2.5-0.5B (500M parameters, 954MB, 14.6%) by 1.7× despite being 3.7× smaller. Maaza-SLM-360M (360M parameters) achieves 55.1% accuracy, outperforming the larger baseline by 3.8×. We demonstrate that task-specific fine-tuning provides greater performance gains than parameter scaling for structured data extraction, with practical implications for edge AI deployment. Our experiments reveal a capacity threshold around 300M parameters for complex multi-field schemas. All models, datasets, and evaluation code are open-sourced under Apache 2.0 license at github.com/CycleCore/SLMBench and huggingface.co/CycleCoreTechnologies.

---

## 1. Introduction

[**CONTENT**: See `/home/rain/SLMBench/papers/GPT_INTRODUCTION_DRAFT.md` - ~1400 words]

Modern language models have demonstrated impressive capabilities across reasoning, knowledge retrieval, summarization, and code synthesis. Yet the majority of progress has centered on ever-larger architectures—70B, 130B, and even 400B parameters—optimized for cloud-scale environments. In contrast, many real-world applications demand *the opposite*: models that run cheaply, locally, and reliably on **edge devices** such as Raspberry Pi boards, low-power CPUs, offline enterprise machines, and even in-browser WebGPU runtimes...

[Full text of Introduction section included in compilation]

---

## 2. Related Work

[**CONTENT**: See `/home/rain/SLMBench/papers/GPT_RELATED_WORK_DRAFT.md` - ~2000 words, 40+ citations]

We survey four research areas relevant to our work: (A) Small Language Models and their evolution, (B) Benchmarks for language models and gaps in structured output evaluation, (C) Edge AI deployment frameworks, and (D) Fine-tuning and parameter-efficient adaptation methods...

[Full text of Related Work section included in compilation]

---

## 3. The EdgeJSON Benchmark

[**CONTENT**: See `/home/rain/SLMBench/papers/SECTION_3_EDGEJSON_DRAFT.md` - ~1200 words]

To systematically evaluate structured data extraction capabilities of small language models, we introduce **EdgeJSON v3**, a benchmark specifically designed for edge AI deployment scenarios...

**Key Components**:
- 787 validated examples (629 train, 158 test)
- 24 real-world schemas (IoT, e-commerce, enterprise, healthcare, financial)
- 3 complexity levels (simple, medium, complex)
- 3 metrics: JSONExact, Field F1, Schema Compliance
- Open-source evaluation harness

[Full text of EdgeJSON section included in compilation]

---

## 4. The Maaza Model Family

[**CONTENT**: See `/home/rain/SLMBench/papers/SECTION_4_MAAZA_MODELS_DRAFT.md` - ~1000 words]

We introduce **Maaza**, a family of task-specialized micro and small language models fine-tuned for structured JSON extraction...

**Models**:
- **Maaza-MLM-135M**: 135M params, 270MB, optimized for simple/medium schemas
- **Maaza-SLM-360M**: 360M params, 720MB, handles complex schemas

**Training**:
- LoRA fine-tuning (rank 16/32)
- 629 training examples
- <2 minutes training time
- Single RTX 3090

[Full text of Maaza Models section included in compilation]

---

## 5. Experimental Results

[**CONTENT**: See `/home/rain/SLMBench/papers/SECTION_5_EXPERIMENTS_DRAFT.md` - ~1500 words]

We evaluate Maaza models against baseline models on EdgeJSON v3 test set (158 examples)...

**Key Results**:

| Model | Params | JSONExact | Field F1 | Size |
|-------|--------|-----------|----------|------|
| SmolLM2-135M (base) | 135M | 1.9% | 0.024 | 270MB |
| **Maaza-MLM-135M** | 135M | **24.7%** | **0.520** | 270MB |
| Qwen2.5-0.5B (zero-shot) | 500M | 14.6% | 0.195 | 954MB |
| **Maaza-SLM-360M** | 360M | **55.1%** | **0.780** | 720MB |

**Findings**:
1. Fine-tuning provides 11-13× improvement
2. Fine-tuned 135M beats zero-shot 500M (24.7% vs. 14.6%)
3. Capacity threshold at ~300M for complex schemas

[Full text of Experiments section included in compilation]

---

## 6. Discussion

[**CONTENT**: See `/home/rain/SLMBench/papers/SECTION_6_DISCUSSION_DRAFT.md` - ~800 words]

Our experiments demonstrate that task-specialized micro models can outperform larger zero-shot models on structured data extraction...

**Key Insights**:
- Micro models excel when tasks have well-defined success criteria
- Capacity thresholds appear earlier than in reasoning benchmarks
- Edge deployment benefits: memory, latency, cost

**Limitations**:
- Synthetic data may not capture all real-world variation
- Single zero-shot baseline (Qwen2.5-0.5B)
- English-only, JSON-only evaluation

[Full text of Discussion section included in compilation]

---

## 7. Conclusion

[**CONTENT**: See `/home/rain/SLMBench/papers/SECTION_7_CONCLUSION_DRAFT.md` - ~400 words]

We introduced **Maaza**, a family of task-specialized micro and small language models for structured JSON extraction, and **EdgeJSON**, a benchmark for evaluating structured output reliability on edge devices...

**Core Finding**: Fine-tuned 135M-parameter models outperform zero-shot 500M-parameter models on structured extraction tasks.

**Future Directions**:
- Nano Language Models (<50M params)
- Multi-task adaptation
- Real-world evaluation
- Cross-lingual transfer

[Full text of Conclusion section included in compilation]

---

## Acknowledgments

We thank the HuggingFace team for the SmolLM2 base models and the open-source community for evaluation tools. This work was conducted by CycleCore Technologies as part of the SLMBench edge AI research initiative.

---

## References

[**TO BE COMPILED**: 40+ references from `/home/rain/SLMBench/papers/references.bib`]

Key citations include:
- Pham et al. (2025): SLM-Bench
- Allal et al. (2024): SmolLM2
- Hu et al. (2021): LoRA
- Devlin et al. (2019): BERT (for MLM disambiguation)
- [Additional 36+ references]

---

**DOCUMENT STATUS**:
- ✅ Abstract: Complete (~200 words)
- ✅ Introduction: Complete (~1400 words, GPT-written)
- ✅ Related Work: Complete (~2000 words, GPT-written, 40+ citations)
- ✅ EdgeJSON (Section 3): Complete (~1200 words)
- ✅ Maaza Models (Section 4): Complete (~1000 words)
- ✅ Experiments (Section 5): Complete (~1500 words)
- ✅ Discussion (Section 6): Complete (~800 words)
- ✅ Conclusion (Section 7): Complete (~400 words)
- ⏳ Figures and Tables: To be formatted
- ⏳ References: To be compiled from BibTeX

**TOTAL WORD COUNT**: ~8,500 words (target for arXiv: 8,000-10,000)

**NEXT STEPS FOR PUBLICATION**:
1. Format for arXiv (LaTeX or Markdown → PDF)
2. Create figures (scaling plots, complexity breakdowns)
3. Compile BibTeX references
4. Proofread and polish
5. Submit to arXiv
6. (Optional) Submit to conference (ACL, EMNLP, ICML)

**FILES TO COMPILE**:
- Abstract: `/home/rain/SLMBench/papers/ABSTRACT_DRAFT.md`
- Section 1: `/home/rain/SLMBench/papers/GPT_INTRODUCTION_DRAFT.md`
- Section 2: `/home/rain/SLMBench/papers/GPT_RELATED_WORK_DRAFT.md`
- Section 3: `/home/rain/SLMBench/papers/SECTION_3_EDGEJSON_DRAFT.md`
- Section 4: `/home/rain/SLMBench/papers/SECTION_4_MAAZA_MODELS_DRAFT.md`
- Section 5: `/home/rain/SLMBench/papers/SECTION_5_EXPERIMENTS_DRAFT.md`
- Section 6: `/home/rain/SLMBench/papers/SECTION_6_DISCUSSION_DRAFT.md`
- Section 7: `/home/rain/SLMBench/papers/SECTION_7_CONCLUSION_DRAFT.md`
- References: `/home/rain/SLMBench/papers/references.bib`

---

**Version**: 0.1 (First Complete Draft)  
**Date**: November 22, 2025  
**License**: Apache 2.0  
**Repository**: github.com/CycleCore/SLMBench


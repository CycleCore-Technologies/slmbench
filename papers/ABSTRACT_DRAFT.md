# Abstract (Draft)

**Date**: November 22, 2025  
**Status**: Draft  
**Word count**: ~200 words

---

## **Abstract**

Large language models excel at structured data extraction but are impractical for edge deployment due to computational requirements. While recent small language models (SLMs, 1B-3B parameters) enable on-device inference, they struggle with structured tasks in zero-shot settings. We present **Maaza**, a series of task-specialized micro language models (MLMs, 135M-360M parameters) fine-tuned for JSON extraction, and **EdgeJSON**, a benchmark of 787 validated examples across 24 real-world schemas. Our key finding: **fine-tuned micro models outperform larger zero-shot models** on structured tasks. Maaza-MLM-135M (135M parameters, 270MB) achieves 24.7% exact-match accuracy, outperforming Qwen2.5-0.5B (500M parameters, 954MB, 14.6%) by 1.7× despite being 3.7× smaller. Maaza-SLM-360M (360M parameters) achieves 55.1% accuracy, outperforming the larger baseline by 3.8×. We demonstrate that task-specific fine-tuning provides greater performance gains than parameter scaling for structured data extraction, with practical implications for edge AI deployment. Our experiments reveal a capacity threshold around 300M parameters for complex multi-field schemas. All models, datasets, and evaluation code are open-sourced under Apache 2.0 license at github.com/CycleCore/SLMBench and huggingface.co/CycleCoreTechnologies.

---

**End of Abstract**


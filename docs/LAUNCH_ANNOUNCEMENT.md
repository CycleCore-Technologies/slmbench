# CycleCore Maaza Models v1.0.0 Launch Announcement

**Date**: November 20, 2025
**Organization**: CycleCore Technologies
**Models**: Maaza MLM-135M-JSON v1.0.0 & Maaza SLM-360M-JSON v1.0.0

---

## TL;DR

CycleCore Technologies announces the first production release of the Maaza model series: ultra-efficient language models specialized for JSON extraction on edge devices. These models prove that tiny, task-specialized models can achieve production-grade performance on structured tasks while running on resource-constrained hardware.

**Key Results**:
- **MLM-135M**: 24.7% JSONExact accuracy in 48.7 seconds of training
- **SLM-360M**: 55.1% JSONExact accuracy, 2.23× improvement over 135M
- **Capacity Breakthrough**: 360M breaks the 0% complex schema ceiling that 135M hits
- **Ultra-Fast Training**: 48-90 seconds on consumer GPU (RTX 4080 SUPER)
- **Open Source**: Apache 2.0 license, full reproducibility

---

## Introduction

Today, we're releasing two task-specialized language models designed for edge JSON extraction:

1. **Maaza MLM-135M-JSON v1.0.0**: Micro Language Model (135M parameters)
2. **Maaza SLM-360M-JSON v1.0.0**: Small Language Model (360M parameters)

Both models are fine-tuned from the SmolLM2 family (Hugging Face) and optimized for structured data extraction on edge devices.

### Why This Matters

**Edge AI is Hungry for Tiny, Specialized Models**

Current language models fall into two categories:
- **Large models** (GPT-4, Claude): Billions of parameters, cloud-only, expensive
- **Small models** (Llama 3.2, Qwen2.5): 1B-8B params, laptop/server, good but still large

**Missing**: Ultra-small models (10M-500M params) that can run on truly resource-constrained edge devices.

**Our Contribution**: We demonstrate that:
1. Models as small as 135M can learn structured tasks (24.7% accuracy)
2. Capacity scaling matters: 360M achieves 2.23× improvement (55.1% accuracy)
3. Training is ultra-fast: 48-90 seconds on consumer hardware
4. Complex schemas hit capacity ceilings: 135M achieves 0%, 360M breaks through at 4%

---

## Model Releases

### Maaza MLM-135M-JSON v1.0.0

**Micro Language Model for Edge Deployment**

| Specification | Value |
|---------------|-------|
| Parameters | 135M total, 4.88M trainable (LoRA) |
| Base Model | SmolLM2-135M (HuggingFaceTB) |
| JSONExact Accuracy | 24.7% (overall) |
| Simple Schemas | 44.7% accuracy |
| Medium Schemas | 13.5% accuracy |
| Complex Schemas | 0.0% (capacity ceiling) |
| Field F1 | 0.520 |
| Training Time | 48.7 seconds |
| Model Size | ~270MB (FP16), ~70MB (Q4) |
| License | Apache 2.0 |

**Perfect Schemas** (100% accuracy):
- `product_info` (2 fields, simple)
- `sensor_reading` (4 fields, simple)

**Use Cases**:
- IoT sensor data extraction
- Ultra-low-latency edge applications
- Raspberry Pi / embedded deployment
- Proof-of-concept for tiny model viability

**HuggingFace**: `CycleCore/Maaza-MLM-135M-JSON-v1`

---

### Maaza SLM-360M-JSON v1.0.0

**Small Language Model for Production Deployment**

| Specification | Value |
|---------------|-------|
| Parameters | 360M total (379M), 17.4M trainable (LoRA) |
| Base Model | SmolLM2-360M (HuggingFaceTB) |
| JSONExact Accuracy | 55.1% (overall) |
| Simple Schemas | 78.9% accuracy |
| Medium Schemas | 51.4% accuracy |
| Complex Schemas | 4.0% (breakthrough) |
| Field F1 | 0.729 |
| Training Time | 90.1 seconds |
| Model Size | ~720MB (FP16), ~180MB (Q4) |
| License | Apache 2.0 |

**Perfect Schemas** (100% accuracy):
- `log_entry` (4 fields, simple)
- `product_info` (2 fields, simple)
- `sensor_reading` (4 fields, simple)
- `transaction_record` (5 fields, simple)

**High-Accuracy Schemas** (80%+):
- `notification` (88.9%)
- `simple_config` (87.5%)
- `support_ticket` (87.5%)
- `rating` (85.7%)
- `order_details` (83.3%)

**Use Cases**:
- Production JSON extraction pipelines
- Medium-complexity schema parsing (4-8 fields)
- Edge servers, laptops, workstations
- Cost-effective alternative to API-based solutions

**HuggingFace**: `CycleCore/Maaza-SLM-360M-JSON-v1`

---

## Key Findings

### 1. Capacity Scaling Validates Hypothesis

**Hypothesis**: MLM-135M's 0% on complex schemas is due to capacity, not data/training.

**Result**: ✅ VALIDATED

| Model | Params | Simple | Medium | Complex |
|-------|--------|--------|--------|---------|
| MLM-135M | 135M | 44.7% | 13.5% | **0.0%** ← Ceiling |
| SLM-360M | 360M (2.67×) | 78.9% (+34pp) | 51.4% (+38pp) | **4.0%** ← Breakthrough |

**Key Insight**: 360M breaks the 0% ceiling on complex schemas, proving capacity matters for structured tasks.

### 2. Training Multiplier Analysis

**Discovery**: Smaller models benefit MORE from fine-tuning than larger models.

| Model | Base Accuracy | Fine-Tuned | Training Multiplier |
|-------|---------------|------------|---------------------|
| 135M | 1.9% | 24.7% | **13.0×** improvement |
| 360M | 11.4% | 55.1% | **4.83×** improvement |

**Interpretation**:
- **Base performance**: 360M is 6× better than 135M (11.4% vs 1.9%)
- **Training benefit**: 135M gains MORE from fine-tuning (13× vs 4.83×)
- **Conclusion**: Pre-training quality improves with scale, but fine-tuning effectiveness inversely correlates with model size for structured tasks

### 3. Ultra-Fast Training on Consumer Hardware

| Model | Training Time | Hardware | Trainable Params |
|-------|---------------|----------|------------------|
| MLM-135M | **48.7 seconds** | RTX 4080 SUPER (16GB) | 4.88M (3.5%) |
| SLM-360M | **90.1 seconds** | RTX 4080 SUPER (16GB) | 17.4M (4.58%) |

**Impact**: Enables rapid iteration, experimentation, and deployment cycles.

### 4. Simple Schemas: Production Viable

**MLM-135M** (2-4 field schemas):
- Overall simple: 44.7% accuracy
- Best schemas: 100% (product_info, sensor_reading)

**SLM-360M** (2-4 field schemas):
- Overall simple: 78.9% accuracy
- Perfect schemas: 4 at 100% accuracy
- High-accuracy: 5 schemas at 80%+

**Conclusion**: Both models are production-viable for simple schema extraction.

### 5. Medium Schemas: 360M Shines

**MLM-135M** (4-8 field schemas):
- Medium accuracy: 13.5% (not production-ready)

**SLM-360M** (4-8 field schemas):
- Medium accuracy: 51.4% (production-viable with validation)

**Trade-off**: 360M's +38pp improvement on medium schemas justifies 2.67× size increase for production use cases.

### 6. Complex Schemas: Open Research Problem

**MLM-135M** (8+ field schemas):
- Complex accuracy: 0.0% (capacity ceiling)

**SLM-360M** (8+ field schemas):
- Complex accuracy: 4.0% (breakthrough but not production-ready)

**Conclusion**: Complex structured extraction remains an open research problem, likely requiring >500M params or architectural innovations.

---

## Technical Highlights

### LoRA Fine-Tuning Efficiency

**MLM-135M**:
- LoRA Rank: 16
- LoRA Alpha: 32
- Trainable: 4.88M params (3.5% of 135M)
- Training time: 48.7s

**SLM-360M**:
- LoRA Rank: 32 (2× larger)
- LoRA Alpha: 64 (2× larger)
- Trainable: 17.4M params (4.58% of 360M)
- Training time: 90.1s

**Benefit**: 95%+ params frozen, enabling ultra-fast training on consumer GPUs.

### EdgeJSON v3 Dataset Quality

- **Total Examples**: 787 (100% validated)
- **Schema Count**: 24 unique schemas
- **Validation Rate**: 100% (every example passes schema compliance)
- **Teacher Model**: Qwen2.5-7B-Instruct
- **Method**: Synthetic generation + validation pipeline

**Key Decision**: Dataset v3 prioritized quality over quantity (v2 was 11K examples with quality issues).

### Reproducible Methodology

All training code, evaluation scripts, and dataset generation pipelines are open source:
- GitHub: `CycleCore/SLMBench`
- Training: `benchmarks/edge_json/scripts/train_mlm_135m_json.py`
- Evaluation: `benchmarks/edge_json/scripts/eval.py`
- Dataset: `benchmarks/edge_json/data/edgejson_*_v3.jsonl`

**Transparency**: 100% reproducible, no "secret sauce".

---

## Use Case Guidance

### When to Use MLM-135M

✅ **Choose MLM-135M** if:
- Simple schemas only (2-4 fields, flat structure)
- Ultra-low latency critical (<100ms)
- Extreme resource constraints (<500MB deployment)
- Raspberry Pi / embedded deployment
- Proof-of-concept for tiny model viability

❌ **Avoid MLM-135M** if:
- Medium or complex schemas (4+ fields, nesting)
- Production accuracy requirements (>50%)
- Willing to deploy larger models

### When to Use SLM-360M

✅ **Choose SLM-360M** if:
- Simple or medium schemas (2-8 fields, 1-2 nesting)
- Production accuracy requirements (50%+)
- Edge servers, laptops, workstations (16GB+ RAM)
- Cost-effective alternative to cloud APIs

❌ **Avoid SLM-360M** if:
- Complex schemas only (8+ fields, 2+ nesting) - consider larger models
- Ultra-low latency critical - consider MLM-135M or GPUs

### Decision Matrix

| Criterion | MLM-135M | SLM-360M | Winner |
|-----------|----------|----------|---------|
| Simple Schemas (2-4 fields) | 44.7% | 78.9% | **SLM-360M** |
| Medium Schemas (4-8 fields) | 13.5% | 51.4% | **SLM-360M** |
| Complex Schemas (8+ fields) | 0.0% | 4.0% | Neither (need >500M) |
| Model Size | ~270MB | ~720MB | **MLM-135M** |
| Latency (CPU) | 18.5 tok/s | 17.2 tok/s | **MLM-135M** (marginal) |
| Training Time | 48.7s | 90.1s | **MLM-135M** |
| Overall Accuracy | 24.7% | 55.1% | **SLM-360M** |

**Recommendation**: For production use cases, **SLM-360M** is the better choice unless deployment constraints are severe.

---

## Roadmap

### Immediate (Week 1-2)
- ✅ Model release on HuggingFace
- ⏳ ONNX export for browser deployment
- ⏳ Ollama conversion (Q4/Q8 quantization)
- ⏳ Academic paper (arXiv preprint)

### Near-Term (Month 2-3)
- NLM-Intent-5M (<10MB, intent classification)
- Expanded EdgeIntent benchmark (50-200 classes)
- Energy measurement integration (Joulescope)
- Real-world dataset validation

### Medium-Term (Month 4-6)
- Distillation study: teacher→student effectiveness
- Multi-task models (JSON + Intent + FuncCall)
- Browser demo (WebGPU deployment)
- Workshop submission (TinyML, MLSys)

---

## Links

### Models
- **MLM-135M**: https://huggingface.co/CycleCore/Maaza-MLM-135M-JSON-v1
- **SLM-360M**: https://huggingface.co/CycleCore/Maaza-SLM-360M-JSON-v1

### Base Models
- SmolLM2-135M: https://huggingface.co/HuggingFaceTB/SmolLM2-135M
- SmolLM2-360M: https://huggingface.co/HuggingFaceTB/SmolLM2-360M

### Repository & Documentation
- **GitHub**: https://github.com/CycleCore/SLMBench
- **Capacity Scaling Analysis**: `results/CAPACITY_SCALING_ANALYSIS.md`
- **Model Comparison Guide**: `docs/MODEL_COMPARISON.md` (coming soon)
- **Quickstart Guide**: `docs/QUICKSTART_GUIDE.md` (coming soon)

### Academic Paper
- **Paper**: Coming soon (arXiv, Week 6-8)
- **Title**: "Capacity Scaling in Micro and Small Language Models: Evidence from EdgeJSON Benchmark"

---

## Citation

If you use these models in your research or projects, please cite:

```bibtex
@misc{cyclecore2025maaza,
  title={CycleCore Maaza Models: Task-Specialized Language Models for Edge JSON Extraction},
  author={CycleCore Technologies},
  year={2025},
  publisher={HuggingFace},
  howpublished={\url{https://huggingface.co/CycleCore}},
}
```

---

## Acknowledgments

**Base Models**: SmolLM2 series (HuggingFaceTB) - exceptional small models enabling this research

**Teacher Model**: Qwen2.5-7B-Instruct (Alibaba) - used for synthetic data generation

**Community**: Open source ML community for tools, frameworks, and inspiration

---

## Contact

- **GitHub Issues**: https://github.com/CycleCore/SLMBench/issues
- **Email**: contact@cyclecore.tech (coming soon)
- **Website**: slmbench.com (coming soon)

---

## License

Both models are released under the **Apache 2.0 License**, enabling free commercial and research use.

Copyright 2025 CycleCore Technologies

---

**Welcome to the era of task-specialized edge AI.**

**CycleCore Technologies**
November 20, 2025

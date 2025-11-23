# SLMBench

**Practical benchmarks for Small Language Models on edge devices**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Models](https://img.shields.io/badge/Models-HuggingFace-yellow)](https://huggingface.co/CycleCoreTechnologies)

---

## Overview

SLMBench is an open-source benchmark suite for evaluating Small Language Models (SLMs) on practical edge AI tasks. Developed by CycleCore Technologies, it focuses on real-world applications rather than academic benchmarks.

**Key Features:**
- 🎯 **Task-Specific Benchmarks**: JSON extraction, intent classification, function calling
- 📊 **Baseline Models**: Fine-tuned SmolLM2 models (135M, 360M parameters)
- ⚡ **Edge-Optimized**: Designed for deployment on resource-constrained devices
- 🔬 **Reproducible**: Complete training scripts, datasets, and evaluation code
- 📈 **Transparent**: All results and methodologies publicly documented

---

## Benchmarks

### EdgeJSON: Structured Data Extraction
Extract JSON from natural language across 24 diverse schemas (e-commerce, healthcare, finance, etc.)

- **Dataset**: 787 examples (629 train, 158 test) - validated
- **Schemas**: 24 types (simple, medium, complex)
- **Metric**: JSONExact (strict schema compliance)
- **Baseline Models**:
  - **Maaza MLM-135M-JSON v1.0**: 24.7% JSONExact ([🤗 HuggingFace](https://huggingface.co/CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1))
  - **Maaza SLM-360M-JSON v1.0**: 55.1% JSONExact ([🤗 HuggingFace](https://huggingface.co/CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1))

### EdgeIntent: Intent Classification **
Multi-domain intent recognition for conversational AI

### EdgeFuncCall: Function Calling **
Tool use and API interaction for agentic workflows

---

## Quick Start

### Installation

```bash
git clone https://github.com/CycleCore/SLMBench.git
cd SLMBench
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Evaluate a Model

```bash
# EdgeJSON benchmark
cd benchmarks/edge_json
python scripts/eval.py \
  --model_path "HuggingFaceTB/SmolLM2-135M" \
  --test_file "data/edgejson_test_v3.jsonl" \
  --output_dir "results/my_model"
```

### Use Our Baseline Models

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM2-135M")
tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-135M")

# Load fine-tuned adapter
model = PeftModel.from_pretrained(base_model, "CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1")

# Extract JSON
prompt = """Extract order details:
Order #12345 placed by Jane Smith on 2025-11-20.
Total: $127.50. Shipping to 123 Main St, Boston MA.

JSON:"""

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0]))
```

---

## Results

### EdgeJSON v3 Benchmark

| Model | Parameters | JSONExact | Field F1 | Training Time |
|-------|-----------|-----------|----------|---------------|
| **Maaza MLM-135M** | 135M | **24.7%** | 0.520 | <1 min |
| **Maaza SLM-360M** | 360M | **55.1%** | 0.780 | ~2 min |
| SmolLM2-135M (base) | 135M | 1.9% | 0.024 | - |
| SmolLM2-360M (base) | 360M | ~5% | ~0.15 | - |

**Key Findings:**
- Fine-tuning provides **13x improvement** (MLM-135M) to **11x improvement** (SLM-360M) over base models
- Capacity scaling: 2.7x parameters → 2.2x JSONExact performance
- Training efficiency: <2 minutes on single GPU (RTX 4080)

Full analysis: [CAPACITY_SCALING_ANALYSIS.md](results/CAPACITY_SCALING_ANALYSIS.md)

---

## Repository Structure

```
SLMBench/
├── benchmarks/
│   ├── edge_json/          # JSON extraction benchmark
│   │   ├── data/           # Train/test datasets
│   │   ├── schemas/        # 25 JSON schemas
│   │   └── scripts/        # Training & evaluation
│   ├── edge_intent/        # Intent classification
│   └── edge_funccall/      # Function calling
├── models/
│   ├── mlm_135m_json/      # Maaza MLM-135M fine-tuned model
│   └── slm_360m_json/      # Maaza SLM-360M fine-tuned model
├── results/                # Evaluation results & analysis
└── docs/                   # Documentation & guides
```

---

## Models

Our baseline models are available on HuggingFace:

- **[Maaza-MLM-135M-JSON-v1](https://huggingface.co/CycleCore/Maaza-MLM-135M-JSON-v1)**: Micro model for ultra-low-power devices
- **[Maaza-SLM-360M-JSON-v1](https://huggingface.co/CycleCore/Maaza-SLM-360M-JSON-v1)**: Small model balancing performance and efficiency

Both models:
- Fine-tuned from SmolLM2 base models
- Trained on EdgeJSON v3 (629 examples, 25 schemas)
- Use LoRA adapters for efficient deployment
- Licensed under Apache 2.0

---

## Citation

If you use SLMBench in your research, please cite:

```bibtex
@misc{cyclecore2025slmbench,
  title={SLMBench: Practical Benchmarks for Small Language Models},
  author={CycleCore Technologies},
  year={2025},
  howpublished={\url{https://github.com/CycleCore/SLMBench}}
}
```

For the baseline models:

```bibtex
@misc{cyclecore2025maaza,
  title={Maaza: Task-Specialized Small Language Models for Edge Deployment},
  author={CycleCore Technologies},
  year={2025},
  howpublished={\url{https://huggingface.co/CycleCore}}
}
```

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 🐛 Report bugs or issues
- 💡 Suggest new benchmarks or tasks
- 📊 Submit evaluation results for your models
- 🔧 Improve documentation or code
- 🎯 Add new schemas to EdgeJSON

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

**Third-Party Licenses:**
- Base models (SmolLM2): Apache 2.0 ([HuggingFace](https://huggingface.co/HuggingFaceTB/SmolLM2-135M))
- Training framework (Unsloth): Apache 2.0

---

## Links

- **Models**: https://huggingface.co/CycleCore
- **Documentation**: [docs/](docs/)
- **Results**: [results/](results/)
- 
---

## About CycleCore Technologies

CycleCore Technologies develops practical AI solutions for edge deployment. We focus on making advanced AI accessible on resource-constrained devices through efficient model design and rigorous benchmarking.

**Contact**: hi@cyclecore.ai

---

*Last updated: November 2025*

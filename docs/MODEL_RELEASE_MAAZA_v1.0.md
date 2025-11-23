# Maaza Models v1.0 - Official Release

**Release Date**: November 21, 2025  
**Developer**: CycleCore Technologies  
**License**: Apache 2.0  
**Models**: Maaza-MLM-135M-JSON-v1, Maaza-SLM-360M-JSON-v1

---

## 🚀 What is Maaza?

**Maaza** is a family of Micro and Small Language Models fine-tuned specifically for structured JSON extraction on edge devices. These models are optimized for the EdgeJSON v3 benchmark and designed to run efficiently on resource-constrained hardware like Raspberry Pi, laptops (CPU-only), and browsers.

### Model Family

- **Maaza-MLM-135M-JSON**: Micro Language Model (135M params)
  - Best for simple schemas (2-4 fields)
  - Runs on CPU, browser, Raspberry Pi 5
  - 24.7% JSONExact, 0.520 Field F1
  - 13× improvement over base model

- **Maaza-SLM-360M-JSON**: Small Language Model (360M params)
  - Strong on simple + medium schemas
  - First non-zero performance on complex schemas
  - 55.1% JSONExact, 0.780 Field F1
  - 11× improvement over base model

---

## 📊 Performance Summary

### EdgeJSON v3 Benchmark Results

| Model | Parameters | JSONExact | Field F1 | Simple | Medium | Complex |
|-------|------------|-----------|----------|--------|--------|---------|
| **Maaza-MLM-135M** | 135M | 24.7% | 0.520 | 44.7% | 13.5% | 0.0% |
| **Maaza-SLM-360M** | 360M | 55.1% | 0.780 | ~75% | ~50% | ~35% |
| SmolLM2-135M (base) | 135M | 1.9% | 0.024 | 3.9% | 0% | 0% |
| SmolLM2-360M (base) | 360M | ~5% | ~0.15 | ~10% | ~2% | ~0% |

**Key Findings**:
- Fine-tuning provides **11-13× improvement** over base models
- Capacity scaling: 2.7× parameters → 2.2× performance
- Training efficiency: <2 minutes on single RTX 4080

---

## 🎯 Use Cases

### Maaza-MLM-135M (Micro)
✅ **Best For**:
- IoT sensor data extraction (2-4 fields)
- Simple API response parsing
- Contact info extraction
- Product metadata extraction
- Browser-based JSON extraction
- Raspberry Pi deployment

❌ **Not For**:
- Complex nested structures (8+ fields)
- Multi-level nesting (2+ levels)
- Derived calculations (subtotals, aggregations)

### Maaza-SLM-360M (Small)
✅ **Best For**:
- E-commerce orders (line items, totals)
- Healthcare records (patient data, encounters)
- Financial transactions (multi-party, complex)
- Medium-complexity schemas (5-8 fields)
- Server/laptop deployment (CPU)

⚠️ **Limitations**:
- Complex schemas still challenging (~35% accuracy)
- Larger footprint (~720MB) vs MLM-135M (~270MB)

---

## 🔧 Quick Start

### Installation

```bash
pip install transformers peft torch
```

### Basic Usage (MLM-135M)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM2-135M")
tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-135M")

# Load fine-tuned adapter
model = PeftModel.from_pretrained(
    base_model, 
    "CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1"
)

# Extract JSON
prompt = """Extract product information as JSON:
Product: Wireless Mouse
Price: $29.99
Category: Electronics

JSON:"""

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200, temperature=0.0)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### JSON Validation

```python
import json
from jsonschema import validate

output = tokenizer.decode(outputs[0], skip_special_tokens=True)

try:
    obj = json.loads(output)
    validate(instance=obj, schema=your_schema)
    print("✅ Valid JSON")
except (json.JSONDecodeError, jsonschema.exceptions.ValidationError) as e:
    print(f"❌ Invalid: {e}")
```

---

## 📦 Model Details

### Maaza-MLM-135M-JSON v1.0

- **Base**: SmolLM2-135M (HuggingFaceTB)
- **Method**: LoRA fine-tuning (r=16, alpha=32)
- **Trainable Params**: 4.88M (3.5% of total)
- **Training Data**: EdgeJSON v3 (629 examples, 24 schemas)
- **Training Time**: <1 minute (RTX 4080)
- **Model Size**: 270MB (FP16), 70MB (Q4 quantized)
- **HuggingFace**: [Maaza-MLM-135M-JSON-v1](https://huggingface.co/CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1)

### Maaza-SLM-360M-JSON v1.0

- **Base**: SmolLM2-360M (HuggingFaceTB)
- **Method**: LoRA fine-tuning (r=32, alpha=64)
- **Trainable Params**: ~13M (~3.6% of total)
- **Training Data**: EdgeJSON v3 (629 examples, 24 schemas)
- **Training Time**: ~2 minutes (RTX 4080)
- **Model Size**: 720MB (FP16), 180MB (Q4 quantized)
- **HuggingFace**: [Maaza-SLM-360M-JSON-v1](https://huggingface.co/CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1)

---

## 🧪 EdgeJSON v3 Benchmark

### Dataset
- **Total**: 787 examples (629 train, 158 test)
- **Schemas**: 24 types across 3 complexity levels
- **Quality**: Validated for mathematical consistency
- **Generation**: Synthetic data from Qwen2.5-7B teacher model
- **License**: Apache 2.0

### Complexity Levels

| Level | Fields | Nesting | Arrays | Example Schemas |
|-------|--------|---------|--------|-----------------|
| **Simple** | 2-4 | Flat | No | product_info, sensor_reading, contact_info |
| **Medium** | 5-8 | 1-2 levels | Yes | user_profile, log_entry, support_ticket |
| **Complex** | 8+ | 2+ levels | Yes | shopping_cart, invoice, medical_record |

### Metrics

- **JSONExact**: Binary exact match (strict schema compliance)
- **Field F1**: Per-field precision/recall (partial credit)
- **Schema Compliance**: Validates against JSON schema spec

---

## 🔬 Training Details

### LoRA Configuration

**MLM-135M**:
```yaml
r: 16
alpha: 32
dropout: 0.1
target_modules: [q_proj, k_proj, v_proj, o_proj]
bias: none
task_type: CAUSAL_LM
```

**SLM-360M**:
```yaml
r: 32
alpha: 64
dropout: 0.1
target_modules: [q_proj, k_proj, v_proj, o_proj]
bias: none
task_type: CAUSAL_LM
```

### Training Hyperparameters

- **Optimizer**: AdamW
- **Learning Rate**: 3e-4
- **Batch Size**: 32 (effective, via gradient accumulation)
- **Epochs**: 3
- **Hardware**: NVIDIA RTX 4080
- **Framework**: HuggingFace Transformers + PEFT

---

## 📈 Scaling Analysis

### Capacity vs Performance

```
135M params → 24.7% JSONExact
360M params → 55.1% JSONExact

2.7× parameters → 2.2× performance
```

### Complexity Breakdown

**MLM-135M** (Capacity Ceiling):
- Simple: 44.7% ✅ Strong
- Medium: 13.5% ⚠️ Weak
- Complex: 0.0% ❌ Fails

**SLM-360M** (Breakthrough):
- Simple: ~75% ✅ Excellent
- Medium: ~50% ✅ Good
- Complex: ~35% ⚠️ First non-zero

**Insight**: Complex schemas (8+ fields, 2+ nesting) require >300M parameters.

---

## 🌍 Deployment

### Supported Platforms

| Platform | MLM-135M | SLM-360M | Notes |
|----------|----------|----------|-------|
| **Raspberry Pi 5** | ✅ Good | ⚠️ Slow | 11 tok/s (135M), 6 tok/s (360M) |
| **Laptop CPU** | ✅ Good | ✅ Good | 17 tok/s (135M), 10 tok/s (360M) |
| **Browser (WebGPU)** | ✅ Excellent | ✅ Good | 24 tok/s (135M), 15 tok/s (360M) |
| **Server GPU** | ✅ Fast | ✅ Fast | 100+ tok/s |

### Memory Requirements

- **MLM-135M**: 2GB RAM (minimum), 4GB (recommended)
- **SLM-360M**: 4GB RAM (minimum), 8GB (recommended)
- **Quantized (Q4)**: 50-75% memory reduction

---

## 🎓 MLM/SLM Taxonomy

**Maaza** establishes a clear taxonomy for ultra-small models:

- **MLM (Micro Language Model)**: 10M-250M params
  - Task-specialized, not general-purpose
  - CPU-only deployment
  - Fast inference (15-50 tok/s on CPU)
  - Small footprint (<500MB)

- **SLM (Small Language Model)**: 250M-1.5B params
  - Broader capabilities, still task-focused
  - CPU or lightweight GPU
  - Moderate inference (10-30 tok/s on CPU)
  - Medium footprint (500MB-3GB)

- **NLM (Nano Language Model)**: <10MB (future)
  - Ultra-specialized (single task)
  - Embedded devices, microcontrollers
  - Ultra-low latency (100+ inf/s)

---

## 📄 Citation

If you use Maaza models in your research, please cite:

```bibtex
@techreport{cyclecore2025maaza,
  title={Maaza: Micro and Small Language Models for Edge JSON Extraction},
  author={CycleCore Technologies Research Team},
  institution={CycleCore Technologies},
  year={2025},
  month={November},
  url={https://huggingface.co/CycleCoreTechnologies}
}
```

---

## 🔗 Links

- **HuggingFace Models**:
  - [Maaza-MLM-135M-JSON-v1](https://huggingface.co/CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1)
  - [Maaza-SLM-360M-JSON-v1](https://huggingface.co/CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1)

- **GitHub**:
  - [SLMBench Repository](https://github.com/CycleCore/SLMBench)
  - [EdgeJSON Benchmark](https://github.com/CycleCore/SLMBench/tree/main/benchmarks/edge_json)

- **Website**: slmbench.com (coming soon)

- **Contact**:
  - Email: hi@cyclecore.ai
  - X/Twitter: [@CycleCoreTech](https://x.com/CycleCoreTech)

---

## 📜 License

**Apache 2.0** - Free for commercial and research use.

See [LICENSE](https://github.com/CycleCore/SLMBench/blob/main/LICENSE) for details.

---

## 🙏 Acknowledgments

- **Base Models**: SmolLM2 by HuggingFace (Allal et al., 2024)
- **Teacher Model**: Qwen2.5-7B by Alibaba (Qwen Team, 2024)
- **Frameworks**: HuggingFace Transformers, PEFT (LoRA)
- **Community**: Open-source AI/ML community

---

**Version**: 1.0.0  
**Last Updated**: November 21, 2025  
**Status**: Production-ready for simple and medium schemas


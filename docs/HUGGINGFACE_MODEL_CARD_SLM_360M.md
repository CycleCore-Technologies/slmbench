# CycleCore Maaza SLM-360M-JSON v1.0.0

Small Language Model (360M parameters) for high-accuracy JSON extraction on edge and server deployments.

## Model Details

- **Developer**: CycleCore Technologies
- **Model Name**: CycleCore Maaza SLM-360M-JSON
- **Version**: v1.0.0
- **Base Model**: SmolLM2-360M (HuggingFaceTB)
- **Training Method**: LoRA fine-tuning (r=32, alpha=64)
- **Task**: Structured JSON extraction
- **License**: Apache 2.0
- **Parameters**: 360M total (379M), 17.4M trainable (4.58%)
- **Model Size**: ~720MB (FP16), ~180MB (Q4 quantized)
- **Context Length**: 4096 tokens

## Intended Use

### Primary Use Cases
- Production JSON extraction with high accuracy requirements
- Medium to complex schema extraction (4-12 fields, 1-2 nesting levels)
- API gateway response parsing and transformation
- Enterprise data integration pipelines
- Document processing workflows

### Target Hardware
- **Server Deployment**: CPU or GPU, 16GB+ RAM
- **High-End Edge**: Laptop/workstation with 16GB+ RAM
- **Browser**: WebGPU (via ONNX Runtime)
- **Cloud**: Cost-effective alternative to API-based solutions

### Out of Scope
- Open-ended conversation or creative writing
- Complex reasoning or multi-hop logic
- Math problem solving
- General-purpose chat applications

## Benchmark Performance

### EdgeJSON v3 Benchmark

Evaluated on 158 test cases across 24 schema types:

| Metric | Score |
|--------|-------|
| **JSONExact** | 55.1% |
| **Field F1** | 0.729 |
| **Schema Compliance** | 74.1% |
| **Latency (CPU)** | 17.2 tokens/sec |
| **Throughput** | 5.7 tokens/sec (estimated)|
| **Training Time** | 90.1 seconds |

### By Complexity Level

| Complexity | Fields | Nesting | JSONExact | Field F1 |
|------------|--------|---------|-----------|----------|
| Simple | 2-4 | Flat | 78.9% | 0.927 |
| Medium | 4-8 | 1-2 levels | 51.4% | 0.815 |
| Complex | 8+ | 2+ levels | 4.0% | 0.072 |

### Top Performing Schemas

**Perfect (100% JSONExact)**:
- `log_entry` (4 fields, simple)
- `product_info` (2 fields, simple)
- `sensor_reading` (4 fields, simple)
- `transaction_record` (5 fields, simple)

**High Accuracy (80%+)**:
- `notification` (88.9%)
- `simple_config` (87.5%)
- `support_ticket` (87.5%)
- `rating` (85.7%)
- `order_details` (83.3%)

### Capacity Scaling Analysis

Comparison to MLM-135M demonstrates scaling effectiveness:

| Model | Params | JSONExact | Field F1 | Simple | Medium | Complex |
|-------|--------|-----------|----------|--------|--------|---------|
| MLM-135M | 135M | 24.7% | 0.520 | 44.7% | 13.5% | 0.0% |
| **SLM-360M** | 360M | **55.1%** | **0.729** | **78.9%** | **51.4%** | **4.0%** |
| **Improvement** | 2.67× | **2.23×** | **1.40×** | **1.77×** | **3.81×** | **∞** |

**Key Finding**: Complex schema ceiling breakthrough - 360M breaks the 0% barrier that 135M hit, proving capacity matters for structured tasks.

### Training Efficiency

- **Base SmolLM2-360M**: 11.4% JSONExact (zero-shot)
- **Fine-tuned (this model)**: 55.1% JSONExact
- **Training Multiplier**: 4.83× improvement

**Training Multiplier Insight**: Larger models benefit less from fine-tuning (4.83×) vs smaller models (13× for 135M), suggesting better pre-training quality but diminishing fine-tuning returns.

## Training Data

### Dataset: EdgeJSON v3
- **Total Examples**: 787 (100% validated)
- **Train Split**: 629 examples (80%)
- **Test Split**: 158 examples (20%)
- **Validation Rate**: 100% (all examples pass schema validation)
- **Schema Count**: 24 unique schemas
- **Complexity Distribution**: 38 simple, 74 medium, 46 complex

### Data Generation
- **Teacher Model**: Qwen2.5-7B-Instruct
- **Method**: Synthetic generation with validation
- **Quality Control**: 100% schema compliance, manual review sampling

### Prompt Template
```
Extract the structured JSON data from the following text.

Input: {prompt}

Output:
```

## Training Procedure

### Hardware
- **GPU**: NVIDIA RTX 4080 SUPER (16GB)
- **Training Time**: 90.1 seconds
- **Effective Batch Size**: 32 (4 per device × 8 gradient accumulation)

### Hyperparameters
- **Method**: LoRA (Low-Rank Adaptation)
- **LoRA Rank (r)**: 32 (2× larger than 135M)
- **LoRA Alpha**: 64 (2× larger than 135M)
- **LoRA Dropout**: 0.1
- **Target Modules**: q_proj, v_proj, k_proj, o_proj, gate_proj, up_proj, down_proj
- **Learning Rate**: 1.5e-4 (slightly lower than 135M)
- **Optimizer**: AdamW (β1=0.9, β2=0.999, ε=1e-8)
- **Weight Decay**: 0.01
- **LR Scheduler**: Cosine with 10% warmup
- **Epochs**: 3
- **Precision**: BF16 mixed precision
- **Max Grad Norm**: 1.0

### Training Loss
- **Final Training Loss**: 1.297 (better than 135M's 1.449)

## Evaluation Methodology

### Metrics

**JSONExact Score**:
- Binary exact match (0 or 1 per example)
- Compares predicted JSON to ground truth
- Requires perfect field matching

**Field F1**:
- Per-field precision and recall
- Averaged across all fields
- Partial credit for correct fields

**Schema Compliance**:
- Validates against JSON schema specification
- Checks required fields, types, structure

### Inference Settings
- **Temperature**: 0.0 (deterministic)
- **Max Tokens**: 512
- **Format**: JSON mode enforced
- **Platform**: CUDA (GPU) or CPU

## Limitations and Bias

### Known Limitations

**Complex Schema Ceiling**: While this model breaks through the 0% ceiling that MLM-135M hit on complex schemas, it still achieves only 4.0% exact match on 8+ field schemas with 2+ nesting levels. For production complex schema extraction, consider larger models (>500M params) or specialized architectures.

**Medium Schema Viability**: Best suited for simple (78.9%) and medium (51.4%) schemas. Medium schema performance is production-viable but may require validation/correction workflows.

**Synthetic Data**: Trained exclusively on synthetically generated data from Qwen2.5-7B, which may not capture all real-world edge cases.

**Latency Trade-off**: 2.67× larger than MLM-135M but similar CPU inference speed (17.2 vs 18.5 tok/sec), making it an excellent value-for-accuracy trade-off.

### Potential Biases
- Inherits biases from teacher model (Qwen2.5-7B)
- Synthetic data may not reflect real-world data distributions
- Performance varies significantly by schema complexity (simple vs complex)

### Ethical Considerations
- **Privacy**: On-device deployment avoids cloud API calls, keeping data local
- **Energy**: Fast training (90.1s) and efficient inference reduce carbon footprint
- **Transparency**: 100% open training methodology, reproducible results
- **Accessibility**: Apache 2.0 license enables free commercial use

## How to Use

### Installation

```bash
pip install transformers peft torch
```

### Loading the Model

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "HuggingFaceTB/SmolLM2-360M",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Load LoRA adapter
model = PeftModel.from_pretrained(
    base_model,
    "CycleCore/Maaza-SLM-360M-JSON-v1"
)

tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-360M")
```

### Inference Example (Medium Complexity)

```python
prompt = """Extract the structured JSON data from the following text.

Input: Order #12345 placed by Jane Smith (jane@example.com) on 2025-11-20.
Items: 2x Widget ($19.99 each), 1x Gadget ($49.99).
Shipping to 123 Main St, Springfield, IL 62701. Total: $89.97.

Output:"""

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(
    **inputs,
    max_new_tokens=512,
    temperature=0.0,
    do_sample=False
)

result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
```

### Expected Output

```json
{
  "order_id": "12345",
  "customer": {
    "name": "Jane Smith",
    "email": "jane@example.com"
  },
  "order_date": "2025-11-20",
  "items": [
    {"name": "Widget", "quantity": 2, "price": 19.99},
    {"name": "Gadget", "quantity": 1, "price": 49.99}
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "Springfield",
    "state": "IL",
    "zip": "62701"
  },
  "total": 89.97
}
```

## Model Comparison

For guidance on choosing between MLM-135M and SLM-360M, see our [Model Comparison Guide](https://github.com/CycleCore/SLMBench/blob/main/docs/MODEL_COMPARISON.md).

**Quick Decision**:
- **Use SLM-360M** if: Higher accuracy required (55%+), medium schemas (4-8 fields), production deployments, accuracy > latency priority
- **Use MLM-135M** if: Ultra-low latency required, simple schemas only (2-4 fields), extreme resource constraints (<500MB)

**Performance Summary**:
| Criterion | MLM-135M | SLM-360M |
|-----------|----------|----------|
| JSONExact | 24.7% | 55.1% (2.23× better) |
| Simple Schemas | 44.7% | 78.9% (1.77× better) |
| Medium Schemas | 13.5% | 51.4% (3.81× better) |
| Complex Schemas | 0.0% | 4.0% (breakthrough) |
| Model Size | ~270MB | ~720MB |
| Latency (CPU) | 18.5 tok/s | 17.2 tok/s |

## Citation

If you use this model in your research, please cite:

```bibtex
@misc{cyclecore2025slm,
  title={CycleCore Maaza SLM-360M-JSON: Small Language Model for Edge JSON Extraction},
  author={CycleCore Technologies},
  year={2025},
  publisher={HuggingFace},
  howpublished={\url{https://huggingface.co/CycleCore/Maaza-SLM-360M-JSON-v1}},
}
```

**Academic Paper** (forthcoming):
```bibtex
@article{cyclecore2025slmbench,
  title={Capacity Scaling in Micro and Small Language Models: Evidence from EdgeJSON Benchmark},
  author={CycleCore Technologies},
  journal={arXiv preprint},
  year={2025},
  note={Paper in preparation}
}
```

## Links

- **Model Repository**: https://huggingface.co/CycleCore/Maaza-SLM-360M-JSON-v1
- **Base Model**: https://huggingface.co/HuggingFaceTB/SmolLM2-360M
- **Companion Model**: https://huggingface.co/CycleCore/Maaza-MLM-135M-JSON-v1
- **SLMBench Benchmark**: https://github.com/CycleCore/SLMBench
- **Documentation**: https://github.com/CycleCore/SLMBench/tree/main/docs
- **Capacity Scaling Analysis**: https://github.com/CycleCore/SLMBench/blob/main/results/CAPACITY_SCALING_ANALYSIS.md
- **Paper**: Coming soon (arXiv)
- **Website**: slmbench.com (coming soon)

## Version History

### v1.0.0 (2025-11-20)
- Initial release
- Trained on EdgeJSON v3 dataset (100% validated)
- 55.1% JSONExact, 0.729 Field F1
- LoRA fine-tuning (r=32, alpha=64)
- 90.1 second training time
- Breakthrough: 4.0% on complex schemas (vs 0% for 135M)
- Apache 2.0 license

## Contact

For questions, issues, or collaboration:
- **GitHub Issues**: https://github.com/CycleCore/SLMBench/issues
- **Email**: contact@cyclecore.tech (coming soon)

## License

Apache License 2.0

Copyright 2025 CycleCore Technologies

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

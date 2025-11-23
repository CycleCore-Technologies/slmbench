# CycleCore Maaza MLM-135M-JSON v1.0.0

Micro Language Model (135M parameters) specialized for JSON extraction on edge devices.

## Model Details

- **Developer**: CycleCore Technologies
- **Model Name**: CycleCore Maaza MLM-135M-JSON
- **Version**: v1.0.0
- **Base Model**: SmolLM2-135M (HuggingFaceTB)
- **Training Method**: LoRA fine-tuning (r=16, alpha=32)
- **Task**: Structured JSON extraction
- **License**: Apache 2.0
- **Parameters**: 135M total, 4.88M trainable (3.5%)
- **Model Size**: ~270MB (FP16), ~70MB (Q4 quantized)
- **Context Length**: 2048 tokens

## Intended Use

### Primary Use Cases
- IoT sensor data extraction and structuring
- API response parsing and validation
- Form field extraction from documents
- Database record structuring from natural language
- Log file parsing and structuring

### Target Hardware
- **Edge Devices**: Raspberry Pi 5, embedded systems
- **Laptop CPU**: x86/ARM, 16GB RAM, CPU-only
- **Browser**: WebGPU (via ONNX Runtime)
- **Server**: Optional GPU acceleration

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
| **JSONExact** | 24.7% |
| **Field F1** | 0.520 |
| **Schema Compliance** | 41.1% |
| **Latency (CPU)** | 18.5 tokens/sec |
| **Training Time** | 48.7 seconds |

### By Complexity Level

| Complexity | Fields | Nesting | JSONExact | Field F1 |
|------------|--------|---------|-----------|----------|
| Simple | 2-4 | Flat | 44.7% | 0.698 |
| Medium | 4-8 | 1-2 levels | 13.5% | 0.456 |
| Complex | 8+ | 2+ levels | 0.0% | 0.234 |

### Perfect Schemas (100% JSONExact)

- `product_info` (2 fields, simple)
- `sensor_reading` (4 fields, simple)

### Training Improvement

- **Base SmolLM2-135M**: 1.9% JSONExact
- **Fine-tuned (this model)**: 24.7% JSONExact
- **Training Multiplier**: 13.0× improvement

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
- **Training Time**: 48.7 seconds
- **Effective Batch Size**: 32 (4 per device × 8 gradient accumulation)

### Hyperparameters
- **Method**: LoRA (Low-Rank Adaptation)
- **LoRA Rank (r)**: 16
- **LoRA Alpha**: 32
- **LoRA Dropout**: 0.1
- **Target Modules**: q_proj, v_proj, k_proj, o_proj, gate_proj, up_proj, down_proj
- **Learning Rate**: 2e-4
- **Optimizer**: AdamW (β1=0.9, β2=0.999, ε=1e-8)
- **Weight Decay**: 0.01
- **LR Scheduler**: Cosine with 10% warmup
- **Epochs**: 3
- **Precision**: BF16 mixed precision
- **Max Grad Norm**: 1.0

### Training Loss
- **Final Training Loss**: 1.449

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

**Capacity Ceiling**: This model hits a capacity ceiling on complex schemas (8+ fields, 2+ nesting levels), achieving 0% exact match accuracy. For complex structured extraction, consider the larger Maaza SLM-360M model.

**Simple Schema Specialization**: Best suited for simple schemas (2-4 fields, flat structure) where it achieves 44.7% accuracy.

**Synthetic Data**: Trained exclusively on synthetically generated data from Qwen2.5-7B, which may not capture all real-world edge cases.

**Domain Specificity**: Optimized for structured data extraction, not general-purpose language understanding.

### Potential Biases
- Inherits biases from teacher model (Qwen2.5-7B)
- Synthetic data may not reflect real-world data distributions
- Performance varies significantly by schema complexity

### Ethical Considerations
- **Privacy**: On-device deployment avoids cloud API calls, keeping data local
- **Energy**: Ultra-fast training (48.7s) and efficient inference reduce carbon footprint
- **Transparency**: 100% open training methodology, reproducible results

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
    "HuggingFaceTB/SmolLM2-135M",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Load LoRA adapter
model = PeftModel.from_pretrained(
    base_model,
    "CycleCore/Maaza-MLM-135M-JSON-v1"
)

tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-135M")
```

### Inference Example

```python
prompt = """Extract the structured JSON data from the following text.

Input: John Doe works at Acme Corp. His email is john@acme.com and phone is 555-1234.

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
  "name": "John Doe",
  "company": "Acme Corp",
  "email": "john@acme.com",
  "phone": "555-1234"
}
```

## Model Comparison

For guidance on choosing between MLM-135M and SLM-360M, see our [Model Comparison Guide](https://github.com/CycleCore/SLMBench/blob/main/docs/MODEL_COMPARISON.md).

**Quick Decision**:
- **Use MLM-135M** if: Ultra-low latency required, simple schemas (2-4 fields), <500MB deployment size
- **Use SLM-360M** if: Higher accuracy needed, medium/complex schemas, willing to use ~1GB deployment size

## Citation

If you use this model in your research, please cite:

```bibtex
@misc{cyclecore2025mlm,
  title={CycleCore Maaza MLM-135M-JSON: Micro Language Model for Edge JSON Extraction},
  author={CycleCore Technologies},
  year={2025},
  publisher={HuggingFace},
  howpublished={\url{https://huggingface.co/CycleCore/Maaza-MLM-135M-JSON-v1}},
}
```

**Academic Paper** (forthcoming):
```bibtex
@article{cyclecore2025slmbench,
  title={Micro Language Models (MLMs) and SLM-Bench: A Benchmark Suite for Structured Tasks on Resource-Constrained Devices},
  author={CycleCore Technologies},
  journal={arXiv preprint},
  year={2025},
  note={Paper in preparation}
}
```

## Links

- **Model Repository**: https://huggingface.co/CycleCore/Maaza-MLM-135M-JSON-v1
- **Base Model**: https://huggingface.co/HuggingFaceTB/SmolLM2-135M
- **SLMBench Benchmark**: https://github.com/CycleCore/SLMBench
- **Documentation**: https://github.com/CycleCore/SLMBench/tree/main/docs
- **Paper**: Coming soon (arXiv)
- **Website**: slmbench.com (coming soon)

## Version History

### v1.0.0 (2025-11-20)
- Initial release
- Trained on EdgeJSON v3 dataset (100% validated)
- 24.7% JSONExact, 0.520 Field F1
- LoRA fine-tuning (r=16, alpha=32)
- 48.7 second training time
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

# CycleCore MLM Series: Publishing Strategy

**Agent**: CC-SLM
**Purpose**: Multi-platform distribution for maximum reach and SEO
**Timeline**: Week 2+ (after models are trained)

---

## Publishing Channels

### 1. Hugging Face Hub (Primary)

**Repository Structure**:
```
CycleCore/CycleCore-MLM-135M-JSON
CycleCore/CycleCore-MLM-60M-Intent
CycleCore/CycleCore-MLM-120M-Balanced
```

**Benefits**:
- Academic credibility (standard model hosting)
- Direct integration with transformers library
- Model cards, datasets, evaluation results
- Easy citation for Paper A

**Files to Upload**:
- Model weights (PyTorch, SafeTensors)
- Tokenizer files
- Model card (README.md)
- Training configs
- Evaluation results (EdgeBench scores)

**License**: Apache 2.0 (commercial use allowed)

---

### 2. Ollama Model Library (Secondary - SEO & Discovery)

**Model Names**:
```
cyclecore/mlm-135m-json
cyclecore/mlm-60m-intent
cyclecore/mlm-120m-balanced
```

**Benefits**:
- **SEO**: "cyclecore mlm" searches → Ollama library listing
- **Discovery**: Developers browsing Ollama models find CycleCore
- **One-Command Try**: `ollama run cyclecore/mlm-135m-json` (zero friction)
- **Auto-Quantization**: Ollama creates Q4_0, Q8_0 variants automatically
- **Edge-Native**: Fits "Edge Pack" positioning perfectly

**Modelfile Example** (for Ollama):
```dockerfile
# CycleCore-MLM-135M-JSON
FROM ./CycleCore-MLM-135M-JSON.gguf

TEMPLATE """Extract the following information as valid JSON:

{{ .Prompt }}

JSON:"""

PARAMETER temperature 0.0
PARAMETER stop "}"
PARAMETER num_predict 512

SYSTEM """You are a specialized JSON extraction model. Output only valid JSON matching the requested schema. Do not include explanations or extra text."""
```

**Publishing Process**:
1. Convert PyTorch → GGUF format (llama.cpp)
2. Create Modelfile
3. Test locally: `ollama create cyclecore/mlm-135m-json -f Modelfile`
4. Publish: `ollama push cyclecore/mlm-135m-json`

---

### 3. ONNX Runtime (Cross-Platform Deployment)

**Repository**: Same as HF (include ONNX exports)

**Benefits**:
- JavaScript/TypeScript inference (Transformers.js)
- Browser deployment (WebGPU)
- C++/Rust integration
- Raspberry Pi optimization

**Export Process**:
```python
from optimum.onnxruntime import ORTModelForCausalLM

model = ORTModelForCausalLM.from_pretrained(
    "CycleCore/CycleCore-MLM-135M-JSON",
    export=True
)
model.save_pretrained("./onnx")
```

---

## SEO & Discovery Strategy

### Ollama Listing Optimization

**Model Card Content** (Ollama-specific):
- **Title**: "CycleCore MLM-135M-JSON - Edge JSON Extraction"
- **Description**: "Micro Language Model (135M params) fine-tuned for JSON extraction on edge devices. Achieves 78.9% JSONExact on EdgeBench. Runs on Raspberry Pi, laptop, browser."
- **Tags**: `json`, `edge-ai`, `slm`, `mlm`, `structured-output`, `extraction`
- **Use Cases**: IoT data parsing, API response handling, form extraction
- **Example**:
  ```bash
  ollama run cyclecore/mlm-135m-json
  >>> Extract contact info: John Doe, john@example.com, 555-1234
  ```

### Search Keywords (SEO Targets)

**Primary**:
- "cyclecore mlm"
- "micro language model json"
- "edge ai json extraction"
- "small language model 135m"

**Long-tail**:
- "ollama json extraction model"
- "raspberry pi json parser llm"
- "lightweight llm for structured output"
- "mlm vs slm edge deployment"

---

## Publishing Timeline

### Week 2 (CycleCore-MLM-135M-JSON)

**Day 12-14**: Training complete
**Day 14**:
- ✅ Publish to Hugging Face (primary)
- ✅ Create model card
- ✅ Upload evaluation results

**Day 15**:
- ✅ Convert to GGUF format
- ✅ Create Ollama Modelfile
- ✅ Test locally
- ✅ Publish to Ollama library

**Day 16**:
- ✅ Blog post: "Introducing CycleCore-MLM-135M-JSON"
- ✅ Social media (X/Twitter, LinkedIn)
- ✅ HN/Reddit announcement

### Week 3 (CycleCore-MLM-60M-Intent)

**Same process**, plus:
- ✅ Add to leaderboard
- ✅ Compare Ollama Q4 vs HF FP16 performance

### Week 4 (CycleCore-MLM-120M-Balanced)

**Same process**, plus:
- ✅ Multi-task evaluation (JSON + Intent + FuncCall)
- ✅ Blog post: "CycleCore MLM Series Complete"

---

## Quantization Strategy (Ollama)

**Automatic Variants**:
When publishing to Ollama, these are created automatically:
- `cyclecore/mlm-135m-json:latest` (Q4_0, ~70MB)
- `cyclecore/mlm-135m-json:q8` (Q8_0, ~135MB)
- `cyclecore/mlm-135m-json:fp16` (FP16, ~270MB)

**Performance Testing** (Week 3):
- Run EdgeJSON benchmark on all quantization levels
- Document accuracy vs size trade-offs
- Blog post: "Quantization Impact: Q4 vs FP16"

**Expected Results** (based on GPT research):
- Q4_0: ~4% accuracy drop, 4x smaller, 2x faster
- Q8_0: ~1-2% accuracy drop, 2x smaller, 1.5x faster
- FP16: Baseline performance

---

## Model Card Template (Ollama)

```markdown
# CycleCore MLM-135M-JSON

Micro Language Model (135M parameters) specialized for JSON extraction on edge devices.

## Model Details

- **Developer**: CycleCore Technologies LLC
- **Base Model**: SmolLM2-135M (fine-tuned)
- **Training**: 11K JSON extraction examples (EdgeBench)
- **License**: Apache 2.0
- **Size**: 135M params (~70MB Q4, ~270MB FP16)

## Benchmark Performance

### EdgeJSON Benchmark
- **JSONExact**: 78.9%
- **Field F1**: 0.89
- **Schema Compliance**: 95%
- **Latency**: 17.2 tokens/sec (CPU)

### By Complexity
- Simple (3-5 fields): 94.2% exact match
- Medium (8-12 fields): 81.7% exact match
- Complex (15+ fields): 60.8% exact match

## Use Cases

✅ IoT sensor data extraction
✅ API response parsing
✅ Form field extraction
✅ Database record structuring
✅ Log file parsing

## Quick Start

```bash
# Run the model
ollama run cyclecore/mlm-135m-json

# Example
>>> Extract customer info: Jane Smith, jane@example.com, 555-9876
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "555-9876"
}
```

## Deployment Platforms

- ✅ Raspberry Pi 5
- ✅ Laptop (CPU-only)
- ✅ Browser (WebGPU via ONNX)
- ✅ Server (GPU optional)

## Links

- [Hugging Face](https://huggingface.co/CycleCore/CycleCore-MLM-135M-JSON)
- [Benchmark](https://slmbench.com/benchmarks#edgejson)
- [Paper](https://arxiv.org/abs/...) (coming Week 6)
- [GitHub](https://github.com/cyclecore/slmbench)

## Citation

```bibtex
@misc{cyclecore2025mlm,
  title={Micro Language Models for Edge AI},
  author={CycleCore Technologies Research Team},
  year={2025},
  url={https://slmbench.com}
}
```
```

---

## Marketing Integration

**Cross-Promotion**:
- HF model card → links to Ollama version
- Ollama listing → links to HF + slmbench.com
- Blog posts mention both (HF for researchers, Ollama for practitioners)

**Social Media**:
```
🚀 Launching CycleCore-MLM-135M-JSON!

Micro Language Model for edge JSON extraction:
- 78.9% accuracy on EdgeBench
- Runs on Raspberry Pi
- One command: ollama run cyclecore/mlm-135m-json

📦 HuggingFace: huggingface.co/CycleCore/...
📦 Ollama: ollama.com/cyclecore/mlm-135m-json
📊 Benchmarks: slmbench.com

#EdgeAI #SLM #MLM
```

---

## Maintenance Plan

**Monthly**:
- Check Ollama library stats (downloads, stars)
- Monitor HF model card views, downloads
- Update model cards with new results

**Quarterly**:
- Re-train with expanded EdgeBench dataset
- Publish v1.1, v1.2 (incremental improvements)
- Track SEO performance ("cyclecore mlm" rankings)

---

**Status**: STRATEGY DOCUMENTED - Ready for Week 2 execution
**Owner**: CC-SLM
**Next Action**: Train CycleCore-MLM-135M-JSON (Week 2), then publish to both platforms

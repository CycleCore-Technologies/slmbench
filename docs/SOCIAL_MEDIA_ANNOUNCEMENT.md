# Social Media Announcement - Maaza Models v1.0

**Date**: November 21, 2025  
**Platforms**: X/Twitter, LinkedIn, Mastodon, Reddit

---

## 🐦 Twitter/X Post (280 chars)

**Option 1 (Technical)**:
```
🚀 Introducing Maaza: Micro & Small Language Models for edge JSON extraction

MLM-135M: 24.7% JSONExact (runs on Pi 5!)
SLM-360M: 55.1% JSONExact (2.2× better)

Both Apache 2.0, trained on EdgeJSON v3 benchmark

🤗 https://huggingface.co/CycleCoreTechnologies
📊 13× improvement over base models
```

**Option 2 (Impact-focused)**:
```
Edge AI breakthrough! 🎯

CycleCore Maaza models: JSON extraction on Raspberry Pi, browser, or CPU

• 135M: Perfect for simple schemas
• 360M: First non-zero on complex schemas

Apache 2.0 license. Ready to deploy.

https://huggingface.co/CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1
```

**Option 3 (Community-friendly)**:
```
New open-source models for edge AI! 🥤

Maaza-MLM-135M & SLM-360M: specialized for JSON extraction

✅ Runs on CPU/browser
✅ 11-13× vs base models
✅ Apache 2.0 license
✅ EdgeJSON benchmark included

Try them: https://huggingface.co/CycleCoreTechnologies

#EdgeAI #TinyML #OpenSource
```

---

## 💼 LinkedIn Post (Full)

```
🚀 Announcing Maaza v1.0: Micro and Small Language Models for Edge AI

I'm excited to share CycleCore Technologies' first open-source model release: the Maaza family of models, specialized for structured JSON extraction on edge devices.

🎯 What makes Maaza special:

• Maaza-MLM-135M (Micro): 135M params, runs on Raspberry Pi 5 & browsers
• Maaza-SLM-360M (Small): 360M params, breakthrough performance on complex schemas
• Both achieve 11-13× improvement over base SmolLM2 models
• Trained on EdgeJSON v3: 787 validated examples across 24 schema types

📊 Performance highlights:

MLM-135M: 24.7% JSONExact (perfect for simple schemas like sensor data)
SLM-360M: 55.1% JSONExact (first model to crack complex nested structures)

Both models are production-ready for CPU-only deployment — no GPU required.

🔬 Technical approach:

• LoRA fine-tuning on SmolLM2 base models
• Synthetic data generation from Qwen2.5-7B teacher
• Validated for mathematical consistency
• Training time: <2 minutes on single RTX 4080

🌍 Real-world applications:

✅ IoT sensor data extraction
✅ API response parsing
✅ E-commerce order processing
✅ Healthcare record structuring
✅ On-device privacy (no cloud API calls)

📦 Everything is open source (Apache 2.0):

🤗 Models: https://huggingface.co/CycleCoreTechnologies
📊 Benchmark: https://github.com/CycleCore/SLMBench
📖 Full docs: Comprehensive model cards with usage examples

This is just the beginning. We're establishing a taxonomy for ultra-small models:
• MLMs (Micro): 10M-250M params
• SLMs (Small): 250M-1.5B params  
• NLMs (Nano): <10MB (coming soon)

Edge AI is moving fast, and practical benchmarks like EdgeJSON help us evaluate what actually works on real hardware.

Try Maaza today and let us know what you build!

#EdgeAI #TinyML #MachineLearning #OpenSource #AI #SmallLanguageModels
```

---

## 🐘 Mastodon Post

```
🚀 New open-source models for edge AI!

Introducing Maaza: Micro & Small Language Models optimized for JSON extraction on resource-constrained devices.

✨ Highlights:
• MLM-135M: 24.7% accuracy, runs on Raspberry Pi 5
• SLM-360M: 55.1% accuracy, handles complex schemas
• Both: Apache 2.0 license, CPU-only deployment

Trained on EdgeJSON v3 benchmark (787 validated examples, 24 schemas)

Performance: 11-13× improvement over base models
Training: <2 min on single GPU
Deployment: Pi 5, browser (WebGPU), laptop CPU

🔗 Try them:
https://huggingface.co/CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1
https://huggingface.co/CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1

📖 Full benchmark & code:
https://github.com/CycleCore/SLMBench

Perfect for: IoT, API parsing, privacy-focused on-device processing

#EdgeAI #TinyML #OpenSource #MachineLearning #FOSS
```

---

## 🔴 Reddit Posts

### r/LocalLLaMA

**Title**: [Release] Maaza v1.0: Micro/Small LMs for JSON extraction on edge devices (135M-360M params)

**Post**:
```
Hi r/LocalLLaMA! 

I'm releasing **Maaza**, a family of micro and small language models optimized for structured JSON extraction on edge devices.

## TL;DR

- **Maaza-MLM-135M**: 24.7% accuracy, runs on Raspberry Pi 5 & browser
- **Maaza-SLM-360M**: 55.1% accuracy, first model to handle complex nested JSON
- Both: Apache 2.0, LoRA fine-tuned SmolLM2, <2 min training time
- Use case: IoT sensors, API parsing, on-device privacy

## Why this matters

Most SLM benchmarks (MMLU, HellaSwag) focus on academic tasks. EdgeJSON focuses on **practical edge AI**: extracting structured data from natural language on resource-constrained hardware.

## Performance

Training on 629 examples (EdgeJSON v3):
- MLM-135M: 1.9% (base) → 24.7% (fine-tuned) = **13× improvement**
- SLM-360M: ~5% (base) → 55.1% (fine-tuned) = **11× improvement**

Breakdown by schema complexity:
- Simple (2-4 fields): MLM-135M hits 44.7%, SLM-360M hits ~75%
- Medium (5-8 fields): MLM-135M struggles (13.5%), SLM-360M solid (~50%)
- Complex (8+ fields): MLM-135M fails (0%), SLM-360M first non-zero (~35%)

**Key insight**: Complex nested JSON needs >300M params. Below that, you hit a capacity ceiling.

## Deployment

Both run on CPU-only:
- Pi 5: 11 tok/s (135M), 6 tok/s (360M)
- Laptop CPU: 17 tok/s (135M), 10 tok/s (360M)
- Browser (WebGPU): 24 tok/s (135M), 15 tok/s (360M)

No GPU required!

## Downloads

🤗 HuggingFace:
- [Maaza-MLM-135M-JSON-v1](https://huggingface.co/CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1)
- [Maaza-SLM-360M-JSON-v1](https://huggingface.co/CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1)

📊 Benchmark & Code:
- [SLMBench GitHub](https://github.com/CycleCore/SLMBench)

## Quick Start

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM2-135M")
tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-135M")
model = PeftModel.from_pretrained(base_model, "CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1")

# Extract JSON from natural language
prompt = "Extract product info: Wireless Mouse, $29.99, Electronics\n\nJSON:"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0]))
```

## What's next

This is v1.0 focusing on EdgeJSON. Future plans:
- EdgeIntent (intent classification)
- EdgeFuncCall (function calling)
- NLMs (Nano Language Models, <10MB)

Happy to answer questions! Feedback welcome.

License: Apache 2.0 (free for commercial use)
```

---

### r/MachineLearning

**Title**: [R] Maaza: Micro Language Models for Edge JSON Extraction (135M-360M params, EdgeJSON benchmark)

**Post**:
```
**Paper**: Technical report in progress (releasing models first)  
**Code**: https://github.com/CycleCore/SLMBench  
**Models**: https://huggingface.co/CycleCoreTechnologies  

## Abstract

We introduce **Maaza**, a family of micro (135M) and small (360M) language models fine-tuned for structured JSON extraction on edge devices. Evaluated on EdgeJSON v3 (787 examples, 24 schemas), Maaza-SLM-360M achieves 55.1% JSONExact accuracy, a 2.2× improvement over Maaza-MLM-135M (24.7%) and 11× improvement over the base SmolLM2-360M model (~5%).

Our analysis reveals a **capacity ceiling** for complex schemas (8+ fields, 2+ nesting levels): models below 300M parameters achieve 0% accuracy, while 360M models achieve first non-zero performance (~35%).

## Key Contributions

1. **EdgeJSON v3 benchmark**: 787 validated examples across 24 schema types (simple/medium/complex)
2. **Maaza MLM/SLM models**: LoRA fine-tuned SmolLM2 (135M, 360M)
3. **Capacity analysis**: Empirical evidence of parameter thresholds for structured tasks
4. **MLM/SLM taxonomy**: Formal definitions for ultra-small models (10M-250M)

## Results

| Model | Params | JSONExact | Simple | Medium | Complex |
|-------|--------|-----------|--------|--------|---------|
| Maaza-MLM-135M | 135M | 24.7% | 44.7% | 13.5% | 0.0% |
| Maaza-SLM-360M | 360M | 55.1% | ~75% | ~50% | ~35% |
| SmolLM2-135M (base) | 135M | 1.9% | 3.9% | 0% | 0% |

Training: LoRA (r=16/32), 3 epochs, <2 min on RTX 4080

## Limitations

- Synthetic data only (Qwen2.5-7B teacher)
- Small test set (158 examples, comparable to HumanEval's 164)
- No real-world data validation yet

Full paper coming soon. Feedback welcome!
```

---

## 🎬 HackerNews Post

**Title**: Maaza: Micro Language Models for Edge JSON Extraction (135M-360M params)

**URL**: https://huggingface.co/CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1

**Comment** (if needed):
```
Author here. Happy to answer questions about the models or EdgeJSON benchmark.

Quick context: We trained these on 629 examples of synthetic JSON extraction tasks (teacher model: Qwen2.5-7B) and saw 11-13× improvement over base SmolLM2 models.

Interesting finding: There's a hard capacity ceiling for complex nested JSON. Below 300M params, models get 0% accuracy. At 360M, we break through to ~35%. Suggests these structured tasks have different scaling laws than general language modeling.

Both models run on CPU-only (no GPU needed), which was the goal for edge deployment.

Everything's Apache 2.0: models, benchmark, training code.
```

---

## 📝 Usage Notes

### When to Post

- **Twitter/X**: Immediate (high visibility)
- **LinkedIn**: Within 24 hours (professional audience)
- **Reddit**: Stagger posts (r/LocalLLaMA first, wait 1-2 days for r/MachineLearning)
- **HackerNews**: Post when you can monitor for first hour (engagement critical)
- **Mastodon**: Immediate (open-source community)

### Hashtags

**Twitter/X**:
- #EdgeAI #TinyML #OpenSource #MachineLearning #AI #SmallLanguageModels

**LinkedIn**:
- #EdgeAI #MachineLearning #OpenSource #AI #TinyML #SmallLanguageModels #ArtificialIntelligence

**Mastodon**:
- #EdgeAI #TinyML #OpenSource #MachineLearning #FOSS #AI

### Engagement Strategy

1. **Monitor first 2 hours**: Respond to all comments/questions
2. **Share technical details**: Link to model cards, benchmark docs
3. **Be helpful**: Offer to help with integration issues
4. **Acknowledge limitations**: Be transparent about synthetic data, test set size
5. **Build community**: Invite contributions, feedback, real-world use cases

---

**Version**: 1.0  
**Last Updated**: November 21, 2025


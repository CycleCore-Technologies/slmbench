# Introducing CycleCore SLMBench: Practical Edge AI Evaluation

**Date**: November 19, 2025
**Author**: CycleCore Technologies Research Team
**Reading time**: 5 minutes

---

## The Problem: Academic Benchmarks Don't Cover Edge Deployment

If you've been following the rapid evolution of Small Language Models (SLMs) in 2025, you've witnessed an exciting shift: models like SmolLM2, Qwen2.5, and Llama 3.2 are bringing LLM-like capabilities to edge devices. These models can run on Raspberry Pis, laptops without GPUs, and even in web browsers.

But there's a gap.

Academic benchmarks like MMLU, HellaSwag, and GSM8K tell us how well models perform on reasoning, common sense, and math. The recently published SLM-Bench paper (August 2025) made important strides by introducing energy measurement and systematic SLM evaluation.

Yet **none of these benchmarks** thoroughly address the tasks that actually matter for production edge AI deployment:

- **JSON extraction**: Can your model reliably output valid JSON matching a schema?
- **Intent classification**: Can it route user requests to the right handler?
- **Function calling**: Can it extract parameters and invoke local APIs correctly?

These are the tasks that determine whether an SLM succeeds or fails in real-world applications - email filtering, IoT sensor management, voice assistants, edge agents.

---

## The Gap: What's Missing from Current Benchmarks

Let's be specific about what's underserved:

### 1. Structured Output Evaluation

Academic benchmarks focus on open-ended generation or multiple-choice answers. But edge applications need **structured outputs**:

- JSON that validates against schemas
- Classification labels (not explanations)
- Function calls with correctly extracted parameters

When SmolLM2-135M generates invalid JSON 60% of the time on real-world schemas, that's not reflected in MMLU scores.

### 2. Function Calling Assessment

Function calling is emerging as a key LLM capability (GPT-4, Claude, Gemini all have it). Yet there's no standardized benchmark for evaluating function calling on **edge-deployed** models.

Questions like:
- Can a 500M parameter model correctly extract function parameters?
- Does it recover gracefully from missing information?
- Can it handle multi-turn scenarios?

...remain unanswered.

### 3. Cross-Platform Validation

Most benchmarks test on NVIDIA GPUs. But edge AI runs on:
- Raspberry Pi 5 (ARM CPU, 8GB RAM)
- Mid-range laptops (x86 CPU, no discrete GPU)
- Web browsers (WebGPU acceleration)

Performance can vary dramatically across these platforms. A model that's fast on a server GPU might be unusably slow on a Pi.

### 4. Energy Measurement

The SLM-Bench paper introduced energy measurement, which is excellent. But the methodology focuses on server/Jetson hardware. We need standardized protocols for:
- Battery-powered edge devices
- Real-world deployment scenarios
- Cost-per-inference calculations

---

## The Solution: EdgeBench Suite

This is why we're launching **CycleCore Technologies SLMBench**.

Our **EdgeBench** suite consists of three practical tasks designed specifically for edge AI evaluation:

### EdgeJSON: JSON Extraction Benchmark

**What**: 1,000 test cases evaluating structured JSON output
**Complexity Levels**: Simple (3-5 fields), Medium (8-12 fields, nested), Complex (15+ fields, arrays)
**Metrics**:
- **JSONExact**: Exact match percentage
- **FieldF1**: Per-field precision/recall/F1
- **SchemaCompliance**: Valid JSON structure

**Why It Matters**: IoT sensors, API responses, database records - edge AI lives on structured data.

**Example**:
```
Input: "Extract customer info: John Doe, john@example.com, 555-1234"
Expected Output: {
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-1234"
}
```

### EdgeIntent: Intent Classification Benchmark

**What**: 1,000 test cases, 50-200 class taxonomies
**Variants**: 50-class (common intents), 100-class (e-commerce), 200-class (enterprise)
**Metrics**:
- **Top-1 Accuracy**: Correct class
- **Top-5 Accuracy**: Correct class in top 5
- **Latency**: Inferences per second (CPU)

**Why It Matters**: Voice assistants, chatbots, email routing - classification is everywhere.

**Example**:
```
Input: "Set an alarm for 7am tomorrow"
Output: "set_alarm"
```

### EdgeFuncCall: Function Calling Benchmark

**What**: 500 test cases, multi-turn scenarios
**Scenarios**: Single-turn calls, multi-turn dialogues, error recovery
**Metrics**:
- **FunctionExact**: Correct function name
- **ParamF1**: Parameter extraction F1
- **ErrorRecovery**: Graceful error handling

**Why It Matters**: Edge agents need to trigger local APIs - lights, thermostats, notifications.

**Example**:
```
Input: "Send an email to alice@example.com with subject 'Meeting Tomorrow'"
Output: {
  "function": "send_email",
  "params": {
    "to": "alice@example.com",
    "subject": "Meeting Tomorrow"
  }
}
```

---

## Our Approach: Transparent, Reproducible, Independent

EdgeBench is built on three principles:

### 1. Practical Focus

We're not replacing academic benchmarks - we complement them. MMLU tells you if a model can reason; EdgeBench tells you if it can **ship**.

### 2. Transparent Methodology

- Open-source evaluation harness (Python, available on GitHub)
- Synthetic data generation via teacher models (Qwen2.5-7B, Llama 3.2-3B)
- Full methodology documentation (no "secret sauce")
- Reproducible results (anyone can run our benchmarks)

### 3. Cross-Platform Testing

All models evaluated on:
- **Raspberry Pi 5**: ARM CPU, 8GB RAM (edge reference platform)
- **Laptop CPU**: x86, 16GB RAM, no GPU (consumer hardware)
- **Browser**: WebGPU acceleration (emerging platform)

Energy measurement coming in Month 2 (Joulescope JS110 protocol).

---

## What's Coming: CycleCore MLM Series

We're not just building benchmarks - we're training baseline models.

Meet the **CycleCore Micro Language Models (MLMs)**:

- **CycleCore-MLM-135M-JSON**: Fine-tuned for JSON extraction (launching Week 2)
- **CycleCore-MLM-60M-Intent**: Ultra-compact intent classifier (Week 3)
- **CycleCore-MLM-120M-Balanced**: Multi-task model (Week 4)

These models serve dual purposes:
1. **Baselines** for EdgeBench (validate benchmark quality)
2. **Proof-of-concept** for task-specialized SLMs (not general chat)

All trained on our NVIDIA RTX 4080, all open-sourced on Hugging Face.

---

## Week-by-Week Roadmap

**Week 1** (Current): EdgeJSON dataset + baseline evaluations
**Week 2**: CycleCore-MLM-135M-JSON training, blog post with results
**Week 3**: EdgeIntent benchmark + CycleCore-MLM-60M-Intent, **leaderboard launch**
**Week 4**: EdgeFuncCall benchmark + CycleCore-MLM-120M-Balanced, **evaluation service launch**

By Day 30, you'll be able to:
- View the public leaderboard (10+ models evaluated)
- Download EdgeBench and run it yourself (open-source)
- Request professional evaluation ($2.5K-$7.5K per model)

---

## Why "Edge Pack"?

You might be wondering about the "Edge Pack" branding.

Simple: we're positioning EdgeBench as the **practical edge AI evaluation suite**. Academic SLM-Bench covers breadth; we cover depth in the tasks that matter for production deployment.

Think of it as:
- **Academic SLM-Bench**: Comprehensive research benchmark (15 models, 9 tasks, 23 datasets)
- **EdgeBench (Edge Pack)**: Production deployment benchmark (JSON, Intent, FuncCall, cross-platform)

Complementary, not competitive.

---

## Try It Yourself

Want to run EdgeBench on your model?

**Coming Week 2**:
- GitHub repository: `github.com/cyclecore/slmbench`
- EdgeJSON dataset (1,000 test cases)
- Evaluation harness (Python script)
- Baseline results (SmolLM2, Qwen2.5)

**Already have a model?**

Join our waitlist for professional evaluation: [hello@slmbench.com](mailto:hello@slmbench.com)

---

## What Makes CycleCore SLMBench Different?

Three things:

### 1. We're Independent

We don't sell models. We don't favor specific vendors. EdgeBench is a **transparent, independent evaluation service**.

Our leaderboard placement is free and permanent - we charge for the evaluation work, not for visibility.

### 2. We're Practical

We test what matters for edge deployment:
- Can it run on a Pi?
- Is the JSON valid?
- Does it work in a browser?

Not: "Can it write poetry?" (though that's cool too).

### 3. We're Building It Live

This isn't vaporware. We're building EdgeBench, training models, and publishing results week-by-week.

Follow along:
- **Blog**: Weekly updates (this is post #1 of many)
- **Twitter/X**: [@CycleCoreTech](https://twitter.com/CycleCoreTech)
- **GitHub**: [github.com/cyclecore/slmbench](https://github.com/cyclecore/slmbench)

---

## Conclusion: Edge AI Needs Better Benchmarks

The SLM revolution is happening. Models that can run on Raspberry Pis, in browsers, on laptops without GPUs - they're here.

But academic benchmarks weren't designed for edge deployment. They don't measure JSON validity, intent classification accuracy, or cross-platform performance.

**EdgeBench does.**

We're building the practical evaluation suite that the edge AI community needs. Open-source harness, transparent methodology, independent results.

Stay tuned for Week 2, when we publish EdgeJSON baseline results and launch CycleCore-MLM-135M-JSON.

---

**Questions? Feedback?**
Email: [hello@slmbench.com](mailto:hello@slmbench.com)
Twitter/X: [@CycleCoreTech](https://twitter.com/CycleCoreTech)

---

*CycleCore Technologies SLMBench is part of CycleCore Technologies LLC, a privacy-first AI infrastructure company. Learn more at [cyclecore.ai](https://cyclecore.ai).*

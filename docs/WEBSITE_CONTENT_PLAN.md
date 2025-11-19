# CycleCore Technologies SLMBench: Website Content Plan

**Domain**: slmbench.com
**Design**: CycleCore dark mode (pure black #0a0a0a)
**Launch**: Week 1 (Days 1-2)

---

## Homepage (`/`)

### Hero Section

**Headline**: "CycleCore Technologies SLMBench"
**Subhead**: "Edge Pack - Practical Benchmarks for Production SLM Deployment"

**Value Proposition** (3-4 sentences):
> While academic benchmarks focus on general capabilities, EdgeBench evaluates what matters for production edge AI: function calling, JSON extraction, and intent classification. Test your Small Language Models on real-world tasks across Raspberry Pi, laptops, and browsers.

**CTA Buttons**:
- [View Leaderboard] (primary, links to `/leaderboard`)
- [Request Evaluation] (secondary, links to `/evaluation`)

### Three-Feature Grid

**Feature 1: EdgeBench Suite**
- Icon: 📊
- **Title**: "Practical Edge AI Tasks"
- **Description**: Evaluate SLMs on JSON extraction, intent classification, and function calling - the tasks that matter for production deployment.
- **Link**: Learn more → `/benchmarks`

**Feature 2: Public Leaderboard**
- Icon: 🏆
- **Title**: "Transparent Rankings"
- **Description**: Compare 10+ SLMs across EdgeJSON, EdgeIntent, and EdgeFuncCall. All methodology open-source and reproducible.
- **Link**: View rankings → `/leaderboard`

**Feature 3: Evaluation Service**
- Icon: 🔬
- **Title**: "Professional Evaluation"
- **Description**: Get your SLM independently evaluated on EdgeBench. Detailed reports, energy measurement, cross-platform testing.
- **Link**: Request evaluation → `/evaluation`

### Footer

- **CycleCore Technologies LLC** (logo/branding)
- Links: [About](/about) | [Blog](/blog) | [GitHub](https://github.com/cyclecore) | [Contact](mailto:hello@cyclecore.ai)
- Social: Twitter/X, LinkedIn
- © 2025 CycleCore Technologies LLC

---

## Leaderboard Page (`/leaderboard`)

### Layout

**Title**: "EdgeBench Leaderboard"
**Subtitle**: "Rankings updated as new models are evaluated. All results reproducible using our open-source harness."

### Table (Sortable)

| Rank | Model | Size | EdgeJSON | EdgeIntent | EdgeFuncCall | Avg | Platform |
|------|-------|------|----------|------------|--------------|-----|----------|
| 1 | CycleCore-MLM-135M-JSON | 135M | 78.9% | 79.2% | 68.1% | 75.4% | All |
| 2 | Qwen2.5-1.5B | 1.5B | 71.2% | 86.3% | 74.2% | 77.2% | All |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Filters**:
- Model size: All / <100M / 100M-500M / 500M-2B / >2B
- Platform: All / Raspberry Pi 5 / Laptop CPU / Browser
- Task: All / EdgeJSON / EdgeIntent / EdgeFuncCall

**Details on Click**:
- Full benchmark breakdown (simple/medium/complex)
- Latency measurements
- Model card link (Hugging Face)

### Submission CTA

**Box**: "Want to see your model on the leaderboard?"
- [Submit Model for Evaluation](/evaluation)

---

## Benchmarks Page (`/benchmarks`)

### EdgeJSON Section

**Title**: "EdgeJSON: JSON Extraction Benchmark"

**Description**:
> Structured output is critical for production edge AI. EdgeJSON evaluates models on extracting valid JSON from natural language, across 3 complexity levels (simple, medium, complex).

**Examples**:
```
Input: "Extract customer info: John Doe, john@example.com, 555-1234"
Output: {"name": "John Doe", "email": "john@example.com", "phone": "555-1234"}
```

**Metrics**:
- JSONExact: Exact match percentage
- FieldF1: Per-field precision/recall/F1
- SchemaCompliance: Valid JSON structure

**Dataset**: 1,000 test cases | [Download on GitHub](https://github.com/cyclecore/slmbench)

---

### EdgeIntent Section

**Title**: "EdgeIntent: Intent Classification Benchmark"

**Description**:
> Voice assistants and chatbots need fast, accurate intent classification. EdgeIntent tests models on 50-200 class taxonomies, simulating real-world edge deployment.

**Examples**:
```
Input: "Set an alarm for 7am tomorrow"
Output: "set_alarm"

Input: "What's the weather like in Seattle?"
Output: "weather_query"
```

**Metrics**:
- Top-1 Accuracy
- Top-5 Accuracy
- Latency (inferences/sec)

**Dataset**: 1,000 test cases (50 classes) | [Download on GitHub](https://github.com/cyclecore/slmbench)

---

### EdgeFuncCall Section

**Title**: "EdgeFuncCall: Function Calling Benchmark"

**Description**:
> Function calling is emerging as a key LLM capability, but academic benchmarks don't cover edge deployment. EdgeFuncCall tests parameter extraction, error recovery, and multi-turn scenarios.

**Examples**:
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

**Metrics**:
- FunctionExact: Correct function name
- ParamF1: Parameter extraction F1
- ErrorRecovery: Graceful error handling

**Dataset**: 500 test cases | [Download on GitHub](https://github.com/cyclecore/slmbench)

---

## Evaluation Service Page (`/evaluation`)

### Title

"Professional SLM Evaluation Service"

### Positioning

> Get your Small Language Model independently evaluated on EdgeBench. CycleCore Technologies provides rigorous, transparent testing with detailed reports - perfect for model developers, hardware vendors, and enterprises deploying edge AI.

### Pricing Tiers

**Basic - $2,500**
- EdgeJSON benchmark (1,000 test cases)
- Baseline comparisons (vs 3 reference models)
- Latency measurement (1 platform)
- PDF report + leaderboard placement

**Standard - $5,000**
- EdgeJSON + EdgeIntent benchmarks
- Baseline comparisons (vs 5 reference models)
- Latency measurement (2 platforms: laptop + Pi 5)
- PDF report + leaderboard placement
- 1-hour consultation

**Premium - $7,500**
- Full EdgeBench suite (JSON + Intent + FuncCall)
- Baseline comparisons (vs 8 reference models)
- Cross-platform testing (laptop + Pi 5 + browser)
- Energy measurement (Joulescope protocol)
- Detailed PDF report + leaderboard placement
- 2-hour consultation + custom metrics (if requested)

### What's Included

- ✅ Independent evaluation (transparent methodology)
- ✅ Reproducible results (open-source harness)
- ✅ Detailed PDF report (20-30 pages)
- ✅ Leaderboard placement (free, permanent)
- ✅ Model card review (Hugging Face)
- ✅ Consultation call (Standard/Premium)

### Request Form

- Model name / Hugging Face repo
- Contact info (name, email, company)
- Tier selection (Basic / Standard / Premium)
- Additional notes / custom requirements
- [Submit Request] button → Email to hello@slmbench.com

---

## Blog (`/blog`)

### Blog Index Page

**Title**: "SLMBench Blog - Edge AI Insights"

**Post List** (reverse chronological):
1. [Post Title] - [Date] - [2 min read]
   - Excerpt (2-3 sentences)
   - [Read More →]

**Categories** (sidebar):
- Benchmarks
- Model Releases
- Edge AI Trends
- Technical Deep Dives

---

## Blog Posts (Week 1 Content)

### Post 1: Introduction

**Title**: "Introducing CycleCore SLMBench: Practical Edge AI Evaluation"
**Date**: 2025-11-20
**Length**: 1,200-1,500 words
**URL**: `/blog/introducing-cyclecore-slmbench`

**Outline**:
1. **The Problem**: Academic benchmarks (MMLU, HellaSwag) don't cover edge deployment needs
2. **The Gap**: Missing function calling, JSON extraction, cross-platform testing
3. **The Solution**: EdgeBench suite (JSON, Intent, FuncCall)
4. **CycleCore's Approach**: Practical tasks, transparent methodology, open-source harness
5. **What's Coming**: Leaderboard, evaluation service, CycleCore MLMs
6. **Call to Action**: Try EdgeBench, submit your model

**Images**:
- EdgeBench overview diagram (3 tasks)
- Hardware platforms (Pi 5, laptop, browser)
- Example EdgeJSON task (input → output)

---

### Post 2: MLM/NLM Definitions

**Title**: "MLMs and NLMs: Defining Micro and Nano Language Models"
**Date**: 2025-11-21
**Length**: 1,500-2,000 words
**URL**: `/blog/mlms-and-nlms-definitions`

**Outline**:
1. **The Landscape**: LLMs → SLMs → MLMs → NLMs (model hierarchy)
2. **Why Size Matters**: Edge deployment, energy, cost
3. **MLM Definition**: 10M-250M params, structured task specialists
4. **NLM Definition**: <10MB, ultra-specialized, embedded devices
5. **Use Cases**: JSON extraction (MLM), intent routing (NLM)
6. **CycleCore's Role**: Training baseline MLMs, defining categories
7. **Academic Positioning**: Paper A (arXiv submission), TinyML workshop

**Images**:
- Model hierarchy chart (LLM → SLM → MLM → NLM)
- Size comparison (params vs footprint)
- Use case examples (JSON extraction, intent classification)

---

### Post 3: EdgeJSON Benchmark

**Title**: "EdgeJSON: Function Calling Benchmarks for SLMs"
**Date**: 2025-11-22
**Length**: 1,000-1,200 words
**URL**: `/blog/edgejson-benchmark`

**Outline**:
1. **The Gap**: Structured output evaluation missing from academic benchmarks
2. **Why JSON Matters**: IoT, APIs, production edge AI
3. **EdgeJSON Task**: 1,000 test cases, 3 complexity levels
4. **Metrics**: JSONExact, FieldF1, SchemaCompliance
5. **Baseline Results**: SmolLM2-135M vs Qwen2.5-0.5B (preliminary)
6. **Methodology**: Synthetic generation, validation, reproducibility
7. **Try It**: GitHub repo, evaluation harness

**Images**:
- Example schemas (simple, medium, complex)
- Baseline results table
- Evaluation code snippet

---

### Post 4: Baseline Results (Week 2)

**Title**: "EdgeJSON Benchmark Results: Baseline Models"
**Date**: 2025-11-27
**Length**: 1,500-2,000 words
**URL**: `/blog/edgejson-baseline-results`

**Outline**:
1. **Introduction**: EdgeJSON benchmark now complete
2. **Models Evaluated**: SmolLM2 (135M, 360M, 1.7B), Qwen2.5 (0.5B, 1.5B), Llama 3.2 (1B, 3B)
3. **Results**: Tables, charts, Pareto curves (accuracy vs latency)
4. **Analysis**: Which models excel? Which struggle?
5. **CycleCore-MLM-135M-JSON**: Fine-tuned model results (+36% vs base)
6. **Insights**: Task specialization beats general-purpose
7. **Next Steps**: EdgeIntent benchmark, leaderboard launch

**Images**:
- Results table (all models)
- Pareto curve (accuracy vs latency)
- Complexity breakdown (simple, medium, complex)
- CycleCore MLM comparison

---

### Post 5: Leaderboard Launch (Week 3)

**Title**: "CycleCore SLMBench Leaderboard: Compare 10+ Edge AI Models"
**Date**: 2025-12-04
**Length**: 1,000-1,200 words
**URL**: `/blog/leaderboard-launch`

**Outline**:
1. **Announcement**: Leaderboard now live at slmbench.com
2. **Current Rankings**: Top 5 models (EdgeJSON + EdgeIntent)
3. **Methodology**: Transparent, reproducible, open-source
4. **Submission Process**: How to get your model evaluated
5. **CycleCore MLMs**: 135M-JSON and 60M-Intent results
6. **What's Next**: EdgeFuncCall benchmark (Week 4)

**Images**:
- Leaderboard screenshot
- Top 3 models comparison
- Submission flow diagram

---

## About Page (`/about`)

### CycleCore Technologies SLMBench

**Mission**:
> CycleCore Technologies SLMBench provides practical, transparent benchmarks for Small Language Models deployed at the edge. Our EdgeBench suite evaluates what matters for production: function calling, structured output, and cross-platform compatibility.

**Why We Exist**:
- Academic benchmarks (MMLU, HellaSwag) focus on general capabilities
- Edge deployment needs are different: JSON extraction, intent classification, energy efficiency
- Existing SLM evaluations lack function calling, cross-platform testing
- We fill the gap with EdgeBench + independent evaluation service

**Our Approach**:
- **Practical**: Real-world tasks, not academic puzzles
- **Transparent**: Open-source harness, reproducible methodology
- **Independent**: Evaluation-as-a-Service (not paid placement)
- **Cross-platform**: Pi, laptop, browser (not just GPUs)

**Team**:
- CycleCore Technologies LLC (parent company)
- CC-SLM (SLM-Bench Edge Pack agent)
- [Links to CycleCore.ai, LinkedIn, GitHub]

**Contact**:
- Email: hello@slmbench.com
- GitHub: github.com/cyclecore/slmbench
- Twitter/X: @CycleCoreTech

---

## GitHub README

**Repository**: `cyclecore/slmbench`

### Title

```
# CycleCore SLMBench - Edge Pack

Practical benchmarks for Small Language Models (SLMs) deployed at the edge.
```

### Features

- **EdgeJSON**: JSON extraction benchmark (1,000 test cases)
- **EdgeIntent**: Intent classification (50-200 classes)
- **EdgeFuncCall**: Function calling evaluation (500 test cases)
- Evaluation harness (Python, open-source)
- Leaderboard: slmbench.com

### Quick Start

```bash
# Clone repo
git clone https://github.com/cyclecore/slmbench.git
cd slmbench

# Install dependencies
pip install -r requirements.txt

# Run EdgeJSON evaluation
python benchmarks/edge_json/scripts/eval.py \
  --model HuggingFaceTB/SmolLM2-135M \
  --dataset benchmarks/edge_json/dataset/test.jsonl
```

### Documentation

- [EdgeBench Spec](docs/EDGEBENCH_SPEC.md)
- [Evaluation Guide](docs/EVALUATION_GUIDE.md)
- [Paper A](papers/paper_a_mlm_edgebench/)

### Citation

```bibtex
@misc{cyclecore2025slmbench,
  title={Micro Language Models and EdgeBench: A Benchmark Suite for Structured Tasks on Resource-Constrained Devices},
  author={CycleCore Technologies Research Team},
  year={2025},
  eprint={...},
  archivePrefix={arXiv}
}
```

---

## SEO Keywords

**Primary**:
- Small Language Models
- SLM benchmarks
- Edge AI evaluation
- Micro Language Models (MLM)
- Nano Language Models (NLM)

**Secondary**:
- JSON extraction benchmark
- Intent classification SLM
- Function calling edge AI
- Raspberry Pi SLM
- Browser LLM deployment

**Long-tail**:
- "Best small language model for edge deployment"
- "JSON extraction benchmark for SLMs"
- "Evaluate SLM on Raspberry Pi"
- "CycleCore MLM series"

---

## Content Calendar (Weeks 1-4)

| Week | Day | Content | Status |
|------|-----|---------|--------|
| 1 | Mon | Homepage + design system | 📝 Planned |
| 1 | Tue | Post 1: Introduction | 📝 Planned |
| 1 | Wed | Post 2: MLM/NLM definitions | 📝 Planned |
| 1 | Thu | Post 3: EdgeJSON benchmark | 📝 Planned |
| 1 | Fri | Social media (X, LinkedIn) | 📝 Planned |
| 2 | Mon | EdgeJSON dataset release | 📝 Planned |
| 2 | Thu | Post 4: Baseline results | 📝 Planned |
| 2 | Fri | HN/Reddit submission | 📝 Planned |
| 3 | Mon | EdgeIntent benchmark | 📝 Planned |
| 3 | Thu | Leaderboard launch | 📝 Planned |
| 3 | Thu | Post 5: Leaderboard announcement | 📝 Planned |
| 3 | Fri | HN/Reddit submission #2 | 📝 Planned |
| 4 | Mon | EdgeFuncCall benchmark | 📝 Planned |
| 4 | Thu | Evaluation service launch | 📝 Planned |
| 4 | Fri | Outreach to SLM developers | 📝 Planned |

---

**Status**: CONTENT PLAN COMPLETE - Ready for execution
**Design**: Borrow from cyclecore.ai dark mode
**Hosting**: TBD (user setup required)

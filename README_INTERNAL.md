# SLMBench

**Product Name**: SLM-Bench Edge Pack
**Domain**: slmbench.com (to be acquired)
**Owner**: CycleCore Technologies LLC
**Agent**: CC-SLM (Claude Code - SLM Benchmark)
**Territory Status**: Puerto Rico Model (Lexopoly Federation)
**Mission**: Edge AI evaluation service + benchmarks for Small Language Models

---

## Overview

SLM-Bench Edge Pack is CycleCore Technologies' edge AI evaluation initiative that provides:

1. **Benchmark Suite**: Practical edge AI tasks (JSON extraction, intent classification, function calling)
2. **Baseline Models**: CycleCore-certified fine-tuned SLMs (SmolLM2, Qwen2.5)
3. **Evaluation Service**: Independent testing and validation for SLM developers
4. **Thought Leadership**: Technical content establishing CycleCore as edge AI authority

**Target Market**: SLM developers, hardware vendors, enterprises deploying edge AI
**Value Proposition**: Rigorous, transparent edge AI evaluation with energy measurement
**Business Model**: Evaluation-as-a-Service ($2.5K-$7.5K per model) + enterprise consulting

---

## The Opportunity

**Market Gap (November 2025):**
- Academic benchmarks (SLM-Bench, MMLU, HellaSwag) don't cover function calling
- No standardized energy measurement protocols for edge deployment
- Missing cross-platform validation (Raspberry Pi, laptop, browser)
- Enterprises need independent validation for SLM procurement

**CycleCore Differentiation:**
- Practical task focus (not academic)
- Standardized energy measurement (Joulescope hardware protocol)
- Cross-hardware testing (Pi 5, x86 laptop, WebGPU browser)
- Transparent methodology (publish all results, charge for service not placement)

---

## Three-Stream Mission

**Stream 1: Research + Thought Leadership**
- Publish SLM ecosystem insights
- Technical blog posts on edge deployment
- Open-source benchmark suite (credibility building)
- Academic paper submissions (workshops/demos)

**Stream 2: Build Benchmark Infrastructure**
- Edge Pack tasks: JSON extraction, intent classification, function calling
- Hardware test platforms: Raspberry Pi 5, laptop, browser (WebGPU)
- Energy measurement protocol (Joulescope JS110)
- Baseline models: Fine-tuned SmolLM2-1.7B, Qwen2.5-1.5B

**Stream 3: Marketing + Community**
- SLM rankings leaderboard (public, free access)
- Developer documentation
- Case studies and evaluation reports
- Social media presence (technical credibility)

---

## Technical Approach

### Benchmark Suite (Edge Pack v1.0)

**Task 1: JSON Extraction**
- Dataset: 1,000+ real-world schemas (diverse complexity)
- Metrics: Schema compliance, field accuracy, error handling
- Baseline: SmolLM2-1.7B, Qwen2.5-1.5B

**Task 2: Intent Classification**
- Dataset: 50-200 class taxonomy (enterprise scale)
- Variants: Few-shot, zero-shot
- Metrics: Accuracy, latency, energy per inference

**Task 3: Function Calling**
- Dataset: Multi-turn tool use scenarios
- Metrics: Parameter extraction accuracy, error recovery
- Baseline: Llama 3.2 3B, custom distilled model

### Hardware Platforms

1. **Raspberry Pi 5 (8GB)** - Edge reference platform
2. **Mid-range laptop (x86, 16GB RAM)** - Consumer hardware
3. **Browser (WebGPU on Chrome)** - Emerging platform

### Energy Measurement

- Hardware: Joulescope JS110 power meter
- Protocol: Standardized test runs, controlled environment
- Metrics: Joules per task, tokens per joule, cost per 1M tokens

---

## Technology Stack

- **Benchmarking**: Python (HuggingFace Transformers, ONNX Runtime)
- **Browser Models**: WebLLM, Transformers.js (WebGPU acceleration)
- **Evaluation Platform**: TBD (FastAPI + PostgreSQL + Redis, or static site)
- **Energy Monitoring**: Joulescope API (Python SDK)

---

## Code Sharing Framework

Per Constitutional Amendment 001 Section 5.2 and DOCK-025 Section 4.3:

**SLM-Bench can freely copy code from Lexopoly products**:
- Infrastructure setup (deployment, monitoring)
- Data pipelines (if applicable)
- UI components (if building evaluation platform)

**Process**: Direct copy + document source in commit message (no pre-approval required).

**See**: `/home/rain/federation/ops/spinup/CC_SLM_SPINUP_PLAN.md` for details.

---

## Development

### Prerequisites
- Python 3.10+
- Node.js 18+ (for browser testing)
- Docker (for reproducible environments)
- Joulescope JS110 (for energy measurement)

### Setup
```bash
cd /home/rain/SLMBench
# TBD: Python venv setup, dependency installation
```

---

## Governance

**Territory Status**: Puerto Rico Model
**Oversight**: CC-FCO (Federation Compliance Officer)
**Review Gates**: Day 7, 14, 30, then quarterly
**Commercial Boundary**: Pre-approved (complementary to MCPBodega, Lexopoly products)

**Governance Documents**:
- Constitutional Amendment 001: Multi-LLC Membership Framework
- DOCK-025: Multi-LLC Coordination Protocol
- CC-SLM Spinup Plan: `/home/rain/federation/ops/spinup/CC_SLM_SPINUP_PLAN.md`

---

## Timeline

**Phase 1: Research + Planning** (Weeks 1-2):
- Review GPT chat brainstorming
- Validate ecosystem research findings
- Define benchmark task specifications
- Acquire hardware (Joulescope, Raspberry Pi 5 if needed)

**Phase 2: Benchmark MVP** (Weeks 3-6):
- Build JSON extraction task + evaluation scripts
- Establish energy measurement protocol
- Fine-tune SmolLM2-1.7B baseline model
- Publish initial benchmark results (open, free)

**Phase 3: Service Launch** (Weeks 7-12):
- Build evaluation service workflow
- Create pricing + service offering
- Marketing materials (blog posts, case studies)
- First paid evaluation engagement

**Revenue Target**: $50K-$100K Year 1 (10-20 evaluations)

---

## Status

**Current Phase**: Pre-spinup (directory structure created)
**Next Step**: CC-SLM agent spinup via Federation Spinup Wizard
**Research Assets**:
- GPT chat brainstorming: `research/GPT_CHAT_SLM_BRAINSTORM.md` (to be added)
- Ecosystem research: `research/ECOSYSTEM_RESEARCH_20251119.md`

**Estimated Start**: 2025-11-19

---

## License

**Ownership**: CycleCore Technologies LLC (100%)
**Code Sharing**: Lexopoly LLC can copy code (per federation code sharing agreement)
**External**: Proprietary (benchmark suite may be open-source for credibility)

---

**Federation Integration**: ✅ Ready for Federation Spinup Wizard
**Agent**: CC-SLM (Territory: CycleCore Technologies LLC)

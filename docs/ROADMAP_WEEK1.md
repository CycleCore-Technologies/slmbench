# Week 1 Tactical Roadmap: Foundation + Content

**Timeline**: Days 0-7
**Agent**: CC-SLM
**Goal**: Launch slmbench.com with content + prepare 4080 training environment

---

## Day 0: Project Setup (Today)

### Morning (2-3 hours)

**✅ Documentation** (COMPLETE):
- [x] Strategic plan saved: `STRATEGIC_PLAN_30DAY_MVP.md`
- [x] Week 1 roadmap: `ROADMAP_WEEK1.md` (this document)
- [ ] Model training plan: `MODEL_TRAINING_PLAN.md`
- [ ] Paper A outline: `PAPER_A_OUTLINE.md`
- [ ] Website content plan: `WEBSITE_CONTENT_PLAN.md`

**Project Structure**:
```bash
# Create directory structure
mkdir -p benchmarks/{edge_json,edge_intent,edge_funccall}/{dataset,scripts,results}
mkdir -p models/{mlm_135m_json,mlm_60m_intent,mlm_120m_balanced}
mkdir -p papers/paper_a_mlm_slm-bench
mkdir -p website/{content,static/{css,js,images},templates}
```

**Git**:
```bash
# Commit research updates
git add research/GPT_CHAT_SLM_BRAINSTORM.md
git commit -m "docs: Add full GPT chat transcript (MLM/NLM brainstorming)"

# Commit documentation
git add docs/
git commit -m "docs: Add strategic plan and Week 1 roadmap"
```

### Afternoon (2-3 hours)

**Research Synthesis**:
- [ ] Read `research/ECOSYSTEM_RESEARCH_20251119.md` in full (30 min)
- [ ] Extract key insights for Paper A (30 min):
  - Academic SLM-Bench gaps
  - Competitive landscape (SmolLM, Qwen, Llama 3.2)
  - Market validation (recent publications)
- [ ] Document findings in `papers/paper_a_mlm_slm-bench/RESEARCH_NOTES.md`

**Paper A Outline**:
- [ ] Create section structure (1 hour)
- [ ] Identify figures/tables needed (30 min)
- [ ] List related work to cite (30 min)

**Deliverable**: Research synthesized, Paper A scaffolding ready

---

## Day 1: Domain + Website Foundation

### Domain Setup (External - User Task)

**DNS Configuration**:
- [ ] Point slmbench.com to hosting provider
- [ ] Configure SSL certificate
- [ ] Test HTTPS access

### Website Foundation (4-5 hours)

**Homepage** (`website/templates/index.html`):
- [ ] Header: "CycleCore Technologies SLMBench - Edge Pack"
- [ ] Hero section: Value proposition
- [ ] 3-feature grid: EdgeBench tasks, Leaderboard, Evaluation service
- [ ] CTA: "View Leaderboard" (coming soon) + "Request Evaluation"
- [ ] Footer: CycleCore branding, social links

**Design System** (borrow from cyclecore.ai):
- [ ] Copy dark mode CSS (pure black #0a0a0a)
- [ ] Adapt typography, spacing, components
- [ ] Create `website/static/css/cyclecore-slm.css`

**Blog Setup**:
- [ ] Create `website/content/` structure
- [ ] Markdown rendering (simple script or static generator)
- [ ] Blog index page (`/blog`)
- [ ] Post template

**Deploy**:
- [ ] Test locally (Python `http.server` or similar)
- [ ] Deploy to hosting
- [ ] Verify slmbench.com loads

**Deliverable**: slmbench.com live with homepage (no blog posts yet)

---

## Day 2: Content Creation (Blog Posts 1-2)

### Post 1: Introduction (3-4 hours)

**Title**: "Introducing CycleCore SLMBench: Practical Edge AI Evaluation"

**Outline**:
1. **The Problem**: Academic benchmarks don't cover function calling, energy, cross-platform
2. **The Solution**: EdgeBench suite (JSON, Intent, FuncCall)
3. **The Difference**: Practical vs research focus
4. **What's Coming**: Leaderboard, evaluation service, CycleCore MLMs

**Content**:
- 1,200-1,500 words
- 2-3 diagrams (benchmark overview, hardware targets)
- Code snippets (example EdgeJSON task)

**Deliverable**: `website/content/01-introducing-cyclecore-slmbench.md`

### Post 2: Category Definitions (3-4 hours)

**Title**: "MLMs and NLMs: Defining Micro and Nano Language Models"

**Outline**:
1. **The Landscape**: LLMs → SLMs → MLMs → NLMs
2. **MLM Definition**: 10M-250M params, edge-focused, structured tasks
3. **NLM Definition**: <10MB, ultra-specialized, embedded devices
4. **Why It Matters**: Practical deployment, energy efficiency, cost
5. **CycleCore's Role**: Training baseline MLMs, defining categories

**Content**:
- 1,500-2,000 words
- Size comparison chart (LLM vs SLM vs MLM vs NLM)
- Use case examples

**Deliverable**: `website/content/02-mlms-and-nlms-definitions.md`

### Publish

- [ ] Render posts to HTML
- [ ] Add to blog index
- [ ] Deploy to slmbench.com
- [ ] Announce on X/Twitter, LinkedIn

**Deliverable**: 2 blog posts live on slmbench.com

---

## Day 3: Content Creation (Blog Post 3) + Paper A Draft

### Post 3: EdgeJSON (3 hours)

**Title**: "EdgeJSON: Function Calling Benchmarks for SLMs"

**Outline**:
1. **The Gap**: Academic benchmarks lack structured output evaluation
2. **EdgeJSON Task**: 1,000 test cases, schema complexity levels
3. **Metrics**: JSONExact, FieldF1, SchemaCompliance
4. **Baseline Results**: SmolLM2-135M, Qwen2.5-0.5B (preliminary)
5. **Methodology**: Synthetic generation via teacher models

**Content**:
- 1,000-1,200 words
- Example JSON schemas (simple, medium, complex)
- Evaluation code snippet

**Deliverable**: `website/content/03-edgejson-benchmark.md`

### Paper A: Introduction Section (2 hours)

- [ ] Write Introduction (500-800 words)
- [ ] Problem statement: Gaps in SLM evaluation
- [ ] Contributions: MLM/NLM definitions, EdgeBench, baselines
- [ ] Paper structure overview

**Deliverable**: `papers/paper_a_mlm_slm-bench/sections/01-introduction.md`

---

## Day 4: 4080 Training Environment Setup

### Python Environment (2 hours)

```bash
# Create virtual environment
cd /home/rain/SLMBench
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers datasets accelerate peft bitsandbytes
pip install wandb tensorboard
pip install pandas numpy scikit-learn

# Save requirements
pip freeze > requirements.txt
```

### Model Downloads (2-3 hours)

**Teacher Models**:
- [ ] Download Qwen2.5-7B-Instruct (Hugging Face)
- [ ] Download Llama 3.2-3B-Instruct (Hugging Face)
- [ ] Test inference on 4080 (verify CUDA works)

**Base Models** (for fine-tuning):
- [ ] Download SmolLM2-135M
- [ ] Download SmolLM2-360M
- [ ] Test loading, basic generation

### Training Scripts (2 hours)

- [ ] Create `models/mlm_135m_json/train.py` (skeleton)
- [ ] LoRA/QLoRA configuration
- [ ] Logging (WandB or TensorBoard)
- [ ] Checkpoint saving

**Deliverable**: 4080 ready for training, models downloaded

---

## Day 5: EdgeJSON Dataset Generation

### Synthetic Data Pipeline (4-5 hours)

**Script**: `benchmarks/edge_json/scripts/generate_dataset.py`

**Approach**:
1. Define schema templates (simple, medium, complex)
2. Use Qwen2.5-7B to generate:
   - Input prompts ("Extract customer info from...")
   - Expected JSON outputs
3. Validation: Ensure schema compliance
4. Dataset split: 800 train, 100 val, 100 test

**Schemas**:
- **Simple**: 3-5 fields, flat structure (e.g., {"name": str, "email": str})
- **Medium**: 8-12 fields, nested (e.g., customer + order details)
- **Complex**: 15+ fields, arrays, deep nesting (e.g., multi-item order)

**Output**:
- `benchmarks/edge_json/dataset/train.jsonl`
- `benchmarks/edge_json/dataset/val.jsonl`
- `benchmarks/edge_json/dataset/test.jsonl`

### Evaluation Harness (2 hours)

**Script**: `benchmarks/edge_json/scripts/eval.py`

**Metrics**:
- JSONExact: Exact match (1/0)
- FieldF1: Per-field precision/recall/F1
- SchemaCompliance: Valid JSON structure

**Deliverable**: EdgeJSON dataset (1,000 samples) + evaluation script

---

## Day 6: Baseline Evaluations

### Run Baseline Models (3-4 hours)

**Models to evaluate**:
- SmolLM2-135M
- SmolLM2-360M
- Qwen2.5-0.5B
- Qwen2.5-1.5B

**Process**:
```bash
cd benchmarks/edge_json
python scripts/eval.py --model HuggingFaceTB/SmolLM2-135M --dataset dataset/test.jsonl
python scripts/eval.py --model Qwen/Qwen2.5-0.5B --dataset dataset/test.jsonl
# ... repeat for all models
```

**Results**:
- Save to `benchmarks/edge_json/results/baseline_results.json`
- Generate comparison table (markdown)

### Analysis (1 hour)

- [ ] Identify which models excel at which schema complexity
- [ ] Latency measurements (tokens/sec)
- [ ] Note failure modes (common JSON errors)

**Deliverable**: Baseline results for EdgeJSON

---

## Day 7: Week 1 Review + Week 2 Planning

### Morning: Documentation Update (2 hours)

**Update `docs/WEEK1_SUMMARY.md`**:
- [ ] Completed items checklist
- [ ] Blockers encountered (if any)
- [ ] Key learnings
- [ ] Adjustments for Week 2

**Website Analytics**:
- [ ] Traffic to slmbench.com (if any)
- [ ] Blog post engagement
- [ ] Social media reactions

### Afternoon: Week 2 Prep (2 hours)

**CycleCore-MLM-135M-JSON Training**:
- [ ] Review baseline results
- [ ] Decide: Fine-tune SmolLM2-135M OR distill from Qwen2.5-7B
- [ ] Prepare training config
- [ ] Estimate training time (4080 utilization)

**EdgeIntent Planning**:
- [ ] Define intent classification taxonomy (50-200 classes)
- [ ] Identify data sources (synthetic vs real-world)
- [ ] Sketch evaluation metrics

**Paper A Progress**:
- [ ] Complete Related Work section (draft)
- [ ] Start MLM Specification section

**Deliverable**: Week 1 complete, Week 2 roadmap refined

---

## Week 1 Success Criteria

**Website**:
- [x] slmbench.com domain live
- [ ] Homepage deployed (CycleCore dark mode)
- [ ] 3 blog posts published
- [ ] Social media announcement (X/Twitter, LinkedIn)

**Benchmark**:
- [ ] EdgeJSON dataset (1,000 samples)
- [ ] Evaluation harness working
- [ ] Baseline results (4 models)

**4080 Environment**:
- [ ] Python venv + dependencies
- [ ] Teacher models downloaded (Qwen2.5-7B, Llama 3.2-3B)
- [ ] Training scripts scaffolded

**Documentation**:
- [x] Strategic plan saved
- [x] Week 1 roadmap (this document)
- [ ] Paper A outline + Introduction section
- [ ] Week 1 summary + learnings

**Academic**:
- [ ] Paper A: Introduction + Related Work (draft)
- [ ] Research notes from ecosystem study

---

## Blockers / Dependencies

**External (User):**
- [ ] slmbench.com DNS configuration
- [ ] CycleCore.ai dark mode CSS access (or recreate from scratch)
- [ ] Hugging Face account for model hosting

**Internal:**
- [ ] 4080 availability (confirm no conflicts with other projects)
- [ ] Disk space for model downloads (~50-100GB)

---

## Next Week Preview: Week 2

**Focus**: Train first CycleCore model + EdgeIntent benchmark

**Key Milestones**:
- CycleCore-MLM-135M-JSON training (24-48 hours on 4080)
- EdgeIntent dataset generation (50-200 classes)
- Blog Post 4: EdgeJSON baseline results
- Leaderboard v0.1 (static JSON → HTML table)

---

**Status**: WEEK 1 IN PROGRESS
**Last Updated**: 2025-11-19 (Day 0)

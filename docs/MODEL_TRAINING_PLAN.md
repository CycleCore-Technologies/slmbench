# CycleCore MLM Series: Training Plan

**Hardware**: NVIDIA RTX 4080 (16GB VRAM)
**Timeline**: Weeks 1-4 (MVP phase)
**Goal**: Train 3 baseline models while validating EdgeBench tasks

---

## Training Strategy Overview

### Feedback Loop Approach

```
EdgeBench Task → Synthetic Data → Train MLM → Evaluate → Refine Task
```

**Why This Works**:
- Benchmark development generates training data automatically
- Training validates benchmark quality (too easy? too hard?)
- Models serve as baselines AND proof-of-concept
- 4080 stays productive during benchmark design phases

### Teacher-Student Distillation

**Teacher Models** (7B-3B params):
- Qwen2.5-7B-Instruct: Excellent JSON, multilingual
- Llama 3.2-3B-Instruct: Strong reasoning, function calling

**Student Models** (60M-250M params):
- CycleCore-MLM-{size}-{specialty}
- Distilled via:
  1. Generate synthetic data with teacher
  2. Train student to match teacher outputs
  3. Evaluate on EdgeBench

---

## Model 1: CycleCore-MLM-135M-JSON

**Timeline**: Week 2 (Days 8-14)
**Training Time**: 24-48 hours on 4080
**Goal**: JSON extraction specialist

### Specifications

**Architecture**:
- Base: SmolLM2-135M (135M params)
- Approach: Fine-tuning (easier than distillation from scratch)
- Context length: 2048 tokens
- Precision: BF16 (4080 supports it)

**Dataset**:
- Source: EdgeJSON benchmark (1,000 samples)
- Augmentation: 10K additional synthetic samples via Qwen2.5-7B
- Total: ~11K train, 1K val
- Format: Instruction-following (prompt → JSON output)

### Training Configuration

```python
# LoRA fine-tuning (memory efficient)
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,                    # LoRA rank
    lora_alpha=32,           # Scaling factor
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

training_args = TrainingArguments(
    output_dir="./models/mlm_135m_json/checkpoints",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    gradient_accumulation_steps=4,   # Effective batch size: 32
    learning_rate=2e-4,
    warmup_steps=100,
    logging_steps=50,
    save_steps=500,
    eval_steps=500,
    bf16=True,                        # Use BF16 on 4080
    optim="adamw_torch",
    max_grad_norm=1.0,
)
```

**Estimated VRAM Usage**: ~8-10GB (LoRA + BF16 + batch size 8)
**Estimated Time**: 24-36 hours (3 epochs, ~11K samples)

### Evaluation

**Metrics**:
- EdgeJSON benchmark: JSONExact, FieldF1
- Comparison: vs SmolLM2-135M base, vs Qwen2.5-0.5B
- Latency: Tokens/sec on CPU (edge deployment simulation)

**Success Criteria**:
- JSONExact > 70% (vs SmolLM2-135M base ~40-50%)
- FieldF1 > 0.85
- Latency: 15-25 tokens/sec on CPU

### Deliverables

- [ ] Fine-tuned model weights
- [ ] Hugging Face repo: `CycleCore/CycleCore-MLM-135M-JSON`
- [ ] Model card (architecture, training, benchmarks)
- [ ] EdgeJSON results (add to leaderboard)

---

## Model 2: CycleCore-MLM-60M-Intent

**Timeline**: Week 2-3 (Days 12-18)
**Training Time**: 18-24 hours on 4080
**Goal**: Ultra-compact intent classification router

### Specifications

**Architecture**:
- Base: **Distill from Llama 3.2-3B** (not fine-tune existing)
- Target size: 60M params (custom architecture)
- Layers: 12, Hidden: 512, Heads: 8
- Context: 1024 tokens (shorter than MLM-135M)

**Dataset**:
- Source: EdgeIntent benchmark (1,000 samples, 50-200 classes)
- Augmentation: 20K synthetic samples via Llama 3.2-3B
- Total: ~21K train, 2K val
- Format: Text → intent class (classification)

### Distillation Approach

**Why Distill (Not Fine-Tune)**:
- No existing 60M model fits our needs
- Llama 3.2-3B is strong at intent classification
- Learn to build custom architectures

**Distillation Loss**:
```python
# Combined loss: KL divergence + cross-entropy
loss = 0.5 * kl_div(student_logits, teacher_logits) + \
       0.5 * cross_entropy(student_logits, labels)
```

### Training Configuration

```python
# Full model training (not LoRA)
training_args = TrainingArguments(
    output_dir="./models/mlm_60m_intent/checkpoints",
    num_train_epochs=5,
    per_device_train_batch_size=16,
    gradient_accumulation_steps=2,    # Effective batch size: 32
    learning_rate=5e-4,               # Higher LR for from-scratch
    warmup_steps=500,
    logging_steps=100,
    save_steps=1000,
    eval_steps=1000,
    bf16=True,
    optim="adamw_torch",
)
```

**Estimated VRAM Usage**: ~6-8GB (smaller model)
**Estimated Time**: 18-24 hours (5 epochs, ~21K samples)

### Evaluation

**Metrics**:
- EdgeIntent benchmark: Top-1 accuracy, Top-5 accuracy
- Latency: Inferences/sec on CPU
- Size: Model footprint (MB)

**Success Criteria**:
- Top-1 accuracy > 85% (50 classes), > 75% (200 classes)
- Latency: 50+ inferences/sec on CPU
- Size: <120MB unquantized

### Deliverables

- [ ] Distilled model weights
- [ ] Hugging Face repo: `CycleCore/CycleCore-MLM-60M-Intent`
- [ ] Model card + distillation methodology
- [ ] EdgeIntent results (add to leaderboard)

---

## Model 3: CycleCore-MLM-120M-Balanced

**Timeline**: Week 3-4 (Days 19-28)
**Training Time**: 36-48 hours on 4080
**Goal**: Multi-task model (JSON + Intent)

### Specifications

**Architecture**:
- Base: Qwen2.5-1.5B → distill down to 120M
- Balanced for both structured output and classification
- Layers: 18, Hidden: 768, Heads: 12
- Context: 2048 tokens

**Dataset**:
- EdgeJSON: 11K samples
- EdgeIntent: 21K samples
- EdgeFuncCall: 5K samples (preliminary)
- Total: ~37K mixed tasks
- Format: Multi-task instruction-following

### Multi-Task Training

**Task Mixing**:
- 40% JSON extraction
- 40% Intent classification
- 20% Function calling

**Loss Weighting**:
```python
# Weighted loss based on task type
if task_type == "json":
    loss_weight = 1.0
elif task_type == "intent":
    loss_weight = 1.0
elif task_type == "funccall":
    loss_weight = 1.5  # Harder task, upweight
```

### Training Configuration

```python
training_args = TrainingArguments(
    output_dir="./models/mlm_120m_balanced/checkpoints",
    num_train_epochs=4,
    per_device_train_batch_size=12,
    gradient_accumulation_steps=3,    # Effective batch size: 36
    learning_rate=3e-4,
    warmup_steps=1000,
    logging_steps=100,
    save_steps=1500,
    eval_steps=1500,
    bf16=True,
    optim="adamw_8bit",               # Memory optimization
)
```

**Estimated VRAM Usage**: ~10-12GB
**Estimated Time**: 36-48 hours (4 epochs, ~37K samples)

### Evaluation

**Metrics**:
- EdgeJSON: JSONExact, FieldF1
- EdgeIntent: Top-1/Top-5 accuracy
- EdgeFuncCall: Parameter extraction F1
- Aggregate: Weighted average across tasks

**Success Criteria**:
- JSONExact > 75%
- Intent Top-1 > 88%
- FuncCall F1 > 0.80
- Competitive with Qwen2.5-1.5B on EdgeBench

### Deliverables

- [ ] Multi-task distilled model
- [ ] Hugging Face repo: `CycleCore/CycleCore-MLM-120M-Balanced`
- [ ] Model card + multi-task methodology
- [ ] Full EdgeBench results (all 3 tasks)

---

## Post-MVP: CycleCore-NLM-5M-Filter

**Timeline**: Month 2 (after MVP launch)
**Training Time**: 12-18 hours on 4080
**Goal**: Proof-of-concept <10MB model

### Specifications

**Architecture**:
- Distill from CycleCore-MLM-60M-Intent
- Target: 5M params
- Layers: 6, Hidden: 256, Heads: 4
- Context: 512 tokens

**Specialty**:
- Spam detection (binary classification)
- PII filtering (named entity detection)
- Toxicity detection

**Quantization**:
- INT8 quantization → <10MB footprint
- ONNX export for cross-platform deployment

**Success Criteria**:
- Size: <10MB (INT8)
- Accuracy: >92% on spam detection
- Latency: 100+ inferences/sec on Raspberry Pi 5

---

## 4080 Utilization Schedule

### Week 1 (Setup)
- **Mon-Tue**: Download models, test inference
- **Wed-Fri**: Idle or other projects
- **Weekend**: Dataset generation (CPU-bound, 4080 idles)

### Week 2 (MLM-135M-JSON)
- **Mon**: Start training (24-48 hour run)
- **Tue-Wed**: Training continues (monitor, no intervention)
- **Thu**: Training completes, evaluate
- **Fri**: Publish to Hugging Face

### Week 3 (MLM-60M-Intent)
- **Mon**: Start distillation (18-24 hour run)
- **Tue**: Training continues
- **Wed**: Training completes, evaluate
- **Thu-Fri**: EdgeIntent benchmark work

### Week 4 (MLM-120M-Balanced)
- **Mon**: Start multi-task training (36-48 hour run)
- **Tue-Wed**: Training continues
- **Thu**: Training completes, evaluate
- **Fri**: Full EdgeBench evaluation, leaderboard update

**Idle Time**: ~40-50% (available for other projects like Orchestra, ComplianceLogger)

---

## Training Infrastructure

### File Structure

```
models/
├── mlm_135m_json/
│   ├── train.py              # Training script
│   ├── config.yaml           # Hyperparameters
│   ├── checkpoints/          # Model checkpoints
│   ├── logs/                 # TensorBoard/WandB logs
│   └── README.md             # Training notes
├── mlm_60m_intent/
│   ├── distill.py            # Distillation script
│   ├── architecture.py       # Custom 60M architecture
│   └── ...
└── mlm_120m_balanced/
    ├── multitask_train.py
    └── ...
```

### Logging & Monitoring

**WandB** (Weights & Biases):
- Real-time loss curves
- GPU utilization tracking
- Hyperparameter logging
- Model checkpointing

**TensorBoard** (Backup):
- Local logging if WandB unavailable
- Validation metrics visualization

### Checkpointing Strategy

- Save every 500 steps
- Keep last 3 checkpoints
- Save best model (by validation loss)
- Upload final model to Hugging Face

---

## Model Publishing

### Hugging Face Repos

**Naming Convention**:
```
CycleCore/CycleCore-MLM-135M-JSON
CycleCore/CycleCore-MLM-60M-Intent
CycleCore/CycleCore-MLM-120M-Balanced
```

**Model Card Template**:
```markdown
# CycleCore-MLM-135M-JSON

## Model Description
Fine-tuned SmolLM2-135M specialized for JSON extraction tasks.

## Training
- Base: HuggingFaceTB/SmolLM2-135M
- Method: LoRA fine-tuning (r=16)
- Dataset: 11K synthetic JSON extraction samples
- Hardware: NVIDIA RTX 4080
- Training time: 36 hours

## Benchmarks
| Task | JSONExact | FieldF1 |
|------|-----------|---------|
| EdgeJSON (simple) | 92.3% | 0.94 |
| EdgeJSON (medium) | 78.5% | 0.87 |
| EdgeJSON (complex) | 61.2% | 0.78 |

## Usage
[Inference code examples]

## Citation
[Link to Paper A when published]
```

### License

**Model Weights**: Apache 2.0 (open source, commercial use OK)
**Training Code**: MIT License
**EdgeBench Data**: CC BY 4.0 (attribution required)

---

## Risk Mitigation

### Training Failures

**Risk**: Training doesn't converge
**Mitigation**:
- Start with smaller learning rate (1e-4 vs 2e-4)
- Increase warmup steps
- Monitor validation loss closely

### VRAM Overflow

**Risk**: 4080 runs out of memory
**Mitigation**:
- Reduce batch size (8 → 4)
- Use gradient checkpointing
- Switch to 8-bit optimizers (bitsandbytes)

### 4080 Conflicts

**Risk**: Other projects need 4080
**Mitigation**:
- Training runs are pausable (save checkpoint, resume later)
- Coordinate with Orchestra/ComplianceLogger via GPU auto-unload
- Run training overnight/weekends when 4080 less used

---

## Success Metrics

**By Day 30**:
- ✅ 3 CycleCore MLMs trained and published
- ✅ All 3 evaluated on EdgeBench
- ✅ Added to slmbench.com leaderboard
- ✅ 4080 utilization: 50-60% (training weeks)

**Long-term** (Month 2-3):
- Train NLM series (<10MB models)
- Quantize MLMs (INT8, INT4)
- Deploy to edge hardware (Pi 5, browser)

---

**Status**: READY FOR EXECUTION
**Dependencies**: EdgeBench datasets, 4080 access, Hugging Face account
**Owner**: CC-SLM

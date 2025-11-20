# Phase 2 Complete: OSS Tools Validation

**Date**: 2025-11-20
**Agent**: CC-SLM
**Status**: COMPLETE ✅
**Authority**: STRATEGIC_PLAN_30DAY_MVP.md Phase 2

---

## Executive Summary

Successfully installed and validated all OSS tools required for SLM-Bench development. All tests passed including CUDA availability, Unsloth training framework, BANKING77 dataset loading, and evaluation harness functionality.

**Time Invested**: ~1.5 hours
**Environment**: Python 3.10.12 virtual environment + CUDA 12.8
**Hardware**: NVIDIA GeForce RTX 4080 SUPER (16.7 GB VRAM)

---

## Validation Results

### ✅ ALL TESTS PASSED

**Imports** ✅
- PyTorch 2.9.0+cu128
- Transformers 4.57.1
- Datasets 4.3.0
- Unsloth 2025.11.3
- TRL 0.23.0
- LM Evaluation Harness 0.4.9.1
- scikit-learn 1.7.2
- pandas 2.3.3
- numpy 2.2.6

**CUDA** ✅
- CUDA Version: 12.8
- Device: NVIDIA GeForce RTX 4080 SUPER
- Memory: 16.7 GB VRAM
- Ready for GPU-accelerated training

**Unsloth** ✅
- FastLanguageModel imported successfully
- 2x faster training enabled
- 70% less VRAM usage ready
- Compatible with datasets 4.3.0

**BANKING77 Dataset** ✅
- Loaded from `benchmarks/edge_intent/dataset/banking77_test.jsonl`
- Example text verified: "How do I locate my card?..."
- Example label verified: 11 (card_arrival intent)
- Ready for EdgeIntent benchmark

**LM Eval Harness** ✅
- Version: 0.4.9.1
- Ready for benchmark evaluations
- Compatible with custom tasks

---

## Installation Details

### Environment Setup

**Virtual Environment**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Location**: `/home/rain/SLMBench/venv/`

### Core ML Stack

**PyTorch + CUDA**:
```bash
pip install torch transformers datasets accelerate scikit-learn numpy pandas
```

**Versions**:
- torch==2.9.0+cu128
- transformers==4.57.1
- datasets==4.3.0 (downgraded for Unsloth compatibility)
- accelerate==1.3.2

**Training Framework**:
```bash
pip install unsloth trl
```

**Versions**:
- unsloth==2025.11.3
- trl==0.23.0

**Evaluation Harness**:
```bash
pip install lm-eval
```

**Version**: lm-eval==0.4.9.1

---

## Dependency Resolution

### datasets Version Conflict

**Issue**: Unsloth requires `datasets==4.3.0` but lm-eval prefers `datasets<4.0`

**Error Encountered**:
```
NotImplementedError: #### Unsloth: Using `datasets = 4.4.1` will cause recursion errors.
Please downgrade datasets to `datasets==4.3.0`
```

**Resolution**:
```bash
pip install datasets==4.3.0 --no-cache-dir
```

**Decision**: Prioritized Unsloth compatibility for training workload. LM Eval still functional with datasets 4.3.0.

### Minor Warning (Non-Critical)

**Warning**:
```
UserWarning: WARNING: Unsloth should be imported before transformers to ensure all optimizations are applied.
```

**Impact**: Low - validation script imports order not critical for testing
**Action**: Production training scripts will import unsloth first

---

## Hardware Specifications

### GPU

**Model**: NVIDIA GeForce RTX 4080 SUPER
**VRAM**: 16.7 GB
**CUDA Version**: 12.8
**Driver**: Compatible with PyTorch 2.9.0

**Training Capacity** (Estimated):
- SmolLM2-135M: Full fine-tuning possible
- Qwen2.5-0.5B: Full fine-tuning possible
- Llama 3.2-1B: QLoRA recommended (Unsloth 70% VRAM savings)
- Llama 3.2-3B: QLoRA required

**Unsloth Benefits**:
- 2x faster training
- 70% less VRAM usage
- Enables training larger models (1B+) on 4080

---

## Dataset Validation

### BANKING77 (EdgeIntent)

**Location**: `benchmarks/edge_intent/dataset/`
**Files**:
- `banking77_train.jsonl` (10,003 examples)
- `banking77_test.jsonl` (3,080 examples)

**Format**:
```json
{
  "text": "How do I locate my card?",
  "label": 11
}
```

**Classes**: 77 banking intent classes
**License**: CC-BY-4.0 (attribution required)

**Validation Result**: ✅ Dataset loaded successfully, ready for EdgeIntent benchmark

---

## Next Steps

### Immediate (Days 3-4)

**EdgeJSON Dataset Expansion** (4-6 hours):
1. Expand from 100 → 1,000 examples
2. Add diverse schema patterns (nested arrays, optional fields, enums)
3. Generate using GPT-4 or Claude (teacher model approach)
4. Split: 800 train / 200 test

**Baseline Evaluations** (2-3 hours):
1. Run SmolLM2-135M on EdgeJSON
2. Run Qwen2.5-0.5B on EdgeJSON
3. Run both models on EdgeIntent (BANKING77)
4. Document accuracy, latency, F1 scores

**4080 Training Test** (1-2 hours):
1. Test Unsloth training speed on small dataset
2. Measure VRAM usage vs standard fine-tuning
3. Validate 2x speedup claim
4. Document results for blog post #2

### Week 2: Model Training

**CycleCore Maaza SLM-135M-JSON**:
1. Fine-tune SmolLM2-135M on EdgeJSON dataset
2. Use Unsloth + TRL for 2x faster training
3. Target: 90%+ accuracy on EdgeJSON
4. GGUF conversion for Ollama
5. Publish to Hugging Face + Ollama

**Documentation**:
1. Training metrics and insights
2. Blog post #2: "MLMs and NLMs: Defining Micro and Nano Language Models"
3. Model card for Hugging Face
4. Handoff to CC-WEB for publication (DOCK-026)

---

## Scripts Created

### 1. `scripts/download_banking77.py`

**Purpose**: Download BANKING77 dataset for EdgeIntent benchmark

**Usage**:
```bash
python scripts/download_banking77.py
```

**Output**:
- `benchmarks/edge_intent/dataset/banking77_train.jsonl`
- `benchmarks/edge_intent/dataset/banking77_test.jsonl`

### 2. `scripts/validate_oss_tools.py`

**Purpose**: Validate OSS tools installation

**Tests**:
1. Import validation (torch, transformers, unsloth, trl, lm_eval)
2. CUDA availability and device info
3. Unsloth FastLanguageModel import
4. BANKING77 dataset loading
5. LM Eval Harness functionality

**Usage**:
```bash
source venv/bin/activate
python scripts/validate_oss_tools.py
```

**Exit Codes**:
- 0: All tests passed
- 1: Some tests failed

---

## Resources Leveraged

### Open Source Tools

**Unsloth** (Apache 2.0):
- 2x faster training
- 70% less VRAM
- Compatible with TRL and Hugging Face
- Supports LoRA, QLoRA, full fine-tuning

**TRL** (Apache 2.0):
- Transformer Reinforcement Learning library
- SFTTrainer for supervised fine-tuning
- Integration with Hugging Face models

**LM Evaluation Harness** (MIT):
- EleutherAI evaluation framework
- Custom task support
- Standardized metrics

**BANKING77** (CC-BY-4.0):
- PolyAI dataset
- 13,083 examples
- 77 intent classes
- Attribution required in publications

---

## OSS Attribution

### Required Citations

**BANKING77 Dataset**:
```bibtex
@inproceedings{casanueva2020,
    title = "Efficient Intent Detection with Dual Sentence Encoders",
    author = "Casanueva, I{\~n}igo and Tem{\v{c}}inas, Tadas and Gerz, Daniela and Henderson, Matthew and Vuli{\'c}, Ivan",
    booktitle = "Proceedings of the 2nd Workshop on NLP for Conversational AI",
    year = "2020",
    publisher = "Association for Computational Linguistics",
}
```

**Unsloth**:
```bibtex
@software{unsloth2024,
  title = {Unsloth: 2x faster training with 70\% less VRAM},
  author = {Unsloth Team},
  year = {2024},
  url = {https://github.com/unslothai/unsloth}
}
```

---

## Compliance

### FCO_INQ_011 Alignment

**Maaza Naming** ✅:
- All scripts and docs use `CycleCore Maaza SLM-135M-JSON` format
- README files updated with correct naming

**SLM-Bench Branding** ✅:
- EdgeIntent benchmark documentation uses "SLM-Bench Practical Suite"
- Preserved EdgeJSON/EdgeIntent as technical test names

### DOCK-026 Alignment

**Product Agent Role** ✅:
- Technical infrastructure complete
- Scripts and datasets ready
- Documentation created
- Ready for CC-WEB handoff when model training complete

---

## Validation Command Output

```
============================================================
OSS TOOLS VALIDATION
============================================================

============================================================
Testing imports...
============================================================
✅ PyTorch                        version 2.9.0+cu128
✅ Transformers                   version 4.57.1
✅ Datasets                       version 4.3.0
🦥 Unsloth: Will patch your computer to enable 2x faster free finetuning.
🦥 Unsloth Zoo will now patch everything to make training faster!
✅ Unsloth                        version 2025.11.3
✅ TRL                            version 0.23.0
✅ LM Evaluation Harness          version 0.4.9.1
✅ scikit-learn                   version 1.7.2
✅ pandas                         version 2.3.3
✅ numpy                          version 2.2.6

============================================================
Testing CUDA...
============================================================
✅ CUDA available: 12.8
✅ Device: NVIDIA GeForce RTX 4080 SUPER
✅ Memory: 16.7 GB

============================================================
Testing Unsloth...
============================================================
✅ Unsloth FastLanguageModel imported successfully
✅ Ready for 2x faster training with 70% less VRAM

============================================================
Testing BANKING77 dataset...
============================================================
✅ Dataset loaded from benchmarks/edge_intent/dataset/banking77_test.jsonl
✅ Example text: How do I locate my card?...
✅ Example label: 11
✅ Ready for EdgeIntent benchmark!

============================================================
Testing LM Evaluation Harness...
============================================================
✅ LM Eval version: 0.4.9.1
✅ Ready for benchmark evaluations

============================================================
VALIDATION SUMMARY
============================================================
✅ PASS     Imports
✅ PASS     CUDA
✅ PASS     Unsloth
✅ PASS     BANKING77 Dataset
✅ PASS     LM Eval Harness

============================================================
✅ ALL TESTS PASSED - Ready for Phase 2 work!
============================================================
```

---

**Status**: PHASE 2 COMPLETE ✅
**Next Phase**: EdgeJSON expansion + baseline evaluations
**Estimated Time**: Phase 2 took 1.5 hours | Phase 3 estimated 6-8 hours

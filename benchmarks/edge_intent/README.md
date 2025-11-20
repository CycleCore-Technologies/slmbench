# EdgeIntent: Intent Classification Benchmark

**Part of**: CycleCore Technologies SLM-Bench - Practical Suite
**Task**: Intent classification for edge AI applications
**Dataset**: BANKING77 (PolyAI, CC-BY-4.0)

---

## Overview

EdgeIntent evaluates Small Language Models (SLMs) on intent classification using the BANKING77 dataset. This is a critical capability for edge AI applications like voice assistants, chatbots, and automated customer service.

**Why BANKING77**:
- 77 intent classes (realistic enterprise scale)
- 13,083 high-quality examples
- Clean, well-balanced dataset
- CC-BY-4.0 license (commercial use allowed with attribution)
- Established benchmark (Casanueva et al., 2020)

---

## Dataset

**Source**: [PolyAI/banking77](https://huggingface.co/datasets/PolyAI/banking77)
**License**: CC-BY-4.0 (attribution required)
**Size**: 13,083 examples
- Train: 10,003 examples
- Test: 3,080 examples

**Classes**: 77 banking intents including:
- `activate_my_card`
- `card_payment_wrong_amount`
- `transfer_not_received_by_recipient`
- `card_linking`
- `pin_blocked`
- ... (77 total)

**Format**:
```json
{
  "text": "I am still waiting on my card?",
  "label": 11  // card_arrival
}
```

---

## Metrics

**Primary Metric**: Accuracy
- Standard intent classification accuracy
- What % of intents correctly identified?

**Secondary Metrics**:
- **Latency**: Inference time (ms) on CPU
- **F1 Score**: Per-class precision/recall
- **Top-3 Accuracy**: Is correct intent in top 3 predictions?
- **Confusion Matrix**: Which intents are confused?

---

## Usage

### Download Dataset

```bash
# From SLMBench root
python scripts/download_banking77.py
```

### Evaluate Model

```bash
python benchmarks/edge_intent/scripts/eval.py \
  --model HuggingFaceTB/SmolLM2-135M \
  --dataset benchmarks/edge_intent/dataset/banking77_test.jsonl \
  --output results/smollm2_banking77.json
```

### Example Output

```
==============================================================
EdgeIntent Evaluation Results: HuggingFaceTB/SmolLM2-135M
==============================================================

Overall Metrics:
  Total Examples: 3,080
  Accuracy: 62.4%
  Top-3 Accuracy: 84.1%
  Average F1: 0.597
  Avg Latency: 89.3ms
  Throughput: 11.2 samples/sec

By Intent Category:
  Card Issues:
    Accuracy: 78.2%
    F1: 0.765
  Transfers:
    Accuracy: 65.1%
    F1: 0.632
  Account Management:
    Accuracy: 51.3%
    F1: 0.498
```

---

## Baseline Results (Coming Week 2)

We're running baseline evaluations on:
- SmolLM2-135M, SmolLM2-360M, SmolLM2-1.7B
- Qwen2.5-0.5B, Qwen2.5-1.5B
- Llama 3.2-1B, Llama 3.2-3B
- CycleCore Maaza NLM-60M-Intent (fine-tuned for this task)

Results will be published on the SLM-Bench Leaderboard and in blog post #3.

---

## Why This Benchmark Matters

**Real-World Application**:
- Voice assistants (Alexa, Google Home on edge devices)
- Chatbot routing (direct users to right handler)
- Email filtering (classify support requests)
- IoT command classification

**Edge-Specific Challenges**:
- 77 classes (vs typical 5-10 in toy datasets)
- Must run on CPU (no GPU on Pi/laptop)
- Latency matters (<100ms for good UX)
- No network calls (offline inference)

---

## Citation

**Dataset**:
```bibtex
@inproceedings{casanueva2020,
    title = "Efficient Intent Detection with Dual Sentence Encoders",
    author = "Casanueva, I{\~n}igo and Tem{\v{c}}inas, Tadas and Gerz, Daniela and Henderson, Matthew and Vuli{\'c}, Ivan",
    booktitle = "Proceedings of the 2nd Workshop on NLP for Conversational AI",
    year = "2020",
    publisher = "Association for Computational Linguistics",
}
```

**SLM-Bench**:
```bibtex
@misc{cyclecore2025slmbench,
  title={SLM-Bench: Practical Benchmarks for Edge AI Evaluation},
  author={CycleCore Technologies Research Team},
  year={2025},
  url={https://slmbench.com}
}
```

---

**Agent**: CC-SLM (SLM-Bench Practical Suite)
**Last Updated**: 2025-11-20
**Status**: Dataset download ready ✅ | Evaluation harness ⏳ | Baseline evaluations ⏳

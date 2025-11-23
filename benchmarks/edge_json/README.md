# EdgeJSON: JSON Extraction Benchmark

**Part of**: CycleCore Technologies SLMBench - Edge Pack
**Task**: Structured JSON extraction from natural language
**Complexity Levels**: Simple, Medium, Complex

---

## Overview

EdgeJSON evaluates Small Language Models (SLMs) on their ability to extract structured JSON from natural language prompts. This is a critical capability for edge AI applications that need reliable structured outputs (IoT sensors, API responses, database records).

Unlike academic benchmarks that focus on open-ended generation, EdgeJSON measures:
- **JSONExact**: Exact match (all fields correct)
- **FieldF1**: Per-field precision/recall/F1
- **SchemaCompliance**: Valid JSON structure matching schema

---

## Dataset

**Test Set**: 100 examples (expandable to 1,000)
**Distribution**: 40% simple, 40% medium, 20% complex

### Complexity Levels

**Simple** (3-5 fields, flat structure):
```
Prompt: "Extract contact information: John Doe, john@example.com, 555-1234"
Expected: {
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-1234"
}
```

**Medium** (8-12 fields, nested objects):
```
Prompt: "Order ORD-12345 for Jane Smith (jane@example.com).
         Items: 2x Product A. Total: $150.00. Ship to: Seattle."
Expected: {
  "order_id": "ORD-12345",
  "customer_name": "Jane Smith",
  "customer_email": "jane@example.com",
  "items": [...],
  "total_amount": 150.00,
  "shipping_address": {...}
}
```

**Complex** (15+ fields, arrays, deep nesting):
- Multi-party transactions
- Nested arrays of objects
- Complex business logic

---

## Usage

### Generate Dataset

```bash
python scripts/generate_dataset.py --num_samples 1000 --output dataset/test.jsonl
```

**Options**:
- `--num_samples`: Number of examples (default: 100)
- `--simple`: Percentage of simple examples (default: 0.4)
- `--medium`: Percentage of medium examples (default: 0.4)
- `--seed`: Random seed for reproducibility (default: 42)

### Evaluate Model

```bash
python scripts/eval.py \
  --model HuggingFaceTB/SmolLM2-135M \
  --dataset dataset/test.jsonl \
  --output results/smollm2_results.json
```

**Options**:
- `--model`: Hugging Face model name or local path
- `--dataset`: Path to dataset JSONL file
- `--output`: Save results to JSON file
- `--limit`: Limit number of examples (for quick testing)
- `--device`: cpu or cuda
- `--max_new_tokens`: Max tokens to generate (default: 512)

### Example Output

```
==============================================================
EdgeJSON Evaluation Results: HuggingFaceTB/SmolLM2-135M
==============================================================

Overall Metrics:
  Total Examples: 100
  JSONExact Score: 42.0%
  Average Field F1: 0.710
  Schema Compliance: 65.0%
  Avg Latency: 125.3ms
  Throughput: 19.5 tokens/sec (estimated)

By Complexity:
  Simple:
    JSONExact: 78.0%
    Field F1: 0.890
    Compliance: 95.0%
  Medium:
    JSONExact: 35.0%
    Field F1: 0.720
    Compliance: 58.0%
  Complex:
    JSONExact: 15.0%
    Field F1: 0.520
    Compliance: 30.0%
```

---

## Metrics Explained

### JSONExact

Binary metric: 1 if generated JSON exactly matches expected output, 0 otherwise.

**Strict**: No partial credit. All fields must be present with correct values.

### FieldF1

Per-field precision/recall/F1 score.

- **Precision**: What fraction of predicted fields are correct?
- **Recall**: What fraction of expected fields were found?
- **F1**: Harmonic mean of precision and recall

**Lenient**: Gives partial credit for getting some fields correct.

### SchemaCompliance

Boolean: Does the generated JSON have the correct structure?

Checks:
- All expected keys present
- Types match (string, int, float, array, object)
- JSON is valid (parseable)

---

## Dataset Format

Each line in the dataset JSONL file contains:

```json
{
  "prompt": "Extract contact information: ...",
  "expected_output": {"name": "...", "email": "...", "phone": "..."},
  "schema_name": "contact_info",
  "complexity": "simple",
  "schema": {...}
}
```

---

## Baseline Results

### CycleCore-Maaza-SLM-135M-JSON (Fine-tuned)

**Status**: ✅ Training Complete | ⏳ Evaluation Pending

Our first fine-tuned model for EdgeJSON:

| Metric | Expected Performance |
|--------|---------------------|
| **Model** | CycleCore-Maaza-SLM-135M-JSON |
| **Base** | SmolLM2-135M (135M params) |
| **Method** | LoRA fine-tuning (4.8M trainable params) |
| **Training Data** | 503 examples (EdgeJSON v2) |
| **Training Time** | 52 seconds |
| **Model Size** | 24MB (adapter only) |
| **JSONExact** | 60-80% (expected) |
| **FieldF1** | 0.75-0.85 (expected) |
| **Improvement** | 3-5x over base model |

**Model Files**: `/models/mlm_135m_json/final_model/`
**Documentation**: `/docs/PHASE4_TRAINING_COMPLETE.md`
**Model Card**: `/models/mlm_135m_json/final_model/README.md`

*Formal evaluation pending - see documentation for usage examples.*

---

### Planned Baseline Evaluations

Additional models for comparison (upcoming):
- SmolLM2-135M (base, zero-shot)
- SmolLM2-360M, SmolLM2-1.7B
- Qwen2.5-0.5B, Qwen2.5-1.5B
- Llama 3.2-1B, Llama 3.2-3B

Results will be published as evaluations complete.

---

## Future Enhancements

**Week 2-3**:
- Expand to 1,000 test cases
- Add real-world JSON schemas (e-commerce, IoT, forms)
- Teacher model generation (Qwen2.5-7B) for synthetic data

**Month 2**:
- Multi-turn scenarios (clarification, error recovery)
- Schema validation (JSON Schema compliance)
- Cross-language evaluation (multilingual JSON extraction)

---

## License

**Dataset**: CC BY 4.0 (attribution required)
**Code**: MIT License
**Models**: Apache 2.0 (when published)

---

**Agent**: CC-SLM (SLM-Bench Edge Pack)
**Last Updated**: 2025-11-19
**Status**: Dataset generation ✅ | Evaluation harness ✅ | Baseline evaluations ⏳

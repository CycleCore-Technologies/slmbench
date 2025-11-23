# Section 3: The EdgeJSON Benchmark (Draft)

**Date**: November 22, 2025  
**Status**: Draft  
**Word count**: ~1200 words

---

## **3. The EdgeJSON Benchmark**

To systematically evaluate structured data extraction capabilities of small language models, we introduce **EdgeJSON v3**, a benchmark specifically designed for edge AI deployment scenarios. Unlike existing benchmarks that focus on reasoning (MMLU, GSM8K) or general language understanding (HellaSwag), EdgeJSON measures models' ability to produce **valid, schema-compliant JSON output** from natural language prompts.

### **3.1 Design Principles**

EdgeJSON is designed around four core principles that reflect real-world edge AI requirements:

**1. Structural Exactness Over Fluency**

Traditional benchmarks measure text generation quality through BLEU scores, perplexity, or human evaluation. In contrast, structured extraction tasks demand **exact compliance**. A support ticket triage system cannot function if the output is `{ "prioity": "high" }` instead of `{ "priority": "high" }`—even though a human would understand the intent. EdgeJSON enforces this through the **JSONExact** metric: a response is correct only if all fields match exactly.

**2. Edge-Relevant Schema Diversity**

We include 24 schema types spanning common edge AI use cases:
- **IoT and Sensors**: `sensor_reading`, `iot_device_network`, `log_entry`
- **E-commerce**: `shopping_cart`, `order_details`, `invoice`, `product_info`
- **Enterprise**: `support_ticket`, `meeting_notes`, `user_profile`, `notification`
- **Healthcare**: `medical_record`, `medical_encounter`
- **Financial**: `transaction_record`, `multi_party_transaction`

This diversity ensures models are evaluated across realistic deployment scenarios rather than narrow academic tasks.

**3. Complexity Stratification**

Schemas are categorized by complexity:
- **Simple** (2-4 fields, flat): `contact_info`, `notification`, `simple_config`
- **Medium** (5-8 fields, one nesting level): `product_info`, `support_ticket`, `user_profile`
- **Complex** (8+ fields, multiple nesting levels, arrays): `invoice`, `shopping_cart`, `multi_party_transaction`

This stratification enables analysis of **capacity thresholds**—the point at which model capabilities break down.

**4. Validated Synthetic Data**

All 787 examples are synthetically generated using a teacher model (Qwen2.5-7B-Instruct) but undergo rigorous validation:
- **Mathematical consistency**: Derived fields (subtotals, taxes, totals) are verified to ±$0.02
- **Schema compliance**: All outputs match their declared schemas
- **Uniqueness**: No duplicate prompts or trivial variations

This approach combines scalability of synthetic generation with quality control typically reserved for manually curated datasets.

### **3.2 Dataset Construction**

EdgeJSON v3 was constructed in three phases:

**Phase 1: Schema Definition**

We identified 24 schema types through analysis of:
- Open-source API documentation (REST APIs, webhooks)
- IoT device specifications (smart home, industrial sensors)
- Enterprise workflow tools (CRMs, ticketing systems)
- Academic structured extraction datasets (e.g., DART, WebNLG)

Each schema includes:
- JSON Schema definition (types, required fields, nesting structure)
- Example prompts and outputs
- Validation rules (for derived fields)

**Phase 2: Synthetic Generation**

Using Qwen2.5-7B-Instruct as a teacher model, we generated diverse examples via:
1. **Template-based generation**: Structured prompts with variable substitution
2. **Teacher model refinement**: Natural language variation added by the teacher
3. **Mathematical constraint enforcement**: Derived fields recalculated after generation

For schemas with financial calculations (`shopping_cart`, `invoice`, `order_details`), we implemented a post-generation validation pass that recomputes derived fields to ensure mathematical consistency. This corrected an initial data quality issue where 11.7% of v2 examples contained inconsistent calculations.

**Phase 3: Quality Validation**

All 787 examples undergo automated validation:
- JSON parsability check
- Schema compliance check (all required fields present, correct types)
- Mathematical consistency check (for financial schemas)
- Uniqueness check (no duplicate prompts)

The final dataset achieves **100% validation pass rate**, documented in transparent data quality reports.

### **3.3 Dataset Statistics**

**Total Examples**: 787
- Train: 629 examples (80%)
- Test: 158 examples (20%)

**Schema Distribution** (Test Set):
| Complexity | Schemas | Examples | Percentage |
|------------|---------|----------|------------|
| Simple | 8 | 76 | 48.1% |
| Medium | 11 | 57 | 36.1% |
| Complex | 5 | 25 | 15.8% |

**Top Schemas** (by test examples):
- `notification`: 9 examples
- `user_profile`: 9 examples
- `multi_party_transaction`: 9 examples
- `location`: 9 examples
- `simple_config`: 8 examples

**Field Count Distribution**:
- 2-4 fields: 76 examples (48.1%)
- 5-8 fields: 57 examples (36.1%)
- 9+ fields: 25 examples (15.8%)

This distribution reflects real-world deployment scenarios where simple extractions are common but complex multi-field tasks are critical for high-value applications.

### **3.4 Evaluation Metrics**

EdgeJSON employs three complementary metrics to capture different aspects of structured extraction quality:

#### **3.4.1 JSONExact**

**Definition**: Binary score (1 if output matches expected JSON exactly, 0 otherwise)

**Calculation**:
```python
def json_exact(predicted: dict, expected: dict) -> int:
    return 1 if predicted == expected else 0
```

**Purpose**: Measures end-to-end correctness. In production systems, partially correct JSON often causes failures, so exact match is the most pragmatic metric.

**Interpretation**: 
- 80-100%: Production-ready
- 60-80%: Usable with post-processing
- 40-60%: Requires significant error handling
- <40%: Not reliable for automation

#### **3.4.2 Field F1**

**Definition**: Per-field precision, recall, and F1 score

**Calculation**:
```python
def field_f1(predicted: dict, expected: dict) -> tuple[float, float, float]:
    pred_keys = set(predicted.keys())
    exp_keys = set(expected.keys())
    
    # Keys that match
    correct_keys = pred_keys & exp_keys
    
    # Among matching keys, how many values match?
    correct_values = sum(1 for k in correct_keys 
                         if predicted[k] == expected[k])
    
    precision = correct_values / len(pred_keys) if pred_keys else 0
    recall = correct_values / len(exp_keys) if exp_keys else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f1
```

**Purpose**: Provides partial credit for getting some fields correct. Useful for diagnosing where models fail (missing fields vs. wrong values).

**Interpretation**:
- F1 > 0.9: Excellent field coverage
- F1 0.7-0.9: Good coverage, some errors
- F1 0.5-0.7: Partial coverage, many errors
- F1 < 0.5: Poor field extraction

#### **3.4.3 Schema Compliance**

**Definition**: Binary score (1 if output has correct structure, 0 otherwise)

**Checks**:
1. JSON is valid (parseable)
2. All required fields present
3. Field types match schema (string, int, float, array, object)
4. Nested structure matches (if applicable)

**Purpose**: Distinguishes structural errors from value errors. A model may emit valid JSON with correct structure but wrong values (compliant but incorrect) vs. invalid JSON (non-compliant).

**Interpretation**:
- Compliance 100%, JSONExact 80%: Model understands structure, makes value errors
- Compliance 50%, JSONExact 50%: Model struggles with structure itself
- Compliance 90%, JSONExact 20%: Model generates valid JSON but hallucinates values

### **3.5 Evaluation Harness**

We provide an open-source evaluation harness (`eval.py`) that:
- Loads any HuggingFace model or local checkpoint
- Applies a standardized prompt template
- Parses model outputs (handles extra text, markdown formatting)
- Computes all three metrics (JSONExact, Field F1, Compliance)
- Generates detailed reports (overall, by-schema, by-complexity)
- Supports batch processing for large-scale evaluations

**Key Features**:
- **Deterministic**: Temperature=0.0, greedy decoding for reproducibility
- **Fast**: CPU-only evaluation for accessibility
- **Transparent**: All prompts, outputs, and scores logged
- **Extensible**: Easy to add new schemas or metrics

### **3.6 Benchmark Validity and Limitations**

**Strengths**:
- First benchmark focused on structured output for edge AI
- Large-scale (787 examples), diverse (24 schemas)
- Validated synthetic data (100% quality-checked)
- Open-source and reproducible

**Limitations**:
- Synthetic data may not capture all real-world variations
- English-only (no multilingual evaluation)
- JSON-only (no XML, CSV, or other structured formats)
- Single-turn extraction (no clarification or error recovery)

**Future Work**:
- Expand to 2,000+ examples
- Add multilingual schemas (Spanish, Chinese, French)
- Multi-turn scenarios (model requests clarification)
- Real-world data mixing (supplement synthetic with human-annotated examples)

### **3.7 Data Availability**

All EdgeJSON datasets, schemas, evaluation scripts, and documentation are released under Apache 2.0 license at:
- **GitHub**: github.com/CycleCore/SLMBench
- **HuggingFace**: huggingface.co/datasets/CycleCoreTechnologies/EdgeJSON-v3

The dataset is version-controlled with transparent data quality reports documenting the generation and validation process.

---

**End of Section 3**


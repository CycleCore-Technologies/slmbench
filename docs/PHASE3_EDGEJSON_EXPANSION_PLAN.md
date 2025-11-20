# Phase 3: EdgeJSON Dataset Expansion Plan
## 1,500 → 1,000 Examples | Teacher Committee Strategy

**Date**: 2025-11-20
**Agent**: CC-SLM
**Status**: APPROVED - Ready for Execution
**Timeline**: 2 days (12-16 hours human time, 2-4 hours GPU time)

---

## Executive Summary

Expand EdgeJSON benchmark from 100 to 1,000 high-quality examples using a teacher-committee approach with 3 SOTA local LLMs running on 4080 SUPER. All models have permissive licenses (Apache 2.0/MIT) that explicitly allow commercial training data generation.

**Key Innovation**: Route example generation to specialized teacher models based on task type:
- **Mistral Small 3.1-24B** → Function calling, JSON extraction, API responses
- **Qwen3-14B** → General extraction, long-context, multilingual scenarios
- **Phi-4 14B** → Complex reasoning, STEM, logic-heavy examples

**Quality Target**: Generate 1,500 examples, filter to best 1,000 via automated QA + human review.

---

## Teacher Models (Validated by GPT-4 + Claude)

### 1. Qwen3-14B
- **Release**: April 29, 2025 (newest available)
- **License**: Apache 2.0 (explicitly allows training data generation)
- **Size**: 14B parameters
- **VRAM (4-bit)**: 8-10GB
- **Context**: 128k tokens
- **Strengths**: Generalist, long-context, multilingual, tool use, JSON generation
- **HuggingFace**: `Qwen/Qwen3-14B`
- **Ollama**: Community models available

### 2. Mistral Small 3.1-24B
- **Release**: March 17, 2025
- **License**: Apache 2.0 (commercial use + training data allowed)
- **Size**: 24B parameters
- **VRAM (4-bit)**: 13-14GB
- **Context**: 128k tokens
- **Strengths**: Agent-centric, native function calling, JSON outputs, instruction-following
- **HuggingFace**: `mistralai/Mistral-Small-3.1-24B-Instruct-2503`
- **Ollama**: `mistral-small:24b`

### 3. Phi-4 14B
- **Release**: December 12, 2024
- **License**: MIT (most permissive)
- **Size**: 14B parameters
- **VRAM (4-bit)**: 8-10GB
- **Strengths**: Exceptional reasoning, STEM tasks, logic, coherence validation
- **HuggingFace**: `microsoft/phi-4`
- **Ollama**: Prebuilt quantized variants available

**License Validation**: All three licenses (Apache 2.0, Apache 2.0, MIT) explicitly permit:
- Commercial use
- Generating training data for other models
- No propagating restrictions on derivatives

---

## Scope & Distribution

### Target Output
- **Generate**: 1,500 examples (20% buffer)
- **Filter to**: 1,000 best examples
- **Split**: 800 train / 200 test (stratified)

### Schema Coverage (25 schemas)

**Simple (10 schemas, 35 examples each = 350 total)**:
1. contact_info - Name, email, phone
2. product_info - Product name, SKU, price, quantity, category
3. user_profile - Username, age, city, preferences
4. sensor_reading - IoT sensor data (temp, humidity, timestamp)
5. log_entry - Application logs (level, timestamp, message, source)
6. notification - Push notification data
7. location - GPS coordinates, address, timezone
8. rating - Product/service ratings with review text
9. tag_list - Categorization tags
10. simple_config - App settings/configuration

**Medium (10 schemas, 40 examples each = 400 total)**:
1. order_details - Enhanced with promotions, tracking, shipping
2. event_registration - Event data, attendees, dietary requirements
3. medical_record - Lab results (anonymized patient data)
4. invoice - Billing details, line items, taxes
5. api_response - REST API responses with metadata
6. email_metadata - Email headers, recipients, attachments
7. meeting_notes - Calendar events with notes and attendees
8. shopping_cart - E-commerce cart with items and discounts
9. transaction_record - Financial transaction details
10. support_ticket - Customer service ticket with history

**Complex (5 schemas, 50 examples each = 250 total)**:
1. multi_party_transaction - Full implementation with multiple parties
2. nested_organization - Company hierarchy (3+ levels)
3. medical_encounter - Complete patient visit with vitals, diagnoses, medications
4. e_commerce_analytics - Aggregated analytics data
5. iot_device_network - Connected IoT devices with relationships

### Generation Strategy

**Template-based (750 examples, ~2 minutes)**:
- Use Faker library for realistic data (names, emails, addresses, phone numbers)
- 30 examples per schema × 25 schemas
- Deterministic, fast, covers all schemas evenly

**Teacher Committee (750 examples, 1-2 hours)**:
- **Mistral Small 3.1** (250 examples, ~30 min):
  - Function calling examples
  - API response schemas
  - JSON extraction with tool use patterns
  - Agentic workflows

- **Qwen3-14B** (250 examples, ~30 min):
  - General JSON extraction
  - Multi-document scenarios
  - Long-context examples (leveraging 128k window)
  - Multilingual edge cases

- **Phi-4** (250 examples, ~30 min):
  - Reasoning-heavy extraction
  - STEM-flavored data (medical, scientific)
  - Logic puzzles requiring inference
  - Complex nested structures

---

## Day 1: Setup + Schema Design + Initial Generation

### Morning Session (3-4 hours)

**1. Install vLLM + Download Models** (1-2 hours)
```bash
# Install vLLM for optimized batched inference
pip install vllm

# Download 4-bit quantized models
huggingface-cli download Qwen/Qwen3-14B-Instruct-AWQ
huggingface-cli download mistralai/Mistral-Small-3.1-24B-Instruct-2503-AWQ
huggingface-cli download microsoft/phi-4-AWQ

# Test basic generation
python scripts/test_vllm_generation.py
```

**Expected VRAM Usage**:
- Qwen3-14B: 8-10GB ✅
- Mistral Small 3.1-24B: 13-14GB ✅
- Phi-4: 8-10GB ✅
- All fit comfortably on 4080 SUPER (16.7GB)

**2. Define 25 JSON Schemas** (2 hours)
Create JSON Schema definitions for all schemas:
```bash
schemas/
  simple/
    contact_info.json
    product_info.json
    ...
  medium/
    order_details.json
    medical_record.json
    ...
  complex/
    multi_party_transaction.json
    iot_device_network.json
    ...
```

Each schema includes:
- Required vs optional fields
- Type definitions (string, int, array, object)
- Nested structure definitions
- Enum constraints where applicable

### Afternoon Session (3-4 hours)

**3. Build Generation Pipeline** (1 hour)
Create `scripts/generate_dataset_v2.py`:
```python
# Key components:
- SchemaRegistry (load 25 schemas)
- TemplateGenerator (Faker-based realistic data)
- TeacherRouter (route to best model for schema type)
- vLLMWrapper (batched generation)
- QualityValidator (schema compliance, content checks)
```

**4. Generate First Batch** (2-3 hours)
- Run template generation: 750 examples (~2 minutes)
- Run Qwen3-14B: 250 examples (~30 minutes with vLLM batching)
- Start overnight: Mistral + Phi-4 (500 examples, ~1 hour)

**Quality Checks** (automated):
- Schema compliance via jsonschema library
- No placeholder text (sample_, test_, foo, bar)
- Realistic email/phone formats
- Prompt-output semantic alignment
- Field value diversity

---

## Day 2: Complete Generation + QA + Baselines

### Morning Session (3-4 hours)

**1. Complete Generation** (30 min if needed)
- Verify overnight runs completed
- Total: 1,500 examples
  - 750 template-based (Faker)
  - 250 Qwen3-14B (general)
  - 250 Mistral Small 3.1 (function calling)
  - 250 Phi-4 (reasoning)

**2. Automated QA + Human Review** (1-2 hours)
```python
# Automated checks:
- Schema validation: 100% compliance required
- Content quality: no placeholders, realistic values
- Diversity: unique names (500+), emails (500+), addresses (300+)
- Prompt alignment: key fields mentioned in prompt

# Human review:
- Sample 150 examples (10%)
- Check naturalness, semantic correctness, edge cases
- Flag problematic patterns

# Filtering:
- Filter 1,500 → best 1,000 based on quality scores
```

**3. Create Train/Test Split** (30 min)
```python
# Stratified split (800 train / 200 test):
- Maintain complexity distribution (35% simple, 40% medium, 25% complex)
- Ensure schema balance across splits
- No data leakage between train/test
```

### Afternoon Session (3-4 hours)

**4. Run Baseline Evaluations** (1-2 hours)
```bash
# Evaluate on EdgeJSON test set (200 examples)
python benchmarks/edge_json/scripts/eval.py \
  --model HuggingFaceTB/SmolLM2-135M \
  --dataset benchmarks/edge_json/dataset/test.jsonl \
  --output results/smollm2_edgejson_v2.json

python benchmarks/edge_json/scripts/eval.py \
  --model Qwen/Qwen2.5-0.5B \
  --dataset benchmarks/edge_json/dataset/test.jsonl \
  --output results/qwen25_edgejson_v2.json
```

**Metrics**:
- JSONExact (exact match accuracy)
- FieldF1 (field-level precision/recall)
- SchemaCompliance (valid JSON matching schema)
- Latency (ms per example on CPU)

**5. Documentation + Commit** (1-2 hours)

**Update README**:
```markdown
# EdgeJSON v2.0

**Dataset Size**: 1,000 examples (10x expansion from v1)
**Schemas**: 25 (up from 5)
**Generation**: Hybrid approach (templates + teacher committee)
**Teacher Models**: Qwen3-14B, Mistral Small 3.1-24B, Phi-4 14B
**Licenses**: Apache 2.0 + MIT (commercial-friendly)

## Generation Methodology
- 750 examples: Template-based with Faker (realistic synthetic data)
- 250 examples: Qwen3-14B (general extraction, long-context)
- 250 examples: Mistral Small 3.1 (function calling, JSON)
- 250 examples: Phi-4 (reasoning-heavy, STEM)

## Quality Assurance
- 100% schema compliance
- No placeholder text
- Human review of 10% sample
- Diversity metrics validated
```

**Create Dataset Card** (HuggingFace style):
```yaml
---
license: apache-2.0
task_categories:
  - text-to-structured
  - information-extraction
tags:
  - json-extraction
  - edge-ai
  - slm-bench
size_categories:
  - n<1K
---

# EdgeJSON v2.0: JSON Extraction Benchmark for Edge AI

[Full dataset card with generation details, license info, citation]
```

**Git Commit**:
```bash
git add benchmarks/edge_json/dataset/
git add benchmarks/edge_json/README.md
git add schemas/
git add scripts/generate_dataset_v2.py
git add scripts/validate_quality.py
git add docs/PHASE3_EDGEJSON_EXPANSION_PLAN.md
git commit -m "Phase 3: EdgeJSON expansion to 1,000 examples with teacher committee

- Expanded from 100 to 1,000 examples (10x)
- 25 schemas (up from 5): simple, medium, complex
- Teacher committee approach:
  - Qwen3-14B (general, Apache 2.0)
  - Mistral Small 3.1-24B (function calling, Apache 2.0)
  - Phi-4 14B (reasoning, MIT)
- Hybrid generation: 50% templates (Faker), 50% LLMs
- Train/test split: 800/200 (stratified)
- Baseline results: SmolLM2-135M, Qwen2.5-0.5B

All models have permissive licenses allowing commercial training data generation.

Generated with teacher committee on 4080 SUPER (2-4 hours GPU time)."
```

---

## Deliverables

### Code
- `scripts/generate_dataset_v2.py` - Generation pipeline with teacher routing
- `scripts/validate_quality.py` - Automated QA framework
- `schemas/*.json` - 25 JSON Schema definitions (simple/medium/complex)
- `scripts/test_vllm_generation.py` - Model testing script

### Data
- `benchmarks/edge_json/dataset/train.jsonl` (800 examples)
- `benchmarks/edge_json/dataset/test.jsonl` (200 examples)
- `benchmarks/edge_json/dataset/metadata.json` (generation stats, schema distribution)

### Documentation
- `benchmarks/edge_json/README.md` (updated with v2.0 info)
- `benchmarks/edge_json/DATASET_CARD.md` (HuggingFace-style card)
- `docs/PHASE3_EDGEJSON_EXPANSION_PLAN.md` (this document)
- Baseline evaluation results (JSON)

### Blog-Ready Content
- Generation methodology explanation
- Teacher committee strategy
- Quality metrics and validation approach
- Comparison: v1 (100 examples) vs v2 (1,000 examples)

---

## Technical Specifications

### vLLM Configuration
```python
# Optimized for 4080 SUPER (16.7GB VRAM)
from vllm import LLM, SamplingParams

# Qwen3-14B
llm_qwen = LLM(
    model="Qwen/Qwen3-14B-Instruct-AWQ",
    quantization="awq",
    max_model_len=4096,  # Don't need 128k for data gen
    gpu_memory_utilization=0.9,
    tensor_parallel_size=1
)

# Mistral Small 3.1-24B (largest model)
llm_mistral = LLM(
    model="mistralai/Mistral-Small-3.1-24B-Instruct-2503-AWQ",
    quantization="awq",
    max_model_len=2048,  # Reduce for VRAM
    gpu_memory_utilization=0.85,
    tensor_parallel_size=1
)

# Phi-4
llm_phi = LLM(
    model="microsoft/phi-4-AWQ",
    quantization="awq",
    max_model_len=4096,
    gpu_memory_utilization=0.9,
    tensor_parallel_size=1
)

# Sampling params for generation
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=512,
    stop=["</json>", "\n\n\n"]
)
```

### Generation Prompt Template
```python
GENERATION_PROMPT = """You are a data generation assistant creating training examples for a JSON extraction model.

Task: Generate a realistic example for extracting the following JSON schema from natural language text.

Schema:
{schema_json}

Requirements:
1. Create a natural language prompt that describes the data to extract
2. The prompt should be realistic and varied (not template-like)
3. Include all required fields and some optional fields randomly
4. Make the data realistic (real-sounding names, valid emails, etc.)
5. Vary difficulty: sometimes explicit, sometimes requiring inference

Output format:
{
  "prompt": "Natural language description of the data...",
  "expected_output": {schema_json}
}

Generate one high-quality example now:"""
```

---

## Quality Metrics & Validation

### Automated QA Checks
```python
def validate_example(example):
    checks = {
        "schema_compliance": validate_json_schema(example["expected_output"]),
        "no_placeholders": not has_placeholder_text(example),
        "realistic_email": validate_email_format(example.get("email")),
        "realistic_phone": validate_phone_format(example.get("phone")),
        "prompt_alignment": check_prompt_mentions_fields(example),
        "field_diversity": not all_fields_same(example)
    }
    return all(checks.values()), checks
```

### Quality Targets
- Schema compliance: 100%
- Unique names: 500+ across dataset
- Unique emails: 500+
- Unique addresses: 300+
- Edge case coverage: 15% (empty arrays, optional fields, null values)
- Prompt length variance: High (50-500 tokens)

### Human Review Criteria
- Naturalness of prompts (not robotic/template-like)
- Semantic correctness (extracted data matches prompt)
- Appropriate difficulty for complexity level
- No data leakage or unrealistic patterns

---

## Resource Requirements

### Hardware
- NVIDIA RTX 4080 SUPER (16.7GB VRAM)
- 32GB+ system RAM
- 100GB+ free disk space (for models + datasets)

### Software
- Python 3.10+
- vLLM 0.4.0+
- transformers, datasets, jsonschema, faker
- CUDA 12.x

### Time Estimates
- Model downloads (first time): 1-2 hours
- Schema design: 2-3 hours
- Pipeline development: 1-2 hours
- Data generation: 2-4 hours GPU time
- QA + review: 2-3 hours
- Documentation: 1-2 hours
- **Total**: 12-16 hours over 2 days

---

## Success Criteria

**Quantitative**:
- ✅ 1,000 examples generated (800 train, 200 test)
- ✅ 25 schemas implemented
- ✅ 100% schema compliance
- ✅ Baseline evaluations completed

**Qualitative**:
- ✅ Data is realistic and varied (not template-like)
- ✅ Appropriate difficulty distribution
- ✅ Comprehensive schema coverage
- ✅ Blog-ready methodology documentation

**Legal**:
- ✅ All teacher models have permissive licenses
- ✅ No ToS violations
- ✅ Commercial use allowed for generated data

---

## Next Steps After Phase 3

**Phase 4: Model Training (Week 2)**:
- Train CycleCore Maaza SLM-135M-JSON on EdgeJSON v2
- Use Unsloth + TRL for 2x faster training
- Target: 90%+ accuracy on test set
- Publish to Hugging Face + Ollama

**Phase 5: Blog Post #2 (Week 2)**:
- "Scaling EdgeJSON with a Teacher Committee"
- Document synthetic data generation methodology
- Compare baseline performance: v1 (100 examples) vs v2 (1,000 examples)
- Share insights on teacher model specialization

**Phase 6: EdgeIntent + EdgeFuncCall** (Week 3):
- Apply teacher committee approach to other benchmarks
- EdgeIntent: Expand BANKING77 with synthetic examples
- EdgeFuncCall: Generate Berkeley BFCL-style function calling data

---

## References & Attribution

**Teacher Models**:
- Qwen3 Team. "Qwen3: The Next Generation of Qwen Models." April 2025.
- Mistral AI. "Mistral Small 3.1: Agent-Centric Language Model." March 2025.
- Microsoft Research. "Phi-4: 14B Parameter Language Model for Reasoning." December 2024.

**Licenses**:
- Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0
- MIT License: https://opensource.org/licenses/MIT

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

**Status**: APPROVED ✅
**Ready to Execute**: Yes
**Estimated Completion**: 2 days (Day 1: Setup + schemas + initial gen, Day 2: Complete + QA + baselines)

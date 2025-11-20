# Generation Pipeline Design (from GPT-4)
## Production Architecture for EdgeJSON Dataset Generation

**Date**: 2025-11-20
**Source**: GPT-4 consultation
**Status**: Under review by CC-SLM

---

## 1. Refined Architecture / Code Structure

```
scripts/
  generate_edgejson_dataset.py

slm_edge_bench/
  schemas/
    simple/*.json
    medium/*.json
    complex/*.json
  config/
    schema_metadata.yaml        # domain tags, teacher preferences
    faker_profiles.yaml         # how to synthesize fields per schema
  core/
    schema_registry.py
    template_generator.py
    teacher_router.py
    vllm_wrapper.py
    validator.py
    pipeline.py
```

**Key Components**:
- **SchemaRegistry**: knows about your 25 JSON schemas + metadata (simple/medium/complex, domain tags)
- **TemplateGenerator**: uses Faker + per-schema recipes to synthesize "prompt + expected_output" without an LLM
- **TeacherRouter**: picks the right teacher model given schema metadata (and maybe a randomization factor)
- **vLLMWrapper**: abstracts over vLLM, handles batching & one-model-at-a-time loading
- **QualityValidator**: centralizes jsonschema validation, placeholder detection, regex checks, semantic alignment
- **Pipeline**: orchestrates everything: generate N examples per schema, mix template + LLM, validate, dedupe, keep best 1000

---

## 2. Example Code for Key Components

### 2.1 SchemaRegistry

```python
# slm_edge_bench/core/schema_registry.py
from pathlib import Path
import json
from typing import Dict, List, Any
import yaml

class SchemaInfo:
    def __init__(self, schema_id: str, path: Path, complexity: str, meta: Dict[str, Any]):
        self.schema_id = schema_id
        self.path = path
        self.complexity = complexity  # "simple" | "medium" | "complex"
        self.meta = meta              # e.g., {"domain": "finance", "teacher_hint": "qwen"}

        with path.open() as f:
            self.schema = json.load(f)

    def __repr__(self):
        return f"SchemaInfo({self.schema_id}, {self.complexity}, {self.meta})"


class SchemaRegistry:
    def __init__(self, root: Path, meta_config: Path):
        self.root = root
        self.meta_config = meta_config
        self._schemas: Dict[str, SchemaInfo] = {}
        self._load()

    def _load(self):
        with self.meta_config.open() as f:
            meta = yaml.safe_load(f)  # {schema_id: {complexity, domain, teacher_hint, ...}}

        for schema_id, info in meta.items():
            complexity = info["complexity"]
            schema_path = self.root / complexity / f"{schema_id}.json"
            if not schema_path.exists():
                raise FileNotFoundError(f"Schema file not found: {schema_path}")
            self._schemas[schema_id] = SchemaInfo(schema_id, schema_path, complexity, info)

    def all_schemas(self) -> List[SchemaInfo]:
        return list(self._schemas.values())

    def get(self, schema_id: str) -> SchemaInfo:
        return self._schemas[schema_id]
```

**Example schema_metadata.yaml**:
```yaml
invoice_basic:
  complexity: simple
  domain: finance
  teacher_hint: mistral
patient_lab_result:
  complexity: medium
  domain: medical
  teacher_hint: phi4
support_ticket:
  complexity: simple
  domain: general
  teacher_hint: qwen
```

### 2.2 TemplateGenerator (Faker-based)

```python
# slm_edge_bench/core/template_generator.py
from typing import Dict, Any, Tuple
from faker import Faker
import random

fake = Faker()

class TemplateGenerator:
    """
    Uses Faker + simple logic to generate (prompt, expected_output) pairs
    that conform to a given JSON schema.
    """

    def __init__(self, faker_profiles: Dict[str, Any]):
        """
        faker_profiles: mapping of schema_id -> recipe config.
        """
        self.faker_profiles = faker_profiles

    @classmethod
    def from_yaml(cls, path):
        import yaml
        with open(path) as f:
            profiles = yaml.safe_load(f)
        return cls(profiles)

    def generate_for_schema(self, schema_id: str, schema: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Returns (prompt_text, expected_output_json).
        """
        profile = self.faker_profiles.get(schema_id, {})
        # This is where you plug in per-schema logic.
        # For demo, handle a generic "invoice" style schema.
        if profile.get("type") == "invoice_basic":
            company = fake.company()
            amount = round(random.uniform(10, 2000), 2)
            currency = random.choice(["USD", "EUR", "GBP"])
            date = fake.date_between(start_date="-2y", end_date="today").isoformat()
            invoice_id = fake.bothify(text="INV-#####")
            prompt = (
                f"Invoice {invoice_id}\n"
                f"Vendor: {company}\n"
                f"Total: {amount} {currency}\n"
                f"Invoice date: {date}\n"
                "Please extract the invoice information as JSON."
            )
            expected = {
                "invoice_id": invoice_id,
                "vendor": company,
                "total_amount": amount,
                "currency": currency,
                "invoice_date": date,
            }
            return prompt, expected

        # Fallback trivial template:
        prompt = "Synthetic example for schema_id=" + schema_id
        expected = {}  # TODO: build generically from schema if needed
        return prompt, expected
```

**Example faker_profiles.yaml**:
```yaml
invoice_basic:
  type: invoice_basic
patient_lab_result:
  type: lab_result
support_ticket:
  type: support_ticket
```

### 2.3 TeacherRouter

```python
# slm_edge_bench/core/teacher_router.py
from typing import Literal
from .schema_registry import SchemaInfo

TeacherName = Literal["qwen", "mistral", "phi4"]

class TeacherRouter:
    def __init__(self, default_teacher: TeacherName = "qwen"):
        self.default_teacher = default_teacher

    def pick_teacher(self, schema_info: SchemaInfo) -> TeacherName:
        # First use explicit hint from metadata
        hint = schema_info.meta.get("teacher_hint")
        if hint in ("qwen", "mistral", "phi4"):
            return hint

        # Fallback heuristics based on domain/complexity
        domain = schema_info.meta.get("domain", "")
        if domain in ("api", "integration"):
            return "mistral"
        if domain in ("medical", "STEM", "scientific"):
            return "phi4"
        # Qwen as broad generalist
        return self.default_teacher
```

### 2.4 vLLMWrapper (batched, one model at a time)

```python
# slm_edge_bench/core/vllm_wrapper.py
from typing import List, Dict
from dataclasses import dataclass
from vllm import LLM, SamplingParams

@dataclass
class ModelConfig:
    name: str      # "qwen3-14b" etc.
    hf_path: str   # Hugging Face model id
    max_tokens: int = 512
    temperature: float = 0.4
    top_p: float = 0.95

class VLLMWrapper:
    """
    Lightweight wrapper over vLLM that loads one model at a time.
    """

    def __init__(self, configs: Dict[str, ModelConfig]):
        self.configs = configs
        self.llm = None
        self.current_model_name = None

    def _ensure_model_loaded(self, model_key: str):
        if self.current_model_name == model_key and self.llm is not None:
            return
        # unload previous
        self.llm = None
        cfg = self.configs[model_key]
        self.llm = LLM(
            model=cfg.hf_path,
            dtype="auto",
            tensor_parallel_size=1,
        )
        self.current_model_name = model_key

    def generate(self, model_key: str, prompts: List[str]) -> List[str]:
        self._ensure_model_loaded(model_key)
        cfg = self.configs[model_key]
        sampling_params = SamplingParams(
            temperature=cfg.temperature,
            top_p=cfg.top_p,
            max_tokens=cfg.max_tokens,
        )
        outputs = self.llm.generate(prompts, sampling_params)
        # vLLM returns a list of RequestOutput; we take the first completion per prompt
        completions = []
        for out in outputs:
            text = out.outputs[0].text
            completions.append(text.strip())
        return completions
```

**Best practice for VRAM**:
- Use 4-bit / AWQ models
- One model loaded at a time
- Batch size 4–8
- Keep max_tokens modest (256–512)
- No insane context length

### 2.5 QualityValidator

```python
# slm_edge_bench/core/validator.py
import json
import re
from typing import Dict, Any, Tuple
from jsonschema import Draft7Validator

PLACEHOLDER_RE = re.compile(r"\b(sample_|test_|foo|bar|lorem ipsum)\b", re.IGNORECASE)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+?[0-9\-\s\(\)]{7,}$")

class QualityValidator:
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
        self.validator = Draft7Validator(schema)

    def _validate_schema(self, obj: Dict[str, Any]) -> bool:
        errors = list(self.validator.iter_errors(obj))
        return len(errors) == 0

    def _has_placeholders(self, s: str) -> bool:
        return bool(PLACEHOLDER_RE.search(s))

    def _check_contact_fields(self, obj: Dict[str, Any]) -> bool:
        """
        Optionally enforce that email/phone-like fields are realistic when present.
        """
        def walk(d: Any) -> bool:
            if isinstance(d, dict):
                for k, v in d.items():
                    if isinstance(v, str):
                        lk = k.lower()
                        if "email" in lk and v and not EMAIL_RE.match(v):
                            return False
                        if ("phone" in lk or "tel" in lk) and v and not PHONE_RE.match(v):
                            return False
                    if not walk(v):
                        return False
            elif isinstance(d, list):
                for x in d:
                    if not walk(x):
                        return False
            return True

        return walk(obj)

    def _check_semantic_alignment(self, prompt: str, obj: Dict[str, Any]) -> bool:
        """
        Cheap heuristic: require that at least some string values in the JSON
        appear in the prompt.
        """
        hits = 0
        total = 0

        def collect_strings(d: Any):
            nonlocal hits, total
            if isinstance(d, dict):
                for v in d.values():
                    collect_strings(v)
            elif isinstance(d, list):
                for v in d:
                    collect_strings(v)
            elif isinstance(d, str):
                total += 1
                if d and d.lower() in prompt.lower():
                    hits += 1

        collect_strings(obj)
        if total == 0:
            return True
        return hits / total >= 0.3  # tune threshold

    def validate_pair(self, prompt: str, output_text: str) -> Tuple[bool, str, Dict[str, Any] | None]:
        """
        Returns (ok, reason, parsed_json).
        """
        try:
            json_str = output_text.strip()
            # Strip markdown code blocks
            if "```" in json_str:
                json_str = json_str.split("```", 2)[1]
                json_str = json_str.replace("json", "", 1).strip()
            obj = json.loads(json_str)
        except Exception as e:
            return False, f"json_parse_error: {e}", None

        if not self._validate_schema(obj):
            return False, "schema_violation", None

        if self._has_placeholders(prompt) or self._has_placeholders(json.dumps(obj)):
            return False, "placeholders_detected", None

        if not self._check_contact_fields(obj):
            return False, "invalid_contact_format", None

        if not self._check_semantic_alignment(prompt, obj):
            return False, "weak_semantic_alignment", None

        return True, "ok", obj
```

---

## 3. Prompt Template for Teacher Models

```python
JSON_PROMPT_TEMPLATE = """You are a careful data extraction system.
You will be given a piece of unstructured or semi-structured text and a JSON schema.
Your job is to extract the relevant information and return a JSON object that strictly follows the schema.

- Do not include any extra keys.
- Use null for fields that cannot be determined.
- Use realistic values consistent with the input text.
- Output ONLY the JSON object, no extra text.

SCHEMA (JSON Schema):
{schema_json}

TEXT:
{text}
"""

def build_prompt(schema: Dict[str, Any], text: str) -> str:
    import json
    schema_str = json.dumps(schema, ensure_ascii=False, indent=2)
    return JSON_PROMPT_TEMPLATE.format(schema_json=schema_str, text=text)
```

**Alternative for function/API schemas**:
```python
FUNC_PROMPT_TEMPLATE = """You are an AI function that returns structured JSON.
Given a description of a request and a JSON schema, fill the schema fields.

RULES:
- Only output a JSON object.
- Respect types and allowed values from the schema description.
- If a field is not specified, use null or an empty string according to the schema.

SCHEMA:
{schema_json}

REQUEST:
{text}
"""
```

---

## 4. Best Practices for Memory Management with vLLM

**On 4080 SUPER (16.7GB)**:

1. **Use 4-bit / AWQ models**: Qwen3-14B-AWQ, Mistral-Small-24B-AWQ, Phi-4-14B-AWQ
2. **One model loaded at a time**: Lazily load requested teacher, set `self.llm = None` before loading another
3. **Batch generation**: Start with batch_size=4, test, bump to 8 if VRAM allows
4. **Keep max_tokens modest**: 256–512 for JSON generation (not novels)
5. **No insane context length**: Keep input length reasonable to avoid KV cache explosion
6. **Run each teacher in its own pass**: Generate all Mistral examples, then Qwen, then Phi

---

## 5. Efficient Validation and Filtering Strategy

**Goal**: 1,500 raw → best 1,000

### Step 1: Generate with oversampling per schema
- For each of 25 schemas: Target ~60 examples (30 template, 30 LLM) = 1,500 total

### Step 2: Validate each example
- Run QualityValidator on (prompt, output) with the schema
- If fails → drop or log as "bad"
- If passes → keep parsed JSON + metadata (schema_id, teacher, source_type)

### Step 3: Score examples (optional)
Assign quality score:
- +1 if JSONExact passes
- +1 if semantic alignment ratio > 0.6
- +1 if from teacher with high confidence
- –1 if prompt/JSON contain weird patterns

Or simpler: everything that passes = score 1

### Step 4: Balance across schemas & teachers
- Per schema: Take up to K examples (e.g., 40) sorted by score
- Combine across schemas
- If total > 1000, randomly subsample while preserving balance

### Step 5: Write final JSONL
```json
{
  "id": "edgejson_000123",
  "schema_id": "invoice_basic",
  "teacher": "mistral",
  "source": "llm",
  "prompt": "...",
  "expected_output": { ... }
}
```

---

## Next Steps

GPT offers to help with:
1. Teacher committee logic (ask two teachers, only keep samples where they agree)
2. Wire all components into pipeline.py with main() orchestration

**Status**: Awaiting CC-SLM assessment and approval

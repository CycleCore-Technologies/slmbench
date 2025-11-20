"""
Quality Validator - Multi-level validation for generated JSON examples.

Validates schema compliance, data realism, and semantic alignment.
"""

import json
import re
from typing import Dict, Any, Tuple, Optional
from jsonschema import Draft7Validator
from dataclasses import dataclass


# Regex patterns for validation
PLACEHOLDER_RE = re.compile(
    r"\b(sample_|test_|foo|bar|lorem ipsum|placeholder|example\.com|xxx|yyy|zzz)\b",
    re.IGNORECASE
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[+]?[0-9\-\s()]{7,}$")


@dataclass
class ValidationResult:
    """Result of validating a (prompt, output) pair."""
    valid: bool
    reason: str
    parsed_json: Optional[Dict[str, Any]] = None


class QualityValidator:
    """
    Multi-level validator for JSON extraction examples.

    Validation levels:
    1. JSON parsing
    2. Schema compliance
    3. Placeholder detection
    4. Contact field format validation
    5. Semantic alignment (prompt ↔ output)
    """

    def __init__(self, schema: Dict[str, Any], alignment_threshold: float = 0.3):
        """
        Initialize quality validator.

        Args:
            schema: JSON schema to validate against
            alignment_threshold: Minimum ratio of JSON values that should appear in prompt
        """
        self.schema = schema
        self.validator = Draft7Validator(schema)
        self.alignment_threshold = alignment_threshold

    def validate_pair(self, prompt: str, output_text: str) -> ValidationResult:
        """
        Validate a (prompt, output) pair.

        Args:
            prompt: Input text prompt
            output_text: Generated output (should be JSON)

        Returns:
            ValidationResult with validation status and details
        """
        # Level 1: Parse JSON
        try:
            json_str = self._clean_json_output(output_text)
            obj = json.loads(json_str)
        except Exception as e:
            return ValidationResult(
                valid=False,
                reason=f"json_parse_error: {str(e)[:100]}",
                parsed_json=None
            )

        # Level 2: Schema validation
        if not self._validate_schema(obj):
            return ValidationResult(
                valid=False,
                reason="schema_violation",
                parsed_json=None
            )

        # Level 3: Placeholder detection
        if self._has_placeholders(prompt) or self._has_placeholders(json.dumps(obj)):
            return ValidationResult(
                valid=False,
                reason="placeholders_detected",
                parsed_json=None
            )

        # Level 4: Contact field validation
        if not self._check_contact_fields(obj):
            return ValidationResult(
                valid=False,
                reason="invalid_contact_format",
                parsed_json=None
            )

        # Level 5: Semantic alignment
        if not self._check_semantic_alignment(prompt, obj):
            return ValidationResult(
                valid=False,
                reason="weak_semantic_alignment",
                parsed_json=None
            )

        # All checks passed
        return ValidationResult(
            valid=True,
            reason="ok",
            parsed_json=obj
        )

    def _clean_json_output(self, output_text: str) -> str:
        """Clean up JSON output by removing markdown code blocks, etc."""
        text = output_text.strip()

        # Remove markdown code blocks
        if "```" in text:
            # Extract content between first and last ```
            parts = text.split("```")
            if len(parts) >= 3:
                # Take the middle part (between first and last ```)
                text = parts[1]
                # Remove "json" language identifier if present
                text = re.sub(r"^\s*json\s*", "", text, flags=re.IGNORECASE)

        return text.strip()

    def _validate_schema(self, obj: Dict[str, Any]) -> bool:
        """Validate object against JSON schema."""
        errors = list(self.validator.iter_errors(obj))
        return len(errors) == 0

    def _has_placeholders(self, text: str) -> bool:
        """Check if text contains obvious placeholder values."""
        return bool(PLACEHOLDER_RE.search(text))

    def _check_contact_fields(self, obj: Dict[str, Any]) -> bool:
        """
        Validate that email and phone fields have realistic formats.

        Returns False if any email or phone field has invalid format.
        """
        def walk(d: Any) -> bool:
            if isinstance(d, dict):
                for key, value in d.items():
                    if isinstance(value, str):
                        key_lower = key.lower()
                        # Check email format
                        if "email" in key_lower and value:
                            if not EMAIL_RE.match(value):
                                return False
                        # Check phone format
                        if ("phone" in key_lower or "tel" in key_lower) and value:
                            if not PHONE_RE.match(value):
                                return False
                    # Recurse into nested structures
                    if not walk(value):
                        return False
            elif isinstance(d, list):
                for item in d:
                    if not walk(item):
                        return False
            return True

        return walk(obj)

    def _check_semantic_alignment(self, prompt: str, obj: Dict[str, Any]) -> bool:
        """
        Check that JSON values are semantically aligned with the prompt.

        Heuristic: At least X% of string values in the JSON should appear
        somewhere in the prompt text (case-insensitive).
        """
        hits = 0
        total = 0
        prompt_lower = prompt.lower()

        def collect_strings(d: Any):
            nonlocal hits, total
            if isinstance(d, dict):
                for value in d.values():
                    collect_strings(value)
            elif isinstance(d, list):
                for item in d:
                    collect_strings(item)
            elif isinstance(d, str):
                # Only check meaningful strings (length > 2)
                if len(d) > 2:
                    total += 1
                    # Check if this value appears in the prompt
                    if d.lower() in prompt_lower:
                        hits += 1

        collect_strings(obj)

        # If no strings to check, consider it valid
        if total == 0:
            return True

        # Require at least alignment_threshold ratio of strings to match
        alignment_ratio = hits / total
        return alignment_ratio >= self.alignment_threshold


class ValidationStats:
    """Track validation statistics across multiple examples."""

    def __init__(self):
        self.total = 0
        self.valid = 0
        self.reasons = {}

    def add(self, result: ValidationResult):
        """Add a validation result to stats."""
        self.total += 1
        if result.valid:
            self.valid += 1
        else:
            reason = result.reason
            self.reasons[reason] = self.reasons.get(reason, 0) + 1

    def summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        return {
            "total": self.total,
            "valid": self.valid,
            "invalid": self.total - self.valid,
            "pass_rate": round(self.valid / self.total * 100, 2) if self.total > 0 else 0,
            "failure_reasons": self.reasons
        }

    def __repr__(self):
        s = self.summary()
        return (
            f"ValidationStats(total={s['total']}, valid={s['valid']}, "
            f"pass_rate={s['pass_rate']}%)"
        )


if __name__ == "__main__":
    # Test the validator
    print("Testing QualityValidator\n")
    print("=" * 70)

    # Test schema
    test_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "phone": {"type": "string"}
        },
        "required": ["name", "email"],
        "additionalProperties": False
    }

    validator = QualityValidator(test_schema, alignment_threshold=0.3)

    # Test cases
    test_cases = [
        {
            "name": "Valid example",
            "prompt": "Contact: John Doe, email john.doe@example.com, phone +1-555-1234",
            "output": '{"name": "John Doe", "email": "john.doe@example.com", "phone": "+1-555-1234"}'
        },
        {
            "name": "Invalid JSON",
            "prompt": "Contact: Jane Smith",
            "output": '{"name": "Jane Smith", invalid json here'
        },
        {
            "name": "Schema violation (missing required field)",
            "prompt": "Contact: Bob Jones",
            "output": '{"name": "Bob Jones"}'
        },
        {
            "name": "Placeholder detected",
            "prompt": "Contact: Test User",
            "output": '{"name": "foo", "email": "test@example.com"}'
        },
        {
            "name": "Invalid email format",
            "prompt": "Contact: Alice Brown, email: alice",
            "output": '{"name": "Alice Brown", "email": "not-an-email"}'
        },
        {
            "name": "Weak semantic alignment",
            "prompt": "Contact: Charlie Davis",
            "output": '{"name": "Different Person", "email": "other@example.com"}'
        },
        {
            "name": "Valid with markdown code block",
            "prompt": "Contact: Eve Wilson, email eve@test.com, phone 555-9999",
            "output": '```json\n{"name": "Eve Wilson", "email": "eve@test.com", "phone": "555-9999"}\n```'
        }
    ]

    stats = ValidationStats()

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 70)
        result = validator.validate_pair(test_case["prompt"], test_case["output"])
        stats.add(result)

        print(f"  Valid: {result.valid}")
        print(f"  Reason: {result.reason}")
        if result.parsed_json:
            print(f"  Parsed JSON: {json.dumps(result.parsed_json, indent=2)}")

    print("\n" + "=" * 70)
    print("\nValidation Statistics:")
    print(stats)
    print(f"\nDetailed summary:")
    summary = stats.summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")

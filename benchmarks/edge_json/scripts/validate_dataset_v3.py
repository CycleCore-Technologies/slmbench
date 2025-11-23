#!/usr/bin/env python3
"""
Dataset Validation Script for EdgeJSON v3

Validates mathematical consistency for schemas with derived fields:
- shopping_cart: subtotal, tax, total calculations
- invoice: line_items, subtotal, tax, total_amount calculations
- order_details: total_amount from items

Usage:
    python validate_dataset_v3.py benchmarks/edge_json/data/edgejson_train_v2.jsonl
    python validate_dataset_v3.py benchmarks/edge_json/data/edgejson_test_v2.jsonl

Output:
    - Validation statistics
    - List of failed examples with detailed errors
    - Pass rate by schema

Author: CycleCore Technologies (with Claude Code)
Date: 2025-11-20
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ValidationResult:
    """Result of validating a single example."""
    valid: bool
    error: Optional[str] = None
    example_id: Optional[str] = None
    schema_id: Optional[str] = None


class MathValidator:
    """Validates mathematical consistency in generated examples."""

    TOLERANCE = 0.02  # $0.02 tolerance for rounding errors

    def validate_shopping_cart(self, output: Dict) -> ValidationResult:
        """
        Validate shopping_cart mathematical consistency.

        Expected relationships:
        - subtotal = sum(item.quantity * item.price * (1 - discount/100))
        - tax = subtotal * tax_rate (if present)
        - total = subtotal + shipping_cost + tax
        """
        try:
            # Calculate expected subtotal from items
            expected_subtotal = 0.0
            for item in output.get("items", []):
                item_total = item["quantity"] * item["price"]

                # Apply discount if present
                if "discount_percentage" in item and item["discount_percentage"] > 0:
                    item_total *= (1 - item["discount_percentage"] / 100)

                expected_subtotal += item_total

            expected_subtotal = round(expected_subtotal, 2)

            # Check subtotal if present
            if "subtotal" in output:
                actual_subtotal = output["subtotal"]
                if abs(expected_subtotal - actual_subtotal) > self.TOLERANCE:
                    return ValidationResult(
                        valid=False,
                        error=f"Subtotal mismatch: expected {expected_subtotal:.2f} "
                              f"(from items), got {actual_subtotal:.2f} "
                              f"(diff: {abs(expected_subtotal - actual_subtotal):.2f})"
                    )

            # Calculate expected total
            expected_total = output.get("subtotal", expected_subtotal)

            if "shipping_cost" in output:
                expected_total += output["shipping_cost"]

            if "tax" in output:
                expected_total += output["tax"]

            expected_total = round(expected_total, 2)

            # Check total
            if "total" in output:
                actual_total = output["total"]
                if abs(expected_total - actual_total) > self.TOLERANCE:
                    components = [f"subtotal: {output.get('subtotal', expected_subtotal):.2f}"]
                    if "shipping_cost" in output:
                        components.append(f"shipping: {output['shipping_cost']:.2f}")
                    if "tax" in output:
                        components.append(f"tax: {output['tax']:.2f}")

                    return ValidationResult(
                        valid=False,
                        error=f"Total mismatch: expected {expected_total:.2f} "
                              f"({' + '.join(components)}), got {actual_total:.2f} "
                              f"(diff: {abs(expected_total - actual_total):.2f})"
                    )

            return ValidationResult(valid=True)

        except Exception as e:
            return ValidationResult(valid=False, error=f"Validation error: {str(e)}")

    def validate_invoice(self, output: Dict) -> ValidationResult:
        """
        Validate invoice mathematical consistency.

        Expected relationships:
        - line_items[].total = quantity * unit_price
        - subtotal = sum(line_items[].total)
        - tax = subtotal * tax_rate (if tax_rate present)
        - total_amount = subtotal + tax
        """
        try:
            # Calculate expected subtotal from line items
            expected_subtotal = 0.0

            for idx, item in enumerate(output.get("line_items", [])):
                item_total = item["quantity"] * item["unit_price"]
                item_total = round(item_total, 2)

                # Check line item total if present
                if "total" in item:
                    if abs(item_total - item["total"]) > self.TOLERANCE:
                        return ValidationResult(
                            valid=False,
                            error=f"Line item {idx} total mismatch: "
                                  f"expected {item_total:.2f} "
                                  f"(qty: {item['quantity']} * price: {item['unit_price']:.2f}), "
                                  f"got {item['total']:.2f}"
                        )

                expected_subtotal += item_total

            expected_subtotal = round(expected_subtotal, 2)

            # Check subtotal if present
            if "subtotal" in output:
                actual_subtotal = output["subtotal"]
                if abs(expected_subtotal - actual_subtotal) > self.TOLERANCE:
                    return ValidationResult(
                        valid=False,
                        error=f"Subtotal mismatch: expected {expected_subtotal:.2f} "
                              f"(from line items), got {actual_subtotal:.2f} "
                              f"(diff: {abs(expected_subtotal - actual_subtotal):.2f})"
                    )

            # Calculate expected total
            expected_total = output.get("subtotal", expected_subtotal)

            if "tax" in output:
                expected_total += output["tax"]

            expected_total = round(expected_total, 2)

            # Check total_amount
            if "total_amount" in output:
                actual_total = output["total_amount"]
                if abs(expected_total - actual_total) > self.TOLERANCE:
                    components = [f"subtotal: {output.get('subtotal', expected_subtotal):.2f}"]
                    if "tax" in output:
                        components.append(f"tax: {output['tax']:.2f}")

                    return ValidationResult(
                        valid=False,
                        error=f"Total amount mismatch: expected {expected_total:.2f} "
                              f"({' + '.join(components)}), got {actual_total:.2f} "
                              f"(diff: {abs(expected_total - actual_total):.2f})"
                    )

            return ValidationResult(valid=True)

        except Exception as e:
            return ValidationResult(valid=False, error=f"Validation error: {str(e)}")

    def validate_order_details(self, output: Dict) -> ValidationResult:
        """
        Validate order_details mathematical consistency.

        Expected relationships:
        - total_amount = sum(item.quantity * item.price)
        """
        try:
            # Calculate expected total from items
            expected_total = 0.0

            for item in output.get("items", []):
                expected_total += item["quantity"] * item["price"]

            expected_total = round(expected_total, 2)

            # Check total_amount
            if "total_amount" in output:
                actual_total = output["total_amount"]
                if abs(expected_total - actual_total) > self.TOLERANCE:
                    return ValidationResult(
                        valid=False,
                        error=f"Total amount mismatch: expected {expected_total:.2f} "
                              f"(from items), got {actual_total:.2f} "
                              f"(diff: {abs(expected_total - actual_total):.2f})"
                    )

            return ValidationResult(valid=True)

        except Exception as e:
            return ValidationResult(valid=False, error=f"Validation error: {str(e)}")

    def validate_example(self, example: Dict) -> ValidationResult:
        """Validate a single example based on its schema."""
        schema_id = example.get("schema_id", example.get("schema_name", "unknown"))
        output = example.get("expected_output", {})

        result = ValidationResult(valid=True, schema_id=schema_id)

        # Check if this schema requires math validation
        if schema_id == "shopping_cart":
            result = self.validate_shopping_cart(output)
        elif schema_id == "invoice":
            result = self.validate_invoice(output)
        elif schema_id == "order_details":
            result = self.validate_order_details(output)

        # Attach metadata
        result.schema_id = schema_id
        result.example_id = example.get("id", "unknown")

        return result


class DatasetValidator:
    """Validates an entire dataset file."""

    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        self.validator = MathValidator()
        self.results: List[ValidationResult] = []
        self.examples: List[Dict] = []

    def load_dataset(self) -> List[Dict]:
        """Load dataset from JSONL file."""
        examples = []

        with open(self.dataset_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    example = json.loads(line)
                    examples.append(example)
                except json.JSONDecodeError as e:
                    print(f"⚠️  JSON parse error on line {line_num}: {e}")

        return examples

    def validate(self) -> Tuple[List[ValidationResult], Dict]:
        """
        Validate all examples in the dataset.

        Returns:
            Tuple of (results list, statistics dict)
        """
        print(f"Loading dataset from {self.dataset_path}...")
        self.examples = self.load_dataset()
        print(f"✓ Loaded {len(self.examples)} examples\n")

        print("Validating examples...")
        self.results = []

        for idx, example in enumerate(self.examples):
            result = self.validator.validate_example(example)
            self.results.append(result)

            if (idx + 1) % 50 == 0:
                print(f"  Validated {idx + 1}/{len(self.examples)} examples...")

        print(f"✓ Validated {len(self.examples)} examples\n")

        # Calculate statistics
        stats = self._calculate_statistics()

        return self.results, stats

    def _calculate_statistics(self) -> Dict:
        """Calculate validation statistics."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.valid)
        failed = total - passed

        # Group by schema
        by_schema = defaultdict(lambda: {"total": 0, "passed": 0, "failed": 0})

        for result in self.results:
            schema = result.schema_id or "unknown"
            by_schema[schema]["total"] += 1
            if result.valid:
                by_schema[schema]["passed"] += 1
            else:
                by_schema[schema]["failed"] += 1

        # Failed examples
        failed_examples = [r for r in self.results if not r.valid]

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "by_schema": dict(by_schema),
            "failed_examples": failed_examples
        }

    def print_report(self, stats: Dict):
        """Print validation report to console."""
        print("=" * 80)
        print("VALIDATION REPORT")
        print("=" * 80)
        print()

        # Overall statistics
        print(f"Dataset: {self.dataset_path}")
        print(f"Total examples: {stats['total']}")
        print(f"✓ Passed: {stats['passed']} ({stats['pass_rate']:.1f}%)")
        print(f"✗ Failed: {stats['failed']} ({100 - stats['pass_rate']:.1f}%)")
        print()

        # By schema
        print("Validation by Schema:")
        print("-" * 80)
        print(f"{'Schema':<30} {'Total':>8} {'Passed':>8} {'Failed':>8} {'Pass %':>10}")
        print("-" * 80)

        for schema, counts in sorted(stats["by_schema"].items()):
            pass_pct = (counts["passed"] / counts["total"] * 100) if counts["total"] > 0 else 0
            print(f"{schema:<30} {counts['total']:>8} {counts['passed']:>8} "
                  f"{counts['failed']:>8} {pass_pct:>9.1f}%")

        print()

        # Failed examples
        if stats["failed"] > 0:
            print(f"Failed Examples ({len(stats['failed_examples'])}):")
            print("-" * 80)

            for idx, result in enumerate(stats['failed_examples'][:20], 1):  # Show first 20
                print(f"{idx}. Schema: {result.schema_id}, ID: {result.example_id}")
                print(f"   Error: {result.error}")
                print()

            if len(stats['failed_examples']) > 20:
                print(f"... and {len(stats['failed_examples']) - 20} more failures")

        print("=" * 80)

        # Final verdict
        if stats["pass_rate"] == 100.0:
            print("✓ VALIDATION PASSED: 100% of examples are valid")
        else:
            print(f"✗ VALIDATION FAILED: {stats['failed']} examples have errors")
            print("  → Fix these issues before proceeding to training")

        print("=" * 80)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python validate_dataset_v3.py <dataset.jsonl>")
        print()
        print("Examples:")
        print("  python validate_dataset_v3.py benchmarks/edge_json/data/edgejson_train_v2.jsonl")
        print("  python validate_dataset_v3.py benchmarks/edge_json/data/edgejson_test_v2.jsonl")
        sys.exit(1)

    dataset_path = sys.argv[1]

    if not Path(dataset_path).exists():
        print(f"Error: Dataset file not found: {dataset_path}")
        sys.exit(1)

    # Run validation
    validator = DatasetValidator(dataset_path)
    results, stats = validator.validate()
    validator.print_report(stats)

    # Exit with error code if validation failed
    if stats["pass_rate"] < 100.0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

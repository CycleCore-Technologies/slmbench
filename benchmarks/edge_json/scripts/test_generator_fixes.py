#!/usr/bin/env python3
"""
Test script to validate template generator fixes.

Generates 10 examples from affected schemas (shopping_cart, invoice, order_details)
and validates them using the validation script.

Expected: 100% pass rate (30/30 examples valid)

Author: CycleCore Technologies (with Claude Code)
Date: 2025-11-20
"""

import json
import sys
from pathlib import Path

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from schema_loader import SchemaLoader
from template_generator import TemplateGenerator

# Import validator from validation script
sys.path.insert(0, str(Path(__file__).parent))
from validate_dataset_v3 import MathValidator


def test_generator():
    """Test the fixed template generator on 10 examples per affected schema."""

    # Initialize components
    schemas_root = Path(__file__).parent.parent / "schemas"
    loader = SchemaLoader(schemas_root)
    generator = TemplateGenerator(seed=42)
    validator = MathValidator()

    # Schemas to test (those with derived fields)
    test_schemas = ["shopping_cart", "invoice", "order_details"]
    examples_per_schema = 10

    print("=" * 80)
    print("TESTING TEMPLATE GENERATOR FIXES")
    print("=" * 80)
    print()
    print(f"Generating {examples_per_schema} examples per schema...")
    print(f"Schemas: {', '.join(test_schemas)}")
    print()

    all_results = []
    total_examples = 0
    total_passed = 0
    total_failed = 0

    for schema_id in test_schemas:
        print(f"Testing {schema_id}...")

        # Load schema
        try:
            schema_info = loader.get(schema_id)
        except Exception as e:
            print(f"  ✗ Failed to load schema: {e}")
            continue

        # Generate examples
        schema_results = []
        for i in range(examples_per_schema):
            try:
                # Generate example
                prompt, expected_output = generator.generate_for_schema(
                    schema_info.schema_id,
                    schema_info.schema
                )

                # Create example dict for validation
                example = {
                    "id": f"test_{schema_id}_{i:03d}",
                    "schema_id": schema_id,
                    "prompt": prompt,
                    "expected_output": expected_output
                }

                # Validate example
                result = validator.validate_example(example)
                schema_results.append(result)

                if result.valid:
                    total_passed += 1
                else:
                    total_failed += 1
                    print(f"  ✗ Example {i}: {result.error}")

                total_examples += 1

            except Exception as e:
                print(f"  ✗ Error generating example {i}: {e}")
                total_failed += 1
                total_examples += 1

        # Report schema results
        schema_passed = sum(1 for r in schema_results if r.valid)
        schema_failed = len(schema_results) - schema_passed

        if schema_passed == len(schema_results):
            print(f"  ✓ {schema_id}: {schema_passed}/{len(schema_results)} passed (100%)")
        else:
            print(f"  ✗ {schema_id}: {schema_passed}/{len(schema_results)} passed ({schema_passed/len(schema_results)*100:.1f}%)")

        all_results.extend(schema_results)
        print()

    # Final report
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print()
    print(f"Total examples: {total_examples}")
    print(f"✓ Passed: {total_passed} ({total_passed/total_examples*100:.1f}%)")
    print(f"✗ Failed: {total_failed} ({total_failed/total_examples*100:.1f}%)")
    print()

    if total_failed == 0:
        print("✓ TEST PASSED: All examples are mathematically consistent!")
        print("  → Generator fixes are working correctly")
        print("  → Ready to proceed with bulk regeneration")
        print()
        return 0
    else:
        print("✗ TEST FAILED: Some examples still have math errors")
        print("  → Review failed examples above")
        print("  → Fix generator before proceeding")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(test_generator())

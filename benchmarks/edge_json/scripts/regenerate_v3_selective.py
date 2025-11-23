#!/usr/bin/env python3
"""
Selective Regeneration Script for EdgeJSON v3

Creates v3 dataset by:
1. Keeping clean examples from v2 (695 examples)
2. Regenerating corrupted examples with fixed template generator (92 examples)
3. Optionally adding new examples to boost underrepresented schemas

Usage:
    python regenerate_v3_selective.py --input-train benchmarks/edge_json/data/edgejson_train_v2.jsonl \
                                       --input-test benchmarks/edge_json/data/edgejson_test_v2.jsonl \
                                       --output-train benchmarks/edge_json/data/edgejson_train_v3.jsonl \
                                       --output-test benchmarks/edge_json/data/edgejson_test_v3.jsonl

Author: CycleCore Technologies (with Claude Code)
Date: 2025-11-20
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict, Counter

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from schema_loader import SchemaLoader
from template_generator import TemplateGenerator
from validate_dataset_v3 import MathValidator


def load_jsonl(path: Path) -> List[Dict]:
    """Load JSONL file into list of dicts."""
    examples = []
    with open(path, 'r') as f:
        for line in f:
            examples.append(json.loads(line))
    return examples


def save_jsonl(examples: List[Dict], path: Path):
    """Save list of dicts to JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')


def identify_corrupted(examples: List[Dict], validator: MathValidator) -> Set[str]:
    """Identify IDs of corrupted examples."""
    corrupted_ids = set()

    for example in examples:
        result = validator.validate_example(example)
        if not result.valid:
            corrupted_ids.add(example['id'])

    return corrupted_ids


def regenerate_example(example_id: str, schema_id: str, loader: SchemaLoader,
                      generator: TemplateGenerator) -> Dict:
    """Regenerate a single example with fixed template generator."""

    schema_info = loader.get(schema_id)

    # Generate new example
    prompt, expected_output = generator.generate_for_schema(
        schema_info.schema_id,
        schema_info.schema
    )

    # Create example dict with same ID structure
    new_example = {
        "id": example_id,
        "schema_id": schema_id,
        "schema_name": schema_id,
        "prompt": prompt,
        "expected_output": expected_output
    }

    return new_example


def selective_regeneration(input_path: Path, output_path: Path, split: str,
                          loader: SchemaLoader, generator: TemplateGenerator,
                          validator: MathValidator) -> Dict:
    """
    Perform selective regeneration on a dataset split.

    Args:
        input_path: Path to input v2 dataset
        output_path: Path to output v3 dataset
        split: "train" or "test"
        loader: Schema loader
        generator: Template generator (fixed)
        validator: Math validator

    Returns:
        Statistics dict
    """

    print(f"\n{'=' * 80}")
    print(f"Processing {split.upper()} split")
    print(f"{'=' * 80}\n")

    # Load v2 examples
    print(f"Loading {input_path}...")
    v2_examples = load_jsonl(input_path)
    print(f"✓ Loaded {len(v2_examples)} examples\n")

    # Identify corrupted examples
    print("Identifying corrupted examples...")
    corrupted_ids = identify_corrupted(v2_examples, validator)
    print(f"✓ Found {len(corrupted_ids)} corrupted examples")
    print(f"✓ Found {len(v2_examples) - len(corrupted_ids)} clean examples\n")

    # Separate clean and corrupted
    clean_examples = []
    corrupted_examples = []

    for example in v2_examples:
        if example['id'] in corrupted_ids:
            corrupted_examples.append(example)
        else:
            clean_examples.append(example)

    print(f"Clean examples to keep: {len(clean_examples)}")
    print(f"Corrupted examples to regenerate: {len(corrupted_examples)}")

    # Show breakdown by schema
    corrupted_by_schema = Counter(ex['schema_id'] for ex in corrupted_examples)
    print("\nCorrupted by schema:")
    for schema_id, count in sorted(corrupted_by_schema.items()):
        print(f"  - {schema_id}: {count}")
    print()

    # Regenerate corrupted examples
    print(f"Regenerating {len(corrupted_examples)} corrupted examples...")
    regenerated = []

    for i, old_example in enumerate(corrupted_examples):
        try:
            new_example = regenerate_example(
                old_example['id'],
                old_example['schema_id'],
                loader,
                generator
            )

            # Validate regenerated example
            result = validator.validate_example(new_example)

            if result.valid:
                regenerated.append(new_example)
            else:
                print(f"  ✗ Warning: Regenerated example {old_example['id']} still invalid: {result.error}")
                # Keep it anyway for now, will be caught in final validation
                regenerated.append(new_example)

            if (i + 1) % 10 == 0:
                print(f"  Regenerated {i + 1}/{len(corrupted_examples)}...")

        except Exception as e:
            print(f"  ✗ Error regenerating {old_example['id']}: {e}")

    print(f"✓ Regenerated {len(regenerated)}/{len(corrupted_examples)} examples\n")

    # Combine clean + regenerated
    v3_examples = clean_examples + regenerated

    print(f"v3 dataset composition:")
    print(f"  - Clean from v2: {len(clean_examples)}")
    print(f"  - Regenerated: {len(regenerated)}")
    print(f"  - Total: {len(v3_examples)}\n")

    # Save v3 dataset
    print(f"Saving {output_path}...")
    save_jsonl(v3_examples, output_path)
    print(f"✓ Saved {len(v3_examples)} examples\n")

    # Statistics
    stats = {
        "split": split,
        "v2_total": len(v2_examples),
        "clean": len(clean_examples),
        "corrupted": len(corrupted_ids),
        "regenerated": len(regenerated),
        "v3_total": len(v3_examples),
        "corrupted_by_schema": dict(corrupted_by_schema)
    }

    return stats


def main():
    parser = argparse.ArgumentParser(description="Selective regeneration for EdgeJSON v3")
    parser.add_argument("--input-train", type=Path, required=True, help="Input train v2 dataset")
    parser.add_argument("--input-test", type=Path, required=True, help="Input test v2 dataset")
    parser.add_argument("--output-train", type=Path, required=True, help="Output train v3 dataset")
    parser.add_argument("--output-test", type=Path, required=True, help="Output test v3 dataset")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")

    args = parser.parse_args()

    print("=" * 80)
    print("EDGEJSON V3 SELECTIVE REGENERATION")
    print("=" * 80)
    print()
    print("Strategy:")
    print("  1. Validate v2 examples")
    print("  2. Keep clean examples (695 expected)")
    print("  3. Regenerate corrupted examples (92 expected)")
    print("  4. Create v3 datasets with fixed examples")
    print()

    # Initialize components
    schemas_root = Path(__file__).parent.parent / "schemas"
    loader = SchemaLoader(schemas_root)
    generator = TemplateGenerator(seed=args.seed)
    validator = MathValidator()

    # Process train split
    train_stats = selective_regeneration(
        args.input_train,
        args.output_train,
        "train",
        loader,
        generator,
        validator
    )

    # Process test split
    test_stats = selective_regeneration(
        args.input_test,
        args.output_test,
        "test",
        loader,
        generator,
        validator
    )

    # Final summary
    print("=" * 80)
    print("REGENERATION COMPLETE")
    print("=" * 80)
    print()

    print("Train split:")
    print(f"  v2: {train_stats['v2_total']} examples")
    print(f"  v3: {train_stats['v3_total']} examples ({train_stats['clean']} clean + {train_stats['regenerated']} regenerated)")
    print()

    print("Test split:")
    print(f"  v2: {test_stats['v2_total']} examples")
    print(f"  v3: {test_stats['v3_total']} examples ({test_stats['clean']} clean + {test_stats['regenerated']} regenerated)")
    print()

    print("Total:")
    total_v2 = train_stats['v2_total'] + test_stats['v2_total']
    total_v3 = train_stats['v3_total'] + test_stats['v3_total']
    total_clean = train_stats['clean'] + test_stats['clean']
    total_regen = train_stats['regenerated'] + test_stats['regenerated']

    print(f"  v2: {total_v2} examples")
    print(f"  v3: {total_v3} examples ({total_clean} clean + {total_regen} regenerated)")
    print()

    print("Next steps:")
    print("  1. Run comprehensive validation: python benchmarks/edge_json/scripts/validate_dataset_v3.py <v3_file>")
    print("  2. If 100% pass rate, proceed to training")
    print("  3. If failures remain, debug and regenerate again")
    print()


if __name__ == "__main__":
    main()

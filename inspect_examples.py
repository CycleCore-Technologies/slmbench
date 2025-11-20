#!/usr/bin/env python3
"""Inspect EdgeJSON dataset examples."""

import json
from pathlib import Path
from collections import defaultdict

data_dir = Path("/home/rain/SLMBench/benchmarks/edge_json/data")

# Load examples
train_examples = []
with open(data_dir / "edgejson_train_v2.jsonl") as f:
    for line in f:
        train_examples.append(json.loads(line))

test_examples = []
with open(data_dir / "edgejson_test_v2.jsonl") as f:
    for line in f:
        test_examples.append(json.loads(line))

print("=" * 80)
print("EdgeJSON Dataset Inspection")
print("=" * 80)
print(f"\nTotal examples: {len(train_examples) + len(test_examples)}")
print(f"Train: {len(train_examples)} | Test: {len(test_examples)}")

# Distribution by complexity
by_complexity = defaultdict(int)
by_schema = defaultdict(int)
by_source = defaultdict(int)

for ex in train_examples + test_examples:
    by_complexity[ex['complexity']] += 1
    by_schema[ex['schema_id']] += 1
    by_source[ex['source']] += 1

print("\n" + "=" * 80)
print("Distribution by Complexity")
print("=" * 80)
for comp in ["simple", "medium", "complex"]:
    count = by_complexity[comp]
    pct = count / (len(train_examples) + len(test_examples)) * 100
    print(f"{comp:10s}: {count:3d} ({pct:5.1f}%)")

print("\n" + "=" * 80)
print("Distribution by Source")
print("=" * 80)
for source in ["template", "llm"]:
    count = by_source[source]
    pct = count / (len(train_examples) + len(test_examples)) * 100
    print(f"{source:10s}: {count:3d} ({pct:5.1f}%)")

print("\n" + "=" * 80)
print("Sample Examples")
print("=" * 80)

# Show 1 simple, 1 medium, 1 complex from each source
for complexity in ["simple", "medium", "complex"]:
    for source in ["template", "llm"]:
        # Find example
        example = None
        for ex in train_examples:
            if ex['complexity'] == complexity and ex['source'] == source:
                example = ex
                break

        if not example:
            continue

        print(f"\n{'─' * 80}")
        print(f"Schema: {example['schema_id']} | Complexity: {complexity} | Source: {source}")
        print(f"{'─' * 80}")
        print(f"\nPrompt (first 200 chars):")
        print(example['prompt'][:200] + "..." if len(example['prompt']) > 200 else example['prompt'])
        print(f"\nExpected Output:")
        print(json.dumps(example['expected_output'], indent=2, ensure_ascii=False)[:400])
        if len(json.dumps(example['expected_output'])) > 400:
            print("...")

print("\n" + "=" * 80)
print("Schema Coverage")
print("=" * 80)
for schema_id in sorted(by_schema.keys()):
    count = by_schema[schema_id]
    print(f"{schema_id:30s}: {count:3d} examples")

print("\n" + "=" * 80)

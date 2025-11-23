#!/usr/bin/env python3
"""
Schema Distribution Analyzer for EdgeJSON Dataset

Analyzes schema distribution across training and test sets to identify
potential data coverage issues.

Usage:
    python analyze_schema_distribution.py \
        --train benchmarks/edge_json/data/edgejson_train_v2.jsonl \
        --test benchmarks/edge_json/data/edgejson_test_v2.jsonl \
        --output results/schema_distribution_analysis.json
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List


def load_dataset(path: str) -> List[Dict]:
    """Load JSONL dataset"""
    dataset = []
    with open(path, 'r') as f:
        for line in f:
            dataset.append(json.loads(line))
    return dataset


def analyze_schema_distribution(dataset: List[Dict], split_name: str) -> Dict:
    """Analyze schema distribution in a dataset"""
    schema_counts = Counter()
    complexity_counts = Counter()
    schema_by_complexity = defaultdict(lambda: Counter())

    for example in dataset:
        schema = example.get("schema_id", example.get("schema_name", "unknown"))
        complexity = example.get("complexity", "unknown")

        schema_counts[schema] += 1
        complexity_counts[complexity] += 1
        schema_by_complexity[complexity][schema] += 1

    return {
        "split": split_name,
        "total_examples": len(dataset),
        "num_schemas": len(schema_counts),
        "schema_counts": dict(schema_counts),
        "complexity_counts": dict(complexity_counts),
        "schema_by_complexity": {
            comp: dict(schemas) for comp, schemas in schema_by_complexity.items()
        }
    }


def compare_distributions(train_analysis: Dict, test_analysis: Dict) -> Dict:
    """Compare training and test distributions"""
    train_schemas = set(train_analysis["schema_counts"].keys())
    test_schemas = set(test_analysis["schema_counts"].keys())

    # Find coverage issues
    schemas_only_in_train = train_schemas - test_schemas
    schemas_only_in_test = test_schemas - train_schemas
    common_schemas = train_schemas & test_schemas

    # Calculate representation ratios
    representation_ratios = {}
    for schema in common_schemas:
        train_count = train_analysis["schema_counts"][schema]
        test_count = test_analysis["schema_counts"][schema]
        train_pct = train_count / train_analysis["total_examples"]
        test_pct = test_count / test_analysis["total_examples"]

        representation_ratios[schema] = {
            "train_count": train_count,
            "test_count": test_count,
            "train_percentage": train_pct * 100,
            "test_percentage": test_pct * 100,
            "ratio": test_pct / train_pct if train_pct > 0 else float('inf')
        }

    # Find underrepresented schemas (in training relative to test)
    underrepresented = sorted(
        [(schema, stats) for schema, stats in representation_ratios.items()
         if stats["ratio"] > 1.5],  # Test has 1.5x more than training (proportionally)
        key=lambda x: x[1]["ratio"],
        reverse=True
    )

    # Find overrepresented schemas (in training relative to test)
    overrepresented = sorted(
        [(schema, stats) for schema, stats in representation_ratios.items()
         if stats["ratio"] < 0.67],  # Training has 1.5x more than test (proportionally)
        key=lambda x: x[1]["ratio"]
    )

    return {
        "common_schemas": list(common_schemas),
        "schemas_only_in_train": list(schemas_only_in_train),
        "schemas_only_in_test": list(schemas_only_in_test),
        "representation_ratios": representation_ratios,
        "underrepresented_in_training": [
            {"schema": schema, **stats} for schema, stats in underrepresented
        ],
        "overrepresented_in_training": [
            {"schema": schema, **stats} for schema, stats in overrepresented
        ]
    }


def generate_summary_report(train_analysis: Dict, test_analysis: Dict, comparison: Dict) -> str:
    """Generate a text summary of the analysis"""
    report = []
    report.append("=" * 60)
    report.append("EdgeJSON Schema Distribution Analysis")
    report.append("=" * 60)
    report.append("")

    # Overall stats
    report.append("Dataset Overview:")
    report.append(f"  Training: {train_analysis['total_examples']} examples across {train_analysis['num_schemas']} schemas")
    report.append(f"  Test: {test_analysis['total_examples']} examples across {test_analysis['num_schemas']} schemas")
    report.append("")

    # Complexity distribution
    report.append("Complexity Distribution:")
    report.append("  Training:")
    for complexity, count in sorted(train_analysis["complexity_counts"].items()):
        pct = (count / train_analysis['total_examples']) * 100
        report.append(f"    {complexity}: {count} ({pct:.1f}%)")
    report.append("  Test:")
    for complexity, count in sorted(test_analysis["complexity_counts"].items()):
        pct = (count / test_analysis['total_examples']) * 100
        report.append(f"    {complexity}: {count} ({pct:.1f}%)")
    report.append("")

    # Schema coverage
    report.append("Schema Coverage:")
    report.append(f"  Common schemas: {len(comparison['common_schemas'])}")
    report.append(f"  Only in training: {len(comparison['schemas_only_in_train'])}")
    report.append(f"  Only in test: {len(comparison['schemas_only_in_test'])}")

    if comparison["schemas_only_in_test"]:
        report.append("")
        report.append("  ⚠️  WARNING: Schemas in test but NOT in training:")
        for schema in comparison["schemas_only_in_test"]:
            test_count = test_analysis["schema_counts"][schema]
            report.append(f"    - {schema}: {test_count} test examples (NEVER SEEN IN TRAINING!)")

    report.append("")

    # Underrepresented schemas
    if comparison["underrepresented_in_training"]:
        report.append("Underrepresented Schemas (proportionally less in training than test):")
        for item in comparison["underrepresented_in_training"][:10]:
            schema = item["schema"]
            report.append(f"  - {schema}:")
            report.append(f"      Train: {item['train_count']} ({item['train_percentage']:.1f}%)")
            report.append(f"      Test: {item['test_count']} ({item['test_percentage']:.1f}%)")
            report.append(f"      Ratio: {item['ratio']:.2f}x (test has {item['ratio']:.2f}x more)")
        report.append("")

    # Overrepresented schemas
    if comparison["overrepresented_in_training"]:
        report.append("Overrepresented Schemas (proportionally more in training than test):")
        for item in comparison["overrepresented_in_training"][:10]:
            schema = item["schema"]
            report.append(f"  - {schema}:")
            report.append(f"      Train: {item['train_count']} ({item['train_percentage']:.1f}%)")
            report.append(f"      Test: {item['test_count']} ({item['test_percentage']:.1f}%)")
            report.append(f"      Ratio: {item['ratio']:.2f}x (train has {1/item['ratio']:.2f}x more)")
        report.append("")

    # Recommendations
    report.append("=" * 60)
    report.append("Recommendations")
    report.append("=" * 60)

    if comparison["schemas_only_in_test"]:
        report.append("")
        report.append("🚨 CRITICAL: Test set contains schemas never seen in training!")
        report.append("   → Model cannot learn these schemas and will fail on them")
        report.append("   → Either remove these from test set or add to training set")

    if len(comparison["underrepresented_in_training"]) > 5:
        report.append("")
        report.append("⚠️  SIGNIFICANT: Many schemas are underrepresented in training")
        report.append("   → Consider rebalancing training data")
        report.append("   → Or use weighted sampling during training")

    report.append("")

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Analyze EdgeJSON schema distribution")
    parser.add_argument("--train", type=str, required=True, help="Path to training JSONL")
    parser.add_argument("--test", type=str, required=True, help="Path to test JSONL")
    parser.add_argument("--output", type=str, help="Path to save analysis JSON (optional)")

    args = parser.parse_args()

    # Load datasets
    print(f"Loading training data: {args.train}")
    train_data = load_dataset(args.train)

    print(f"Loading test data: {args.test}")
    test_data = load_dataset(args.test)

    # Analyze distributions
    print("\nAnalyzing distributions...")
    train_analysis = analyze_schema_distribution(train_data, "training")
    test_analysis = analyze_schema_distribution(test_data, "test")

    # Compare distributions
    print("Comparing training vs test...")
    comparison = compare_distributions(train_analysis, test_analysis)

    # Generate summary report
    report = generate_summary_report(train_analysis, test_analysis, comparison)
    print("\n" + report)

    # Save detailed analysis if output specified
    if args.output:
        output_data = {
            "training": train_analysis,
            "test": test_analysis,
            "comparison": comparison
        }

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\nDetailed analysis saved to: {output_path}")


if __name__ == "__main__":
    main()

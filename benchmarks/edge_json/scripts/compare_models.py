# Copyright 2025 CycleCore Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python3
"""
Model Comparison Script for EdgeJSON Benchmark

Compares two evaluation results (e.g., base model vs fine-tuned model)
and generates detailed comparison metrics.

Usage:
    python compare_models.py \
        --baseline results/base_model_evaluation.json \
        --comparison results/fine_tuned_evaluation.json \
        --output results/comparison_data.json
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class ComparisonMetrics:
    """Comparison metrics between two models"""
    baseline_value: float
    comparison_value: float
    absolute_change: float
    relative_change: float  # Percentage
    improvement_ratio: float  # comparison / baseline


def calculate_comparison(baseline: float, comparison: float) -> ComparisonMetrics:
    """Calculate comparison metrics between two values"""
    absolute_change = comparison - baseline

    # Avoid division by zero
    if baseline == 0:
        relative_change = 0.0 if comparison == 0 else float('inf')
        improvement_ratio = 0.0 if comparison == 0 else float('inf')
    else:
        relative_change = (absolute_change / baseline) * 100
        improvement_ratio = comparison / baseline

    return ComparisonMetrics(
        baseline_value=baseline,
        comparison_value=comparison,
        absolute_change=absolute_change,
        relative_change=relative_change,
        improvement_ratio=improvement_ratio
    )


def compare_overall_metrics(baseline_data: Dict, comparison_data: Dict) -> Dict:
    """Compare overall metrics between two models"""
    baseline_agg = baseline_data["aggregate"]
    comparison_agg = comparison_data["aggregate"]

    overall_comparison = {
        "json_exact": asdict(calculate_comparison(
            baseline_agg["json_exact_score"],
            comparison_agg["json_exact_score"]
        )),
        "field_f1": asdict(calculate_comparison(
            baseline_agg["avg_field_f1"],
            comparison_agg["avg_field_f1"]
        )),
        "schema_compliance": asdict(calculate_comparison(
            baseline_agg["schema_compliance_rate"],
            comparison_agg["schema_compliance_rate"]
        )),
        "latency_ms": asdict(calculate_comparison(
            baseline_agg["avg_latency_ms"],
            comparison_agg["avg_latency_ms"]
        )),
        "tokens_per_sec": asdict(calculate_comparison(
            baseline_agg["tokens_per_sec"],
            comparison_agg["tokens_per_sec"]
        ))
    }

    return overall_comparison


def compare_by_complexity(baseline_data: Dict, comparison_data: Dict) -> Dict:
    """Compare metrics by complexity level"""
    baseline_agg = baseline_data["aggregate"]
    comparison_agg = comparison_data["aggregate"]

    complexity_comparison = {}

    for complexity in ["simple", "medium", "complex"]:
        if complexity not in baseline_agg["by_complexity"]:
            continue

        baseline_stats = baseline_agg["by_complexity"][complexity]
        comparison_stats = comparison_agg["by_complexity"][complexity]

        complexity_comparison[complexity] = {
            "json_exact": asdict(calculate_comparison(
                baseline_stats["json_exact"],
                comparison_stats["json_exact"]
            )),
            "field_f1": asdict(calculate_comparison(
                baseline_stats["avg_field_f1"],
                comparison_stats["avg_field_f1"]
            )),
            "schema_compliance": asdict(calculate_comparison(
                baseline_stats["schema_compliance"],
                comparison_stats["schema_compliance"]
            ))
        }

    return complexity_comparison


def compare_by_schema(baseline_data: Dict, comparison_data: Dict) -> Dict:
    """Compare metrics by schema type"""
    baseline_agg = baseline_data["aggregate"]
    comparison_agg = comparison_data["aggregate"]

    schema_comparison = {}

    # Get all schemas from both datasets
    all_schemas = set(baseline_agg["by_schema"].keys()) | set(comparison_agg["by_schema"].keys())

    for schema in all_schemas:
        baseline_stats = baseline_agg["by_schema"].get(schema, {
            "json_exact": 0.0,
            "avg_field_f1": 0.0,
            "schema_compliance": 0.0
        })

        comparison_stats = comparison_agg["by_schema"].get(schema, {
            "json_exact": 0.0,
            "avg_field_f1": 0.0,
            "schema_compliance": 0.0
        })

        schema_comparison[schema] = {
            "json_exact": asdict(calculate_comparison(
                baseline_stats["json_exact"],
                comparison_stats["json_exact"]
            )),
            "field_f1": asdict(calculate_comparison(
                baseline_stats["avg_field_f1"],
                comparison_stats["avg_field_f1"]
            )),
            "schema_compliance": asdict(calculate_comparison(
                baseline_stats["schema_compliance"],
                comparison_stats["schema_compliance"]
            ))
        }

    return schema_comparison


def rank_schemas_by_improvement(schema_comparison: Dict) -> Dict[str, List]:
    """Rank schemas by improvement in JSONExact score"""
    schema_improvements = []

    for schema, metrics in schema_comparison.items():
        json_exact_improvement = metrics["json_exact"]["absolute_change"]
        schema_improvements.append({
            "schema": schema,
            "improvement": json_exact_improvement,
            "baseline": metrics["json_exact"]["baseline_value"],
            "comparison": metrics["json_exact"]["comparison_value"]
        })

    # Sort by improvement (descending)
    top_improvements = sorted(schema_improvements, key=lambda x: x["improvement"], reverse=True)
    bottom_improvements = sorted(schema_improvements, key=lambda x: x["improvement"])

    return {
        "top_5": top_improvements[:5],
        "bottom_5": bottom_improvements[:5]
    }


def main():
    parser = argparse.ArgumentParser(description="Compare EdgeJSON evaluation results")
    parser.add_argument("--baseline", type=str, required=True, help="Path to baseline evaluation JSON")
    parser.add_argument("--comparison", type=str, required=True, help="Path to comparison evaluation JSON")
    parser.add_argument("--output", type=str, required=True, help="Path to save comparison data JSON")

    args = parser.parse_args()

    # Load evaluation results
    print(f"Loading baseline: {args.baseline}")
    with open(args.baseline, 'r') as f:
        baseline_data = json.load(f)

    print(f"Loading comparison: {args.comparison}")
    with open(args.comparison, 'r') as f:
        comparison_data = json.load(f)

    # Extract model names
    baseline_name = baseline_data["aggregate"]["model_name"]
    comparison_name = comparison_data["aggregate"]["model_name"]

    print(f"\nComparing:")
    print(f"  Baseline: {baseline_name}")
    print(f"  Comparison: {comparison_name}")
    print()

    # Compare overall metrics
    print("Comparing overall metrics...")
    overall_comparison = compare_overall_metrics(baseline_data, comparison_data)

    # Compare by complexity
    print("Comparing by complexity...")
    complexity_comparison = compare_by_complexity(baseline_data, comparison_data)

    # Compare by schema
    print("Comparing by schema...")
    schema_comparison = compare_by_schema(baseline_data, comparison_data)

    # Rank schemas
    print("Ranking schemas by improvement...")
    schema_rankings = rank_schemas_by_improvement(schema_comparison)

    # Create comparison output
    comparison_output = {
        "baseline_model": baseline_name,
        "comparison_model": comparison_name,
        "overall": overall_comparison,
        "by_complexity": complexity_comparison,
        "by_schema": schema_comparison,
        "schema_rankings": schema_rankings
    }

    # Save output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(comparison_output, f, indent=2)

    print(f"\nComparison data saved to: {output_path}")

    # Print quick summary
    print("\n" + "="*60)
    print("Quick Summary")
    print("="*60)

    json_exact = overall_comparison["json_exact"]
    print(f"\nJSONExact Score:")
    print(f"  Baseline: {json_exact['baseline_value']:.1%}")
    print(f"  Comparison: {json_exact['comparison_value']:.1%}")
    print(f"  Change: {json_exact['absolute_change']:+.1%} ({json_exact['relative_change']:+.1f}%)")

    field_f1 = overall_comparison["field_f1"]
    print(f"\nField F1 Score:")
    print(f"  Baseline: {field_f1['baseline_value']:.3f}")
    print(f"  Comparison: {field_f1['comparison_value']:.3f}")
    print(f"  Change: {field_f1['absolute_change']:+.3f} ({field_f1['relative_change']:+.1f}%)")

    print(f"\nTop 5 Most Improved Schemas:")
    for i, schema_info in enumerate(schema_rankings["top_5"], 1):
        print(f"  {i}. {schema_info['schema']}: {schema_info['improvement']:+.1%}")

    print(f"\nBottom 5 (Least Improved/Regressed) Schemas:")
    for i, schema_info in enumerate(schema_rankings["bottom_5"], 1):
        print(f"  {i}. {schema_info['schema']}: {schema_info['improvement']:+.1%}")

    print()


if __name__ == "__main__":
    main()

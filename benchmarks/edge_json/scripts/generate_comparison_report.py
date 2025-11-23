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
Comparison Report Generator for EdgeJSON Benchmark

Generates a detailed markdown report comparing two models' performance.

Usage:
    python generate_comparison_report.py \
        --comparison results/comparison_data.json \
        --output results/comparison_report.md
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict


def format_percentage(value: float) -> str:
    """Format a float as percentage"""
    return f"{value * 100:.1f}%"


def format_change(value: float, is_percentage: bool = False) -> str:
    """Format a change value with +/- sign"""
    if is_percentage:
        formatted = format_percentage(value)
    else:
        formatted = f"{value:.3f}"

    return f"+{formatted}" if value >= 0 else formatted


def format_improvement_ratio(value: float) -> str:
    """Format improvement ratio"""
    if value == float('inf'):
        return "∞x"
    elif value == 0:
        return "0x"
    else:
        return f"{value:.2f}x"


def generate_executive_summary(comparison: Dict) -> str:
    """Generate executive summary section"""
    overall = comparison["overall"]
    json_exact = overall["json_exact"]
    field_f1 = overall["field_f1"]

    # Determine overall result
    if json_exact["relative_change"] > 50:
        result = "🎉 **Significant Improvement**"
    elif json_exact["relative_change"] > 10:
        result = "✅ **Moderate Improvement**"
    elif json_exact["relative_change"] > 0:
        result = "📈 **Slight Improvement**"
    elif json_exact["relative_change"] == 0:
        result = "➡️ **No Change**"
    elif json_exact["relative_change"] > -10:
        result = "📉 **Slight Regression**"
    else:
        result = "❌ **Significant Regression**"

    summary = f"""## Executive Summary

{result}

**Key Metrics:**
- **JSONExact Score**: {format_percentage(json_exact["baseline_value"])} → {format_percentage(json_exact["comparison_value"])} ({format_change(json_exact["absolute_change"], is_percentage=True)}, {json_exact["relative_change"]:+.1f}%)
- **Field F1 Score**: {field_f1["baseline_value"]:.3f} → {field_f1["comparison_value"]:.3f} ({format_change(field_f1["absolute_change"])}, {field_f1["relative_change"]:+.1f}%)
- **Improvement Ratio**: {format_improvement_ratio(json_exact["improvement_ratio"])} on JSONExact

**Key Findings:**
"""

    # Analyze complexity performance
    complexity = comparison["by_complexity"]
    for level in ["simple", "medium", "complex"]:
        if level in complexity:
            comp_exact = complexity[level]["json_exact"]
            summary += f"- **{level.capitalize()}** tasks: {format_percentage(comp_exact['baseline_value'])} → {format_percentage(comp_exact['comparison_value'])} ({format_change(comp_exact['absolute_change'], is_percentage=True)})\n"

    # Top improvements
    top_schemas = comparison["schema_rankings"]["top_5"]
    if top_schemas and top_schemas[0]["improvement"] > 0:
        best_schema = top_schemas[0]
        summary += f"\n**Best Improvement**: `{best_schema['schema']}` (+{format_percentage(best_schema['improvement'])})\n"

    # Bottom improvements
    bottom_schemas = comparison["schema_rankings"]["bottom_5"]
    if bottom_schemas and bottom_schemas[0]["improvement"] < 0:
        worst_schema = bottom_schemas[0]
        summary += f"**Worst Regression**: `{worst_schema['schema']}` ({format_change(worst_schema['improvement'], is_percentage=True)})\n"

    return summary


def generate_overall_metrics_table(comparison: Dict) -> str:
    """Generate overall metrics comparison table"""
    overall = comparison["overall"]

    table = """## Overall Metrics Comparison

| Metric | Baseline | Comparison | Absolute Change | Relative Change | Ratio |
|--------|----------|------------|-----------------|-----------------|-------|
"""

    # JSONExact
    je = overall["json_exact"]
    table += f"| **JSONExact Score** | {format_percentage(je['baseline_value'])} | {format_percentage(je['comparison_value'])} | {format_change(je['absolute_change'], is_percentage=True)} | {je['relative_change']:+.1f}% | {format_improvement_ratio(je['improvement_ratio'])} |\n"

    # Field F1
    ff1 = overall["field_f1"]
    table += f"| **Field F1 Score** | {ff1['baseline_value']:.3f} | {ff1['comparison_value']:.3f} | {format_change(ff1['absolute_change'])} | {ff1['relative_change']:+.1f}% | {format_improvement_ratio(ff1['improvement_ratio'])} |\n"

    # Schema Compliance
    sc = overall["schema_compliance"]
    table += f"| **Schema Compliance** | {format_percentage(sc['baseline_value'])} | {format_percentage(sc['comparison_value'])} | {format_change(sc['absolute_change'], is_percentage=True)} | {sc['relative_change']:+.1f}% | {format_improvement_ratio(sc['improvement_ratio'])} |\n"

    # Latency
    lat = overall["latency_ms"]
    table += f"| **Avg Latency (ms)** | {lat['baseline_value']:.1f} | {lat['comparison_value']:.1f} | {lat['absolute_change']:+.1f} | {lat['relative_change']:+.1f}% | {format_improvement_ratio(lat['improvement_ratio'])} |\n"

    # Throughput
    tps = overall["tokens_per_sec"]
    table += f"| **Throughput (tok/s)** | {tps['baseline_value']:.1f} | {tps['comparison_value']:.1f} | {tps['absolute_change']:+.1f} | {tps['relative_change']:+.1f}% | {format_improvement_ratio(tps['improvement_ratio'])} |\n"

    return table


def generate_complexity_breakdown(comparison: Dict) -> str:
    """Generate complexity breakdown section"""
    complexity = comparison["by_complexity"]

    section = """## Performance by Complexity

| Complexity | Metric | Baseline | Comparison | Change | Relative Change |
|------------|--------|----------|------------|--------|-----------------|
"""

    for level in ["simple", "medium", "complex"]:
        if level not in complexity:
            continue

        comp_data = complexity[level]

        # JSONExact
        je = comp_data["json_exact"]
        section += f"| **{level.capitalize()}** | JSONExact | {format_percentage(je['baseline_value'])} | {format_percentage(je['comparison_value'])} | {format_change(je['absolute_change'], is_percentage=True)} | {je['relative_change']:+.1f}% |\n"

        # Field F1
        ff1 = comp_data["field_f1"]
        section += f"| | Field F1 | {ff1['baseline_value']:.3f} | {ff1['comparison_value']:.3f} | {format_change(ff1['absolute_change'])} | {ff1['relative_change']:+.1f}% |\n"

        # Schema Compliance
        sc = comp_data["schema_compliance"]
        section += f"| | Compliance | {format_percentage(sc['baseline_value'])} | {format_percentage(sc['comparison_value'])} | {format_change(sc['absolute_change'], is_percentage=True)} | {sc['relative_change']:+.1f}% |\n"

    return section


def generate_schema_rankings(comparison: Dict) -> str:
    """Generate schema rankings section"""
    rankings = comparison["schema_rankings"]

    section = """## Schema Performance Rankings

### Top 5 Most Improved Schemas

| Rank | Schema | Baseline | Comparison | Improvement |
|------|--------|----------|------------|-------------|
"""

    for i, schema_info in enumerate(rankings["top_5"], 1):
        section += f"| {i} | `{schema_info['schema']}` | {format_percentage(schema_info['baseline'])} | {format_percentage(schema_info['comparison'])} | **{format_change(schema_info['improvement'], is_percentage=True)}** |\n"

    section += """
### Bottom 5 (Least Improved / Regressed) Schemas

| Rank | Schema | Baseline | Comparison | Change |
|------|--------|----------|------------|--------|
"""

    for i, schema_info in enumerate(rankings["bottom_5"], 1):
        section += f"| {i} | `{schema_info['schema']}` | {format_percentage(schema_info['baseline'])} | {format_percentage(schema_info['comparison'])} | **{format_change(schema_info['improvement'], is_percentage=True)}** |\n"

    return section


def generate_detailed_schema_table(comparison: Dict) -> str:
    """Generate detailed per-schema comparison table"""
    schema_comparison = comparison["by_schema"]

    section = """## Detailed Per-Schema Comparison

| Schema | JSONExact (Base) | JSONExact (Comp) | Change | Field F1 (Base) | Field F1 (Comp) | Change |
|--------|------------------|------------------|--------|-----------------|-----------------|--------|
"""

    # Sort schemas alphabetically
    for schema in sorted(schema_comparison.keys()):
        metrics = schema_comparison[schema]
        je = metrics["json_exact"]
        ff1 = metrics["field_f1"]

        section += f"| `{schema}` | {format_percentage(je['baseline_value'])} | {format_percentage(je['comparison_value'])} | {format_change(je['absolute_change'], is_percentage=True)} | {ff1['baseline_value']:.3f} | {ff1['comparison_value']:.3f} | {format_change(ff1['absolute_change'])} |\n"

    return section


def generate_analysis_recommendations(comparison: Dict) -> str:
    """Generate analysis and recommendations section"""
    overall = comparison["overall"]
    json_exact = overall["json_exact"]
    complexity = comparison["by_complexity"]

    section = """## Analysis & Recommendations

### Performance Analysis

"""

    # Overall performance
    if json_exact["comparison_value"] < 0.30:
        section += "- **Overall Performance**: The model achieves only {}% JSONExact score, indicating significant room for improvement.\n".format(format_percentage(json_exact["comparison_value"]))
    elif json_exact["comparison_value"] < 0.60:
        section += "- **Overall Performance**: The model achieves {}% JSONExact score, showing moderate but improvable performance.\n".format(format_percentage(json_exact["comparison_value"]))
    else:
        section += "- **Overall Performance**: The model achieves {}% JSONExact score, demonstrating strong extraction capabilities.\n".format(format_percentage(json_exact["comparison_value"]))

    # Complexity analysis
    if "complex" in complexity:
        complex_exact = complexity["complex"]["json_exact"]["comparison_value"]
        simple_exact = complexity["simple"]["json_exact"]["comparison_value"]

        if complex_exact < 0.10:
            section += f"- **Complexity Limitation**: Model struggles with complex schemas ({format_percentage(complex_exact)} accuracy), suggesting capacity constraints.\n"

        if simple_exact > 0.50 and complex_exact < 0.10:
            section += "- **Complexity Gap**: Large performance gap between simple and complex tasks indicates model may be too small for complex reasoning.\n"

    # Fine-tuning effectiveness
    if json_exact["baseline_value"] > 0:
        improvement = json_exact["improvement_ratio"]
        if improvement > 2.0:
            section += f"- **Fine-tuning Impact**: Fine-tuning significantly improved performance ({format_improvement_ratio(improvement)}), indicating effective training.\n"
        elif improvement > 1.2:
            section += f"- **Fine-tuning Impact**: Fine-tuning moderately improved performance ({format_improvement_ratio(improvement)}), room for optimization.\n"
        elif improvement > 0.95:
            section += f"- **Fine-tuning Impact**: Fine-tuning had minimal effect ({format_improvement_ratio(improvement)}), suggesting potential issues with training data or approach.\n"
        else:
            section += f"- **Fine-tuning Impact**: Fine-tuning actually reduced performance ({format_improvement_ratio(improvement)}), indicating serious training issues.\n"

    section += """
### Recommendations

"""

    # Recommendations based on performance
    if json_exact["comparison_value"] < 0.40:
        section += """1. **Increase Training Data**: Current performance suggests insufficient training examples
2. **Review Data Quality**: Validate that training examples are high-quality and representative
3. **Consider Larger Model**: 135M parameters may be insufficient for this task complexity
4. **Extend Training**: Try more epochs (5-10) to ensure convergence
5. **Validate Test Set**: Check for errors or inconsistencies in test data
"""
    else:
        section += """1. **Optimize Hyperparameters**: Fine-tune learning rate, batch size, and epochs
2. **Augment Training Data**: Add more examples for underperforming schemas
3. **Focus on Complex Schemas**: Develop specialized training for complex extraction tasks
4. **Improve Prompt Engineering**: Refine prompt formats for better model understanding
"""

    return section


def generate_report(comparison_data: Dict) -> str:
    """Generate complete comparison report"""
    report = f"""# EdgeJSON Benchmark: Model Comparison Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**Baseline Model**: {comparison_data["baseline_model"]}
**Comparison Model**: {comparison_data["comparison_model"]}

---

"""

    # Generate sections
    report += generate_executive_summary(comparison_data) + "\n\n"
    report += generate_overall_metrics_table(comparison_data) + "\n\n"
    report += generate_complexity_breakdown(comparison_data) + "\n\n"
    report += generate_schema_rankings(comparison_data) + "\n\n"
    report += generate_detailed_schema_table(comparison_data) + "\n\n"
    report += generate_analysis_recommendations(comparison_data) + "\n\n"

    # Footer
    report += """---

**Note**: This report was automatically generated from EdgeJSON evaluation results.
See `/benchmarks/edge_json/README.md` for benchmark details.
"""

    return report


def main():
    parser = argparse.ArgumentParser(description="Generate EdgeJSON comparison report")
    parser.add_argument("--comparison", type=str, required=True, help="Path to comparison data JSON")
    parser.add_argument("--output", type=str, required=True, help="Path to save markdown report")

    args = parser.parse_args()

    # Load comparison data
    print(f"Loading comparison data: {args.comparison}")
    with open(args.comparison, 'r') as f:
        comparison_data = json.load(f)

    # Generate report
    print("Generating comparison report...")
    report = generate_report(comparison_data)

    # Save report
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(report)

    print(f"\n✓ Report saved to: {output_path}")
    print(f"  ({len(report)} characters, {len(report.splitlines())} lines)")


if __name__ == "__main__":
    main()

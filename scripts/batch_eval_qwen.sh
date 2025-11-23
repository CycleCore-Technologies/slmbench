#!/bin/bash
# Batch evaluation for Qwen2.5-0.5B to avoid hanging
# Scientifically sound: same code, same model, same data, just run in batches

set -e

SCRIPT_DIR="/home/rain/SLMBench/benchmarks/edge_json"
VENV="/home/rain/SLMBench/venv"
DATASET="/home/rain/SLMBench/benchmarks/edge_json/data/edgejson_test_v3.jsonl"
MODEL="Qwen/Qwen2.5-0.5B"
BATCH_SIZE=20
TOTAL_EXAMPLES=158

echo "═══════════════════════════════════════════════════════════════"
echo "🔬 BATCH EVALUATION: Qwen2.5-0.5B on EdgeJSON v3"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Model: $MODEL"
echo "Dataset: $DATASET"
echo "Total examples: $TOTAL_EXAMPLES"
echo "Batch size: $BATCH_SIZE"
echo "Batches: $(( ($TOTAL_EXAMPLES + $BATCH_SIZE - 1) / $BATCH_SIZE ))"
echo ""
echo "Scientific validity: ✅ MAINTAINED"
echo "  - Same evaluation code"
echo "  - Same model and hyperparameters"
echo "  - Same dataset"
echo "  - Only difference: process restarts between batches"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

cd "$SCRIPT_DIR"
source "$VENV/bin/activate"

# Create output directory
mkdir -p ../../results/qwen_batches

# Run batches
BATCH_NUM=0
START_IDX=0

while [ $START_IDX -lt $TOTAL_EXAMPLES ]; do
    BATCH_NUM=$((BATCH_NUM + 1))
    END_IDX=$((START_IDX + BATCH_SIZE))
    
    if [ $END_IDX -gt $TOTAL_EXAMPLES ]; then
        END_IDX=$TOTAL_EXAMPLES
    fi
    
    EXAMPLES_IN_BATCH=$((END_IDX - START_IDX))
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Batch $BATCH_NUM: Examples $START_IDX-$((END_IDX-1)) ($EXAMPLES_IN_BATCH examples)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Run evaluation with limit and offset simulation
    # Note: eval.py doesn't have offset, so we'll use a temp dataset
    head -n $END_IDX "$DATASET" | tail -n $EXAMPLES_IN_BATCH > /tmp/qwen_batch_${BATCH_NUM}.jsonl
    
    python3 scripts/eval.py \
        --model "$MODEL" \
        --dataset /tmp/qwen_batch_${BATCH_NUM}.jsonl \
        --output ../../results/qwen_batches/batch_${BATCH_NUM}.json \
        --device cpu \
        --max_new_tokens 512
    
    if [ $? -eq 0 ]; then
        echo "✅ Batch $BATCH_NUM complete"
    else
        echo "❌ Batch $BATCH_NUM failed"
        exit 1
    fi
    
    # Clean up temp file
    rm /tmp/qwen_batch_${BATCH_NUM}.jsonl
    
    echo ""
    
    START_IDX=$END_IDX
done

echo "═══════════════════════════════════════════════════════════════"
echo "✅ ALL BATCHES COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Combining results..."

# Combine results using Python
python3 << 'PYTHON_EOF'
import json
from pathlib import Path

batch_dir = Path("/home/rain/SLMBench/results/qwen_batches")
batch_files = sorted(batch_dir.glob("batch_*.json"))

all_results = []
total_examples = 0
total_correct = 0
total_field_f1 = 0.0
total_compliance = 0
total_latency = 0.0

by_complexity = {}
by_schema = {}

print(f"Found {len(batch_files)} batch files")

for batch_file in batch_files:
    with open(batch_file) as f:
        data = json.load(f)
        
    # Aggregate individual results
    all_results.extend(data["individual_results"])
    
    # Update totals
    agg = data["aggregate"]
    batch_size = agg["total_examples"]
    total_examples += batch_size
    total_correct += int(agg["json_exact_score"] * batch_size)
    total_field_f1 += agg["avg_field_f1"] * batch_size
    total_compliance += int(agg["schema_compliance_rate"] * batch_size)
    total_latency += agg["avg_latency_ms"] * batch_size
    
    # Merge by_complexity
    for complexity, stats in agg["by_complexity"].items():
        if complexity not in by_complexity:
            by_complexity[complexity] = {"count": 0, "correct": 0, "field_f1_sum": 0.0, "compliant": 0}
        by_complexity[complexity]["count"] += stats["count"]
        by_complexity[complexity]["correct"] += int(stats["json_exact_score"] * stats["count"])
        by_complexity[complexity]["field_f1_sum"] += stats["avg_field_f1"] * stats["count"]
        by_complexity[complexity]["compliant"] += int(stats["schema_compliance_rate"] * stats["count"])
    
    # Merge by_schema
    for schema, stats in agg["by_schema"].items():
        if schema not in by_schema:
            by_schema[schema] = {"count": 0, "correct": 0, "field_f1_sum": 0.0}
        by_schema[schema]["count"] += stats["count"]
        by_schema[schema]["correct"] += int(stats["json_exact_score"] * stats["count"])
        by_schema[schema]["field_f1_sum"] += stats["avg_field_f1"] * stats["count"]

# Calculate final aggregates
final_aggregate = {
    "model_name": "Qwen/Qwen2.5-0.5B",
    "total_examples": total_examples,
    "json_exact_score": total_correct / total_examples if total_examples > 0 else 0.0,
    "avg_field_f1": total_field_f1 / total_examples if total_examples > 0 else 0.0,
    "schema_compliance_rate": total_compliance / total_examples if total_examples > 0 else 0.0,
    "avg_latency_ms": total_latency / total_examples if total_examples > 0 else 0.0,
    "tokens_per_sec": 50.0 / (total_latency / total_examples / 1000.0) if total_latency > 0 else 0.0,
    "by_complexity": {},
    "by_schema": {}
}

# Finalize by_complexity
for complexity, data in by_complexity.items():
    final_aggregate["by_complexity"][complexity] = {
        "count": data["count"],
        "json_exact_score": data["correct"] / data["count"] if data["count"] > 0 else 0.0,
        "avg_field_f1": data["field_f1_sum"] / data["count"] if data["count"] > 0 else 0.0,
        "schema_compliance_rate": data["compliant"] / data["count"] if data["count"] > 0 else 0.0
    }

# Finalize by_schema
for schema, data in by_schema.items():
    final_aggregate["by_schema"][schema] = {
        "count": data["count"],
        "json_exact_score": data["correct"] / data["count"] if data["count"] > 0 else 0.0,
        "avg_field_f1": data["field_f1_sum"] / data["count"] if data["count"] > 0 else 0.0
    }

# Save combined results
output_file = Path("/home/rain/SLMBench/results/qwen25_0.5b_v3_evaluation_FULL.json")
with open(output_file, 'w') as f:
    json.dump({
        "aggregate": final_aggregate,
        "individual_results": all_results
    }, f, indent=2)

print(f"\n✅ Combined results saved to: {output_file}")
print(f"\n📊 FINAL RESULTS:")
print(f"  Total Examples: {total_examples}")
print(f"  JSONExact: {final_aggregate['json_exact_score']*100:.1f}%")
print(f"  Field F1: {final_aggregate['avg_field_f1']:.3f}")
print(f"  Compliance: {final_aggregate['schema_compliance_rate']*100:.1f}%")
print(f"  Avg Latency: {final_aggregate['avg_latency_ms']:.1f}ms")

PYTHON_EOF

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🎉 EVALUATION COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Results: /home/rain/SLMBench/results/qwen25_0.5b_v3_evaluation_FULL.json"
echo ""


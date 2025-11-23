#!/bin/bash
# Check status of baseline model evaluation

echo "═══════════════════════════════════════════════════════════════"
echo "🔍 BASELINE EVALUATION STATUS"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check if process is running
if ps aux | grep -q "[Q]wen2.5-0.5B"; then
    echo "✅ Qwen2.5-0.5B evaluation is RUNNING"
    echo ""
    
    # Show recent log output
    if [ -f "/home/rain/SLMBench/results/qwen25_0.5b_v3_evaluation.log" ]; then
        echo "📊 Recent progress:"
        tail -20 /home/rain/SLMBench/results/qwen25_0.5b_v3_evaluation.log | grep -E "Progress|JSONExact|Field F1" || echo "  (generating...)"
    fi
else
    echo "⏸️  No evaluation running"
    
    # Check if results exist
    if [ -f "/home/rain/SLMBench/results/qwen25_0.5b_v3_evaluation.json" ]; then
        echo "✅ Results file exists!"
        echo ""
        echo "📊 Quick summary:"
        python3 -c "
import json
with open('/home/rain/SLMBench/results/qwen25_0.5b_v3_evaluation.json') as f:
    data = json.load(f)
    agg = data['aggregate']
    print(f\"  Model: {agg['model_name']}\")
    print(f\"  Examples: {agg['total_examples']}\")
    print(f\"  JSONExact: {agg['json_exact_score']*100:.1f}%\")
    print(f\"  Field F1: {agg['avg_field_f1']:.3f}\")
    print(f\"  Compliance: {agg['schema_compliance_rate']*100:.1f}%\")
" 2>/dev/null || echo "  (parsing...)"
    else
        echo "❌ No results file found yet"
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"


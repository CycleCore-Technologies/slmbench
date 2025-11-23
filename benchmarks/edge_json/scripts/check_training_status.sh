#!/usr/bin/env bash
"""
Status Check Script for Phase 4 Training
Quick overview of training progress and system health
"""

# Configuration
LOG_DIR="/home/rain/SLMBench/models/mlm_135m_json/logs"
TRAINING_LOG="$LOG_DIR/training.log"
MONITOR_LOG="$LOG_DIR/hardware_monitor.log"

echo "==========================================================================="
echo "Training Status Check - $(date +'%Y-%m-%d %H:%M:%S')"
echo "==========================================================================="
echo ""

# Check if training process is running
echo "Process Status:"
echo "---------------------------------------------------------------------------"
if pgrep -f "train_mlm_135m_json.py" > /dev/null; then
    TRAINING_PID=$(pgrep -f "train_mlm_135m_json.py")
    echo "✓ Training RUNNING (PID: $TRAINING_PID)"

    # Show process details
    ps -p "$TRAINING_PID" -o pid,ppid,%cpu,%mem,etime,cmd --no-headers | awk '{
        printf "  PID: %s\n", $1
        printf "  CPU: %s%%\n", $3
        printf "  Memory: %s%%\n", $4
        printf "  Runtime: %s\n", $5
    }'
else
    echo "✗ Training NOT RUNNING"
    echo "  Training may have completed or crashed"
fi

if pgrep -f "monitor_training.sh" > /dev/null; then
    MONITOR_PID=$(pgrep -f "monitor_training.sh")
    echo "✓ Hardware Monitor RUNNING (PID: $MONITOR_PID)"
else
    echo "✗ Hardware Monitor NOT RUNNING"
fi

echo ""

# GPU Status
echo "GPU Status:"
echo "---------------------------------------------------------------------------"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,utilization.memory,memory.used,memory.total,power.draw --format=csv,noheader,nounits | awk -F',' '{
        printf "  GPU %s: %s\n", $1, $2
        printf "    Temp: %s°C\n", $3
        printf "    Utilization: GPU %s%% | Memory %s%%\n", $4, $5
        printf "    VRAM: %s MB / %s MB (%.1f%%)\n", $6, $7, ($6/$7)*100
        printf "    Power: %s W\n", $8
    }'
else
    echo "  nvidia-smi not available"
fi

echo ""

# Training Progress
echo "Training Progress:"
echo "---------------------------------------------------------------------------"
if [ -f "$TRAINING_LOG" ]; then
    # Extract epoch/step information from recent logs
    echo "Latest training output:"
    tail -30 "$TRAINING_LOG" | grep -E "(Epoch|Step|Loss|eval|Saving|complete)" | tail -10

    echo ""
    echo "Loss trend (last 5 logged):"
    grep -oP "(?<=loss': )[0-9.]+|(?<='loss': )[0-9.]+" "$TRAINING_LOG" | tail -5 | awk '{
        sum+=$1; count++; print "  Step " count ": " $1
    } END {
        if (count > 0) print "  Average: " sum/count
    }'
else
    echo "  Training log not found at $TRAINING_LOG"
fi

echo ""

# Hardware Monitor Summary
echo "Hardware Monitor (latest):"
echo "---------------------------------------------------------------------------"
if [ -f "$MONITOR_LOG" ]; then
    # Show latest GPU temp and VRAM
    echo "Last hardware check:"
    tail -50 "$MONITOR_LOG" | grep -A 1 "GPU Temperature:" | tail -2
    tail -50 "$MONITOR_LOG" | grep -A 1 "VRAM Usage:" | tail -2

    echo ""
    echo "Latest training status from monitor:"
    tail -50 "$MONITOR_LOG" | grep -A 1 "Training Process Status:" | tail -2
else
    echo "  Hardware monitor log not found at $MONITOR_LOG"
fi

echo ""

# Checkpoints
echo "Checkpoints:"
echo "---------------------------------------------------------------------------"
CHECKPOINT_DIR="/home/rain/SLMBench/models/mlm_135m_json"
if [ -d "$CHECKPOINT_DIR" ]; then
    NUM_CHECKPOINTS=$(find "$CHECKPOINT_DIR" -maxdepth 1 -name "checkpoint-*" -type d 2>/dev/null | wc -l)
    echo "  Total checkpoints: $NUM_CHECKPOINTS"

    if [ $NUM_CHECKPOINTS -gt 0 ]; then
        echo "  Latest checkpoints:"
        find "$CHECKPOINT_DIR" -maxdepth 1 -name "checkpoint-*" -type d -printf "%T@ %p\n" 2>/dev/null | \
            sort -rn | head -3 | awk '{print "    " $2 " (" strftime("%Y-%m-%d %H:%M:%S", $1) ")"}'
    fi

    if [ -d "$CHECKPOINT_DIR/final_model" ]; then
        echo "  ✓ Final model exists"
    fi
else
    echo "  Checkpoint directory not found"
fi

echo ""

# Disk Space
echo "Disk Space:"
echo "---------------------------------------------------------------------------"
df -h "$CHECKPOINT_DIR" | awk 'NR==1 {print "  " $0} NR==2 {
    printf "  %s: %s used of %s (%s full)\n", $1, $3, $2, $5
}'

echo ""

# Estimated completion
echo "Estimated Completion:"
echo "---------------------------------------------------------------------------"
if pgrep -f "train_mlm_135m_json.py" > /dev/null && [ -f "$TRAINING_LOG" ]; then
    # Try to parse current epoch/step
    CURRENT_STEP=$(grep -oP "(?<='step': )[0-9]+" "$TRAINING_LOG" | tail -1)
    TOTAL_STEPS=$(grep -oP "(?<=total training steps: )[0-9]+" "$TRAINING_LOG" | head -1)

    if [ -n "$CURRENT_STEP" ] && [ -n "$TOTAL_STEPS" ] && [ "$TOTAL_STEPS" -gt 0 ]; then
        PROGRESS=$(echo "scale=2; ($CURRENT_STEP / $TOTAL_STEPS) * 100" | bc)
        echo "  Progress: Step $CURRENT_STEP / $TOTAL_STEPS (${PROGRESS}%)"

        # Estimate time remaining based on elapsed time
        ELAPSED_SEC=$(ps -p $(pgrep -f "train_mlm_135m_json.py") -o etimes= | tr -d ' ')
        if [ -n "$ELAPSED_SEC" ] && [ "$CURRENT_STEP" -gt 0 ]; then
            SEC_PER_STEP=$(echo "scale=2; $ELAPSED_SEC / $CURRENT_STEP" | bc)
            REMAINING_STEPS=$((TOTAL_STEPS - CURRENT_STEP))
            REMAINING_SEC=$(echo "scale=0; $SEC_PER_STEP * $REMAINING_STEPS / 1" | bc)
            REMAINING_HOURS=$(echo "scale=1; $REMAINING_SEC / 3600" | bc)

            COMPLETION_DATE=$(date -d "+${REMAINING_SEC} seconds" +'%Y-%m-%d %H:%M:%S')
            echo "  Remaining: ~${REMAINING_HOURS} hours"
            echo "  Est. completion: $COMPLETION_DATE"
        fi
    else
        echo "  Unable to parse progress from logs"
    fi
else
    echo "  Training not running or log unavailable"
fi

echo ""
echo "==========================================================================="
echo ""
echo "Commands:"
echo "  View training log:  tail -f $TRAINING_LOG"
echo "  View hardware log:  tail -f $MONITOR_LOG"
echo "  GPU monitor:        watch -n 10 nvidia-smi"
echo ""

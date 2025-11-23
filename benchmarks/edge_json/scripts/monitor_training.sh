#!/usr/bin/env bash
"""
Hardware Monitoring Script for Phase 4 Training
Logs GPU/CPU metrics every 2 hours during overnight training

Monitors:
- GPU temperature
- GPU utilization & VRAM usage
- CPU temperature (if sensors available)
- Training progress (last 10 lines of log)
"""

# Configuration
INTERVAL_SECONDS=7200  # 2 hours
LOG_DIR="/home/rain/SLMBench/models/mlm_135m_json/logs"
MONITOR_LOG="$LOG_DIR/hardware_monitor.log"
TRAINING_LOG="$LOG_DIR/training.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Initialize monitor log
echo "===========================================================================" >> "$MONITOR_LOG"
echo "Hardware Monitor Started: $(date +'%Y-%m-%d %H:%M:%S')" >> "$MONITOR_LOG"
echo "Monitoring interval: ${INTERVAL_SECONDS}s ($(echo "scale=1; $INTERVAL_SECONDS / 3600" | bc) hours)" >> "$MONITOR_LOG"
echo "===========================================================================" >> "$MONITOR_LOG"
echo "" >> "$MONITOR_LOG"

# Counter
ITERATION=0

while true; do
    ITERATION=$((ITERATION + 1))
    TIMESTAMP=$(date +'%Y-%m-%d %H:%M:%S')

    echo "===========================================================================" >> "$MONITOR_LOG"
    echo "Monitor Check #$ITERATION - $TIMESTAMP" >> "$MONITOR_LOG"
    echo "===========================================================================" >> "$MONITOR_LOG"

    # GPU metrics
    if command -v nvidia-smi &> /dev/null; then
        echo "" >> "$MONITOR_LOG"
        echo "GPU Temperature:" >> "$MONITOR_LOG"
        nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits >> "$MONITOR_LOG" 2>&1
        TEMP=$(nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits)
        echo "  Current: ${TEMP}°C" >> "$MONITOR_LOG"

        echo "" >> "$MONITOR_LOG"
        echo "GPU Utilization:" >> "$MONITOR_LOG"
        nvidia-smi --query-gpu=utilization.gpu,utilization.memory --format=csv,noheader >> "$MONITOR_LOG" 2>&1

        echo "" >> "$MONITOR_LOG"
        echo "VRAM Usage:" >> "$MONITOR_LOG"
        nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader >> "$MONITOR_LOG" 2>&1

        echo "" >> "$MONITOR_LOG"
        echo "GPU Power Draw:" >> "$MONITOR_LOG"
        nvidia-smi --query-gpu=power.draw,power.limit --format=csv,noheader >> "$MONITOR_LOG" 2>&1
    else
        echo "nvidia-smi not found" >> "$MONITOR_LOG"
    fi

    # CPU temperature (try multiple methods)
    echo "" >> "$MONITOR_LOG"
    echo "CPU Temperature:" >> "$MONITOR_LOG"

    if command -v sensors &> /dev/null; then
        sensors | grep -i "core\|cpu\|package" | head -5 >> "$MONITOR_LOG" 2>&1
    elif [ -d /sys/class/thermal ]; then
        # Fallback: read from thermal zones
        for zone in /sys/class/thermal/thermal_zone*/temp; do
            if [ -f "$zone" ]; then
                TEMP=$(cat "$zone")
                TEMP_C=$(echo "scale=1; $TEMP / 1000" | bc)
                echo "  Thermal zone: ${TEMP_C}°C" >> "$MONITOR_LOG"
            fi
        done
    else
        echo "  CPU temp monitoring not available" >> "$MONITOR_LOG"
    fi

    # System uptime
    echo "" >> "$MONITOR_LOG"
    echo "System Uptime:" >> "$MONITOR_LOG"
    uptime >> "$MONITOR_LOG" 2>&1

    # Training progress
    echo "" >> "$MONITOR_LOG"
    echo "Training Progress (last 10 lines):" >> "$MONITOR_LOG"
    if [ -f "$TRAINING_LOG" ]; then
        tail -10 "$TRAINING_LOG" >> "$MONITOR_LOG" 2>&1
    else
        echo "  Training log not found at $TRAINING_LOG" >> "$MONITOR_LOG"
    fi

    # Check if training process is still running
    echo "" >> "$MONITOR_LOG"
    echo "Training Process Status:" >> "$MONITOR_LOG"
    if pgrep -f "train_mlm_135m_json.py" > /dev/null; then
        PID=$(pgrep -f "train_mlm_135m_json.py")
        echo "  Running (PID: $PID)" >> "$MONITOR_LOG"

        # Process CPU/Memory usage
        ps -p "$PID" -o %cpu,%mem,etime,cmd --no-headers >> "$MONITOR_LOG" 2>&1
    else
        echo "  NOT RUNNING - Training may have completed or crashed" >> "$MONITOR_LOG"
        echo "  Monitor exiting..." >> "$MONITOR_LOG"
        echo "" >> "$MONITOR_LOG"
        echo "===========================================================================" >> "$MONITOR_LOG"
        echo "Hardware Monitor Stopped: $(date +'%Y-%m-%d %H:%M:%S')" >> "$MONITOR_LOG"
        echo "===========================================================================" >> "$MONITOR_LOG"
        break
    fi

    echo "" >> "$MONITOR_LOG"
    echo "Next check in $(echo "scale=1; $INTERVAL_SECONDS / 3600" | bc) hours (at $(date -d "+${INTERVAL_SECONDS} seconds" +'%H:%M:%S'))" >> "$MONITOR_LOG"
    echo "" >> "$MONITOR_LOG"

    # Sleep until next check
    sleep "$INTERVAL_SECONDS"
done

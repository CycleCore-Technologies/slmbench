#!/usr/bin/env bash
"""
Launch Script for Phase 4: MLM-135M-JSON Training
Starts training with hardware monitoring in background
"""

set -e  # Exit on error

# Configuration
PROJECT_ROOT="/home/rain/SLMBench"
TRAINING_SCRIPT="$PROJECT_ROOT/benchmarks/edge_json/scripts/train_mlm_135m_json.py"
MONITOR_SCRIPT="$PROJECT_ROOT/benchmarks/edge_json/scripts/monitor_training.sh"
LOG_DIR="$PROJECT_ROOT/models/mlm_135m_json/logs"
TRAINING_LOG="$LOG_DIR/training.log"
VENV="$PROJECT_ROOT/venv"

# Parse arguments
VALIDATION_RUN=false
if [[ "$1" == "--validation-run" ]]; then
    VALIDATION_RUN=true
    echo "Running in VALIDATION mode (100 examples, 1 epoch)"
fi

# Ensure log directory exists
mkdir -p "$LOG_DIR"

echo "==========================================================================="
echo "Phase 4: MLM-135M-JSON Training Launcher"
echo "==========================================================================="
echo ""
echo "Project root: $PROJECT_ROOT"
echo "Training script: $TRAINING_SCRIPT"
echo "Log directory: $LOG_DIR"
echo "Validation run: $VALIDATION_RUN"
echo ""

# Step 1: Clear GPU memory
echo "Step 1: Clearing GPU memory..."
echo "---------------------------------------------------------------------------"

# Kill any stale Python/training processes
if pgrep -f "train_mlm_135m_json.py" > /dev/null; then
    echo "Found existing training process, killing..."
    pkill -9 -f "train_mlm_135m_json.py" || true
    sleep 2
fi

# Show current GPU status
if command -v nvidia-smi &> /dev/null; then
    echo ""
    echo "Current GPU status:"
    nvidia-smi --query-gpu=memory.used,memory.total,temperature.gpu --format=csv,noheader
    echo ""
else
    echo "WARNING: nvidia-smi not found, cannot check GPU status"
fi

# Step 2: Activate venv
echo "Step 2: Activating virtual environment..."
echo "---------------------------------------------------------------------------"
source "$VENV/bin/activate"
echo "Python: $(which python)"
echo "Python version: $(python --version)"
echo ""

# Step 3: Verify dependencies
echo "Step 3: Verifying dependencies..."
echo "---------------------------------------------------------------------------"
python -c "import torch; print(f'PyTorch: {torch.__version__}')" || { echo "ERROR: PyTorch not found"; exit 1; }
python -c "import transformers; print(f'Transformers: {transformers.__version__}')" || { echo "ERROR: Transformers not found"; exit 1; }
python -c "import peft; print(f'PEFT: {peft.__version__}')" || { echo "ERROR: PEFT not found"; exit 1; }
echo ""

# Step 4: Start hardware monitoring
echo "Step 4: Starting hardware monitor..."
echo "---------------------------------------------------------------------------"

# Kill any existing monitor
if pgrep -f "monitor_training.sh" > /dev/null; then
    echo "Killing existing monitor..."
    pkill -9 -f "monitor_training.sh" || true
    sleep 1
fi

# Start monitor in background
nohup "$MONITOR_SCRIPT" > /dev/null 2>&1 &
MONITOR_PID=$!
echo "Hardware monitor started (PID: $MONITOR_PID)"
echo "Monitor log: $LOG_DIR/hardware_monitor.log"
echo ""

# Step 5: Start training
echo "Step 5: Starting training..."
echo "---------------------------------------------------------------------------"
START_TIME=$(date +'%Y-%m-%d %H:%M:%S')
echo "Start time: $START_TIME"
echo "Training log: $TRAINING_LOG"
echo ""

# Build training command
TRAIN_CMD="python $TRAINING_SCRIPT"
if [ "$VALIDATION_RUN" = true ]; then
    TRAIN_CMD="$TRAIN_CMD --validation-run"
fi

# Launch training in background with output redirection
nohup $TRAIN_CMD > "$TRAINING_LOG" 2>&1 &
TRAINING_PID=$!

echo "Training started (PID: $TRAINING_PID)"
echo ""

# Wait a few seconds and check if process is still running
sleep 5

if ps -p $TRAINING_PID > /dev/null; then
    echo "✓ Training process is running successfully"
else
    echo "✗ ERROR: Training process died immediately"
    echo "Check logs at: $TRAINING_LOG"
    exit 1
fi

# Show first 20 lines of output
echo ""
echo "First 20 lines of training output:"
echo "---------------------------------------------------------------------------"
head -20 "$TRAINING_LOG"
echo "---------------------------------------------------------------------------"
echo ""

# Calculate estimated completion time
if [ "$VALIDATION_RUN" = true ]; then
    EST_HOURS=2
    EST_DATE=$(date -d "+${EST_HOURS} hours" +'%Y-%m-%d %H:%M:%S')
else
    EST_HOURS=30
    EST_DATE=$(date -d "+${EST_HOURS} hours" +'%Y-%m-%d %H:%M:%S')
fi

echo "==========================================================================="
echo "Training Launched Successfully!"
echo "==========================================================================="
echo ""
echo "Process IDs:"
echo "  Training: $TRAINING_PID"
echo "  Monitor:  $MONITOR_PID"
echo ""
echo "Log files:"
echo "  Training: $TRAINING_LOG"
echo "  Hardware: $LOG_DIR/hardware_monitor.log"
echo ""
echo "Estimated completion:"
echo "  Duration: ~${EST_HOURS} hours"
echo "  Time: $EST_DATE"
echo ""
echo "Monitoring:"
echo "  Check status: ./benchmarks/edge_json/scripts/check_training_status.sh"
echo "  View training log: tail -f $TRAINING_LOG"
echo "  View hardware log: tail -f $LOG_DIR/hardware_monitor.log"
echo ""
echo "To stop training:"
echo "  kill $TRAINING_PID"
echo "  kill $MONITOR_PID"
echo ""
echo "==========================================================================="

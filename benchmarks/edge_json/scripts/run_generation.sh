#!/bin/bash
#
# EdgeJSON Dataset Generation - Automated Run Script
#
# This script waits for Qwen3-14B to finish downloading, then automatically
# generates the full EdgeJSON dataset with logging.
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
LOGS_DIR="$PROJECT_ROOT/benchmarks/edge_json/logs"
DATA_DIR="$PROJECT_ROOT/benchmarks/edge_json/data"

# Model paths
QWEN_MODEL="$PROJECT_ROOT/models/qwen2.5-14b-awq"
MISTRAL_MODEL="$PROJECT_ROOT/models/mistral-small-24b"
PHI4_MODEL="$PROJECT_ROOT/models/phi-4"

# Create timestamp for log file
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_FILE="$LOGS_DIR/generation_$TIMESTAMP.log"

# Functions
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] ✓${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date +'%H:%M:%S')] ✗${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%H:%M:%S')] ⚠${NC} $1" | tee -a "$LOG_FILE"
}

check_model() {
    local model_path=$1
    local model_name=$2

    if [ -d "$model_path" ] && [ -n "$(ls -A "$model_path" 2>/dev/null)" ]; then
        # Check for key model files
        if [ -f "$model_path/config.json" ]; then
            log_success "$model_name found and ready"
            return 0
        fi
    fi

    log_warning "$model_name not ready yet"
    return 1
}

wait_for_qwen() {
    log "Checking if Qwen3-14B download is complete..."

    local max_wait=3600  # Max wait 1 hour
    local elapsed=0
    local check_interval=30

    while [ $elapsed -lt $max_wait ]; do
        if check_model "$QWEN_MODEL" "Qwen3-14B"; then
            return 0
        fi

        log "Waiting for Qwen3-14B download... (${elapsed}s elapsed)"
        sleep $check_interval
        elapsed=$((elapsed + check_interval))
    done

    log_error "Timeout waiting for Qwen3-14B download after ${max_wait}s"
    return 1
}

# Main script
echo ""
echo "================================================================"
echo "  EdgeJSON Dataset Generation - Automated Run"
echo "================================================================"
echo "" | tee "$LOG_FILE"

log "Starting at $(date)"
log "Project root: $PROJECT_ROOT"
log "Log file: $LOG_FILE"
echo ""

# Check Python environment
log "Checking Python environment..."
if [ ! -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    log_error "Virtual environment not found at $PROJECT_ROOT/venv"
    exit 1
fi
log_success "Virtual environment found"

# Activate venv
source "$PROJECT_ROOT/venv/bin/activate"
log_success "Virtual environment activated"

# Check all models
log ""
log "Checking model availability..."
echo ""

# Check Mistral and Phi-4 (should already be downloaded)
check_model "$MISTRAL_MODEL" "Mistral Small 3.1-24B" || {
    log_error "Mistral model not found at $MISTRAL_MODEL"
    exit 1
}

check_model "$PHI4_MODEL" "Phi-4 14B" || {
    log_error "Phi-4 model not found at $PHI4_MODEL"
    exit 1
}

# Wait for Qwen3-14B if needed
echo ""
if ! check_model "$QWEN_MODEL" "Qwen3-14B"; then
    log "Qwen3-14B is still downloading..."
    log "Will check every 30 seconds until ready"
    echo ""

    if ! wait_for_qwen; then
        log_error "Failed to wait for Qwen3-14B download"
        exit 1
    fi
fi

log_success "All models ready!"

# Create data directory if needed
mkdir -p "$DATA_DIR"

# Run generation
echo ""
log "========================================"
log "Starting Dataset Generation"
log "========================================"
echo ""

cd "$PROJECT_ROOT"

log "Running: python benchmarks/edge_json/scripts/generate_dataset_v2.py"
echo "" | tee -a "$LOG_FILE"

# Run the generator and capture all output
if python benchmarks/edge_json/scripts/generate_dataset_v2.py 2>&1 | tee -a "$LOG_FILE"; then
    echo ""
    log_success "Dataset generation completed successfully!"

    # Show results
    echo ""
    log "========================================"
    log "Generation Results"
    log "========================================"
    echo ""

    if [ -f "$DATA_DIR/edgejson_train_v2.jsonl" ]; then
        TRAIN_COUNT=$(wc -l < "$DATA_DIR/edgejson_train_v2.jsonl")
        log_success "Train dataset: $TRAIN_COUNT examples"
    fi

    if [ -f "$DATA_DIR/edgejson_test_v2.jsonl" ]; then
        TEST_COUNT=$(wc -l < "$DATA_DIR/edgejson_test_v2.jsonl")
        log_success "Test dataset: $TEST_COUNT examples"
    fi

    if [ -f "$DATA_DIR/dataset_metadata.json" ]; then
        log_success "Metadata saved"
    fi

    echo ""
    log "Output location: $DATA_DIR"
    log "Log file: $LOG_FILE"
    echo ""

    log "Completed at $(date)"
    exit 0
else
    echo ""
    log_error "Dataset generation failed!"
    log "Check log file for details: $LOG_FILE"
    echo ""
    exit 1
fi

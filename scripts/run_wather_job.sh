#!/bin/bash
set -e

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/hourly.log"

cd "$PROJECT_ROOT"

source venv/bin/activate

echo "=== Run started at $(date) ===" >> "$LOG_FILE"
python -m src.main --run >> "$LOG_FILE" 2>&1
echo "=== Run ended at $(date) ===" >> "$LOG_FILE"

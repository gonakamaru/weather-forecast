#!/bin/bash
set -e

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/hourly.log"

cd "$PROJECT_ROOT"

source venv/bin/activate

GIT_COMMIT="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
GIT_TAG="$(git describe --tags --dirty --always 2>/dev/null || echo 'unknown')"
GIT_BRANCH="$(git branch --show-current 2>/dev/null || echo 'detached')"

{
  echo "=== Run started at $(date) ==="
  echo "Git: commit=$GIT_COMMIT tag=$GIT_TAG branch=$GIT_BRANCH"
  python -m src.main --run
  echo "=== Run ended at $(date) ==="
} >> "$LOG_FILE" 2>&1

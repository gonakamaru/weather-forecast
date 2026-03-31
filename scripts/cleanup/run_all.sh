#!/usr/bin/env bash

# -e -- exit immediately if any command fails (non-zero exit code)
# -u -- treat unset variables as an error instead of silently using an empty string
# -o pipefail -- if any command in a pipe fails, the whole pipe fails (without this, only the last command's exit code matters)
set -euo pipefail

# --- Paths ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

bash "$SCRIPT_DIR/select.sh"
bash "$SCRIPT_DIR/delete.sh"
bash "$SCRIPT_DIR/flush.sh"

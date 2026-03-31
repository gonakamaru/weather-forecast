#!/usr/bin/env bash

# -e -- exit immediately if any command fails (non-zero exit code)
# -u -- treat unset variables as an error instead of silently using an empty string
# -o pipefail -- if any command in a pipe fails, the whole pipe fails (without this, only the last command's exit code matters)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

bash "$SCRIPT_DIR/01_query_old_files.sh"
bash "$SCRIPT_DIR/02_delete_bulk.sh"
bash "$SCRIPT_DIR/03_empty_recycle_bin.sh"
#!/usr/bin/env bash

# Run APEX to empty Salesforce recycle bin

# Strict mode: exit on error, unset variable, or pipe failure.
set -euo pipefail

# --- Paths ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APEX_DIR="$(cd "$SCRIPT_DIR/apex" && pwd)"

# --- Config (overridable via env) ---
TARGET_ORG="${TARGET_ORG:-my-weather-forecast-de-org}"

# --- Derived ---
EMPTY_BIN_FILE_NAME="${EMPTY_BIN_FILE_NAME:-$APEX_DIR/emptybin.apex}"

SF_LOG_LEVEL=DEBUG sf apex run \
    --target-org "$TARGET_ORG" \
    --file "$EMPTY_BIN_FILE_NAME"

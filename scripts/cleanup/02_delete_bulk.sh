#!/usr/bin/env bash

# Delete files according to the IDs in the file.

# --- Paths ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA_DIR="$PROJECT_ROOT/data"

# --- Config (overridable via env) ---
TARGET_ORG="${TARGET_ORG:-my-weather-forecast-de-org}"

# --- Derived ---
DELETE_CANDIDATE_FILE="$DATA_DIR/old_files.csv"

sf data delete bulk \
  --sobject ContentDocument \
  --target-org "$TARGET_ORG" \
  --file "$DELETE_CANDIDATE_FILE" \

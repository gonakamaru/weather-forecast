#!/usr/bin/env bash

# Select IDs of old files and assign them to a file.

# --- Paths ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA_DIR="$PROJECT_ROOT/data"

# --- Config (overridable via env) ---
TARGET_ORG="${TARGET_ORG:-my-weather-forecast-de-org}"
N_DAYS_AGO="${N_DAYS_AGO:-40}"
SELECT_LIMIT="${SELECT_LIMIT:-100}"

# --- Derived ---
DELETE_CANDIDATE_FILE="$DATA_DIR/old_files.csv"
QUERY="SELECT Id FROM ContentDocument WHERE CreatedDate < N_DAYS_AGO:${N_DAYS_AGO} ORDER BY CreatedDate ASC LIMIT ${SELECT_LIMIT}"

# --- Run ---
sf data query \
  --query "$QUERY" \
  --result-format csv \
  --target-org "$TARGET_ORG" > "$DELETE_CANDIDATE_FILE"
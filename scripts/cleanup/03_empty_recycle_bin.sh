#!/usr/bin/env bash

# Run APEX to empty Salesforce recycle bin

TARGET_ORG="${TARGET_ORG:-my-weather-forecast-de-org}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
APEX_DIR="$(cd "$SCRIPT_DIR/apex" && pwd)"

EMPTY_BIN_FILE_NAME="${EMPTY_BIN_FILE_NAME:-$APEX_DIR/emptybin.apex}"

SF_LOG_LEVEL=DEBUG sf apex run \
    --target-org $TARGET_ORG \
    --file $EMPTY_BIN_FILE_NAME \

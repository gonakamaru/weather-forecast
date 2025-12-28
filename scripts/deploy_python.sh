#!/usr/bin/env bash
set -euo pipefail

echo "=== Python CD ==="

git fetch --tags
LATEST_TAG=$(git describe --tags --abbrev=0)

echo "Deploying tag: $LATEST_TAG"

git switch --detach "$LATEST_TAG"

python -m src.main --run --force

echo "Python deployment completed for $LATEST_TAG"
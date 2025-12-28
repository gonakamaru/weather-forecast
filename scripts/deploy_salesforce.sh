#!/usr/bin/env bash
set -euo pipefail

echo "=== Salesforce CD ==="

git fetch --tags
LATEST_TAG=$(git describe --tags --abbrev=0)

echo "Deploying Salesforce metadata for $LATEST_TAG"

git switch --detach "$LATEST_TAG"

sf project deploy start --manifest salesforce/manifest/package.xml

echo "Salesforce deployment completed for $LATEST_TAG"
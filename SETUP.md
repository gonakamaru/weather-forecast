# Setup Guide

This guide walks you through everything you need to get the project running on your Mac.

## Table of Contents

- [System Requirements](#system-requirements)
- [Platform](#platform)
- [1. Homebrew Dependencies](#1-homebrew-dependencies)
- [2. Clone the Repo](#2-clone-the-repo)
- [3. Python via pyenv](#3-python-via-pyenv)
- [4. Python Environment](#4-python-environment)
- [5. Hugging Face and LLaVA Model](#5-hugging-face-and-llava-model)
- [6. Salesforce CLI and npm](#6-salesforce-cli-and-npm)
- [7. Salesforce Custom Object](#7-salesforce-custom-object)
- [8. Run AI Weather Forecast](#8-run-ai-weather-forecast)
- [9. Verify in Salesforce](#9-verify-in-salesforce)
- [10. Dev Org Storage Cleanup](#10-dev-org-storage-cleanup)

## System Requirements

| Item | Requirement |
| --- | --- |
| Hardware | Apple Silicon Mac (M1 or later) |
| RAM | 8 GB minimum |
| macOS | Sequoia (15) or later |
| Python | 3.14 or later |
| Node.js | 18 or later (required for Salesforce CLI) |
| Salesforce | Developer Edition org (free) |
| Disk space | ~3 GB free (LLaVA model weights) |

> **Note:** M1 with 8 GB works, but LLaVA inference takes a few minutes per chart.
> Slow is fine. This is a PoC, not a production system.

## Platform

| Component | Details |
| --- | --- |
| Hardware | Apple Silicon Mac (M1 or later) |
| AI Inference | Apple MPS (Metal Performance Shaders) |
| LLM | LLaVA Interleave Qwen 0.5B (local, via Hugging Face) |
| Salesforce | Developer Edition org |

> All AI inference runs locally on Apple Silicon.
> No external AI APIs or GPU rentals required.

## 1. Homebrew Dependencies

If you don't have Homebrew installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then install the required packages:

```bash
brew install git pyenv poppler node
```

`pyenv` manages your Python version.
`poppler` is required by `pdf2image` for PDF rendering.
`node` is required for the Salesforce CLI.

## 2. Clone the Repo

```bash
git clone https://github.com/gonakamaru/weather-forecast.git

# Go to the project directory
cd weather-forecast

# Copy .env for the project settings and secrets (OAuth2 and JWT options)
cp .env.example .env
```

## 3. Python via pyenv

Install Python 3.14:

```bash
pyenv install 3.14.3
pyenv global 3.14.3
```

Create or add to `~/.zshrc`:

```bash
# Initialize pyenv so this shell uses Python versions managed by pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Reload shell:

```bash
source ~/.zshrc
```

Verify:

```bash
python --version
```

## 4. Python Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Verify Apple Silicon AI Support

Confirm PyTorch can see your Apple Silicon GPU:

```bash
python -c "import torch; print(torch.backends.mps.is_available())"
```

This should print `True`. The pipeline detects MPS automatically at runtime
and falls back to CPU if unavailable.

## 5. Hugging Face and LLaVA Model

This project uses **LLaVA Interleave Qwen 0.5B** running locally via Hugging Face.
It's publicly available, so you don't need a Hugging Face account or authentication
token to use it.

Run the following to download the model:

```bash
python -c "
from transformers import AutoProcessor, AutoModelForImageTextToText
model_id = 'llava-hf/llava-interleave-qwen-0.5b-hf'
AutoProcessor.from_pretrained(model_id)
AutoModelForImageTextToText.from_pretrained(model_id)
print('Model downloaded successfully.')
"
```

The model weights (~1.8 GB) are downloaded automatically on first run and cached at:

```bash
~/.cache/huggingface/hub/models--llava-hf--llava-interleave-qwen-0.5b-hf
```

Since the cache is shared across all projects on your machine, you only need to do this
once. Make sure you have a stable internet connection and enough disk space before you
start.

## 6. Salesforce CLI and npm

> **Note:** Salesforce CLI is distributed via npm only.
> Do not install it via Homebrew.

Install the Salesforce CLI via npm and verify:

```bash
npm install -g @salesforce/cli

sf --version
```

You should see something like `@salesforce/cli/2.x.x darwin-arm64 node-vXX.x.x`.

Then authenticate to your Salesforce Developer Edition org and check if it is properly authenticated.
Make sure to use `--alias my-weather-forecast-de-org`; this alias is used in the deploy script in the next step.

```bash
sf org login web --alias my-weather-forecast-de-org

sf list org
```

```text
┌──┬────────────────────────────┬─────────────────────────┬────────────────────┬───────────┐
│  │ Alias                      │ Username                │ Org Id             │ Status    │
├──┼────────────────────────────┼─────────────────────────┼────────────────────┼───────────┤
│  │ my-weather-forecast-de-org │ go-nakamaru@example.com │ 00DgK0000000000000 │ Connected │
└──┴────────────────────────────┴─────────────────────────┴────────────────────┴───────────┘
```

## 7. Salesforce Custom Object

Run the Salesforce deploy script `deploy_salesforce.sh` against the `my-weather-forecast-de-org` org.

1. Fetches the latest Git tag
2. Checks out the commit at that tag
3. Deploys the metadata to the Salesforce org (`my-weather-forecast-de-org`)
4. Creates the Weather_Report__c custom object and its fields in the org

```bash
source ./scripts/deploy_salesforce.sh
```

| Field | Type | Description |
| --- | --- | --- |
| `Forecast__c` | Long Text Area | AI-generated forecast text |
| `Chart_Image_Id__c` | Text | Deprecated (retained for reference only) |
| `PDF_Hash__c` | Text | PDF hash for deduplication |
| `PDF_Hash_4_4__c` | Text | Short hash variant for deduplication |
| `Import_Timestamp__c` | Date/Time | When the record was imported |

## 8. Run AI Weather Forecast

Deploy Python -- fetches the latest tag, checks it out, and runs the AI Weather Forecast pipeline:

```bash
source ./scripts/deploy_python.sh
```

## 9. Verify in Salesforce

Log in to your Developer Edition org and confirm:

- The Weather_Report__c object exists under Setup > Object Manager
- At least one record has been created with a forecast in the Forecast__c field

## 10. Dev Org Storage Cleanup

Developer Edition orgs come with very limited file storage -- around 20 MB. The weather chart
pipeline uploads a small thumbnail image (~100 KB JPG) on every run, so it fills up faster
than you'd expect.

A set of cleanup scripts is provided under `scripts/cleanup/` to hard delete old ContentDocument
records. Hard delete bypasses the Recycle Bin, so storage is freed immediately.

> **Note:** The acting user must have the **Bulk API Hard Delete** permission set assigned
> in Salesforce before running these scripts.

To run manually:

```bash
bash scripts/cleanup/run_all.sh
```

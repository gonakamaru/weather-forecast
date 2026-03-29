# 🛠 Setup Guide

This guide walks you through everything you need to get the project running on your Mac.
If you just want the quick version, see the [Quick Start](#-quick-start) section.

## 📋 Table of Contents

- [System Requirements](#-system-requirements)
- [Platform](#-platform)
- [1. Homebrew Dependencies](#1-homebrew-dependencies)
- [2. Clone the Repo](#2-clone-the-repo)
- [3. Python via pyenv](#3-python-via-pyenv)
- [4. Python Environment](#4-python-environment)
- [5. Node and Salesforce CLI](#5-node-and-salesforce-cli)
- [6. Salesforce Credentials](#6-salesforce-credentials)
- [7. Hugging Face and LLaVA Model](#7-hugging-face-and-llava-model)
- [Quick Start](#-quick-start)

## 💻 System Requirements

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

## 🖥 Platform

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

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Then install the required packages:

    brew install git pyenv poppler node

`pyenv` manages your Python version.
`poppler` is required by `pdf2image` for PDF rendering.
`node` is required for the Salesforce CLI.

## 2. Clone the Repo

    git clone https://github.com/gonakamaru/weather-forecast.git
    cd weather-forecast

## 3. Python via pyenv

Install Python 3.14:

    pyenv install 3.14.3
    pyenv global 3.14.3

Create or add to `~/.zshrc`:

```bash
# Initialize pyenv so this shell uses Python versions managed by pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Reload Shell:

```bash
source ~/.zshrc
```

Verify:

    python --version

## 4. Python Environment

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Verify Apple Silicon AI Support

Confirm PyTorch can see your Apple Silicon GPU:

    python -c "import torch; print(torch.backends.mps.is_available())"

This should print `True`. The pipeline detects MPS automatically at runtime
and falls back to CPU if unavailable.

## 5. Node and Salesforce CLI

> **Note:** Salesforce CLI is distributed via npm only.
> Do not install it via Homebrew.

Install the Salesforce CLI via npm:

    npm install -g @salesforce/cli

Verify it works:

    sf --version

You should see something like `@salesforce/cli/2.x.x darwin-arm64 node-vXX.x.x`.

Then authenticate to your Salesforce Developer Edition org:

    sf org login web --alias my-weather-forecast-de-org

## 6. Salesforce Credentials

    cp .env.example .env

Then edit `.env` with your Salesforce credentials.
See `.env.example` for OAuth2 and JWT options.

> **Note:** Before running the Python pipeline for the first time, run the
> Salesforce deployment script below. This creates the `Weather_Report__c`
> custom object and its fields in your org:
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `Forecast__c` | Long Text Area | AI-generated forecast text |
> | `Chart_Image_Id__c` | Text | ⚠️ Deprecated |
> | `PDF_Hash__c` | Text | PDF hash for deduplication |
> | `PDF_Hash_4_4__c` | Text | Short hash variant for deduplication |
> | `Import_Timestamp__c` | Date/Time | When the record was imported |
>
> The Python pipeline will fail if this object does not exist in your org.

## 7. Hugging Face and LLaVA Model

This project uses **LLaVA Interleave Qwen 0.5B** running locally via Hugging Face.

This model is publicly available and does not require a Hugging Face account
or authentication token.

Model weights (~1.8 GB) are downloaded automatically on first run and cached at:

    ~/.cache/huggingface/hub/models--llava-hf--llava-interleave-qwen-0.5b-hf

The cache is shared across all projects on your machine, so the download
only happens once.

Make sure you have a stable internet connection and enough disk space
before running the pipeline for the first time.

## 🚀 Quick Start

Once setup is complete, deployment is two commands.

Deploy to Salesforce -- fetches the latest tag, checks it out, and pushes
the metadata to the Salesforce org.

    source ./scripts/deploy_salesforce.sh

Deploy Python -- fetches the latest tag, checks it out, and runs the pipeline.

    source ./scripts/deploy_python.sh

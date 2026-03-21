# 🛠 Setup Guide

This guide walks you through everything you need to get the project running on your Mac.
If you just want the quick version, see the [Quick Start](#-quick-start) section.

## 📋 Table of Contents

- [System Requirements](#-system-requirements)
- [1. Homebrew Dependencies](#1-homebrew-dependencies)
- [2. Node and Salesforce CLI](#2-node-and-salesforce-cli)
- [3. Python via pyenv](#3-python-via-pyenv)
- [4. Clone the Repo](#4-clone-the-repo)
- [5. Python Environment](#5-python-environment)
- [6. Salesforce Credentials](#6-salesforce-credentials)
- [Quick Start](#-quick-start)

## 💻 System Requirements

| Item | Requirement |
| --- | --- |
| Hardware | Apple Silicon Mac (M1 or later) |
| RAM | 8 GB minimum |
| macOS | Sequoia (15) or later |
| Python | 3.14 or later |
| Salesforce | Developer Edition org (free) |
| Disk space | ~5-10 GB free (LLaVA model weights) |

> **Note:** M1 with 8 GB works, but LLaVA inference takes a few minutes per chart.
> Slow is fine. This is a PoC, not a production system.

## 1. Homebrew Dependencies

If you don't have Homebrew installed:

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Then install the required packages:

    brew install git pyenv poppler node

`poppler` is required by `pdf2image` for PDF rendering.
`pyenv` manages your Python version.
`node` is required for the Salesforce CLI.

## 2. Node and Salesforce CLI

Install the Salesforce CLI via npm:

    npm install -g @salesforce/cli

Verify it works:

    sf --version

You should see something like `@salesforce/cli/2.x.x darwin-arm64 node-vXX.x.x`.

Then authenticate to your Salesforce Developer Edition org:

    sf org login web --alias my-org

## 3. Python via pyenv

Install Python 3.14:

    pyenv install 3.14.3
    pyenv global 3.14.3

Verify:

    python --version

## 4. Clone the Repo

    git clone https://github.com/gonakamaru/weather-forecast.git
    cd weather-forecast

## 5. Python Environment

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## 6. Salesforce Credentials

    cp .env.example .env

Then edit `.env` with your Salesforce credentials.
See `.env.example` for OAuth2 and JWT options.

## 🚀 Quick Start

Once setup is complete, deployment is two commands.

Deploy to Salesforce -- fetches the latest tag, checks it out, and pushes the metadata to the Salesforce org.

    source ./scripts/deploy_salesforce.sh

Deploy Python -- fetches the latest tag, checks it out, and runs the pipeline.

    source ./scripts/deploy_python.sh

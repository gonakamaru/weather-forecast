# 🌦️ Weather Chart → Forecast → Salesforce

This is a personal PoC built to explore what a MacBook Air can actually do. It ingests a Japan Meteorological Agency (JMA) surface analysis PDF, runs it through LLaVA locally on Apple Silicon, and stores the results in Salesforce. No cloud AI, no GPU rental, no subscriptions. Just your Mac doing the work.

---

## 📋 Table of Contents

- [What It Does](#-what-it-does)
- [System Requirements](#-system-requirements)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Project Status](#-project-status)
- [Delivery & Deployment](#-delivery--deployment)
- [Next Steps](#-next-steps)

---

## 🔍 What It Does

This project converts a JMA surface analysis PDF into structured content
and stores it in a Salesforce Developer Edition org:

1. **Ingest** a JMA weather chart PDF
2. **Convert** it to a standard PNG and a small preview image
3. **Extract** a short forecast summary using LLaVA (runs locally)
4. **Upload** everything to Salesforce: PDF hash, preview image, and forecast text

Small in scope, but it touches a real cross-section of skills:
PDF tooling, image conversion, local LLM inference,
orchestration design, and Salesforce REST integration.

---

## 💻 System Requirements

| Item | Requirement |
| --- | --- |
| Hardware | Apple Silicon Mac (M1 or later) |
| RAM | 8 GB minimum |
| macOS | Sequoia (15) or later |
| Python | 3.10 or later |
| Salesforce | Developer Edition org (free) |
| Disk space | ~5-10 GB free (LLaVA model weights) |

> **Note:** M1 with 8 GB works, but LLaVA inference takes a few minutes per chart.
> Slow is fine. This is a PoC, not a production system.

---

## 🚀 Quick Start

1. Clone the repo

       git clone https://github.com/gonakamaru/weather-forecast.git
       cd weather-forecast

2. Set up your Python environment

       python3 -m venv .venv
       source .venv/bin/activate
       pip install -r requirements.txt

3. Configure your credentials

       cp .env.example .env

   Then edit `.env` with your Salesforce credentials (see `.env.example` for OAuth2 and JWT options).

4. Deploy to Salesforce -- switches to the latest tagged release and updates your Salesforce org.

       source ./scripts/deploy_salesforce.sh

5. Deploy Python -- switches to the latest tagged release and runs the pipeline.

       source ./scripts/deploy_python.sh

---

## 🏗 Architecture

    JMA PDF
      → pdf2image       (PNG conversion)
      → LLaVA           (local inference on Apple Silicon)
      → forecast text + preview image
      → Salesforce REST API
      → WeatherReport__c (Developer Edition org)

---

## 📊 Project Status

Built and tested on an M1 MacBook Air with 8 GB RAM. It runs. Slowly. But it runs. That's kind of the point.

Current version is **v0.4.1**.

| Feature | Status |
| --- | --- |
| PDF ingestion and PNG conversion | ✅ Done |
| LLaVA-based forecast extraction (local) | ✅ Done |
| Salesforce upload (hash, preview, forecast) | ✅ Done |
| Modular orchestration with execution guards | ✅ Done |
| Structured logging | ✅ Done |
| Unit tests for forecast and Salesforce client | ✅ Done |
| Versioned Salesforce metadata | ✅ Done |
| Standardized deployment scripts | ✅ Done |
| CI automation | ⏳ Deferred |

---

## 📦 Delivery & Deployment

This project uses a **manual Continuous Delivery** model.

### Continuous Delivery

- Deployment is triggered by a human operator
- Python and Salesforce deployments are handled independently
- Each deployment targets an explicit Git tag (e.g. `v0.4.1`)
- Environment setup (venv, Salesforce auth, secrets) is assumed complete before execution
- CI tooling is intentionally out of scope for v0.4

Standardized deployment scripts are provided to keep releases repeatable and reduce operator error.

### Continuous Integration

Automated CI (tests, merge validation, pipeline orchestration)
is **intentionally deferred** and will be revisited once delivery practices are stabilized.

---

## 🔮 Next Steps

- Move secrets out of `.env` and `.key` files into environment variables
  so the Python side has no file dependencies for configuration
- Make the shell scripts responsible for loading secrets into the environment
- Work toward Docker-friendly deployment as the end goal
- Add a pipeline orchestrator for cleaner flow control
- Add a `SETUP.md` with detailed environment setup steps

---

## 📎 References

- [CHANGELOG](./CHANGELOG.md)
- [VERSIONING](./VERSIONING.md)
- [JMA Surface Analysis Charts](https://www.jma.go.jp/bosai/map.html#contents=spas)

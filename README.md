# 🌤️ Weather Chart → Forecast → Salesforce

A local-first proof-of-concept that ingests JMA surface analysis PDFs,
extracts a forecast using LLaVA, and stores the results in Salesforce —
running entirely on your own Apple Silicon Mac. No cloud AI. No GPU rental.

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
4. **Upload** everything to Salesforce — PDF hash, preview image, and forecast text

Small in scope, but it touches a real cross-section of skills:
PDF tooling, image conversion, local LLM inference,
orchestration design, and Salesforce REST integration.

---

## 💻 System Requirements

| Item | Requirement |
| --- | --- |
| Hardware | Apple Silicon Mac (M1 or later) |
| RAM | 8 GB minimum — 16 GB recommended |
| macOS | Ventura (13) or later |
| Python | 3.10 or later |
| Salesforce | Developer Edition org (free) |
| Disk space | ~5–10 GB free (LLaVA model weights) |

> **⚠️ Performance note:** M1 8 GB works but is slow —
> expect a few minutes for LLaVA inference per chart.
> M3 16 GB is the recommended target for comfortable use.
> This is intentional for a locally-run PoC.

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

4. Run the pipeline

       python scripts/run_pipeline.py

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

The end-to-end pipeline is working. Current version is **v0.4.0**.

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
- Each deployment targets an explicit Git tag (e.g. `v0.4.0`)
- Environment setup (venv, Salesforce auth, secrets) is assumed complete before execution
- CI tooling is intentionally out of scope for v0.4

Standardized deployment scripts are provided to keep releases repeatable and reduce operator error.

### Continuous Integration

Automated CI — tests, merge validation, pipeline orchestration —
is **intentionally deferred** and will be revisited once delivery practices are stabilized.

---

## 🔮 Next Steps

- Add a pipeline orchestrator for cleaner flow control
- Add a `SETUP.md` with detailed environment setup steps
- Explore scheduled / automated ingestion
- Evaluate CI options for v0.5

---

## 📎 References

- [CHANGELOG](./CHANGELOG.md)
- [VERSIONING](./VERSIONING.md)
- [JMA Surface Analysis Charts](https://www.jma.go.jp/bosai/map.html#contents=spas)

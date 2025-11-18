# 📘 Weather Chart → Forecast → Salesforce

A compact PoC project exploring PDF ingestion, LLaVA interpretation, and Salesforce storage.

## 🌤️ Project Overview

    This project experiments with turning JMA surface analysis charts into:
    1.  A readable forecast summary (via LLaVA)
    2.  A stored record inside Salesforce Developer Edition, including:
        - Original PDF
        - A resized “tiny preview” image
        - AI-generated forecast text

    The final script will be simple (≈100 lines), but the learning is broad:
    PDF tooling, image conversion, LLM interpretation, CLI design, and Salesforce REST flows.

## 🧩 Project Goals

    -   Explore modular POCs for each subsystem
    -   Integrate them into one reliable script
    -   Store outputs efficiently in Salesforce Free/Dev limits
    -   Keep repo clean, branch-friendly, and easy to extend
    -   Learn each part without pressure

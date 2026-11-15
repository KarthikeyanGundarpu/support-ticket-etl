# Support Ticket ETL & CLI Analytics Engine

![Run Pytest Suite](https://github.com/KarthikeyanGundarpu/support-ticket-etl/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)

A modular Python ETL pipeline and command-line analytics engine built to ingest, clean, normalize, and analyze multi-format support logs (**CSV, JSON, XML, and unstructured Regex text logs**) into a relational **SQLite** database[cite: 1].

---

## Key Features
- **Multi-Format Extraction:** Dedicated parsers for structured (`CSV`, `JSON`, `XML`) and unstructured raw log files using compiled Regular Expressions (`re`)[cite: 1].
- **Schema Normalization & Data Cleaning:** Standardizes timestamps, validates ticket priority/severity levels, handles malformed or missing records, and deduplicates entries prior to storage[cite: 9].
- **SQLite Storage Layer:** Idempotent database loading with structured tables, primary-key constraints, and indexed queries for fast aggregation[cite: 1].
- **CLI Analytics Interface (`argparse`):** Generate synthetic multi-format logs, run ingestion pipelines, and query ticket metrics directly from the terminal.
- **Automated Testing (`pytest` + GitHub Actions):** Unit and integration test suite running automatically via GitHub Actions on every push to `main`[cite: 1, 10].

---

## Project Architecture

```text
support-ticket-etl/
├── .github/
│   └── workflows/
│       └── tests.yml        # GitHub Actions CI workflow running pytest
├── src/                     # Core ETL modules (parsers, transformations, SQLite loader, analytics)
├── tests/                   # Automated Pytest unit & integration test suite
├── generate_logs.py         # Synthetic multi-format log generator (CSV, JSON, XML, .log)
├── main.py                  # CLI entrypoint for ETL ingestion and analytics queries
├── pyproject.toml           # Project metadata and pytest configuration
├── .gitignore
└── README.md

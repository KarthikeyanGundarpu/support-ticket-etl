# Support Ticket ETL & CLI Analytics Engine

![Run Pytest Suite](https://github.com/KarthikeyanGundarpu/support-ticket-etl/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)

A modular Python ETL pipeline and command-line analytics engine built to ingest, clean, normalize, and analyze multi-format support logs (**CSV, JSON, XML, and unstructured Regex text logs**) into a relational **SQLite** database.

---

## Key Features
- **Multi-Format Extraction:** Dedicated parsers for structured (`CSV`, `JSON`, `XML`) and unstructured raw log files using compiled Regular Expressions (`re`).
- **Schema Normalization & Data Cleaning:** Standardizes timestamps, validates ticket priority/severity levels, handles malformed or missing records, and deduplicates entries prior to storage.
- **SQLite Storage Layer:** Idempotent database loading with structured tables, primary-key constraints, and indexed queries for fast aggregation.
- **CLI Analytics Interface (`argparse`):** Generate synthetic multi-format logs, run ingestion pipelines, and query ticket metrics directly from the terminal.
- **Automated Testing (`pytest` + GitHub Actions):** Unit and integration test suite running automatically via GitHub Actions on every push to `main`.

---

## Project Architecture

```text
support-ticket-etl/
â”œâ”€â”€ .github/
â”‚   â””â”€â”€ workflows/
â”‚       â””â”€â”€ tests.yml        # GitHub Actions CI workflow running pytest
â”œâ”€â”€ src/                     # Core ETL modules (parsers, transformations, SQLite loader, analytics)
â”œâ”€â”€ tests/                   # Automated Pytest unit & integration test suite
â”œâ”€â”€ generate_logs.py         # Synthetic multi-format log generator (CSV, JSON, XML, .log)
â”œâ”€â”€ main.py                  # CLI entrypoint for ETL ingestion and analytics queries
â”œâ”€â”€ pyproject.toml           # Project metadata and pytest configuration
â”œâ”€â”€ .gitignore
â””â”€â”€ README.md


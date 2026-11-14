# ServerLogPipeline

An end-to-end Python data engineering and analytics pipeline that ingests raw application server logs, validates records via Object-Oriented models, persists structured events into SQLite, and exports endpoint reliability KPIs to CSV and JSON.

## Architecture & Modules

```text
ServerLogPipeline/
├── src/
│   ├── models.py       # Dataclass LogRecord model with schema & SLA validation
│   ├── parser.py       # Memory-safe streaming file reader & compiled RegEx parser
│   ├── database.py     # SQLite CRUD repository using context managers & parameterized SQL
│   └── analytics.py    # Pandas KPI aggregation (error rates, avg & p95 latency) + CSV/JSON export
├── tests/
│   └── test_pipeline.py # PyTest unit tests covering validation, parsing, CRUD, and metrics
├── generate_logs.py    # Synthetic server log generator with injected malformed records
└── main.py             # CLI orchestrator built with argparse


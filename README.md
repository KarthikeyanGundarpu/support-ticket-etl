Enterprise Support Ticket ETL & Analytics Engine
A modular, object-oriented Python ETL pipeline and CLI tool that ingests, validates, deduplicates, and analyzes customer support tickets across CSV, JSON, XML, and unstructured server logs into a normalized SQLite database.

Key Engineering Highlights
Object-Oriented Domain Modeling (models.py): Encapsulates validation rules via @property setters, compiled regex patterns, computed SLA breach flags, and custom __eq__/__hash__ contracts for O(1) deduplication.
Memory-Efficient Streaming Parsers (parsers.py): Uses an abstract base class (BaseParser) and generator-based yield pipelines (csv.DictReader, ET.iterparse with elem.clear(), and named regex groups) to process large files in O(1) memory.
Transactional SQLite Persistence (database.py): Implements context-managed transactions (PRAGMA foreign_keys = ON), parameterized ON CONFLICT upserts, full CRUD operations, and LEFT JOIN + COALESCE agent performance reporting.
Decorators & CLI (decorators.py, cli.py): Reusable @audit_execution timing/error-logging decorator and an argparse terminal interface.
Project Structure
support-ticket-etl/
├── ticket_engine/
│   ├── __init__.py
│   ├── models.py       # Ticket entity, SLA rules, validation & hash contracts
│   ├── parsers.py      # Polymorphic CSV, JSON, XML & Regex Log streaming parsers
│   ├── database.py     # SQLite schema, CRUD & LEFT JOIN analytics
│   ├── decorators.py   # Execution audit & timing decorator
│   └── cli.py          # Command-line interface
├── tests/
│   └── test_engine.py  # Pytest unit & integration test suite
└── README.mdg

# main.py
import argparse
import os
from pathlib import Path
from src.parser import LogParser
from src.database import LogRepository
from src.analytics import AnalyticsEngine

BASE_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ServerLogPipeline: End-to-End Log ETL, SQLite CRUD & Analytics CLI"
    )
    parser.add_argument(
        "--log-file",
        default=str(BASE_DIR / "data" / "server.log"),
        help="Path to the input raw log file",
    )
    parser.add_argument(
        "--db-path",
        default=str(BASE_DIR / "data" / "logs.db"),
        help="Path to the SQLite database file",
    )
    parser.add_argument(
        "--purge-before",
        default="2026-11-14 10:05:00",
        help="Delete INFO logs older than this timestamp (YYYY-MM-DD HH:MM:SS)",
    )
    parser.add_argument(
        "--reset-db",
        action="store_true",
        help="Drop existing SQLite database before running the pipeline",
    )
    return parser.parse_args()


def run_pipeline(args: argparse.Namespace) -> None:
    if args.reset_db and os.path.exists(args.db_path):
        os.remove(args.db_path)

    # 1. EXTRACT & TRANSFORM
    parser = LogParser()
    valid_records, malformed_lines = parser.parse_file(args.log_file)
    print(f"[1/4] Parsed {len(valid_records)} valid logs | Skipped {len(malformed_lines)} malformed lines.")

    # 2. LOAD
    repo = LogRepository(db_path=args.db_path)
    inserted = repo.insert_many(valid_records)
    print(f"[2/4] Inserted {inserted} rows into SQLite ({args.db_path}).")

    # 3. CRUD OPERATIONS
    error_logs = repo.fetch_logs(level="ERROR")
    reviewed_count = repo.mark_errors_reviewed()
    purged_count = repo.purge_info_before(args.purge_before)
    print(
        f"[3/4] CRUD Check -> Fetched {len(error_logs)} ERRORs | "
        f"Marked {reviewed_count} reviewed | Purged {purged_count} old INFO logs."
    )

    # 4. ANALYTICS & EXPORT
    all_remaining = repo.fetch_logs()
    engine = AnalyticsEngine(all_remaining, output_dir=str(BASE_DIR / "output"))
    paths = engine.export_reports(malformed_count=len(malformed_lines))

    print("\n--- Endpoint Health Summary ---")
    print(engine.summarize_by_endpoint().to_string(index=False))
    print(f"\n[4/4] Reports exported to: {paths['csv']} and {paths['json']}")


if __name__ == "__main__":
    cli_args = parse_args()
    run_pipeline(cli_args)
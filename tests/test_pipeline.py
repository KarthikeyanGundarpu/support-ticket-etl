import pytest
from src.models import LogRecord
from src.parser import LogParser
from src.database import LogRepository
from src.analytics import AnalyticsEngine


def test_log_record_validation():
    valid = LogRecord("2026-11-14 10:00:00", "ERROR", 101, "/api/v1/login", 650, "Timeout")
    assert valid.is_slow is True

    with pytest.raises(ValueError):
        LogRecord("2026-11-14 10:00:00", "CRITICAL", 101, "/api/v1/login", 100, "Bad level")

    with pytest.raises(ValueError):
        LogRecord("2026-11-14 10:00:00", "INFO", 101, "/api/v1/login", -5, "Negative latency")


def test_log_parser_separates_malformed_lines(tmp_path):
    log_file = tmp_path / "sample.log"
    log_file.write_text(
        "2026-11-14 10:00:15 | INFO | user_id=105 | endpoint=/api/v1/search | latency=45ms | msg=OK\n"
        "CORRUPTED_ENTRY ### invalid_format\n",
        encoding="utf-8",
    )

    parser = LogParser()
    valid, malformed = parser.parse_file(str(log_file))

    assert len(valid) == 1
    assert valid[0].user_id == 105
    assert valid[0].latency_ms == 45
    assert len(malformed) == 1


def test_sqlite_crud_lifecycle(tmp_path):
    db_file = tmp_path / "test_logs.db"
    repo = LogRepository(db_path=str(db_file))

    records = [
        LogRecord("2026-11-14 10:01:00", "INFO", 101, "/api/v1/login", 50, "OK"),
        LogRecord("2026-11-14 10:02:00", "ERROR", 102, "/api/v1/payments", 900, "DB error"),
    ]
    assert repo.insert_many(records) == 2
    assert len(repo.fetch_logs(level="ERROR")) == 1
    assert repo.mark_errors_reviewed() == 1
    assert repo.purge_info_before("2026-11-14 10:05:00") == 1
    assert len(repo.fetch_logs()) == 1


def test_analytics_engine_metrics(tmp_path):
    rows = [
        {"id": 1, "level": "INFO", "endpoint": "/api/v1/orders", "latency_ms": 100, "is_slow": 0},
        {"id": 2, "level": "ERROR", "endpoint": "/api/v1/orders", "latency_ms": 900, "is_slow": 1},
    ]
    engine = AnalyticsEngine(rows, output_dir=str(tmp_path))
    summary = engine.summarize_by_endpoint()

    assert summary.iloc[0]["error_rate_pct"] == 50.0
    assert summary.iloc[0]["avg_latency_ms"] == 500.0

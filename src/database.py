# src/database.py
import sqlite3
from typing import List, Dict, Any
from src.models import LogRecord


class LogRepository:
    def __init__(self, db_path: str = "data/logs.db") -> None:
        self.db_path = db_path
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_table(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS server_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            level TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            endpoint TEXT NOT NULL,
            latency_ms INTEGER NOT NULL,
            is_slow INTEGER NOT NULL,
            message TEXT NOT NULL,
            reviewed INTEGER DEFAULT 0
        );
        """
        with self._connect() as conn:
            conn.execute(query)

    # CREATE (Bulk Insert)
    def insert_many(self, records: List[LogRecord]) -> int:
        query = """
        INSERT INTO server_logs (timestamp, level, user_id, endpoint, latency_ms, is_slow, message)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        rows = [
            (r.timestamp, r.level, r.user_id, r.endpoint, r.latency_ms, int(r.is_slow), r.message)
            for r in records
        ]
        with self._connect() as conn:
            cursor = conn.executemany(query, rows)
            return cursor.rowcount

    # READ (Fetch all or filter by level)
    def fetch_logs(self, level: str | None = None) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            if level:
                cursor = conn.execute("SELECT * FROM server_logs WHERE level = ?;", (level,))
            else:
                cursor = conn.execute("SELECT * FROM server_logs;")
            return [dict(row) for row in cursor.fetchall()]

    # UPDATE (Mark ERROR logs as reviewed)
    def mark_errors_reviewed(self) -> int:
        query = "UPDATE server_logs SET reviewed = 1 WHERE level = 'ERROR' AND reviewed = 0;"
        with self._connect() as conn:
            cursor = conn.execute(query)
            return cursor.rowcount

    # DELETE (Purge old INFO logs before a given timestamp)
    def purge_info_before(self, cutoff_timestamp: str) -> int:
        query = "DELETE FROM server_logs WHERE level = 'INFO' AND timestamp < ?;"
        with self._connect() as conn:
            cursor = conn.execute(query, (cutoff_timestamp,))
            return cursor.rowcount
import re
from typing import List, Tuple
from src.models import LogRecord


class LogParser:
    def __init__(self) -> None:
        self.pattern = re.compile(
            r"^(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s*\|\s*"
            r"(?P<level>[A-Z]+)\s*\|\s*"
            r"user_id=(?P<user_id>\d+)\s*\|\s*"
            r"endpoint=(?P<endpoint>\S+)\s*\|\s*"
            r"latency=(?P<latency>\d+)ms\s*\|\s*"
            r"msg=(?P<message>.+)$"
        )

    def parse_line(self, line: str) -> LogRecord | None:
        match = self.pattern.match(line.strip())
        if not match:
            return None

        data = match.groupdict()
        try:
            return LogRecord(
                timestamp=data["timestamp"],
                level=data["level"],
                user_id=int(data["user_id"]),
                endpoint=data["endpoint"],
                latency_ms=int(data["latency"]),
                message=data["message"],
            )
        except ValueError:
            return None

    def parse_file(self, filepath: str) -> Tuple[List[LogRecord], List[str]]:
        valid_records: List[LogRecord] = []
        malformed_lines: List[str] = []

        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                record = self.parse_line(line)
                if record:
                    valid_records.append(record)
                else:
                    malformed_lines.append(line.strip())

        return valid_records, malformed_lines
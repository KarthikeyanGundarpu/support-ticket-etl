from dataclasses import dataclass, asdict
from typing import Dict, Any

VALID_LEVELS = {"INFO", "WARN", "ERROR"}


@dataclass
class LogRecord:
    timestamp: str
    level: str
    user_id: int
    endpoint: str
    latency_ms: int
    message: str

    def __post_init__(self) -> None:
        if self.level not in VALID_LEVELS:
            raise ValueError(f"Invalid log level: {self.level}")
        if self.latency_ms < 0:
            raise ValueError(f"Latency cannot be negative: {self.latency_ms}")

    @property
    def is_slow(self) -> bool:
        """Flags requests exceeding 500ms SLA threshold."""
        return self.latency_ms > 500

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["is_slow"] = self.is_slow
        return data
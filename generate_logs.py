import random
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
LOG_FILE = DATA_DIR / "server.log"

levels = ["INFO", "INFO", "INFO", "WARN", "ERROR"]
endpoints = ["/api/v1/login", "/api/v1/orders", "/api/v1/payments", "/api/v1/search"]
messages = {
    "INFO": "Request completed successfully",
    "WARN": "High response latency detected",
    "ERROR": "Database connection timeout",
}

start_time = datetime(2026, 11, 14, 10, 0, 0)

with open(LOG_FILE, "w", encoding="utf-8") as f:
    for i in range(1, 201):
        ts = (start_time + timedelta(seconds=i * 15)).strftime("%Y-%m-%d %H:%M:%S")
        lvl = random.choice(levels)
        uid = random.randint(100, 125)
        ep = random.choice(endpoints)
        latency = random.randint(20, 150) if lvl == "INFO" else random.randint(300, 1500)
        f.write(f"{ts} | {lvl} | user_id={uid} | endpoint={ep} | latency={latency}ms | msg={messages[lvl]}\n")
        if i % 50 == 0:
            f.write(f"CORRUPTED_LINE_{i} ### raw_dump_unparsed\n")

print(f"Generated {LOG_FILE} with 204 lines.")
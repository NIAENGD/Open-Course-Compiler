from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sqlite3

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def apply_migrations(conn: sqlite3.Connection) -> list[str]:
    applied: list[str] = []
    conn.execute(
        "CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY, applied_at TEXT NOT NULL)"
    )
    known = {row[0] for row in conn.execute("SELECT version FROM schema_migrations")}
    for file in sorted(MIGRATIONS_DIR.glob("*.sql")):
        if file.name in known:
            continue
        conn.executescript(file.read_text())
        conn.execute(
            "INSERT INTO schema_migrations(version, applied_at) VALUES (?, ?)",
            (file.name, datetime.now(timezone.utc).isoformat()),
        )
        applied.append(file.name)
    conn.commit()
    return applied

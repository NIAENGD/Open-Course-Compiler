from __future__ import annotations

import sqlite3
from pathlib import Path

from app.paths import ensure_app_dirs


def connect(database_path: Path | None = None) -> sqlite3.Connection:
    path = database_path or ensure_app_dirs().sqlite_path
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "backend"))

from app.db.migrate import apply_migrations
from app.db.session import connect
from app.paths import ensure_app_dirs

paths = ensure_app_dirs()
with connect(paths.sqlite_path) as conn:
    for version in apply_migrations(conn):
        print(f"applied {version}")
print(paths.sqlite_path)

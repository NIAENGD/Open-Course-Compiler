from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "backend"))

import sqlite3
import tempfile
from pathlib import Path

from app.db.migrate import apply_migrations
from app.db.session import connect
from app.paths import APP_DIRS, ensure_app_dirs

REQUIRED_TABLES = {
    "providers", "courses", "course_suitability", "course_assets", "content_chunks",
    "course_units", "learning_goals", "learning_paths", "learning_path_courses",
    "lessons", "quiz_items", "attempts", "mastery_records", "jobs", "token_ledger",
    "schema_migrations",
}

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp) / "OpenCourseCompiler"
    paths = ensure_app_dirs(root)
    missing_dirs = [directory for directory in APP_DIRS if not (root / directory).is_dir()]
    if missing_dirs:
        raise SystemExit(f"missing dirs: {missing_dirs}")
    with connect(paths.sqlite_path) as conn:
        applied = apply_migrations(conn)
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    missing_tables = REQUIRED_TABLES - tables
    if missing_tables:
        raise SystemExit(f"missing tables: {sorted(missing_tables)}")
    if not applied:
        raise SystemExit("no migrations applied")
print("stage1 verification passed")

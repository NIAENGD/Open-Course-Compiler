from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


APP_DIRS = (
    "config",
    "db/migrations",
    "vector/lancedb",
    "catalog/raw/mit_ocw",
    "catalog/raw/open_yale",
    "catalog/normalized",
    "courses",
    "jobs/logs",
    "jobs/checkpoints",
    "cache/http",
    "cache/ai",
    "cache/embeddings",
    "cache/thumbnails",
    "logs",
)


@dataclass(frozen=True)
class AppPaths:
    root: Path

    @property
    def sqlite_path(self) -> Path:
        return self.root / "db" / "app.sqlite3"


def default_data_root() -> Path:
    override = os.getenv("OCC_DATA_DIR")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".local" / "share" / "OpenCourseCompiler"


def ensure_app_dirs(root: Path | None = None) -> AppPaths:
    data_root = root or default_data_root()
    for relative in APP_DIRS:
        (data_root / relative).mkdir(parents=True, exist_ok=True)
    return AppPaths(root=data_root)

from __future__ import annotations

from dataclasses import dataclass, field
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "Open Course Compiler"
    host: str = "127.0.0.1"
    port: int = 8765
    data_dir: str | None = None
    database_url: str | None = None
    allowed_origins: list[str] = field(default_factory=lambda: ["http://localhost:5173"])


def get_settings() -> Settings:
    return Settings(
        host=os.getenv("OCC_HOST", "127.0.0.1"),
        port=int(os.getenv("OCC_PORT", "8765")),
        data_dir=os.getenv("OCC_DATA_DIR"),
        database_url=os.getenv("OCC_DATABASE_URL"),
    )

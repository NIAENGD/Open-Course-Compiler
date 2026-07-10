from __future__ import annotations

from fastapi import FastAPI

from app.config import get_settings
from app.db.migrate import apply_migrations
from app.db.session import connect
from app.paths import ensure_app_dirs


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0")

    @app.on_event("startup")
    def startup() -> None:
        paths = ensure_app_dirs()
        with connect(paths.sqlite_path) as conn:
            apply_migrations(conn)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "backend"}

    return app


app = create_app()

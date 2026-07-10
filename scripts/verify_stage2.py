from __future__ import annotations

import asyncio
import sqlite3
import tempfile
from pathlib import Path

from app.catalog.repository import list_courses, upsert_course, upsert_provider
from app.db.migrate import apply_migrations
from app.db.session import connect
from app.providers.registry import list_providers
from app.schemas.provider import CatalogSearchFilters


async def main() -> None:
    providers = list_providers()
    assert {p.provider_id for p in providers} == {"mit_ocw", "open_yale"}
    with tempfile.TemporaryDirectory() as tmp:
        with connect(Path(tmp) / "stage2.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            apply_migrations(conn)
            total = 0
            for provider in providers:
                descriptor = provider.descriptor()
                assert descriptor.capabilities.catalog_refresh
                assert descriptor.license_default.code
                upsert_provider(conn, descriptor)
                records = await provider.refresh_catalog(use_network=False)
                assert records
                for record in records:
                    assert record.license.code
                    assert record.canonical_url.startswith("https://")
                    manifest = await provider.fetch_course_manifest(record.provider_course_id)
                    assets = await provider.list_assets(manifest)
                    assert assets
                    upsert_course(conn, record)
                    total += 1
            conn.commit()
            assert total >= 4
            assert list_courses(conn, CatalogSearchFilters(q="calculus", provider="mit_ocw"))
            assert list_courses(conn, CatalogSearchFilters(q="philosophy", provider="open_yale"))
    print("Stage 2 verification passed: providers, licenses, manifests, catalog refresh/search/filter.")


if __name__ == "__main__":
    asyncio.run(main())

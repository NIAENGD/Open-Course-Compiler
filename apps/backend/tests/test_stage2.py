from __future__ import annotations

import asyncio
import sqlite3
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.catalog.repository import list_courses, upsert_course, upsert_provider
from app.db.migrate import apply_migrations
from app.db.session import connect
from app.main import create_app
from app.providers.mit_ocw import MitOcwProvider
from app.providers.registry import list_providers
from app.schemas.base import ProviderId
from app.schemas.provider import CatalogSearchFilters


def test_stage2_provider_contracts_refresh_manifest_assets() -> None:
    asyncio.run(_assert_provider_contracts())


async def _assert_provider_contracts() -> None:
    providers = {provider.provider_id: provider for provider in list_providers()}
    assert set(providers) == {ProviderId.MIT_OCW.value, ProviderId.OPEN_YALE.value}

    for provider in providers.values():
        descriptor = provider.descriptor()
        assert descriptor.license_default.code
        assert descriptor.capabilities.catalog_refresh is True
        records = await provider.refresh_catalog()
        assert records
        assert all(record.provider_id == provider.provider_id for record in records)
        manifest = await provider.fetch_course_manifest(records[0].provider_course_id)
        assets = await provider.list_assets(manifest)
        assert manifest.course.title == records[0].title
        assert assets
        assert all(asset.provider_id == provider.provider_id for asset in assets)


def test_stage2_catalog_upsert_search_filter() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        with connect(Path(tmp) / "app.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            apply_migrations(conn)
            provider = MitOcwProvider()
            upsert_provider(conn, provider.descriptor())
            for record in asyncio.run(provider.refresh_catalog()):
                upsert_course(conn, record)
            conn.commit()

            calculus = list_courses(conn, CatalogSearchFilters(q="calculus"))
            assert len(calculus) == 1
            assert calculus[0].license_code == "CC-BY-NC-SA-4.0"
            eecs = list_courses(
                conn, CatalogSearchFilters(department="Electrical Engineering and Computer Science")
            )
            assert len(eecs) == 1
            assert eecs[0].provider_id == "mit_ocw"


def test_stage2_catalog_api_routes(monkeypatch: pytest.MonkeyPatch) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setenv("OCC_DATA_DIR", tmp)
        app = create_app()
        with TestClient(app) as client:
            providers = client.get("/catalog/providers")
            assert providers.status_code == 200
            assert {p["provider_id"] for p in providers.json()} == {"mit_ocw", "open_yale"}

            refresh = client.post(
                "/catalog/refresh", json={"providers": ["open_yale"], "use_network": False}
            )
            assert refresh.status_code == 200
            assert refresh.json()["upserted"] == 2

            search = client.get(
                "/catalog/search", params={"q": "philosophy", "provider": "open_yale"}
            )
            assert search.status_code == 200
            assert search.json()[0]["provider_id"] == "open_yale"

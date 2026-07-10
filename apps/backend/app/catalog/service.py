from __future__ import annotations

from uuid import uuid4

from app.catalog.repository import upsert_course, upsert_provider
from app.db.session import connect
from app.providers.registry import get_provider, list_providers
from app.schemas.provider import CatalogRefreshRequest, CatalogRefreshSummary, ProviderDescriptor


async def refresh_catalog(request: CatalogRefreshRequest) -> CatalogRefreshSummary:
    selected = request.providers or [p.provider_id for p in list_providers()]
    fetched = upserted = 0
    errors: list[str] = []
    with connect() as conn:
        conn.row_factory = None
        for provider_id in selected:
            try:
                provider = get_provider(provider_id)
                upsert_provider(conn, provider.descriptor())
                records = await provider.refresh_catalog(use_network=request.use_network)
                fetched += len(records)
                for record in records:
                    upsert_course(conn, record)
                    upserted += 1
            except Exception as exc:  # catalog refresh records provider errors and continues
                errors.append(f"{provider_id}: {exc}")
        conn.commit()
    return CatalogRefreshSummary(
        job_id=str(uuid4()), providers=selected, fetched=fetched, upserted=upserted, errors=errors
    )


def provider_descriptors() -> list[ProviderDescriptor]:
    return [p.descriptor() for p in list_providers()]

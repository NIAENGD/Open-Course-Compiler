from __future__ import annotations

from typing import Literal

from pydantic import Field

from app.schemas.base import AssetType, StrictBaseModel


class RawAsset(StrictBaseModel):
    provider_id: str
    course_id: str
    asset_type: AssetType
    url: str | None = None
    title: str | None = None
    local_path: str | None = None
    mime_type: str | None = None
    downloadable: bool = True
    license_scope: Literal["course", "third_party_unknown", "public_domain", "unknown"] = "unknown"
    source_page_url: str | None = None
    metadata: dict = Field(default_factory=dict)


class SourceRef(StrictBaseModel):
    provider_id: str
    course_id: str
    asset_id: str | None = None
    url: str | None = None
    page_start: int | None = None
    page_end: int | None = None
    timestamp_start: float | None = None
    timestamp_end: float | None = None
    section_title: str | None = None


class ContentChunk(StrictBaseModel):
    chunk_id: str
    course_id: str
    unit_id: str | None = None
    asset_id: str | None = None
    chunk_type: str
    text: str
    source_ref: SourceRef
    token_count: int | None = None
    metadata: dict = Field(default_factory=dict)

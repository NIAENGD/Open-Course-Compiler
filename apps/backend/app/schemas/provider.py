from __future__ import annotations

from pydantic import Field

from app.schemas.assets import RawAsset
from app.schemas.base import LicenseInfo, StrictBaseModel
from app.schemas.course import RawCourseRecord


class ProviderCapability(StrictBaseModel):
    catalog_refresh: bool = True
    course_manifest: bool = True
    asset_discovery: bool = True
    has_video: bool = False
    has_audio: bool = False
    has_transcripts: bool = False
    has_readings: bool = False
    has_assessments: bool = False
    supports_downloads: bool = True


class RawCourseManifest(StrictBaseModel):
    provider_id: str
    provider_course_id: str
    canonical_url: str
    title: str
    course: RawCourseRecord
    pages: list[str] = Field(default_factory=list)
    assets: list[RawAsset] = Field(default_factory=list)
    raw_metadata: dict = Field(default_factory=dict)


class ProviderDescriptor(StrictBaseModel):
    provider_id: str
    name: str
    base_url: str
    terms_url: str | None = None
    license_default: LicenseInfo
    capabilities: ProviderCapability


class CatalogRefreshRequest(StrictBaseModel):
    providers: list[str] = Field(default_factory=list)
    use_network: bool = False


class CatalogRefreshSummary(StrictBaseModel):
    job_id: str
    providers: list[str]
    fetched: int
    upserted: int
    errors: list[str] = Field(default_factory=list)


class CatalogSearchFilters(StrictBaseModel):
    q: str | None = None
    provider: str | None = None
    department: str | None = None
    topic: str | None = None
    mode: str | None = None
    min_teachability_score: float | None = None
    license: str | None = None
    has_video: bool | None = None
    has_transcript: bool | None = None
    has_readings: bool | None = None
    has_exams: bool | None = None


class CatalogCourse(StrictBaseModel):
    id: str
    provider_id: str
    provider_course_id: str
    canonical_url: str
    title: str
    course_number: str | None = None
    department: str | None = None
    instructors: list[str] = Field(default_factory=list)
    term: str | None = None
    level: str | None = None
    language: str = "en"
    description: str | None = None
    topics: list[str] = Field(default_factory=list)
    license_code: str | None = None
    license_url: str | None = None
    third_party_exceptions_possible: bool = True
    supported_mode: str | None = None
    teachability_score: float | None = None
    suitability_reason: str | None = None
    catalog_state: str = "indexed"
    capability_flags: dict = Field(default_factory=dict)

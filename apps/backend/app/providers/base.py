from __future__ import annotations

from typing import Protocol

from app.schemas.assets import RawAsset
from app.schemas.course import RawCourseRecord
from app.schemas.provider import ProviderDescriptor, RawCourseManifest


class CourseProvider(Protocol):
    provider_id: str
    name: str
    base_url: str

    def descriptor(self) -> ProviderDescriptor: ...

    async def refresh_catalog(self, use_network: bool = False) -> list[RawCourseRecord]:
        """Fetch lightweight catalog metadata only."""

    async def fetch_course_manifest(self, provider_course_id: str) -> RawCourseManifest:
        """Fetch per-course page structure and asset references."""

    async def list_assets(self, manifest: RawCourseManifest) -> list[RawAsset]:
        """Discover downloadable and parseable assets without downloading them."""

    async def normalize_course(self, manifest: RawCourseManifest) -> RawCourseRecord:
        """Return normalized course metadata."""

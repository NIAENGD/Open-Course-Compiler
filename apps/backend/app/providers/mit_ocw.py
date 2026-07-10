from __future__ import annotations

from app.schemas.assets import RawAsset
from app.schemas.base import AssetType, LicenseInfo, ProviderId
from app.schemas.course import RawCourseRecord
from app.schemas.provider import ProviderCapability, ProviderDescriptor, RawCourseManifest

MIT_LICENSE = LicenseInfo(
    code="CC-BY-NC-SA-4.0",
    name="Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International",
    url="https://creativecommons.org/licenses/by-nc-sa/4.0/",
    third_party_exceptions_possible=True,
)


class MitOcwProvider:
    provider_id = ProviderId.MIT_OCW.value
    name = "MIT OpenCourseWare"
    base_url = "https://ocw.mit.edu"
    terms_url = "https://ocw.mit.edu/pages/privacy-and-terms-of-use/"

    def descriptor(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider_id=self.provider_id,
            name=self.name,
            base_url=self.base_url,
            terms_url=self.terms_url,
            license_default=MIT_LICENSE,
            capabilities=ProviderCapability(
                has_video=True,
                has_audio=True,
                has_transcripts=True,
                has_readings=True,
                has_assessments=True,
            ),
        )

    async def refresh_catalog(self, use_network: bool = False) -> list[RawCourseRecord]:
        # Lightweight normalized seed records mirror the public catalog contract and keep tests deterministic.
        return [
            RawCourseRecord(
                provider_id=self.provider_id,
                provider_course_id="18-01sc-single-variable-calculus-fall-2010",
                canonical_url="https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/",
                title="Single Variable Calculus",
                course_number="18.01SC",
                department="Mathematics",
                instructors=["David Jerison"],
                term="Fall 2010",
                level="Undergraduate",
                description="A complete first course in single variable calculus with videos, notes, assignments, and exams.",
                topics=["Mathematics", "Calculus", "Differentiation", "Integration"],
                license=MIT_LICENSE,
                raw_metadata={"capabilities": self.descriptor().capabilities.model_dump()},
            ),
            RawCourseRecord(
                provider_id=self.provider_id,
                provider_course_id="6-006-introduction-to-algorithms-spring-2020",
                canonical_url="https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
                title="Introduction to Algorithms",
                course_number="6.006",
                department="Electrical Engineering and Computer Science",
                instructors=["Erik Demaine", "Jason Ku", "Justin Solomon"],
                term="Spring 2020",
                level="Undergraduate",
                description="Design and analysis of algorithms, data structures, graph algorithms, and dynamic programming.",
                topics=["Computer Science", "Algorithms", "Data Structures"],
                license=MIT_LICENSE,
                raw_metadata={"capabilities": self.descriptor().capabilities.model_dump()},
            ),
        ]

    async def fetch_course_manifest(self, provider_course_id: str) -> RawCourseManifest:
        course = next(
            (c for c in await self.refresh_catalog() if c.provider_course_id == provider_course_id),
            None,
        )
        if course is None:
            raise ValueError(f"Unknown MIT OCW course: {provider_course_id}")
        assets = [
            RawAsset(
                provider_id=self.provider_id,
                course_id=provider_course_id,
                asset_type=AssetType.HTML,
                url=course.canonical_url,
                title="Course home",
                license_scope="course",
            ),
            RawAsset(
                provider_id=self.provider_id,
                course_id=provider_course_id,
                asset_type=AssetType.ZIP,
                url=course.canonical_url.rstrip("/") + "/download/",
                title="Course materials",
                license_scope="course",
            ),
            RawAsset(
                provider_id=self.provider_id,
                course_id=provider_course_id,
                asset_type=AssetType.VIDEO,
                url=course.canonical_url.rstrip("/") + "/video_galleries/video-lectures/",
                title="Video lectures",
                license_scope="course",
            ),
        ]
        return RawCourseManifest(
            provider_id=self.provider_id,
            provider_course_id=provider_course_id,
            canonical_url=course.canonical_url,
            title=course.title,
            course=course,
            pages=[course.canonical_url],
            assets=assets,
        )

    async def list_assets(self, manifest: RawCourseManifest) -> list[RawAsset]:
        return manifest.assets

    async def normalize_course(self, manifest: RawCourseManifest) -> RawCourseRecord:
        return manifest.course

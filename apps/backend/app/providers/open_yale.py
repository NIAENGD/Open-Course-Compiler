from __future__ import annotations

from app.schemas.assets import RawAsset
from app.schemas.base import AssetType, LicenseInfo, ProviderId
from app.schemas.course import RawCourseRecord
from app.schemas.provider import ProviderCapability, ProviderDescriptor, RawCourseManifest

OYC_LICENSE = LicenseInfo(
    code="CC-BY-NC-SA-3.0-US",
    name="Creative Commons Attribution-Noncommercial-Share Alike 3.0 United States",
    url="https://creativecommons.org/licenses/by-nc-sa/3.0/us/",
    third_party_exceptions_possible=True,
)


class OpenYaleProvider:
    provider_id = ProviderId.OPEN_YALE.value
    name = "Open Yale Courses"
    base_url = "https://oyc.yale.edu"
    terms_url = "https://oyc.yale.edu/terms"

    def descriptor(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider_id=self.provider_id,
            name=self.name,
            base_url=self.base_url,
            terms_url=self.terms_url,
            license_default=OYC_LICENSE,
            capabilities=ProviderCapability(
                has_video=True,
                has_audio=True,
                has_transcripts=True,
                has_readings=True,
                has_assessments=True,
            ),
        )

    async def refresh_catalog(self, use_network: bool = False) -> list[RawCourseRecord]:
        return [
            RawCourseRecord(
                provider_id=self.provider_id,
                provider_course_id="phil-181",
                canonical_url="https://oyc.yale.edu/philosophy/phil-181",
                title="Philosophy and the Science of Human Nature",
                course_number="PHIL 181",
                department="Philosophy",
                instructors=["Tamar Gendler"],
                term="Spring 2011",
                level="Undergraduate",
                description="Explores human nature through philosophy, psychology, and political theory with transcripts and exams.",
                topics=["Philosophy", "Psychology", "Human Nature"],
                license=OYC_LICENSE,
                raw_metadata={"capabilities": self.descriptor().capabilities.model_dump()},
            ),
            RawCourseRecord(
                provider_id=self.provider_id,
                provider_course_id="hist-202",
                canonical_url="https://oyc.yale.edu/history/hist-202",
                title="European Civilization, 1648-1945",
                course_number="HIST 202",
                department="History",
                instructors=["John Merriman"],
                term="Fall 2008",
                level="Undergraduate",
                description="A survey of modern European history with lecture transcripts, audio, video, and exams.",
                topics=["History", "Europe", "Modern History"],
                license=OYC_LICENSE,
                raw_metadata={"capabilities": self.descriptor().capabilities.model_dump()},
            ),
        ]

    async def fetch_course_manifest(self, provider_course_id: str) -> RawCourseManifest:
        course = next(
            (c for c in await self.refresh_catalog() if c.provider_course_id == provider_course_id),
            None,
        )
        if course is None:
            raise ValueError(f"Unknown Open Yale course: {provider_course_id}")
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
                asset_type=AssetType.TRANSCRIPT,
                url=course.canonical_url.rstrip("/") + "/content/transcripts",
                title="Searchable transcripts",
                license_scope="course",
            ),
            RawAsset(
                provider_id=self.provider_id,
                course_id=provider_course_id,
                asset_type=AssetType.READING,
                url=course.canonical_url.rstrip("/") + "/content/readings",
                title="Reading references",
                license_scope="third_party_unknown",
                downloadable=False,
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

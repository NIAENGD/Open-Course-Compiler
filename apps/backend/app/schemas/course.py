from __future__ import annotations

from pydantic import Field

from app.schemas.base import LicenseInfo, StrictBaseModel


class RawCourseRecord(StrictBaseModel):
    provider_id: str
    provider_course_id: str
    canonical_url: str
    title: str
    course_number: str | None = None
    department: str | None = None
    instructors: list[str] = Field(default_factory=list)
    term: str | None = None
    level: str | None = None
    description: str | None = None
    topics: list[str] = Field(default_factory=list)
    license: LicenseInfo
    raw_metadata: dict = Field(default_factory=dict)

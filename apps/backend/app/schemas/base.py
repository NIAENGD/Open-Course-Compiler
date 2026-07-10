from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class ProviderId(str, Enum):
    MIT_OCW = "mit_ocw"
    OPEN_YALE = "open_yale"


class CourseMode(str, Enum):
    FULL_LEARN = "full_learn"
    ASSISTED = "assisted"
    REFERENCE_ONLY = "reference_only"
    UNSUPPORTED = "unsupported"


class AssetType(str, Enum):
    HTML = "html"
    PDF = "pdf"
    VIDEO = "video"
    AUDIO = "audio"
    TRANSCRIPT = "transcript"
    SUBTITLE = "subtitle"
    SLIDES = "slides"
    ASSIGNMENT = "assignment"
    EXAM = "exam"
    SOLUTION = "solution"
    READING = "reading"
    IMAGE = "image"
    CODE = "code"
    DATASET = "dataset"
    ZIP = "zip"
    UNKNOWN = "unknown"


class ProcessingState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class LicenseInfo(StrictBaseModel):
    code: str | None = None
    name: str | None = None
    url: str | None = None
    attribution_required: bool = True
    noncommercial: bool = True
    sharealike: bool = True
    third_party_exceptions_possible: bool = True
    notes: str | None = None


JsonObject = dict[str, Any]

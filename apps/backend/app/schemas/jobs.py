from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import Field

from app.schemas.base import StrictBaseModel


class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class JobType(str, Enum):
    BOOTSTRAP_APP = "bootstrap_app"
    CATALOG_REFRESH = "catalog_refresh"
    GOAL_TO_PATH = "goal_to_path"
    DOWNLOAD_COURSE_ASSETS = "download_course_assets"
    COMPILE_COURSE = "compile_course"


class JobRecord(StrictBaseModel):
    id: str
    job_type: JobType
    status: JobStatus = JobStatus.QUEUED
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    progress: float = Field(default=0, ge=0, le=1)
    checkpoint: dict[str, Any] = Field(default_factory=dict)

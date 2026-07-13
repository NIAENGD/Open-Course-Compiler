from __future__ import annotations

import tempfile
from pathlib import Path

from app.db.migrate import apply_migrations
from app.db.session import connect
from app.paths import APP_DIRS, ensure_app_dirs
from app.schemas.assets import ContentChunk, RawAsset, SourceRef
from app.schemas.base import AssetType, LicenseInfo, ProviderId
from app.schemas.course import RawCourseRecord
from app.schemas.jobs import JobRecord, JobStatus, JobType


def test_paths_create_required_layout() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "OpenCourseCompiler"
        ensure_app_dirs(root)
        assert all((root / relative).is_dir() for relative in APP_DIRS)


def test_migration_creates_stage1_tables() -> None:
    required = {"providers", "courses", "course_assets", "content_chunks", "jobs", "token_ledger"}
    with tempfile.TemporaryDirectory() as tmp:
        with connect(Path(tmp) / "app.sqlite3") as conn:
            assert "0001_stage1_baseline.sql" in apply_migrations(conn)
            tables = {
                row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            }
        assert required.issubset(tables)


def test_shared_contract_schemas_validate() -> None:
    license_info = LicenseInfo(code="CC BY-NC-SA 4.0")
    course = RawCourseRecord(
        provider_id=ProviderId.MIT_OCW.value,
        provider_course_id="18-01sc",
        canonical_url="https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/",
        title="Single Variable Calculus",
        license=license_info,
    )
    asset = RawAsset(provider_id=course.provider_id, course_id="course-1", asset_type=AssetType.PDF)
    chunk = ContentChunk(
        chunk_id="chunk-1",
        course_id="course-1",
        chunk_type="notes",
        text="Derivative rules",
        source_ref=SourceRef(
            provider_id=course.provider_id, course_id="course-1", asset_id=asset.title
        ),
    )
    job = JobRecord(id="job-1", job_type=JobType.BOOTSTRAP_APP, status=JobStatus.QUEUED)
    assert chunk.source_ref.provider_id == "mit_ocw"
    assert job.progress == 0

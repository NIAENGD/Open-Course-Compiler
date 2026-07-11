from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from uuid import uuid4

from app.schemas.stage3 import CourseSuitabilityResult


def persist_suitability(conn: sqlite3.Connection, result: CourseSuitabilityResult) -> None:
    now = datetime.now(UTC).isoformat()
    conn.execute(
        "INSERT INTO course_suitability (id, course_id, supported_mode, teachability_score, ai_grading_reliability, requires_lab, requires_physical_equipment, requires_group_work, requires_final_project, requires_artifact_submission, has_sufficient_transcript_or_notes, has_assessments, risk_flags_json, evidence_json, reason, classifier_version, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            str(uuid4()),
            result.course_id,
            result.supported_mode.value,
            result.teachability_score,
            result.ai_grading_reliability,
            int(result.requires_lab),
            int(result.requires_physical_equipment),
            int(result.requires_group_work),
            int(result.requires_final_project),
            int(result.requires_artifact_submission),
            int(result.has_sufficient_transcript_or_notes),
            int(result.has_assessments),
            json.dumps(result.risk_flags),
            json.dumps(result.evidence),
            result.reason,
            result.classifier_version,
            now,
        ),
    )
    conn.execute(
        "UPDATE courses SET supported_mode=?, teachability_score=?, suitability_reason=?, updated_at=? WHERE id=?",
        (
            result.supported_mode.value,
            result.teachability_score,
            result.reason,
            now,
            result.course_id,
        ),
    )

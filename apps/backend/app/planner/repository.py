from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from uuid import uuid4

from app.schemas.stage3 import LearningPathProposal


def save_path(conn: sqlite3.Connection, proposal: LearningPathProposal) -> None:
    now = datetime.now(UTC).isoformat()
    conn.execute(
        "INSERT INTO learning_path_proposals (id, goal_id, proposal_json, accepted, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET proposal_json=excluded.proposal_json, accepted=excluded.accepted, updated_at=excluded.updated_at",
        (
            proposal.path_id,
            proposal.goal_id,
            proposal.model_dump_json(),
            int(proposal.accepted),
            now,
            now,
        ),
    )
    conn.execute(
        "INSERT INTO learning_paths (id, goal_id, title, description, depth, weekly_hours, language, planner_version, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET title=excluded.title, description=excluded.description, depth=excluded.depth, language=excluded.language, updated_at=excluded.updated_at",
        (
            proposal.path_id,
            proposal.goal_id,
            proposal.title,
            proposal.description,
            proposal.depth,
            None,
            proposal.language,
            "stage3-planner-v1",
            now,
            now,
        ),
    )
    for course in proposal.courses:
        conn.execute(
            "INSERT INTO learning_path_courses (id, path_id, course_id, sequence_index, role, inclusion_reason, mode_override, created_at) SELECT ?, ?, ?, ?, ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM learning_path_courses WHERE path_id=? AND course_id=? AND sequence_index=?)",
            (
                str(uuid4()),
                proposal.path_id,
                course.course_id,
                course.sequence_index,
                course.role,
                course.reason,
                course.supported_mode.value,
                now,
                proposal.path_id,
                course.course_id,
                course.sequence_index,
            ),
        )


def get_path(conn: sqlite3.Connection, path_id: str) -> LearningPathProposal | None:
    row = conn.execute(
        "SELECT proposal_json FROM learning_path_proposals WHERE id=?", (path_id,)
    ).fetchone()
    return LearningPathProposal.model_validate(json.loads(row[0])) if row else None


def accept_path(conn: sqlite3.Connection, path_id: str) -> LearningPathProposal | None:
    proposal = get_path(conn, path_id)
    if proposal is None:
        return None
    accepted = proposal.model_copy(update={"accepted": True})
    save_path(conn, accepted)
    return accepted

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime

from app.schemas.stage3 import ParsedGoal


def _now() -> str:
    return datetime.now(UTC).isoformat()


def save_goal(conn: sqlite3.Connection, goal: ParsedGoal) -> ParsedGoal:
    gid = goal.goal_id or ""
    now = _now()
    conn.execute(
        "INSERT INTO learning_goals (id, raw_goal, parsed_goal_json, preferred_language, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET parsed_goal_json=excluded.parsed_goal_json, updated_at=excluded.updated_at",
        (gid, goal.raw_goal, goal.model_dump_json(), goal.preferred_language, now, now),
    )
    return goal


def get_goal(conn: sqlite3.Connection, goal_id: str) -> ParsedGoal | None:
    row = conn.execute(
        "SELECT parsed_goal_json FROM learning_goals WHERE id=?", (goal_id,)
    ).fetchone()
    return ParsedGoal.model_validate(json.loads(row[0])) if row else None

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from uuid import uuid5, NAMESPACE_URL

from app.schemas.course import RawCourseRecord
from app.schemas.provider import CatalogCourse, CatalogSearchFilters, ProviderDescriptor


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _course_id(provider_id: str, provider_course_id: str) -> str:
    return str(uuid5(NAMESPACE_URL, f"{provider_id}:{provider_course_id}"))


def upsert_provider(conn: sqlite3.Connection, descriptor: ProviderDescriptor) -> None:
    now = _now()
    conn.execute(
        """INSERT INTO providers (id, name, base_url, terms_url, license_default, enabled, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 1, ?, ?)
        ON CONFLICT(id) DO UPDATE SET name=excluded.name, base_url=excluded.base_url,
        terms_url=excluded.terms_url, license_default=excluded.license_default, updated_at=excluded.updated_at""",
        (
            descriptor.provider_id,
            descriptor.name,
            descriptor.base_url,
            descriptor.terms_url,
            descriptor.model_dump_json(),
            now,
            now,
        ),
    )


def upsert_course(conn: sqlite3.Connection, record: RawCourseRecord) -> str:
    now = _now()
    cid = _course_id(record.provider_id, record.provider_course_id)
    conn.execute(
        """INSERT INTO courses (id, provider_id, provider_course_id, canonical_url, title, course_number,
        department, instructors_json, term, level, description, topics_json, license_code, license_url,
        attribution_text, third_party_exceptions_possible, catalog_state, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'indexed', ?, ?)
        ON CONFLICT(provider_id, provider_course_id) DO UPDATE SET canonical_url=excluded.canonical_url,
        title=excluded.title, course_number=excluded.course_number, department=excluded.department,
        instructors_json=excluded.instructors_json, term=excluded.term, level=excluded.level,
        description=excluded.description, topics_json=excluded.topics_json, license_code=excluded.license_code,
        license_url=excluded.license_url, attribution_text=excluded.attribution_text,
        third_party_exceptions_possible=excluded.third_party_exceptions_possible, catalog_state='indexed',
        updated_at=excluded.updated_at""",
        (
            cid,
            record.provider_id,
            record.provider_course_id,
            record.canonical_url,
            record.title,
            record.course_number,
            record.department,
            json.dumps(record.instructors),
            record.term,
            record.level,
            record.description,
            json.dumps(record.topics),
            record.license.code,
            record.license.url,
            f"{record.title} by {record.provider_id}",
            int(record.license.third_party_exceptions_possible),
            now,
            now,
        ),
    )
    return cid


def list_courses(conn: sqlite3.Connection, filters: CatalogSearchFilters) -> list[CatalogCourse]:
    clauses: list[str] = []
    params: list[object] = []
    if filters.q:
        clauses.append(
            "(lower(title) LIKE ? OR lower(description) LIKE ? OR lower(topics_json) LIKE ?)"
        )
        like = f"%{filters.q.lower()}%"
        params.extend([like, like, like])
    for field, value in (
        ("provider_id", filters.provider),
        ("department", filters.department),
        ("supported_mode", filters.mode),
        ("license_code", filters.license),
    ):
        if value:
            clauses.append(f"{field} = ?")
            params.append(value)
    if filters.topic:
        clauses.append("lower(topics_json) LIKE ?")
        params.append(f"%{filters.topic.lower()}%")
    if filters.min_teachability_score is not None:
        clauses.append("teachability_score >= ?")
        params.append(filters.min_teachability_score)
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    rows = conn.execute(
        "SELECT * FROM courses" + where + " ORDER BY provider_id, title", params
    ).fetchall()
    return [_row_to_course(r) for r in rows]


def get_course(conn: sqlite3.Connection, course_id: str) -> CatalogCourse | None:
    row = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    return _row_to_course(row) if row else None


def _row_to_course(row: sqlite3.Row) -> CatalogCourse:
    return CatalogCourse(
        id=row["id"],
        provider_id=row["provider_id"],
        provider_course_id=row["provider_course_id"],
        canonical_url=row["canonical_url"],
        title=row["title"],
        course_number=row["course_number"],
        department=row["department"],
        instructors=json.loads(row["instructors_json"]),
        term=row["term"],
        level=row["level"],
        language=row["language"],
        description=row["description"],
        topics=json.loads(row["topics_json"]),
        license_code=row["license_code"],
        license_url=row["license_url"],
        third_party_exceptions_possible=bool(row["third_party_exceptions_possible"]),
        supported_mode=row["supported_mode"],
        teachability_score=row["teachability_score"],
        suitability_reason=row["suitability_reason"],
        catalog_state=row["catalog_state"],
        capability_flags={},
    )

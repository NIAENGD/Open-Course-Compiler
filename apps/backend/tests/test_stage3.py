from __future__ import annotations

import asyncio
import sqlite3
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from app.catalog.repository import get_course, upsert_course, upsert_provider
from app.db.migrate import apply_migrations
from app.db.session import connect
from app.main import create_app
from app.providers.mit_ocw import MIT_LICENSE, MitOcwProvider
from app.providers.open_yale import OpenYaleProvider
from app.schemas.course import RawCourseRecord
from app.suitability.classifier import classify_course


def test_stage3_suitability_guardrails_and_catalog_persistence() -> None:
    lab = RawCourseRecord(
        provider_id="mit_ocw",
        provider_course_id="lab-1",
        canonical_url="https://example.test/lab",
        title="Robotics Hardware Laboratory",
        description="A lab course with Arduino, circuit board fabrication, team project, and prototype.",
        topics=["robotics hardware", "laboratory"],
        license=MIT_LICENSE,
    )
    with tempfile.TemporaryDirectory() as tmp:
        with connect(Path(tmp) / "app.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            apply_migrations(conn)
            provider = MitOcwProvider()
            upsert_provider(conn, provider.descriptor())
            course_id = upsert_course(conn, lab)
            result = classify_course(get_course(conn, course_id))  # type: ignore[arg-type]
            assert result.supported_mode.value == "reference_only"
            assert result.requires_physical_equipment is True
            assert result.requires_lab is True
            assert result.teachability_score < 0.75


def test_stage3_goal_parse_clarification_and_path_planning_api(monkeypatch) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setenv("OCC_DATA_DIR", tmp)
        app = create_app()
        with TestClient(app) as client:
            refresh = client.post("/catalog/refresh", json={"providers": [], "use_network": False})
            assert refresh.status_code == 200
            assert refresh.json()["upserted"] == 4

            parsed = client.post("/goals/parse", json={"raw_goal": "我想学哲学"})
            assert parsed.status_code == 200
            goal = parsed.json()
            assert goal["needs_clarification"] is True
            assert goal["clarifying_questions"]

            answered = client.post(
                f"/goals/{goal['goal_id']}/answer-clarification",
                json={"answers": [{"question_id": "q_path", "option_id": "intro"}]},
            )
            assert answered.status_code == 200
            assert answered.json()["needs_clarification"] is False

            proposal = client.post("/paths/propose", json={"goal_id": goal["goal_id"]})
            assert proposal.status_code == 200
            body = proposal.json()
            assert body["courses"]
            assert all(course["supported_mode"] == "full_learn" for course in body["courses"])
            assert body["excluded_courses"]
            assert body["courses"][0]["reason"]

            accepted = client.post(f"/paths/{body['path_id']}/accept")
            assert accepted.status_code == 200
            assert accepted.json()["accepted"] is True


def test_stage3_refresh_classifies_courses_for_search() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        with connect(Path(tmp) / "app.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            apply_migrations(conn)
            for provider in [MitOcwProvider(), OpenYaleProvider()]:
                upsert_provider(conn, provider.descriptor())
                for record in asyncio.run(provider.refresh_catalog()):
                    course_id = upsert_course(conn, record)
                    course = get_course(conn, course_id)
                    assert classify_course(course).supported_mode.value in {
                        "full_learn",
                        "assisted",
                        "reference_only",
                    }  # type: ignore[arg-type]
            conn.commit()

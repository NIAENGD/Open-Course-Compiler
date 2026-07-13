from __future__ import annotations

import re

from app.schemas.base import CourseMode
from app.schemas.provider import CatalogCourse
from app.schemas.stage3 import CourseSuitabilityResult

DOWNGRADE = {
    "lab",
    "laboratory",
    "studio",
    "workshop",
    "hardware",
    "circuit board",
    "arduino",
    "robot",
    "robotics hardware",
    "drone",
    "fabrication",
    "machining",
    "wet lab",
    "experiment",
    "fieldwork",
    "team project",
    "group project",
    "prototype",
    "physical model",
    "performance",
    "recital",
    "painting",
    "sculpture",
    "design-build",
}
CAUTION = {
    "final paper",
    "essay",
    "project proposal",
    "programming assignment",
    "capstone",
    "term project",
    "presentation",
    "peer review",
    "portfolio",
    "project",
}
STRONG = {
    "lecture",
    "lectures",
    "transcript",
    "transcripts",
    "notes",
    "readings",
    "exam",
    "exams",
    "problem set",
    "problem sets",
    "quiz",
    "quizzes",
    "syllabus",
    "discussion questions",
    "essay questions",
    "assignments",
    "videos",
}


def _contains(text: str, phrase: str) -> bool:
    return re.search(rf"\b{re.escape(phrase)}\b", text) is not None


def classify_course(course: CatalogCourse) -> CourseSuitabilityResult:
    text = " ".join(
        [course.title, course.description or "", " ".join(course.topics), course.department or ""]
    ).lower()
    found_down = sorted(k for k in DOWNGRADE if _contains(text, k))
    found_caution = sorted(k for k in CAUTION if _contains(text, k))
    found_strong = sorted(k for k in STRONG if _contains(text, k))

    requires_lab = any(k in found_down for k in ["lab", "laboratory", "wet lab", "experiment"])
    requires_physical = any(
        k in found_down
        for k in [
            "hardware",
            "circuit board",
            "arduino",
            "robot",
            "robotics hardware",
            "drone",
            "fabrication",
            "machining",
            "physical model",
            "painting",
            "sculpture",
            "design-build",
        ]
    )
    requires_group = any(k in found_down for k in ["team project", "group project"])
    artifact = any(
        k in found_down
        for k in ["prototype", "physical model", "performance", "recital", "painting", "sculpture"]
    )
    final_project = any(
        k in found_caution for k in ["project", "term project", "capstone", "project proposal"]
    )

    has_transcript_notes = bool(
        {"transcript", "transcripts", "notes", "lecture", "lectures", "videos"} & set(found_strong)
    )
    has_assessments = bool(
        {
            "exam",
            "exams",
            "problem set",
            "problem sets",
            "quiz",
            "quizzes",
            "assignments",
            "essay questions",
            "discussion questions",
        }
        & set(found_strong)
    )
    content = min(1.0, 0.35 + 0.07 * len(found_strong) + (0.1 if course.description else 0))
    transcript = 1.0 if has_transcript_notes else 0.25
    assess = 1.0 if has_assessments else 0.25
    sequential = 0.8 if course.level or course.course_number else 0.55
    text_ratio = 0.9 if not requires_physical else 0.2
    license_clarity = 0.9 if course.license_code and course.license_url else 0.5
    physical_dep = 1.0 if requires_physical or requires_lab else 0.0
    project_dep = 0.8 if final_project or artifact else 0.0
    group_dep = 1.0 if requires_group else 0.0
    score = (
        0.25 * content
        + 0.20 * transcript
        + 0.20 * assess
        + 0.15 * sequential
        + 0.10 * text_ratio
        + 0.10 * license_clarity
        - 0.35 * physical_dep
        - 0.25 * project_dep
        - 0.20 * group_dep
    )
    score = max(0.0, min(1.0, round(score, 2)))

    if requires_physical or requires_lab or requires_group or artifact:
        mode = CourseMode.REFERENCE_ONLY
    elif project_dep >= 0.7:
        mode = CourseMode.ASSISTED
    elif score >= 0.75:
        mode = CourseMode.FULL_LEARN
    elif score >= 0.45:
        mode = CourseMode.ASSISTED
    else:
        mode = CourseMode.REFERENCE_ONLY

    evidence = [f"matched strong suitability keyword: {k}" for k in found_strong]
    evidence += [f"matched downgrade keyword: {k}" for k in found_down]
    evidence += [f"matched caution keyword: {k}" for k in found_caution]
    if course.license_code:
        evidence.append(f"license is declared as {course.license_code}")
    risks = []
    if requires_lab:
        risks.append("lab_dependency")
    if requires_physical:
        risks.append("physical_equipment_dependency")
    if requires_group:
        risks.append("group_work_dependency")
    if final_project:
        risks.append("open_project_dependency")
    if not has_transcript_notes:
        risks.append("insufficient_transcript_or_notes")
    if not has_assessments:
        risks.append("limited_assessments")
    return CourseSuitabilityResult(
        course_id=course.id,
        course_type="lecture_based" if has_transcript_notes else "metadata_only",
        supported_mode=mode,
        teachability_score=score,
        ai_grading_reliability="high" if has_assessments and not final_project else "medium",
        requires_lab=requires_lab,
        requires_physical_equipment=requires_physical,
        requires_group_work=requires_group,
        requires_final_project=final_project,
        requires_artifact_submission=artifact,
        has_sufficient_transcript_or_notes=has_transcript_notes,
        has_assessments=has_assessments,
        risk_flags=risks,
        evidence=evidence or ["metadata inspected by deterministic rule classifier"],
        reason=f"Classified as {mode.value} with score {score} using deterministic guardrails.",
    )

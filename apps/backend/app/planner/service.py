from __future__ import annotations

from uuid import uuid4

from app.schemas.base import CourseMode
from app.schemas.provider import CatalogCourse
from app.schemas.stage3 import ExcludedCourse, LearningPathProposal, ParsedGoal, PathCourse

DOMAIN_TERMS = {
    "philosophy": ["philosophy", "human nature", "psychology"],
    "mathematics": ["mathematics", "calculus"],
    "computer_science": ["computer science", "algorithms", "data structures"],
    "history": ["history", "europe"],
}


def _relevance(goal: ParsedGoal, course: CatalogCourse) -> int:
    text = " ".join(
        [course.title, course.description or "", " ".join(course.topics), course.department or ""]
    ).lower()
    return sum(
        1
        for term in DOMAIN_TERMS.get(goal.domain, []) + goal.subdomains
        if term.replace("_", " ") in text
    )


def build_path(
    goal: ParsedGoal, courses: list[CatalogCourse], preferred_mode: CourseMode | None = None
) -> LearningPathProposal:
    mode = preferred_mode or goal.preferred_course_mode
    ranked = sorted(
        courses, key=lambda c: (_relevance(goal, c), c.teachability_score or 0), reverse=True
    )
    selected: list[PathCourse] = []
    supplemental: list[PathCourse] = []
    excluded: list[ExcludedCourse] = []
    for course in ranked:
        c_mode = CourseMode(course.supported_mode or CourseMode.REFERENCE_ONLY.value)
        rel = _relevance(goal, course)
        if c_mode == CourseMode.FULL_LEARN and (mode == CourseMode.FULL_LEARN) and rel > 0:
            selected.append(
                PathCourse(
                    course_id=course.id,
                    sequence_index=len(selected) + 1,
                    role="foundation" if not selected else "core",
                    supported_mode=c_mode,
                    reason="Included because it matches the learning goal and is classified full_learn.",
                )
            )
        elif c_mode == CourseMode.ASSISTED and rel > 0:
            supplemental.append(
                PathCourse(
                    course_id=course.id,
                    sequence_index=len(supplemental) + 1,
                    role="optional_practice",
                    supported_mode=c_mode,
                    reason="Kept supplemental because assisted courses require learner or instructor judgment.",
                )
            )
        elif c_mode == CourseMode.REFERENCE_ONLY and rel > 0:
            supplemental.append(
                PathCourse(
                    course_id=course.id,
                    sequence_index=len(supplemental) + 1,
                    role="reference",
                    supported_mode=c_mode,
                    reason="Kept as reference_only material rather than the main path.",
                )
            )
        else:
            excluded.append(
                ExcludedCourse(
                    course_id=course.id,
                    reason="Excluded because provider metadata did not match the parsed goal or mode guardrails.",
                )
            )
    assumptions = list(goal.assumptions)
    if goal.time_budget_hours_per_week is None:
        assumptions.append(
            "User did not specify weekly time budget; default path assumes moderate pace."
        )
    title_domain = goal.domain.replace("_", " ").title()
    return LearningPathProposal(
        path_id=str(uuid4()),
        goal_id=goal.goal_id,
        title=f"{title_domain} learning path",
        description="A cross-provider path ordered by conceptual fit and deterministic suitability guardrails.",
        language=goal.preferred_language,
        depth=goal.depth if goal.depth != "unknown" else "undergraduate_intro",
        estimated_total_hours=max(20, 40 * max(1, len(selected))),
        courses=selected,
        supplemental_courses=supplemental,
        excluded_courses=excluded,
        assumptions=assumptions,
    )

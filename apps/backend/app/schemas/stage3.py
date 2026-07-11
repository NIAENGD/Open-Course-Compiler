from __future__ import annotations

from typing import Literal

from pydantic import Field

from app.schemas.base import CourseMode, StrictBaseModel


class CourseSuitabilityResult(StrictBaseModel):
    course_id: str | None = None
    course_type: str
    supported_mode: CourseMode
    teachability_score: float = Field(ge=0, le=1)
    ai_grading_reliability: Literal["low", "medium", "high"]
    requires_lab: bool = False
    requires_physical_equipment: bool = False
    requires_group_work: bool = False
    requires_final_project: bool = False
    requires_artifact_submission: bool = False
    has_sufficient_transcript_or_notes: bool = False
    has_assessments: bool = False
    risk_flags: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    reason: str
    classifier_version: str = "stage3-rules-v1"


class ClarifyingOption(StrictBaseModel):
    id: str
    label: str


class ClarifyingQuestion(StrictBaseModel):
    id: str
    question: str
    options: list[ClarifyingOption]


class ParsedGoal(StrictBaseModel):
    goal_id: str | None = None
    raw_goal: str
    domain: str
    subdomains: list[str] = Field(default_factory=list)
    depth: str = "unknown"
    preferred_language: str = "zh"
    preferred_course_mode: CourseMode = CourseMode.FULL_LEARN
    time_budget_hours_per_week: int | None = Field(default=None, ge=1)
    needs_clarification: bool = False
    clarifying_questions: list[ClarifyingQuestion] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)


class GoalParseRequest(StrictBaseModel):
    raw_goal: str
    preferred_language: str | None = None
    preferred_course_mode: CourseMode | None = None
    time_budget_hours_per_week: int | None = Field(default=None, ge=1)


class ClarificationAnswer(StrictBaseModel):
    question_id: str
    option_id: str | None = None
    free_text: str | None = None


class ClarificationAnswerRequest(StrictBaseModel):
    answers: list[ClarificationAnswer] = Field(default_factory=list)


class PathCourse(StrictBaseModel):
    course_id: str
    sequence_index: int
    role: str
    supported_mode: CourseMode
    reason: str


class ExcludedCourse(StrictBaseModel):
    course_id: str
    reason: str


class LearningPathProposal(StrictBaseModel):
    path_id: str | None = None
    goal_id: str | None = None
    title: str
    description: str
    language: str = "zh"
    depth: str
    estimated_total_hours: int
    courses: list[PathCourse] = Field(default_factory=list)
    supplemental_courses: list[PathCourse] = Field(default_factory=list)
    excluded_courses: list[ExcludedCourse] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    accepted: bool = False


class PathProposeRequest(StrictBaseModel):
    goal_id: str | None = None
    raw_goal: str | None = None
    answers: list[ClarificationAnswer] = Field(default_factory=list)
    candidate_course_ids: list[str] = Field(default_factory=list)
    preferred_mode: CourseMode | None = None

from __future__ import annotations

import sqlite3
from fastapi import APIRouter, HTTPException

from app.catalog.repository import get_course, list_courses
from app.db.session import connect
from app.goals.repository import get_goal, save_goal
from app.goals.service import apply_answers, parse_goal
from app.planner.repository import accept_path as accept_path_record
from app.planner.repository import get_path as get_path_record
from app.planner.repository import save_path
from app.planner.service import build_path
from app.schemas.provider import CatalogSearchFilters
from app.schemas.stage3 import (
    ClarificationAnswerRequest,
    GoalParseRequest,
    ParsedGoal,
    PathProposeRequest,
    LearningPathProposal,
    CourseSuitabilityResult,
)
from app.suitability.classifier import classify_course
from app.suitability.repository import persist_suitability

router = APIRouter(tags=["stage3"])


@router.post("/goals/parse", response_model=ParsedGoal)
def parse_goal_route(request: GoalParseRequest) -> ParsedGoal:
    goal = parse_goal(request)
    with connect() as conn:
        save_goal(conn, goal)
        conn.commit()
    return goal


@router.post("/goals/{goal_id}/answer-clarification", response_model=ParsedGoal)
def answer_clarification(goal_id: str, request: ClarificationAnswerRequest) -> ParsedGoal:
    with connect() as conn:
        goal = get_goal(conn, goal_id)
        if goal is None:
            raise HTTPException(status_code=404, detail="Goal not found")
        updated = apply_answers(goal, request.answers)
        save_goal(conn, updated)
        conn.commit()
        return updated


@router.post("/catalog/courses/{course_id}/suitability", response_model=CourseSuitabilityResult)
def classify_course_route(course_id: str) -> CourseSuitabilityResult:
    with connect() as conn:
        conn.row_factory = sqlite3.Row
        course = get_course(conn, course_id)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        result = classify_course(course)
        persist_suitability(conn, result)
        conn.commit()
        return result


@router.post("/paths/propose", response_model=LearningPathProposal)
def propose_path(request: PathProposeRequest) -> LearningPathProposal:
    with connect() as conn:
        conn.row_factory = sqlite3.Row
        if request.goal_id:
            goal = get_goal(conn, request.goal_id)
            if goal is None:
                raise HTTPException(status_code=404, detail="Goal not found")
        elif request.raw_goal:
            goal = parse_goal(GoalParseRequest(raw_goal=request.raw_goal))
            goal = apply_answers(goal, request.answers)
            save_goal(conn, goal)
        else:
            raise HTTPException(status_code=422, detail="goal_id or raw_goal is required")
        if request.answers and goal.needs_clarification:
            goal = apply_answers(goal, request.answers)
            save_goal(conn, goal)
        filters = CatalogSearchFilters()
        courses = list_courses(conn, filters)
        if request.candidate_course_ids:
            allowed = set(request.candidate_course_ids)
            courses = [course for course in courses if course.id in allowed]
        for course in courses:
            if course.supported_mode is None:
                result = classify_course(course)
                persist_suitability(conn, result)
        courses = list_courses(conn, filters)
        if request.candidate_course_ids:
            allowed = set(request.candidate_course_ids)
            courses = [course for course in courses if course.id in allowed]
        proposal = build_path(goal, courses, request.preferred_mode)
        save_path(conn, proposal)
        conn.commit()
        return proposal


@router.get("/paths/{path_id}", response_model=LearningPathProposal)
def get_path(path_id: str) -> LearningPathProposal:
    with connect() as conn:
        proposal = get_path_record(conn, path_id)
    if proposal is None:
        raise HTTPException(status_code=404, detail="Path not found")
    return proposal


@router.post("/paths/{path_id}/accept", response_model=LearningPathProposal)
def accept_path(path_id: str) -> LearningPathProposal:
    with connect() as conn:
        accepted = accept_path_record(conn, path_id)
        conn.commit()
    if accepted is None:
        raise HTTPException(status_code=404, detail="Path not found")
    return accepted

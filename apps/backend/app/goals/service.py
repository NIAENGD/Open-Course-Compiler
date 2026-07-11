from __future__ import annotations

import re
from uuid import uuid4

from app.schemas.base import CourseMode
from app.schemas.stage3 import (
    ClarifyingOption,
    ClarifyingQuestion,
    GoalParseRequest,
    ParsedGoal,
    ClarificationAnswer,
)

DOMAIN_MAP = {
    "philosophy": ["philosophy", "哲学", "ethics", "伦理", "political philosophy", "政治哲学"],
    "computer_science": [
        "ai",
        "artificial intelligence",
        "算法",
        "computer",
        "计算机",
        "programming",
    ],
    "mathematics": ["math", "数学", "calculus", "微积分", "algebra"],
    "economics": ["economics", "经济"],
    "history": ["history", "历史"],
}


def parse_goal(request: GoalParseRequest) -> ParsedGoal:
    raw = request.raw_goal.strip()
    lower = raw.lower()
    domain = "general"
    for key, terms in DOMAIN_MAP.items():
        if any(term.lower() in lower for term in terms):
            domain = key
            break
    language = request.preferred_language or ("zh" if re.search(r"[\u4e00-\u9fff]", raw) else "en")
    depth = (
        "beginner" if any(x in lower for x in ["from zero", "从零", "intro", "入门"]) else "unknown"
    )
    subdomains: list[str] = []
    if "政治" in raw or "political" in lower:
        subdomains.append("political_philosophy")
    if "ai" in lower or "人工智能" in raw:
        subdomains.append("artificial_intelligence")
    if "calculus" in lower or "微积分" in raw:
        subdomains.append("calculus")
    unclear = domain == "general" or not subdomains or depth == "unknown"
    questions: list[ClarifyingQuestion] = []
    if unclear:
        if domain == "philosophy":
            questions.append(
                ClarifyingQuestion(
                    id="q_path",
                    question="你更想学哪一种哲学路径？",
                    options=[
                        ClarifyingOption(id="intro", label="通识入门"),
                        ClarifyingOption(id="ethics", label="伦理学"),
                        ClarifyingOption(id="political", label="政治哲学"),
                        ClarifyingOption(id="mind", label="心灵哲学"),
                    ],
                )
            )
        elif domain == "general":
            questions.append(
                ClarifyingQuestion(
                    id="q_domain",
                    question="你希望优先学习哪个领域？",
                    options=[
                        ClarifyingOption(id="philosophy", label="哲学"),
                        ClarifyingOption(id="mathematics", label="数学"),
                        ClarifyingOption(id="computer_science", label="计算机科学"),
                    ],
                )
            )
        if depth == "unknown":
            questions.append(
                ClarifyingQuestion(
                    id="q_depth",
                    question="你希望课程深度是什么？",
                    options=[
                        ClarifyingOption(id="intro", label="本科入门"),
                        ClarifyingOption(id="intermediate", label="本科进阶"),
                        ClarifyingOption(id="survey", label="通识综览"),
                    ],
                )
            )
    return ParsedGoal(
        goal_id=str(uuid4()),
        raw_goal=raw,
        domain=domain,
        subdomains=subdomains,
        depth=depth,
        preferred_language=language,
        preferred_course_mode=request.preferred_course_mode or CourseMode.FULL_LEARN,
        time_budget_hours_per_week=request.time_budget_hours_per_week,
        needs_clarification=bool(questions),
        clarifying_questions=questions,
    )


def apply_answers(goal: ParsedGoal, answers: list[ClarificationAnswer]) -> ParsedGoal:
    assumptions = list(goal.assumptions)
    subdomains = list(goal.subdomains)
    depth = goal.depth
    domain = goal.domain
    if not answers:
        assumptions.append(
            "User did not answer clarifying questions; default planner assumptions were applied."
        )
    for answer in answers:
        selected = answer.option_id or (answer.free_text or "").lower()
        if answer.question_id == "q_domain" and selected in DOMAIN_MAP:
            domain = selected
        if selected == "political":
            subdomains.append("political_philosophy")
        if selected in {"intro", "survey"}:
            depth = "undergraduate_intro"
        if selected == "intermediate":
            depth = "undergraduate_intermediate"
    return goal.model_copy(
        update={
            "domain": domain,
            "subdomains": sorted(set(subdomains)),
            "depth": depth if depth != "unknown" else "undergraduate_intro",
            "needs_clarification": False,
            "clarifying_questions": [],
            "assumptions": assumptions,
        }
    )

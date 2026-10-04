"""Composition root for the local controlled-case preview."""

from datetime import date

from mira.application.services import QueueItem, build_queue
from mira.domain.deadlines import CaseDeadlines, evaluate_deadlines
from mira.domain.policy import ControlledCase, DEFAULT_POLICY, F4Evaluation, F4Outcome, evaluate_case
from mira.domain.review import HumanDecision, build_human_decision
from mira.infrastructure.controlled_cases import get_controlled_case, list_controlled_cases
from mira.infrastructure.review_store import get_decision, save_decision

CONTROLLED_TODAY = date(2026, 10, 6)


def controlled_cases() -> tuple[ControlledCase, ...]:
    return list_controlled_cases()


def queue_items(query: str = "", priority: str = "all") -> tuple[QueueItem, ...]:
    decisions = {
        case.case_id: decision
        for case in controlled_cases()
        if (decision := get_decision(case.case_id)) is not None
    }
    return build_queue(controlled_cases(), DEFAULT_POLICY, CONTROLLED_TODAY, query=query, priority=priority, decisions=decisions)


def case_detail(case_id: str) -> tuple[ControlledCase, F4Evaluation, CaseDeadlines, HumanDecision | None] | None:
    case = get_controlled_case(case_id)
    if case is None:
        return None
    return case, evaluate_case(case, DEFAULT_POLICY), evaluate_deadlines(case, CONTROLLED_TODAY), get_decision(case_id)


def run_f4(case_id: str) -> tuple[ControlledCase, F4Evaluation] | None:
    detail = case_detail(case_id)
    if detail is None:
        return None
    case, evaluation, _deadlines, _decision = detail
    return case, evaluation


def register_human_decision(
    *,
    case_id: str,
    action_code: str,
    reason_code: str,
    comment: str,
    operator: str = "Operador demo",
    created_at: str = "04 oct 2026 · 12:00",
) -> tuple[HumanDecision | None, dict[str, str]]:
    detail = case_detail(case_id)
    if detail is None:
        return None, {"case": "Caso controlado no encontrado."}
    _case, evaluation, _deadlines, existing_decision = detail
    if evaluation.outcome not in (F4Outcome.REVIEW, F4Outcome.ESCALATED):
        return None, {"case": "Solo los Casos en revisión o escalados admiten decisión humana."}
    if existing_decision is not None:
        return None, {"case": "Este Caso ya tiene una decisión humana registrada."}
    decision, errors = build_human_decision(
        case_id=case_id,
        action_code=action_code,
        reason_code=reason_code,
        comment=comment,
        operator=operator,
        created_at=created_at,
        platform_outcome=evaluation.outcome,
    )
    if decision is None:
        return None, errors
    return save_decision(decision), {}

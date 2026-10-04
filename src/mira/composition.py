"""Composition root for the local controlled-case preview."""

from mira.application.services import QueueItem, build_queue
from mira.domain.policy import ControlledCase, DEFAULT_POLICY, F4Evaluation, evaluate_case
from mira.infrastructure.controlled_cases import get_controlled_case, list_controlled_cases


def controlled_cases() -> tuple[ControlledCase, ...]:
    return list_controlled_cases()


def queue_items(query: str = "", priority: str = "all") -> tuple[QueueItem, ...]:
    return build_queue(controlled_cases(), DEFAULT_POLICY, query=query, priority=priority)


def case_detail(case_id: str) -> tuple[ControlledCase, F4Evaluation] | None:
    case = get_controlled_case(case_id)
    if case is None:
        return None
    return case, evaluate_case(case, DEFAULT_POLICY)


def run_f4(case_id: str) -> tuple[ControlledCase, F4Evaluation] | None:
    return case_detail(case_id)

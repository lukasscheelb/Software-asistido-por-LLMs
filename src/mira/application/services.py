"""Queries for the controlled MIRA preview."""

from dataclasses import dataclass

from mira.domain.policy import ControlledCase, F4Evaluation, F4Outcome, Policy, evaluate_case
from mira.domain.review import HumanDecision


@dataclass(frozen=True)
class QueueItem:
    case: ControlledCase
    evaluation: F4Evaluation
    decision: HumanDecision | None = None


def build_queue(
    cases: tuple[ControlledCase, ...],
    policy: Policy,
    query: str = "",
    priority: str = "all",
    decisions: dict[str, HumanDecision] | None = None,
) -> tuple[QueueItem, ...]:
    decisions = decisions or {}
    normalized_query = query.casefold()
    items = []
    for case in cases:
        evaluation = evaluate_case(case, policy)
        if evaluation.outcome not in (F4Outcome.REVIEW, F4Outcome.ESCALATED):
            continue
        decision = decisions.get(case.case_id)
        if decision is not None:
            continue
        if priority != "all" and evaluation.priority.casefold() != priority.casefold():
            continue
        searchable = f"{case.case_id} {case.applicant} {evaluation.reason}".casefold()
        if normalized_query and normalized_query not in searchable:
            continue
        items.append(QueueItem(case=case, evaluation=evaluation, decision=decision))

    return tuple(sorted(items, key=lambda item: (item.evaluation.priority != "Alta", item.case.contractual_deadline, item.case.case_id)))

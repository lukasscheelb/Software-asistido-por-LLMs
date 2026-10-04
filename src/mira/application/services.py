"""Queries for the controlled MIRA preview."""

from dataclasses import dataclass
from datetime import date

from mira.domain.deadlines import CaseDeadlines, evaluate_deadlines
from mira.domain.policy import ControlledCase, F4Evaluation, F4Outcome, Policy, evaluate_case
from mira.domain.review import HumanDecision


@dataclass(frozen=True)
class QueueItem:
    case: ControlledCase
    evaluation: F4Evaluation
    deadlines: CaseDeadlines
    decision: HumanDecision | None = None

    @property
    def priority(self) -> str:
        if self.evaluation.priority == "Alta" or self.deadlines.contractual_state == "Vencido":
            return "Alta"
        return "Normal"


def build_queue(
    cases: tuple[ControlledCase, ...],
    policy: Policy,
    today: date,
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
        deadlines = evaluate_deadlines(case, today)
        item = QueueItem(case=case, evaluation=evaluation, deadlines=deadlines, decision=decision)
        if priority != "all" and item.priority.casefold() != priority.casefold():
            continue
        searchable = f"{case.case_id} {case.applicant} {evaluation.reason}".casefold()
        if normalized_query and normalized_query not in searchable:
            continue
        items.append(item)

    return tuple(sorted(items, key=lambda item: (item.priority != "Alta", item.deadlines.contractual_due, item.case.case_id)))

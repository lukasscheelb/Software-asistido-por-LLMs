"""In-memory review intervention store for the local F1 demo."""

from mira.domain.review import HumanDecision


_DECISIONS: dict[str, HumanDecision] = {}


def save_decision(decision: HumanDecision) -> HumanDecision:
    _DECISIONS[decision.case_id] = decision
    return decision


def get_decision(case_id: str) -> HumanDecision | None:
    return _DECISIONS.get(case_id)


def clear_decisions() -> None:
    _DECISIONS.clear()

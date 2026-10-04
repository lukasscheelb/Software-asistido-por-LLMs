from dataclasses import replace
from decimal import Decimal
from mira.domain.policy import evaluate_case, F4Outcome
from mira.infrastructure.controlled_cases import get_controlled_case


def test_absence_never_approves():
    case = get_controlled_case("CC-F4-04")
    for field in ("authenticity", "coherence"):
        assert evaluate_case(replace(case, **{field: None})).outcome == F4Outcome.REVIEW


def test_fraud_does_not_hide_invalid_input():
    assert (
        evaluate_case(
            replace(get_controlled_case("CC-F4-05"), score=Decimal("NaN"))
        ).outcome
        == F4Outcome.ERROR
    )

"""Composition root, using persisted original evaluations and a shared clock."""

from dataclasses import asdict, replace
from decimal import Decimal, InvalidOperation
from mira.application.services import build_queue
from mira.domain.deadlines import evaluate_deadlines
from mira.domain.policy import F4Outcome
from mira.domain.review import build_human_decision, category_by_code, HumanAction
from mira.infrastructure.clock import clock
from mira.infrastructure import review_store as store

CONTROLLED_TODAY = clock.today()


def controlled_cases():
    return store.cases()


def queue_items(query="", priority="all"):
    cases = controlled_cases()
    decisions = {c.case_id: store.get_decision(c.case_id) for c in cases}
    evaluations = {c.case_id: store.snapshot(c.case_id)[1] for c in cases}
    return build_queue(
        cases,
        None,
        clock.today(),
        query=query,
        priority=priority,
        decisions=decisions,
        evaluations=evaluations,
    )


def case_detail(case_id):
    case = next((c for c in controlled_cases() if c.case_id == case_id), None)
    if case is None:
        return None
    return (
        case,
        store.snapshot(case_id)[1],
        evaluate_deadlines(case, clock.today()),
        store.get_decision(case_id),
    )


def run_f4(case_id):
    detail = case_detail(case_id)
    return detail[:2] if detail else None


def register_human_decision(
    *,
    case_id,
    action_code,
    reason_code,
    comment,
    expected_case_version,
    operator="Operador demo",
    discrepancy=False,
):
    detail = case_detail(case_id)
    if not detail:
        return None, {"case": "Caso controlado no encontrado.", "code": "invalid_input"}
    evaluation = detail[1]
    if evaluation.outcome not in (F4Outcome.REVIEW, F4Outcome.ESCALATED):
        return None, {
            "case": "Este Caso no admite intervención F1.",
            "code": "invalid_input",
        }
    decision, errors = build_human_decision(
        case_id=case_id,
        action_code=action_code,
        reason_code=reason_code,
        comment=comment,
        operator=operator,
        created_at=clock.now().isoformat(),
        platform_outcome=evaluation.outcome,
        discrepancy=discrepancy,
    )
    if errors:
        errors["code"] = (
            "reason_required"
            if "comment" in errors or not reason_code
            else "invalid_input"
        )
        return None, errors
    decision = replace(decision, case_version=expected_case_version + 1)
    try:
        store.save_intervention(
            case_id, expected_case_version, "decision", asdict(decision)
        )
    except store.StaleVersion:
        return None, {
            "case": "Versión obsoleta. Recarga el Caso para ver la intervención vigente.",
            "code": "stale_version",
        }
    return decision, {}


def register_correction(
    *,
    case_id,
    expected_case_version,
    corrected,
    reason_code,
    comment,
    operator="Operador demo",
):
    detail = case_detail(case_id)
    if not detail or detail[1].outcome not in (F4Outcome.REVIEW, F4Outcome.ESCALATED):
        return None, {
            "case": "Este Caso no admite Corrección F1.",
            "code": "invalid_input",
        }
    category = category_by_code(reason_code)
    if category is None or (category.requires_comment and not comment.strip()):
        return None, {
            "case": "La Corrección exige motivo; Otro exige comentario.",
            "code": "reason_required",
        }
    if HumanAction.CORRECT not in category.actions:
        return None, {
            "case": "Motivo incompatible con Corrección.",
            "code": "invalid_input",
        }
    try:
        amount = Decimal(corrected)
        if not amount.is_finite() or amount < 0:
            raise InvalidOperation
    except (InvalidOperation, ValueError):
        return None, {
            "case": "Ingresa un importe finito y no negativo.",
            "code": "invalid_input",
        }
    record = store.snapshot(case_id)[0]
    payload = {
        "field": "amount",
        "original": record.current_values["amount"],
        "corrected": str(amount),
        "reason_code": reason_code,
        "reason_label": category.label,
        "comment": comment.strip(),
        "operator": operator.strip() or "Operador demo",
        "created_at": clock.now().isoformat(),
        "discrepancy": True,
        "case_version": expected_case_version + 1,
    }
    try:
        store.save_intervention(case_id, expected_case_version, "correction", payload)
    except store.StaleVersion:
        return None, {
            "case": "Versión obsoleta. Recarga el Caso para ver la intervención vigente.",
            "code": "stale_version",
        }
    return payload, {}

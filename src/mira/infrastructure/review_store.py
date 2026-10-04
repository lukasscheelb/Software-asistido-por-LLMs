"""SQLite snapshots and atomic compare-and-swap interventions."""

from dataclasses import asdict
from datetime import date
from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.db.models import F
from mira.domain.policy import (
    ControlledCase,
    Evidence,
    DEFAULT_POLICY,
    F4Evaluation,
    F4Outcome,
    evaluate_case,
)
from mira.domain.review import HumanDecision, HumanAction, CaseStatus
from mira.infrastructure.models import CaseRecord, EvaluationRecord, InterventionRecord


class StaleVersion(Exception):
    pass


def serial(value):
    if isinstance(value, dict):
        return {k: serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    if isinstance(value, (Decimal, date)):
        return str(value)
    return value


def seed_case(case, policy=DEFAULT_POLICY):
    with transaction.atomic():
        record, created = CaseRecord.objects.get_or_create(
            case_id=case.case_id,
            defaults={
                "payload": serial(asdict(case)),
                "current_values": {"amount": "120000"},
            },
        )
        if created:
            EvaluationRecord.objects.create(
                case=record,
                inputs=serial(asdict(case)),
                policy=serial(asdict(policy)),
                result=serial(asdict(evaluate_case(case, policy))),
            )
    return record


def decode_case(data):
    data = dict(data)
    for field in ("score", "authenticity", "coherence"):
        data[field] = Decimal(data[field]) if data[field] is not None else None
    data["received_date"] = date.fromisoformat(data["received_date"])
    data["evidence"] = tuple(Evidence(**e) for e in data["evidence"])
    return ControlledCase(**data)


def cases():
    return tuple(decode_case(r.payload) for r in CaseRecord.objects.order_by("case_id"))


def snapshot(case_id):
    record = CaseRecord.objects.get(pk=case_id)
    evaluation = record.evaluationrecord
    result = dict(evaluation.result)
    result['outcome'] = F4Outcome(result['outcome'])
    if result['outcome'] == F4Outcome.ERROR and not result.get('errors'):
        # Legacy snapshots lacked field metadata. Derive presentation errors from
        # their preserved inputs; do not evaluate policy or modify stored results.
        errors = {}
        for field in ('score', 'authenticity', 'coherence'):
            raw = evaluation.inputs.get(field)
            if raw is None and field != 'score':
                continue
            try:
                value = Decimal(raw) if raw is not None else None
                valid = value is not None and value.is_finite() and Decimal('0') <= value <= Decimal('100')
            except (InvalidOperation, TypeError, ValueError):
                valid = False
            if not valid:
                errors[field] = 'Debe ser un número finito entre 0 y 100.'
        result['errors'] = errors
    return record, F4Evaluation(**result), evaluation.policy


def save_intervention(case_id, expected_case_version, kind, payload):
    with transaction.atomic():
        changed = CaseRecord.objects.filter(
            pk=case_id, version=expected_case_version
        ).update(version=F("version") + 1)
        if changed != 1:
            raise StaleVersion()
        if (
            kind == "decision"
            and InterventionRecord.objects.filter(
                case_id=case_id, kind="decision"
            ).exists()
        ):
            raise StaleVersion()
        InterventionRecord.objects.create(
            case_id=case_id,
            version=expected_case_version + 1,
            kind=kind,
            payload=serial(payload),
        )
        if kind == "correction":
            record = CaseRecord.objects.get(pk=case_id)
            values = dict(record.current_values)
            values[payload["field"]] = payload["corrected"]
            CaseRecord.objects.filter(pk=case_id).update(current_values=values)
    return payload


def get_decision(case_id):
    event = InterventionRecord.objects.filter(case_id=case_id, kind="decision").last()
    if not event:
        return None
    data = dict(event.payload)
    data["action"] = HumanAction(data["action"])
    data["status"] = CaseStatus(data["status"])
    data["platform_outcome"] = F4Outcome(data["platform_outcome"])
    return HumanDecision(**data)


def history(case_id):
    return list(
        InterventionRecord.objects.filter(case_id=case_id).values(
            "version", "kind", "payload"
        )
    )

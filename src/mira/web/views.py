"""Server-rendered views for the controlled MIRA preview."""

from django.http import Http404, HttpRequest, HttpResponse, FileResponse
from django.shortcuts import render
from django.db import transaction
from mira.infrastructure.review_store import decode_case, get_decision
from mira.domain.deadlines import evaluate_deadlines
from mira.infrastructure.clock import clock

from mira.composition import (
    case_detail,
    controlled_cases,
    queue_items,
    register_human_decision,
    register_correction,
    run_f4,
)
from mira.infrastructure.review_store import snapshot, history
from mira.domain.policy import F4Outcome
from mira.domain.review import ACTION_LABELS, HumanAction, REASON_CATEGORIES


ACTION_OPTIONS = (
    (HumanAction.APPROVE, ACTION_LABELS[HumanAction.APPROVE]),
    (HumanAction.REJECT, ACTION_LABELS[HumanAction.REJECT]),
    (HumanAction.REQUEST_INFO, ACTION_LABELS[HumanAction.REQUEST_INFO]),
)


def bandeja(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    priority = request.GET.get("priority", "all")
    if priority not in {"all", "Alta", "Normal"}:
        priority = "all"
    all_items = queue_items()
    context = {
        "active_navigation": "bandeja",
        "items": queue_items(query=query, priority=priority),
        "query": query,
        "priority": priority,
        "total_pending": len(all_items),
        "high_priority": sum(item.priority == "Alta" for item in all_items),
        "normal_priority": sum(item.priority == "Normal" for item in all_items),
    }
    return render(request, "mira_web/bandeja.html", context)


def ejecutar_f4(request: HttpRequest) -> HttpResponse:
    selected_id = request.POST.get("case_id", "") if request.method == "POST" else ""
    result = run_f4(selected_id) if selected_id else None
    draft = {}
    if result and request.POST.get("draft") == "1":
        from dataclasses import replace
        from decimal import Decimal, InvalidOperation
        from hashlib import sha256
        import json
        from mira.domain.policy import evaluate_case
        from mira.infrastructure.review_store import seed_case

        values = {}
        for field in ("score", "authenticity", "coherence"):
            raw = request.POST.get(field, "").strip()
            draft[field] = raw
            try:
                values[field] = Decimal(raw) if raw else None
            except InvalidOperation:
                values[field] = raw
        case = replace(result[0], **values)
        evaluation = evaluate_case(case)
        if evaluation.outcome != F4Outcome.ERROR:
            identity = json.dumps(
                [
                    selected_id,
                    *(
                        str(values[field].normalize())
                        if values[field] is not None
                        else None
                        for field in ("score", "authenticity", "coherence")
                    ),
                ]
            )
            case = replace(
                case,
                case_id=selected_id
                + "-D-"
                + sha256(identity.encode()).hexdigest()[:16],
            )
            seed_case(case)
        result = case, evaluation
    if result:
        display_values = {
            field: str(getattr(result[0], field))
            if getattr(result[0], field) is not None
            else "Ausente"
            for field in ("score", "authenticity", "coherence")
        }
        if not draft:
            draft = {
                field: str(getattr(result[0], field))
                if getattr(result[0], field) is not None
                else ""
                for field in display_values
            }
    else:
        display_values = {}
    return render(
        request,
        "mira_web/ejecutar_f4.html",
        {
            "active_navigation": "ejecutar",
            "cases": controlled_cases(),
            "selected_id": selected_id,
            "result": result,
            "draft": draft,
            "display_values": display_values,
            "error": ""
            if not selected_id or result
            else "Selecciona un Caso controlado válido.",
            "review_outcomes": (F4Outcome.REVIEW, F4Outcome.ESCALATED),
        },
    )


def detalle_caso(request: HttpRequest, case_id: str) -> HttpResponse:
    result = case_detail(case_id)
    if result is None:
        raise Http404("Caso controlado no encontrado")
    case, evaluation, deadlines, decision = result
    errors: dict[str, str] = {}
    saved = False
    is_correction = request.POST.get("command") == "correct"
    correction_data = (
        {
            field: request.POST.get(
                field, "Operador demo" if field == "operator" else ""
            )
            for field in ("corrected", "reason", "comment", "operator")
        }
        if is_correction
        else {"operator": "Operador demo"}
    )
    form_data = {
        "action": request.POST.get("action", ""),
        "reason": request.POST.get("reason", ""),
        "comment": request.POST.get("comment", ""),
    }
    if request.method == "POST":
        try:
            version = int(request.POST.get("expected_case_version", ""))
            if version < 1:
                raise ValueError()
        except ValueError:
            errors = {
                "case": "Falta una versión válida del Caso. Recarga la página.",
                "code": "invalid_input",
            }
        else:
            if request.POST.get("command") == "correct":
                correction, errors = register_correction(
                    case_id=case_id,
                    expected_case_version=version,
                    corrected=request.POST.get("corrected", ""),
                    reason_code=form_data["reason"],
                    comment=form_data["comment"],
                    operator=request.POST.get("operator", "Operador demo"),
                )
                saved = correction is not None
            else:
                _new_decision, errors = register_human_decision(
                    case_id=case_id,
                    action_code=form_data["action"],
                    reason_code=form_data["reason"],
                    comment=form_data["comment"],
                    expected_case_version=version,
                    operator=request.POST.get("operator", "Operador demo"),
                    discrepancy=request.POST.get("discrepancy") == "on",
                )
                saved = _new_decision is not None
    # A deferred SQLite read transaction freezes related state at its first read.
    # Materialize every projection before leaving it, after the command has ended.
    with transaction.atomic():
        record, evaluation, policy = snapshot(case_id)
        case = decode_case(record.payload)
        deadlines = evaluate_deadlines(case, clock.today())
        decision = get_decision(case_id)
        events = history(case_id)
    stale = errors.get("code") == "stale_version"
    correction_errors = errors if is_correction else {}
    # Associate existing server errors with controls without changing validation.
    correction_field_errors = dict(correction_errors)
    correction_message = correction_errors.get("case", "")
    if correction_message.startswith("Ingresa un importe"):
        correction_field_errors["corrected"] = correction_field_errors.pop("case")
    elif correction_errors.get("code") == "reason_required":
        field = "comment" if form_data["reason"] == "other" else "reason"
        correction_field_errors[field] = correction_field_errors.pop("case")
    elif correction_message == "Motivo incompatible con Corrección.":
        correction_field_errors["reason"] = correction_field_errors.pop("case")
    decision_errors = errors if not is_correction or stale else {}

    return render(
        request,
        "mira_web/detalle_caso.html",
        {
            "active_navigation": "bandeja",
            "case": case,
            "case_version": record.version,
            "current_amount": record.current_values.get("amount"),
            "history": events,
            "can_correct": not stale
            and evaluation.outcome in (F4Outcome.REVIEW, F4Outcome.ESCALATED),
            "correction_data": correction_data,
            "correction_errors": correction_errors,
            "correction_field_errors": correction_field_errors,
            "correction_saved": saved and is_correction,
            "policy": policy,
            "correction_categories": [
                c for c in REASON_CATEGORIES if HumanAction.CORRECT in c.actions
            ],
            "evaluation": evaluation,
            "deadlines": deadlines,
            "decision": decision,
            "can_review": evaluation.outcome in (F4Outcome.REVIEW, F4Outcome.ESCALATED)
            and decision is None
            and not stale,
            "action_options": ACTION_OPTIONS,
            "reason_categories": [
                c
                for c in REASON_CATEGORIES
                if c.code not in ("extraction_error", "evidence_value_mismatch")
            ],
            "errors": decision_errors,
            "form_data": form_data,
            "operator_value": request.POST.get("operator", "Operador demo"),
            "discrepancy_value": request.POST.get("discrepancy") == "on",
            "saved": saved and not is_correction,
        },
    )


def evidencia(request, case_id, index):
    from pathlib import Path

    detail = case_detail(case_id)
    if not detail or index < 1 or index > len(detail[0].evidence):
        raise Http404()
    evidence = detail[0].evidence[index - 1]
    path = (
        Path(__file__).resolve().parents[3]
        / "fixtures"
        / "evidence"
        / evidence.filename
    )
    if not path.is_file():
        raise Http404("Evidencia ficticia no disponible")
    return FileResponse(
        path.open("rb"),
        content_type="image/png" if path.suffix == ".png" else "application/pdf",
    )

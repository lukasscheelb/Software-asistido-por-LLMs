"""Server-rendered views for the controlled MIRA preview."""

from django.http import Http404, HttpRequest, HttpResponse, FileResponse
from django.shortcuts import render

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
        from uuid import uuid4
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
            case = replace(case, case_id=case.case_id + "-D-" + uuid4().hex[:8])
            seed_case(case)
        result = case, evaluation
    return render(
        request,
        "mira_web/ejecutar_f4.html",
        {
            "active_navigation": "ejecutar",
            "cases": controlled_cases(),
            "selected_id": selected_id,
            "result": result,
            "draft": draft,
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
        case, evaluation, deadlines, decision = case_detail(case_id)
    record, _evaluation, policy = snapshot(case_id)

    return render(
        request,
        "mira_web/detalle_caso.html",
        {
            "active_navigation": "bandeja",
            "case": case,
            "case_version": record.version,
            "current_amount": record.current_values.get("amount"),
            "history": history(case_id),
            "policy": policy,
            "correction_categories": [
                c for c in REASON_CATEGORIES if HumanAction.CORRECT in c.actions
            ],
            "evaluation": evaluation,
            "deadlines": deadlines,
            "decision": decision,
            "can_review": evaluation.outcome in (F4Outcome.REVIEW, F4Outcome.ESCALATED)
            and decision is None,
            "action_options": ACTION_OPTIONS,
            "reason_categories": [
                c
                for c in REASON_CATEGORIES
                if c.code not in ("extraction_error", "evidence_value_mismatch")
            ],
            "errors": errors,
            "form_data": form_data,
            "saved": saved,
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

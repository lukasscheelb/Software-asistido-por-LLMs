"""Server-rendered views for the controlled MIRA preview."""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from mira.composition import case_detail, controlled_cases, queue_items, register_human_decision, run_f4
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
    return render(
        request,
        "mira_web/ejecutar_f4.html",
        {
            "active_navigation": "ejecutar",
            "cases": controlled_cases(),
            "selected_id": selected_id,
            "result": result,
            "error": "" if not selected_id or result else "Selecciona un Caso controlado válido.",
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
        decision, errors = register_human_decision(
            case_id=case_id,
            action_code=form_data["action"],
            reason_code=form_data["reason"],
            comment=form_data["comment"],
        )
        saved = decision is not None

    return render(
        request,
        "mira_web/detalle_caso.html",
        {
            "active_navigation": "bandeja",
            "case": case,
            "evaluation": evaluation,
            "deadlines": deadlines,
            "decision": decision,
            "can_review": evaluation.outcome in (F4Outcome.REVIEW, F4Outcome.ESCALATED) and decision is None,
            "action_options": ACTION_OPTIONS,
            "reason_categories": REASON_CATEGORIES,
            "errors": errors,
            "form_data": form_data,
            "saved": saved,
        },
    )

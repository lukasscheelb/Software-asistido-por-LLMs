"""Server-rendered views for the controlled MIRA preview."""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from mira.composition import case_detail, controlled_cases, queue_items, run_f4
from mira.domain.policy import F4Outcome


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
        "high_priority": sum(item.evaluation.priority == "Alta" for item in all_items),
        "normal_priority": sum(item.evaluation.priority == "Normal" for item in all_items),
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
    case, evaluation = result
    return render(request, "mira_web/detalle_caso.html", {"active_navigation": "bandeja", "case": case, "evaluation": evaluation})

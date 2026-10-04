"""Human review rules for the controlled F1 flow."""

from dataclasses import dataclass
from enum import StrEnum

from mira.domain.policy import F4Outcome


class HumanAction(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_INFO = "request_info"
    CORRECT = "correct"


class CaseStatus(StrEnum):
    PENDING_REVIEW = "PENDIENTE DE REVISIÓN"
    APPROVED = "APROBADO"
    REJECTED = "RECHAZADO"
    WAITING_INFO = "ESPERANDO ANTECEDENTES"


@dataclass(frozen=True)
class ReasonCategory:
    code: str
    label: str
    actions: tuple[HumanAction, ...]
    requires_comment: bool = False


@dataclass(frozen=True)
class HumanDecision:
    case_id: str
    action: HumanAction
    action_label: str
    status: CaseStatus
    reason_code: str
    reason_label: str
    comment: str
    operator: str
    created_at: str
    platform_outcome: F4Outcome
    discrepancy: bool
    case_version: int = 1


REASON_CATEGORIES = (
    ReasonCategory("requirements_met", "Requisitos cumplidos", (HumanAction.APPROVE,)),
    ReasonCategory(
        "evidence_consistent", "Evidencia consistente", (HumanAction.APPROVE,)
    ),
    ReasonCategory(
        "requirements_not_met", "Requisitos no cumplidos", (HumanAction.REJECT,)
    ),
    ReasonCategory(
        "evidence_inconsistent", "Evidencia inconsistente", (HumanAction.REJECT,)
    ),
    ReasonCategory(
        "information_incomplete",
        "Antecedentes incompletos",
        (HumanAction.REQUEST_INFO,),
    ),
    ReasonCategory(
        "evidence_unreadable", "Evidencia ilegible", (HumanAction.REQUEST_INFO,)
    ),
    ReasonCategory(
        "clarification_required", "Aclaración requerida", (HumanAction.REQUEST_INFO,)
    ),
    ReasonCategory("extraction_error", "Error de extracción", (HumanAction.CORRECT,)),
    ReasonCategory(
        "evidence_value_mismatch",
        "Valor distinto de la evidencia",
        (HumanAction.CORRECT,),
    ),
    ReasonCategory("other", "Otro", tuple(HumanAction), requires_comment=True),
)


ACTION_LABELS = {
    HumanAction.APPROVE: "Aprobar",
    HumanAction.REJECT: "Rechazar",
    HumanAction.REQUEST_INFO: "Solicitar antecedentes",
}


def status_for_action(action: HumanAction) -> CaseStatus:
    return {
        HumanAction.APPROVE: CaseStatus.APPROVED,
        HumanAction.REJECT: CaseStatus.REJECTED,
        HumanAction.REQUEST_INFO: CaseStatus.WAITING_INFO,
    }[action]


def category_by_code(code: str) -> ReasonCategory | None:
    return next(
        (category for category in REASON_CATEGORIES if category.code == code), None
    )


def categories_for_action(action: HumanAction) -> tuple[ReasonCategory, ...]:
    return tuple(
        category for category in REASON_CATEGORIES if action in category.actions
    )


def build_human_decision(
    *,
    case_id: str,
    action_code: str,
    reason_code: str,
    comment: str,
    operator: str,
    created_at: str,
    discrepancy: bool = False,
    platform_outcome: F4Outcome,
) -> tuple[HumanDecision | None, dict[str, str]]:
    errors: dict[str, str] = {}
    try:
        action = HumanAction(action_code)
    except ValueError:
        errors["action"] = "Selecciona una acción válida."
        action = None

    category = category_by_code(reason_code)
    if category is None:
        errors["reason"] = "Selecciona una categoría de motivo."
    elif action is not None and action not in category.actions:
        errors["reason"] = "La categoría seleccionada no corresponde a la acción."

    clean_comment = comment.strip()
    if category is not None and category.requires_comment and not clean_comment:
        errors["comment"] = "El comentario es obligatorio cuando el motivo es Otro."

    if action == HumanAction.CORRECT:
        errors["action"] = "Utiliza el formulario de Corrección."
    if discrepancy and not clean_comment:
        errors["comment"] = "Declara el motivo del desacuerdo en el comentario."
    if action is None or category is None or errors:
        return None, errors

    return (
        HumanDecision(
            case_id=case_id,
            action=action,
            action_label=ACTION_LABELS[action],
            status=status_for_action(action),
            reason_code=category.code,
            reason_label=category.label,
            comment=clean_comment,
            operator=operator.strip() or "Operador demo",
            created_at=created_at,
            platform_outcome=platform_outcome,
            discrepancy=discrepancy,
        ),
        {},
    )

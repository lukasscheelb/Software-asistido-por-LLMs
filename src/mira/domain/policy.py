"""Pure F4 policy for controlled demonstration cases."""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class F4Outcome(StrEnum):
    ERROR = "ERROR / DERIVACIÓN"
    ESCALATED = "ESCALADO"
    APPROVED = "APROBADO AUTOMÁTICAMENTE"
    REVIEW = "REVISIÓN"


@dataclass(frozen=True)
class Policy:
    version: str
    approval_threshold: Decimal
    authenticity_minimum: Decimal
    coherence_minimum: Decimal
    automation_enabled: bool


@dataclass(frozen=True)
class Evidence:
    filename: str
    kind: str
    location: str
    finding: str


@dataclass(frozen=True)
class ControlledCase:
    case_id: str
    applicant: str
    product: str
    score: Decimal
    authenticity: Decimal
    coherence: Decimal
    fraud_detected: bool
    received_at: str
    internal_deadline: str
    contractual_deadline: str
    evidence: tuple[Evidence, ...]


@dataclass(frozen=True)
class F4Evaluation:
    outcome: F4Outcome
    rule: str
    reason: str
    priority: str

    @property
    def outcome_class(self) -> str:
        return {
            F4Outcome.ERROR: "error",
            F4Outcome.ESCALATED: "escalated",
            F4Outcome.APPROVED: "approved",
            F4Outcome.REVIEW: "review",
        }[self.outcome]


DEFAULT_POLICY = Policy(
    version="POL-F4-2026.10",
    approval_threshold=Decimal("90"),
    authenticity_minimum=Decimal("70"),
    coherence_minimum=Decimal("70"),
    automation_enabled=True,
)


def evaluate_case(case: ControlledCase, policy: Policy = DEFAULT_POLICY) -> F4Evaluation:
    """Evaluate one controlled case without IO or mutable state."""

    numeric_values = (case.score, case.authenticity, case.coherence)
    if any(value < 0 or value > 100 for value in numeric_values):
        return F4Evaluation(
            outcome=F4Outcome.ERROR,
            rule="Validación de entradas",
            reason="El Puntaje y las Señales deben estar entre 0 y 100.",
            priority="Sin prioridad",
        )

    if case.fraud_detected:
        return F4Evaluation(
            outcome=F4Outcome.ESCALATED,
            rule="Precedencia de fraude",
            reason="Fraude detectado: Sí. Caso escalado para revisión prioritaria.",
            priority="Alta",
        )

    if case.score < Decimal("60"):
        return F4Evaluation(
            outcome=F4Outcome.ESCALATED,
            rule="Límite inferior de Puntaje",
            reason="El Puntaje es menor que 60 y requiere revisión prioritaria.",
            priority="Alta",
        )

    clears_approval_barriers = (
        policy.automation_enabled
        and case.score > policy.approval_threshold
        and case.authenticity >= policy.authenticity_minimum
        and case.coherence >= policy.coherence_minimum
    )
    if clears_approval_barriers:
        return F4Evaluation(
            outcome=F4Outcome.APPROVED,
            rule="Barreras de aprobación",
            reason="Puntaje y Señales superan todas las barreras configuradas.",
            priority="Sin prioridad",
        )

    return F4Evaluation(
        outcome=F4Outcome.REVIEW,
        rule="Revisión residual",
        reason="El Caso es válido, pero no cumple todas las barreras de aprobación.",
        priority="Normal",
    )

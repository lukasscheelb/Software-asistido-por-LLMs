"""Fictitious, deterministic cases used by the local MIRA preview."""

from decimal import Decimal

from mira.domain.policy import ControlledCase, Evidence


CONTROLLED_CASES = (
    ControlledCase(
        case_id="CC-F4-01",
        applicant="Comercial Andina SpA",
        product="Capital de trabajo",
        score=Decimal("94"),
        authenticity=Decimal("92"),
        coherence=Decimal("88"),
        fraud_detected=False,
        received_at="01 oct 2026 · 09:12",
        internal_deadline="06 oct 2026",
        contractual_deadline="08 oct 2026",
        evidence=(Evidence("carpeta_financiera_01.pdf", "PDF ficticio", "Página 4 · Resumen financiero", "Los montos y periodos son coherentes entre documentos."),),
    ),
    ControlledCase(
        case_id="CC-F4-02",
        applicant="Servicios Puerto Claro Ltda.",
        product="Línea de crédito",
        score=Decimal("60"),
        authenticity=Decimal("84"),
        coherence=Decimal("68"),
        fraud_detected=False,
        received_at="01 oct 2026 · 10:35",
        internal_deadline="06 oct 2026",
        contractual_deadline="08 oct 2026",
        evidence=(
            Evidence("comprobante_ingresos_02.pdf", "PDF ficticio", "Página 2 · Ingresos mensuales", "El monto declarado requiere contraste con el comprobante."),
            Evidence("resumen_solicitud_02.png", "Imagen ficticia", "Región: total solicitado", "La cifra es legible y no presenta alteraciones visibles."),
        ),
    ),
    ControlledCase(
        case_id="CC-F4-03",
        applicant="Distribuidora Valle Azul SpA",
        product="Anticipo de facturas",
        score=Decimal("82"),
        authenticity=Decimal("74"),
        coherence=Decimal("77"),
        fraud_detected=True,
        received_at="30 sep 2026 · 16:48",
        internal_deadline="05 oct 2026",
        contractual_deadline="07 oct 2026",
        evidence=(Evidence("factura_controlada_03.pdf", "PDF ficticio", "Página 1 · Folio y emisor", "La Señal simulada detectó una inconsistencia de autenticidad."),),
    ),
    ControlledCase(
        case_id="CC-F4-04",
        applicant="Caso de validación",
        product="Entrada inválida controlada",
        score=Decimal("104"),
        authenticity=Decimal("80"),
        coherence=Decimal("81"),
        fraud_detected=False,
        received_at="02 oct 2026 · 11:05",
        internal_deadline="07 oct 2026",
        contractual_deadline="09 oct 2026",
        evidence=(Evidence("entrada_invalida_04.pdf", "PDF ficticio", "Página 1 · Puntaje simulado", "El Puntaje está fuera del rango permitido."),),
    ),
)


def list_controlled_cases() -> tuple[ControlledCase, ...]:
    return CONTROLLED_CASES


def get_controlled_case(case_id: str) -> ControlledCase | None:
    return next((case for case in CONTROLLED_CASES if case.case_id == case_id), None)

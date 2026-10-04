"""Fictitious, deterministic cases used by the local MIRA preview."""

from dataclasses import replace
from datetime import date
from decimal import Decimal

from mira.domain.policy import ControlledCase, Evidence


CONTROLLED_CASES = (
    ControlledCase(
        case_id="CC-F4-01",
        applicant="Comercial Andina SpA",
        product="Capital de trabajo",
        score=Decimal("59.99"),
        authenticity=Decimal("80"),
        coherence=Decimal("80"),
        fraud_detected=False,
        automation_enabled=True,
        received_date=date(2026, 10, 1),
        received_at="01 oct 2026 · 09:12",
        internal_deadline="06 oct 2026",
        contractual_deadline="08 oct 2026",
        evidence=(
            Evidence(
                "carpeta_financiera_01.pdf",
                "PDF ficticio",
                "Página 4 · Puntaje simulado",
                "El Puntaje queda bajo 60 aunque las Señales son favorables.",
            ),
        ),
    ),
    ControlledCase(
        case_id="CC-F4-02",
        applicant="Servicios Puerto Claro Ltda.",
        product="Línea de crédito",
        score=Decimal("60"),
        authenticity=Decimal("80"),
        coherence=Decimal("80"),
        fraud_detected=False,
        automation_enabled=True,
        received_date=date(2026, 10, 1),
        received_at="01 oct 2026 · 10:35",
        internal_deadline="06 oct 2026",
        contractual_deadline="08 oct 2026",
        evidence=(
            Evidence(
                "comprobante_ingresos_02.pdf",
                "PDF ficticio",
                "Página 2 · Puntaje simulado",
                "El Puntaje alcanza el límite inferior, pero no supera la barrera de aprobación.",
            ),
            Evidence(
                "resumen_solicitud_02.png",
                "Imagen ficticia",
                "Región: señales simuladas",
                "Las Señales son favorables y se mantienen dentro del rango esperado.",
            ),
        ),
    ),
    ControlledCase(
        case_id="CC-F4-03",
        applicant="Distribuidora Valle Azul SpA",
        product="Anticipo de facturas",
        score=Decimal("90"),
        authenticity=Decimal("80"),
        coherence=Decimal("80"),
        fraud_detected=False,
        automation_enabled=True,
        received_date=date(2026, 9, 28),
        received_at="28 sep 2026 · 16:48",
        internal_deadline="01 oct 2026",
        contractual_deadline="05 oct 2026",
        evidence=(
            Evidence(
                "factura_controlada_03.pdf",
                "PDF ficticio",
                "Página 1 · Puntaje simulado",
                "El Puntaje iguala 90, por lo que no cumple la regla estricta de Puntaje mayor que 90.",
            ),
        ),
    ),
    ControlledCase(
        case_id="CC-F4-04",
        applicant="Inversiones Cerro Norte SpA",
        product="Crédito de inversión",
        score=Decimal("90.01"),
        authenticity=Decimal("70"),
        coherence=Decimal("70"),
        fraud_detected=False,
        automation_enabled=True,
        received_date=date(2026, 10, 2),
        received_at="02 oct 2026 · 11:05",
        internal_deadline="07 oct 2026",
        contractual_deadline="09 oct 2026",
        evidence=(
            Evidence(
                "respaldo_inversion_04.pdf",
                "PDF ficticio",
                "Página 3 · Barreras mínimas",
                "El Puntaje supera 90 y ambas Señales alcanzan el mínimo exigido.",
            ),
        ),
    ),
    ControlledCase(
        case_id="CC-F4-05",
        applicant="Constructora Litoral Sur Ltda.",
        product="Financiamiento de proyecto",
        score=Decimal("95"),
        authenticity=Decimal("90"),
        coherence=Decimal("90"),
        fraud_detected=True,
        automation_enabled=True,
        received_date=date(2026, 10, 2),
        received_at="02 oct 2026 · 12:20",
        internal_deadline="07 oct 2026",
        contractual_deadline="09 oct 2026",
        evidence=(
            Evidence(
                "alerta_fraude_05.pdf",
                "PDF ficticio",
                "Página 1 · Señal antifraude",
                "La marca de fraude tiene precedencia sobre las Señales favorables.",
            ),
        ),
    ),
    ControlledCase(
        case_id="CC-F4-06",
        applicant="Exportadora Nueva Bahía SpA",
        product="Crédito exportador",
        score=Decimal("95"),
        authenticity=Decimal("69.99"),
        coherence=Decimal("90"),
        fraud_detected=False,
        automation_enabled=True,
        received_date=date(2026, 10, 2),
        received_at="02 oct 2026 · 13:10",
        internal_deadline="07 oct 2026",
        contractual_deadline="09 oct 2026",
        evidence=(
            Evidence(
                "documentos_exportacion_06.pdf",
                "PDF ficticio",
                "Página 2 · Autenticidad",
                "La Señal de autenticidad queda bajo el mínimo configurado.",
            ),
        ),
    ),
    ControlledCase(
        case_id="CC-F4-07",
        applicant="Agrícola Santa Elisa Ltda.",
        product="Capital de temporada",
        score=Decimal("95"),
        authenticity=None,
        coherence=Decimal("90"),
        fraud_detected=False,
        automation_enabled=True,
        received_date=date(2026, 10, 2),
        received_at="02 oct 2026 · 14:05",
        internal_deadline="07 oct 2026",
        contractual_deadline="09 oct 2026",
        evidence=(
            Evidence(
                "carpeta_agricola_07.pdf",
                "PDF ficticio",
                "Página 5 · Señal ausente",
                "La Señal de autenticidad no está disponible para la Evaluación.",
            ),
        ),
    ),
    ControlledCase(
        case_id="CC-F4-08",
        applicant="Transportes Cordillera SpA",
        product="Leasing operativo",
        score=Decimal("95"),
        authenticity=Decimal("90"),
        coherence=Decimal("90"),
        fraud_detected=False,
        automation_enabled=False,
        received_date=date(2026, 10, 2),
        received_at="02 oct 2026 · 15:30",
        internal_deadline="07 oct 2026",
        contractual_deadline="09 oct 2026",
        evidence=(
            Evidence(
                "configuracion_operador_08.pdf",
                "PDF ficticio",
                "Página 1 · Automatización",
                "La automatización del Caso está deshabilitada y exige revisión humana.",
            ),
        ),
    ),
    ControlledCase(
        case_id="CC-F4-09",
        applicant="Caso de validación",
        product="Entrada inválida controlada",
        score=Decimal("101"),
        authenticity=Decimal("90"),
        coherence=Decimal("90"),
        fraud_detected=False,
        automation_enabled=True,
        received_date=date(2026, 10, 2),
        received_at="02 oct 2026 · 16:15",
        internal_deadline="07 oct 2026",
        contractual_deadline="09 oct 2026",
        evidence=(
            Evidence(
                "entrada_invalida_09.pdf",
                "PDF ficticio",
                "Página 1 · Puntaje simulado",
                "El Puntaje está fuera del rango permitido.",
            ),
        ),
    ),
)


def list_controlled_cases() -> tuple[ControlledCase, ...]:
    return CONTROLLED_CASES


def get_controlled_case(case_id: str) -> ControlledCase | None:
    return next((case for case in CONTROLLED_CASES if case.case_id == case_id), None)


F1_CASES = tuple(
    replace(
        CONTROLLED_CASES[index],
        case_id=f"CC-F1-{number:02d}",
        applicant=f"Solicitante ficticio F1 {number}",
    )
    for number, index in enumerate((1, 1, 1, 1, 5, 2), 1)
)


def demo_cases():
    return CONTROLLED_CASES + F1_CASES

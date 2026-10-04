from decimal import Decimal

from django.test import SimpleTestCase
from django.urls import reverse

from mira.application.services import build_queue
from mira.domain.policy import (
    DEFAULT_POLICY,
    ControlledCase,
    Evidence,
    F4Outcome,
    evaluate_case,
)
from mira.infrastructure.controlled_cases import get_controlled_case, list_controlled_cases


def controlled_case(
    case_id: str,
    score: str,
    authenticity: str,
    coherence: str,
    fraud_detected: bool = False,
) -> ControlledCase:
    return ControlledCase(
        case_id=case_id,
        applicant=f"Solicitante {case_id}",
        product="Producto ficticio",
        score=Decimal(score),
        authenticity=Decimal(authenticity),
        coherence=Decimal(coherence),
        fraud_detected=fraud_detected,
        received_at="01 oct 2026 · 09:00",
        internal_deadline="06 oct 2026",
        contractual_deadline="08 oct 2026",
        evidence=(
            Evidence(
                filename=f"{case_id}.pdf",
                kind="PDF ficticio",
                location="Página 1 · Campo controlado",
                finding="Evidencia ficticia para prueba automatizada.",
            ),
        ),
    )


class F4PolicyTests(SimpleTestCase):
    def test_pf04_boundary_matrix_for_supported_f4_cases(self):
        cases = {
            "CC-F4-01": controlled_case("CC-F4-01", "59.99", "80", "80"),
            "CC-F4-02": controlled_case("CC-F4-02", "60", "80", "80"),
            "CC-F4-03": controlled_case("CC-F4-03", "90", "80", "80"),
            "CC-F4-04": controlled_case("CC-F4-04", "90.01", "70", "70"),
            "CC-F4-05": controlled_case("CC-F4-05", "95", "90", "90", fraud_detected=True),
            "CC-F4-06": controlled_case("CC-F4-06", "95", "69.99", "90"),
            "CC-F4-08": controlled_case("CC-F4-08", "95", "90", "90"),
            "CC-F4-09": controlled_case("CC-F4-09", "101", "90", "90"),
        }
        disabled_policy = DEFAULT_POLICY.__class__(
            version="POL-F4-TEST-OFF",
            approval_threshold=DEFAULT_POLICY.approval_threshold,
            authenticity_minimum=DEFAULT_POLICY.authenticity_minimum,
            coherence_minimum=DEFAULT_POLICY.coherence_minimum,
            automation_enabled=False,
        )
        expectations = {
            "CC-F4-01": (DEFAULT_POLICY, F4Outcome.ESCALATED),
            "CC-F4-02": (DEFAULT_POLICY, F4Outcome.REVIEW),
            "CC-F4-03": (DEFAULT_POLICY, F4Outcome.REVIEW),
            "CC-F4-04": (DEFAULT_POLICY, F4Outcome.APPROVED),
            "CC-F4-05": (DEFAULT_POLICY, F4Outcome.ESCALATED),
            "CC-F4-06": (DEFAULT_POLICY, F4Outcome.REVIEW),
            "CC-F4-08": (disabled_policy, F4Outcome.REVIEW),
            "CC-F4-09": (DEFAULT_POLICY, F4Outcome.ERROR),
        }

        for case_id, (policy, expected_outcome) in expectations.items():
            with self.subTest(case_id=case_id):
                self.assertEqual(evaluate_case(cases[case_id], policy).outcome, expected_outcome)

    def test_controlled_queue_only_exposes_human_review_cases(self):
        queue = build_queue(list_controlled_cases(), DEFAULT_POLICY)

        self.assertEqual([item.case.case_id for item in queue], ["CC-F4-03", "CC-F4-02"])
        self.assertTrue(all(item.evaluation.outcome in {F4Outcome.REVIEW, F4Outcome.ESCALATED} for item in queue))


class MiraWebRouteTests(SimpleTestCase):
    def test_home_redirects_to_review_queue(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("web:bandeja"))

    def test_review_queue_renders_controlled_review_cases(self):
        response = self.client.get(reverse("web:bandeja"))

        self.assertContains(response, "Bandeja de revisión")
        self.assertContains(response, "CC-F4-02")
        self.assertContains(response, "CC-F4-03")
        self.assertNotContains(response, "CC-F4-01")

    def test_f4_runner_posts_review_result(self):
        response = self.client.post(reverse("web:ejecutar_f4"), {"case_id": "CC-F4-02"})

        self.assertContains(response, "Resultado F4")
        self.assertContains(response, "CC-F4-02")
        self.assertContains(response, F4Outcome.REVIEW)

    def test_case_detail_shows_evidence_before_score(self):
        response = self.client.get(reverse("web:detalle_caso", args=["CC-F4-02"]))
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertLess(content.index("Evidencia"), content.index("Puntaje y Señales"))
        self.assertContains(response, get_controlled_case("CC-F4-02").evidence[0].filename)

    def test_unknown_case_returns_404(self):
        response = self.client.get(reverse("web:detalle_caso", args=["NO-EXISTE"]))

        self.assertEqual(response.status_code, 404)

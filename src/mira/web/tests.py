from datetime import date
from decimal import Decimal

from django.test import TestCase, SimpleTestCase, TransactionTestCase
from django.core.management import call_command
from django.urls import reverse

from mira.application.services import build_queue
from mira.composition import CONTROLLED_TODAY
from mira.domain.deadlines import add_business_days, evaluate_deadlines
from mira.domain.policy import (
    DEFAULT_POLICY,
    ControlledCase,
    Evidence,
    F4Outcome,
    evaluate_case,
)
from mira.infrastructure.controlled_cases import (
    get_controlled_case,
    list_controlled_cases,
)
from mira.infrastructure.review_store import get_decision


def controlled_case(
    case_id: str,
    score: str,
    authenticity: str | None,
    coherence: str | None,
    fraud_detected: bool = False,
    automation_enabled: bool = True,
) -> ControlledCase:
    return ControlledCase(
        case_id=case_id,
        applicant=f"Solicitante {case_id}",
        product="Producto ficticio",
        score=Decimal(score),
        authenticity=Decimal(authenticity) if authenticity is not None else None,
        coherence=Decimal(coherence) if coherence is not None else None,
        fraud_detected=fraud_detected,
        automation_enabled=automation_enabled,
        received_date=date(2026, 10, 1),
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


class F4PolicyTests(TestCase):
    def setUp(self):
        call_command("load_demo", verbosity=0)

    def test_pf04_boundary_matrix_for_f4_cases(self):
        cases = {
            "CC-F4-01": controlled_case("CC-F4-01", "59.99", "80", "80"),
            "CC-F4-02": controlled_case("CC-F4-02", "60", "80", "80"),
            "CC-F4-03": controlled_case("CC-F4-03", "90", "80", "80"),
            "CC-F4-04": controlled_case("CC-F4-04", "90.01", "70", "70"),
            "CC-F4-05": controlled_case(
                "CC-F4-05", "95", "90", "90", fraud_detected=True
            ),
            "CC-F4-06": controlled_case("CC-F4-06", "95", "69.99", "90"),
            "CC-F4-07": controlled_case("CC-F4-07", "95", None, "90"),
            "CC-F4-08": controlled_case(
                "CC-F4-08", "95", "90", "90", automation_enabled=False
            ),
            "CC-F4-09": controlled_case("CC-F4-09", "101", "90", "90"),
        }
        expectations = {
            "CC-F4-01": F4Outcome.ESCALATED,
            "CC-F4-02": F4Outcome.REVIEW,
            "CC-F4-03": F4Outcome.REVIEW,
            "CC-F4-04": F4Outcome.APPROVED,
            "CC-F4-05": F4Outcome.ESCALATED,
            "CC-F4-06": F4Outcome.REVIEW,
            "CC-F4-07": F4Outcome.REVIEW,
            "CC-F4-08": F4Outcome.REVIEW,
            "CC-F4-09": F4Outcome.ERROR,
        }

        for case_id, expected_outcome in expectations.items():
            with self.subTest(case_id=case_id):
                self.assertEqual(
                    evaluate_case(cases[case_id], DEFAULT_POLICY).outcome,
                    expected_outcome,
                )

    def test_fixture_cases_match_f4_matrix(self):
        expectations = {
            "CC-F4-01": F4Outcome.ESCALATED,
            "CC-F4-02": F4Outcome.REVIEW,
            "CC-F4-03": F4Outcome.REVIEW,
            "CC-F4-04": F4Outcome.APPROVED,
            "CC-F4-05": F4Outcome.ESCALATED,
            "CC-F4-06": F4Outcome.REVIEW,
            "CC-F4-07": F4Outcome.REVIEW,
            "CC-F4-08": F4Outcome.REVIEW,
            "CC-F4-09": F4Outcome.ERROR,
        }

        cases = {case.case_id: case for case in list_controlled_cases()}

        self.assertEqual(set(cases), set(expectations))
        self.assertIsNone(cases["CC-F4-07"].authenticity)
        self.assertFalse(cases["CC-F4-08"].automation_enabled)
        for case_id, expected_outcome in expectations.items():
            with self.subTest(case_id=case_id):
                self.assertEqual(
                    evaluate_case(cases[case_id], DEFAULT_POLICY).outcome,
                    expected_outcome,
                )

    def test_controlled_queue_only_exposes_human_review_cases(self):
        queue = build_queue(list_controlled_cases(), DEFAULT_POLICY, CONTROLLED_TODAY)

        self.assertEqual(
            [item.case.case_id for item in queue],
            [
                "CC-F4-03",
                "CC-F4-01",
                "CC-F4-05",
                "CC-F4-02",
                "CC-F4-06",
                "CC-F4-07",
                "CC-F4-08",
            ],
        )
        self.assertTrue(
            all(
                item.evaluation.outcome in {F4Outcome.REVIEW, F4Outcome.ESCALATED}
                for item in queue
            )
        )

    def test_pf14_business_day_deadlines_are_reproducible(self):
        case = get_controlled_case("CC-F4-02")
        deadlines = evaluate_deadlines(case, CONTROLLED_TODAY)

        self.assertEqual(add_business_days(date(2026, 10, 1), 3), date(2026, 10, 6))
        self.assertEqual(add_business_days(date(2026, 10, 1), 5), date(2026, 10, 8))
        self.assertEqual(deadlines.internal_state, "Vence hoy")
        self.assertEqual(deadlines.contractual_state, "Vigente")

    def test_pf14_contractual_overdue_escalates_priority_without_closing_case(self):
        case = get_controlled_case("CC-F4-03")
        deadlines = evaluate_deadlines(case, CONTROLLED_TODAY)
        queue = build_queue(list_controlled_cases(), DEFAULT_POLICY, CONTROLLED_TODAY)
        item = next(item for item in queue if item.case.case_id == "CC-F4-03")

        self.assertEqual(deadlines.contractual_state, "Vencido")
        self.assertTrue(deadlines.supervisor_mark)
        self.assertEqual(item.priority, "Alta")
        self.assertEqual(item.evaluation.outcome, F4Outcome.REVIEW)

    def test_pf14_internal_pre_alert_is_visible_before_due_date(self):
        case = get_controlled_case("CC-F4-06")
        deadlines = evaluate_deadlines(case, CONTROLLED_TODAY)

        self.assertEqual(deadlines.internal_label, "07 oct 2026")
        self.assertEqual(deadlines.internal_state, "Alerta previa")


class MiraWebRouteTests(TestCase):
    def setUp(self):
        call_command("load_demo", verbosity=0)

    def test_home_redirects_to_review_queue(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("web:bandeja"))

    def test_review_queue_renders_controlled_review_cases(self):
        response = self.client.get(reverse("web:bandeja"))

        self.assertContains(response, "Bandeja de revisión")
        self.assertContains(response, "CC-F4-01")
        self.assertContains(response, "CC-F4-02")
        self.assertContains(response, "CC-F4-03")
        self.assertContains(response, "CC-F4-05")
        self.assertContains(response, "CC-F4-06")
        self.assertContains(response, "CC-F4-07")
        self.assertContains(response, "CC-F4-08")
        self.assertContains(response, "Vencido")
        self.assertContains(response, "Supervisor")
        self.assertNotContains(response, "CC-F4-04")
        self.assertNotContains(response, "CC-F4-09")

    def test_f4_runner_posts_review_result(self):
        response = self.client.post(reverse("web:ejecutar_f4"), {"case_id": "CC-F4-02"})

        self.assertContains(response, "Resultado F4")
        self.assertContains(response, "CC-F4-02")
        self.assertContains(response, F4Outcome.REVIEW)

    def test_f4_runner_posts_auto_off_result(self):
        response = self.client.post(reverse("web:ejecutar_f4"), {"case_id": "CC-F4-08"})

        self.assertContains(response, "Automatización deshabilitada")
        self.assertContains(response, "Deshabilitada")

    def test_f4_runner_posts_missing_signal_result(self):
        response = self.client.post(reverse("web:ejecutar_f4"), {"case_id": "CC-F4-07"})

        self.assertContains(response, "Señal requerida ausente")
        self.assertContains(response, "Ausente")

    def test_case_detail_shows_evidence_before_score(self):
        response = self.client.get(reverse("web:detalle_caso", args=["CC-F4-02"]))
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertLess(content.index("Evidencia"), content.index("Puntaje y Señales"))
        self.assertContains(
            response, get_controlled_case("CC-F4-02").evidence[0].filename
        )

    def test_human_decision_requires_reason(self):
        response = self.client.post(
            reverse("web:detalle_caso", args=["CC-F4-02"]),
            {
                "expected_case_version": "1",
                "action": "request_info",
                "reason": "",
                "comment": "",
            },
        )

        self.assertContains(response, "Selecciona una categoría de motivo.")
        self.assertIsNone(get_decision("CC-F4-02"))

    def test_human_decision_requires_comment_for_other_reason(self):
        response = self.client.post(
            reverse("web:detalle_caso", args=["CC-F4-02"]),
            {
                "expected_case_version": "1",
                "action": "request_info",
                "reason": "other",
                "comment": "   ",
            },
        )

        self.assertContains(
            response, "El comentario es obligatorio cuando el motivo es Otro."
        )
        self.assertIsNone(get_decision("CC-F4-02"))

    def test_human_decision_records_request_info_and_removes_case_from_queue(self):
        response = self.client.post(
            reverse("web:detalle_caso", args=["CC-F4-02"]),
            {
                "expected_case_version": "1",
                "action": "request_info",
                "reason": "information_incomplete",
                "comment": "Falta respaldo bancario.",
            },
        )

        decision = get_decision("CC-F4-02")
        self.assertContains(response, "Decisión registrada correctamente.")
        self.assertContains(response, "ESPERANDO ANTECEDENTES")
        self.assertEqual(decision.reason_label, "Antecedentes incompletos")
        self.assertFalse(decision.discrepancy)

        queue_response = self.client.get(reverse("web:bandeja"))
        self.assertContains(queue_response, "CC-F4-02")

    def test_human_rejection_marks_discrepancy(self):
        response = self.client.post(
            reverse("web:detalle_caso", args=["CC-F4-06"]),
            {
                "expected_case_version": "1",
                "action": "reject",
                "reason": "requirements_not_met",
                "comment": "",
            },
        )

        decision = get_decision("CC-F4-06")
        self.assertContains(response, "RECHAZADO")
        self.assertContains(response, "Discrepancia")
        self.assertFalse(decision.discrepancy)

    def test_unknown_case_returns_404(self):
        response = self.client.get(reverse("web:detalle_caso", args=["NO-EXISTE"]))

        self.assertEqual(response.status_code, 404)


class DurableReviewTests(TestCase):
    def setUp(self):
        call_command("load_demo", verbosity=0)

    def post(self, case="CC-F1-01", **data):
        return self.client.post(reverse("web:detalle_caso", args=[case]), data)

    def test_correction_keeps_original_and_decision(self):
        from mira.infrastructure.review_store import history, snapshot

        self.post(action="approve", reason="requirements_met", expected_case_version=1)
        self.post(
            command="correct",
            corrected="100000",
            reason="extraction_error",
            expected_case_version=2,
            operator="Operadora ficticia",
        )
        self.assertEqual(snapshot("CC-F1-01")[0].version, 3)
        self.assertEqual(get_decision("CC-F1-01").action, "approve")
        event = history("CC-F1-01")[-1]["payload"]
        self.assertEqual((event["original"], event["corrected"]), ("120000", "100000"))
        self.assertTrue(event["discrepancy"])
        call_command("load_demo", verbosity=0)
        self.assertEqual(len(history("CC-F1-01")), 2)

    def test_stale_post_preserves_current_decision(self):
        self.post(
            case="CC-F1-04",
            action="approve",
            reason="requirements_met",
            expected_case_version=1,
        )
        response = self.post(
            case="CC-F1-04",
            action="reject",
            reason="requirements_not_met",
            expected_case_version=1,
        )
        self.assertContains(response, "stale_version")
        self.assertContains(response, "APROBADO")
        self.assertEqual(get_decision("CC-F1-04").action, "approve")

    def test_finite_numeric_validation(self):
        from dataclasses import replace

        for value in ("NaN", "sNaN", "Infinity", "-Infinity"):
            self.assertEqual(
                evaluate_case(
                    replace(get_controlled_case("CC-F4-02"), score=Decimal(value))
                ).outcome,
                F4Outcome.ERROR,
            )

    def test_missing_version_is_rejected(self):
        self.assertContains(
            self.post(action="approve", reason="requirements_met"), "invalid_input"
        )
        self.assertIsNone(get_decision("CC-F1-01"))

    def test_evidence_access_and_historical_policy(self):
        from mira.infrastructure.review_store import seed_case, snapshot
        from mira.domain.policy import Policy
        from dataclasses import replace

        case = get_controlled_case("CC-F4-04")
        seed_case(
            case,
            replace(
                DEFAULT_POLICY, version="changed", approval_threshold=Decimal("99")
            ),
        )
        self.assertEqual(snapshot(case.case_id)[1].outcome, F4Outcome.APPROVED)
        self.assertEqual(snapshot(case.case_id)[2]["version"], DEFAULT_POLICY.version)
        response = self.client.get(reverse("web:evidencia", args=["CC-F4-02", 1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_disagreement_is_explicit(self):
        self.assertContains(
            self.post(
                action="approve",
                reason="requirements_met",
                discrepancy="on",
                expected_case_version=1,
            ),
            "Declara el motivo",
        )
        self.post(
            action="approve",
            reason="requirements_met",
            discrepancy="on",
            comment="No comparto la sugerencia.",
            expected_case_version=1,
        )
        self.assertTrue(get_decision("CC-F1-01").discrepancy)


class ConcurrentReviewTests(TransactionTestCase):
    def test_two_connections_same_version_only_one_wins(self):
        from concurrent.futures import ThreadPoolExecutor
        from django.db import connections
        from mira.composition import register_human_decision
        from mira.infrastructure.review_store import history

        call_command("load_demo", verbosity=0)

        def submit(action, reason):
            try:
                return register_human_decision(
                    case_id="CC-F1-04",
                    action_code=action,
                    reason_code=reason,
                    comment="",
                    expected_case_version=1,
                )
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(
                pool.map(
                    lambda pair: submit(*pair),
                    [
                        ("approve", "requirements_met"),
                        ("reject", "requirements_not_met"),
                    ],
                )
            )
        self.assertEqual(sum(result[0] is not None for result in results), 1)
        self.assertEqual(len(history("CC-F1-04")), 1)


class ImmutableHistoryTests(TestCase):
    def setUp(self):
        call_command("load_demo", verbosity=0)

    def test_snapshots_cannot_be_overwritten_or_deleted_via_repository_models(self):
        from mira.infrastructure.models import EvaluationRecord

        record = EvaluationRecord.objects.first()
        with self.assertRaises(ValueError):
            record.delete()
        with self.assertRaises(ValueError):
            record.save()
        with self.assertRaises(ValueError):
            EvaluationRecord.objects.filter(pk=record.pk).update(result={})

class LegacySnapshotTests(TestCase):
    def test_legacy_error_snapshot_remains_immutable_and_correctable(self):
        from dataclasses import asdict, replace
        from mira.infrastructure.models import CaseRecord, EvaluationRecord
        from mira.infrastructure.review_store import serial, snapshot
        case = replace(get_controlled_case('CC-F4-09'), case_id='LEGACY-ERROR')
        record = CaseRecord.objects.create(case_id=case.case_id, payload=serial(asdict(case)), current_values={'amount':'120000'})
        result = serial(asdict(evaluate_case(case)))
        result.pop('errors')
        original = EvaluationRecord.objects.create(case=record, inputs=serial(asdict(case)), policy=serial(asdict(DEFAULT_POLICY)), result=result)
        response = self.client.post(reverse('web:ejecutar_f4'), {'case_id':case.case_id})
        self.assertContains(response, 'Corregir entradas')
        self.assertIn('score', snapshot(case.case_id)[1].errors)
        original.refresh_from_db()
        self.assertNotIn('errors', original.result)

class CorrectionOtherReasonTests(TestCase):
    def test_other_correction_requires_comment_without_changing_case(self):
        from mira.infrastructure.review_store import snapshot, history
        call_command('load_demo', verbosity=0)
        url = reverse('web:detalle_caso', args=['CC-F1-01'])
        payload = {'command':'correct', 'reason':'other', 'comment':'   ', 'corrected':'100000', 'expected_case_version':'1'}
        response = self.client.post(url, payload)
        self.assertContains(response, 'reason_required')
        record = snapshot('CC-F1-01')[0]
        self.assertEqual(record.version, 1)
        self.assertEqual(record.current_values['amount'], '120000')
        self.assertEqual(history('CC-F1-01'), [])
        response = self.client.post(url, {**payload, 'comment':'El respaldo ficticio indica 100000.'})
        self.assertContains(response, 'Decisión registrada correctamente.')
        record = snapshot('CC-F1-01')[0]
        self.assertEqual(record.version, 2)
        self.assertEqual(record.current_values['amount'], '100000')
        events = history('CC-F1-01')
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['payload']['reason_code'], 'other')
        self.assertEqual(events[0]['payload']['original'], '120000')

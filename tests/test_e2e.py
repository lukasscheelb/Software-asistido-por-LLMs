import pytest
from django.core.management import call_command
from playwright.sync_api import sync_playwright


@pytest.mark.django_db(transaction=True)
def test_integrated_f4_f1_browser(live_server):
    call_command("load_demo", verbosity=0)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        base = live_server.url
        expected = {
            "01": "ESCALADO",
            "02": "REVISIÓN",
            "03": "REVISIÓN",
            "04": "APROBADO AUTOMÁTICAMENTE",
            "05": "ESCALADO",
            "06": "REVISIÓN",
            "07": "REVISIÓN",
            "08": "REVISIÓN",
            "09": "ERROR / DERIVACIÓN",
        }
        for suffix, outcome in expected.items():
            page.goto(base + "/ejecutar-f4/")
            page.locator("[name=case_id]").select_option("CC-F4-" + suffix)
            page.get_by_role("button", name="Ejecutar Política").click()
            assert outcome in page.locator(".result-panel").inner_text()
        page.locator("[name=score]").fill("60")
        page.get_by_role("button", name="Reejecutar borrador").click()
        assert "REVISIÓN" in page.locator(".result-panel").inner_text()
        generated_id = page.locator("#result-title").inner_text()
        page.get_by_role("link", name="Abrir detalle", exact=True).click()
        assert generated_id in page.locator("h1").inner_text()
        assert "60" in page.locator(".score-section").inner_text()
        page.goto(base + "/casos/CC-F1-01/")
        assert page.locator('object[type="application/pdf"]').count() > 0
        pdf = page.request.get(base + "/casos/CC-F1-01/evidencia/1/")
        assert pdf.body().startswith(b"%PDF")
        assert (
            page.locator(".evidence-section").bounding_box()["y"]
            < page.locator(".score-section").bounding_box()["y"]
        )
        page.locator("[name=corrected]").fill("100000")
        page.locator("form:has([name=corrected]) [name=reason]").select_option(
            "extraction_error"
        )
        page.get_by_role("button", name="Registrar Corrección").click()
        assert "Original 120000 → corregido 100000" in page.locator("main").inner_text()
        page.goto(base + "/casos/CC-F1-03/")
        page.locator("[name=action][value=request_info]").check()
        page.locator(".decision-form:has([name=action]) [name=reason]").select_option(
            "information_incomplete"
        )
        page.get_by_role("button", name="Registrar decisión").click()
        assert "ESPERANDO ANTECEDENTES" in page.locator("main").inner_text()
        page.goto(base + "/casos/CC-F1-04/")
        other = browser.new_page()
        other.goto(page.url)
        for tab in (page, other):
            tab.locator("[name=action][value=approve]").check()
            tab.locator(
                ".decision-form:has([name=action]) [name=reason]"
            ).select_option("requirements_met")
        page.get_by_role("button", name="Registrar decisión").click()
        other.get_by_role("button", name="Registrar decisión").click()
        assert "stale_version" in other.locator("main").inner_text()
        assert "APROBADO" in other.locator("main").inner_text()
        page.goto(base + "/bandeja/")
        assert "CC-F1-06" in page.locator("main").inner_text()
        assert "Vencido" in page.locator("main").inner_text()
        page.goto(base + "/casos/CC-F4-02/")
        image = page.request.get(base + "/casos/CC-F4-02/evidencia/2/")
        assert image.body().startswith(b"\x89PNG")
        browser.close()

    from mira.infrastructure.review_store import snapshot

    assert snapshot(generated_id)[0].payload["score"] == "60"
    assert snapshot(generated_id)[1].outcome == "REVISIÓN"
    assert snapshot("CC-F4-09")[0].payload["score"] == "101"
    assert snapshot("CC-F4-09")[1].outcome == "ERROR / DERIVACIÓN"

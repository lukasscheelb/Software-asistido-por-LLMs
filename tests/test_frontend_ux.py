"""Browser acceptance of the approved UX delta using an isolated test DB."""
from pathlib import Path
import pytest
from django.core.management import call_command
from playwright.sync_api import sync_playwright, expect


@pytest.mark.django_db(transaction=True)
def test_frontend_responsive_and_accessible_feedback(live_server):
    call_command("load_demo", verbosity=0)
    output = Path(__file__).resolve().parents[1] / "docs/qa/frontend-2026-10-17"
    output.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        for width in (320, 360, 390, 768, 1366):
            page.set_viewport_size({"width": width, "height": 900})
            for surface, route in (
                ("f1", "/bandeja/"),
                ("f4", "/ejecutar-f4/"),
                ("detalle", "/casos/CC-F1-01/"),
            ):
                page.goto(live_server.url + route)
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"), (width, surface, page.evaluate("[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).map(e=>[e.tagName,e.className,Math.round(e.getBoundingClientRect().right)]).slice(0,15)"))
                if width in (390, 1366):
                    page.screenshot(path=str(output / f"{surface}-{width}.png"), full_page=True)
                if width < 768:
                    page.get_by_text("Menú", exact=True).click()
                    expect(page.locator('.mobile-navigation [aria-current="page"]')).to_have_count(1)
                if surface == "f1":
                    expect(page.get_by_role("columnheader", name="Caso", exact=True)).to_have_count(1)
                if surface == "detalle":
                    expect(page.locator('object[title^="PDF:"]')).not_to_have_count(0)
                    checkbox = page.locator('[name="discrepancy"]')
                    assert checkbox.bounding_box()["width"] == 20
                    evidence = page.locator(".evidence-section").bounding_box()
                    score = page.locator(".score-section").bounding_box()
                    assert evidence["y"] < score["y"]

        page.set_viewport_size({"width": 1366, "height": 900})
        page.goto(live_server.url + "/ejecutar-f4/")
        page.locator("[name=case_id]").select_option("CC-F4-09")
        page.get_by_role("button", name="Evaluar caso", exact=True).click()
        expect(page.locator("[data-error-summary]")).to_be_focused()
        expect(page.locator("#draft-score")).to_have_attribute("aria-invalid", "true")
        assert page.locator("#draft-score").get_attribute("aria-describedby")
        page.locator("[data-error-summary] a").first.click()
        expect(page.locator("#draft-score")).to_be_focused()

        page.goto(live_server.url + "/casos/CC-F1-01/")
        page.keyboard.press("Tab")
        expect(page.locator(".skip-link")).to_be_focused()
        page.keyboard.press("Enter")
        expect(page.locator("#contenido")).to_be_focused()
        page.locator("#decision-comment").focus()
        page.keyboard.press("Tab")
        expect(page.locator("#decision-operator")).to_be_focused()
        page.keyboard.press("Shift+Tab")
        expect(page.locator("#decision-comment")).to_be_focused()
        assert page.locator("#decision-comment").evaluate("e=>getComputedStyle(e).outlineStyle") == "solid"
        page.locator('[name=action][value=approve]').check()
        page.locator("#decision-reason").select_option("other")
        page.locator("#decision-operator").fill("Operador de prueba")
        page.locator("[name=discrepancy]").check()
        page.get_by_role("button", name="Registrar decisión", exact=True).click()
        expect(page.locator("#decision-comment")).to_have_attribute("aria-invalid", "true")
        expect(page.locator("[data-error-summary]")).to_be_focused()
        expect(page.locator("#decision-operator")).to_have_value("Operador de prueba")
        expect(page.locator("[name=discrepancy]")).to_be_checked()
        page.locator("#decision-comment").fill("Revisión de evidencia completada.")
        page.get_by_role("button", name="Registrar decisión", exact=True).click()
        expect(page.locator(".status-stack .status--approved")).to_have_text("APROBADO")

        page.locator("#correction-corrected").fill("-1")
        page.locator("#correction-reason").select_option("extraction_error")
        page.get_by_role("button", name="Registrar Corrección", exact=True).click()
        expect(page.locator("#correction-corrected")).to_have_attribute("aria-invalid", "true")
        expect(page.locator("[data-error-summary]")).to_be_focused()
        expect(page.locator("#correction-corrected")).to_have_value("-1")
        page.locator("#correction-corrected").fill("100000")
        page.get_by_role("button", name="Registrar Corrección", exact=True).click()
        expect(page.get_by_text("Corrección registrada correctamente.")).to_be_visible()

        page.goto(live_server.url + "/casos/CC-F1-04/")
        page.locator('[name=action][value=reject]').check()
        page.locator("#decision-reason").select_option("requirements_not_met")
        page.get_by_role("button", name="Registrar decisión", exact=True).click()
        expect(page.locator(".status-stack .status--rejected")).to_have_text("RECHAZADO")
        browser.close()

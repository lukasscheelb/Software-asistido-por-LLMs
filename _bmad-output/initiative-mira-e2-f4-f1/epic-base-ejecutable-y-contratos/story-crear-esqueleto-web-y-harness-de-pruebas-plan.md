---
title: 'Crear esqueleto web y harness de pruebas'
type: 'feature'
ticket: '3'
created: '2026-10-03'
status: 'built'
route: 'full'
route_source: 'auto'
baseline_revision: '5dd4e9e434d53f912d34e29533aa700460ff03f2'
review: 'thorough'
review_source: 'auto'
lenses_ran: ['blind-hunter', 'edge-case-hunter', 'verification-gap', 'intent-alignment']
review_loop_iteration: 0
context:
  - '_bmad-output/initiative-mira-e2-f4-f1/architecture-mira-f4-f1/ARCHITECTURE-SPINE.md'
  - '_bmad-output/initiative-mira-e2-f4-f1/epic-base-ejecutable-y-contratos/spec-base-ejecutable-y-contratos/SPEC.md'
  - '_bmad-output/initiative-mira-e2-f4-f1/ux-mira-f4-f1/DESIGN.md'
  - '_bmad-output/initiative-mira-e2-f4-f1/ux-mira-f4-f1/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** El repositorio no tiene aplicación ejecutable ni ruta visible; además necesita puntos de conexión estables para incorporar el harness en una story posterior.

**Approach:** Crear el starter CAP-3 con Python 3.13.16, Django 5.2.17 y SQLite; materializar los límites hexagonales, servir una Bandeja inicial en español y documentar en `tests/README.md` cómo conectar después pytest y Playwright 1.63.0, sin implementar todavía el harness. Django 5.2.17 sustituye la 5.2.18 aún no publicada por decisión humana del 2026-10-03.

## Boundaries & Constraints

**Always:** Mantener `web/infrastructure -> application -> domain`; reservar `composition.py` para ensamblaje; usar HTML server-rendered sin dependencia de JavaScript; bloquear el runtime en `uv.lock`; operar solo con Django y SQLite local; dejar rutas y settings consumibles por el futuro harness.

**Never:** Implementar o instalar el harness, pytest, Playwright o pruebas ejecutables; tampoco modelos, fixtures, scoring, reglas F4, decisiones F1, autenticación, servicios externos, infraestructura productiva ni otros artefactos BMAD.

</frozen-after-approval>

## Code Map

- `.python-version`, `pyproject.toml`, `uv.lock` -- runtime y Django exactos; sin dependencias de test.
- `manage.py`, `src/mira/{settings,urls,asgi,wsgi}.py` -- proyecto Django mínimo con SQLite.
- `src/mira/{domain,application,infrastructure}/`, `composition.py` -- structural seed importable, aún sin lógica funcional.
- `src/mira/web/` -- app, rutas, vista, template y CSS de la Bandeja; reutilizar tokens de `DESIGN.md`.
- `tests/README.md` -- contrato para conectar después unit, integration y e2e; sin código ejecutable.
- `README.md`, `.gitignore` -- guía de clon limpio e ignorados locales; preservar documentación existente.
- `_bmad/`, `.agents/`, `skills-lock.json`, PDFs y otros `_bmad-output/` -- no modificar.

## Tasks & Acceptance

**Execution:**
- [x] `.python-version`, `pyproject.toml`, `uv.lock` -- fijar Python, Django y packaging reproducible con `uv`, sin instalar el harness.
- [x] `manage.py`, `src/mira/{settings,urls,asgi,wsgi}.py` -- crear Django mínimo y SQLite local.
- [x] `src/mira/{domain,application,infrastructure}/`, `composition.py` -- crear límites importables y dirección AD-2.
- [x] `src/mira/web/` -- implementar `/` y `/bandeja/` con shell responsive y estado vacío en español.
- [x] `tests/README.md` -- especificar capas, fixtures, ruta visible y comandos previstos para conectar pytest y Playwright después.
- [x] `README.md`, `.gitignore` -- documentar instalación, migración y arranque; ignorar generados locales.

**Acceptance Criteria:**
- Given un clon limpio con `uv`, when se siguen los comandos del README, then Python 3.13.16 y el entorno de `uv.lock` se instalan sin servicios externos.
- Given la aplicación iniciada, when se abre `/`, then llega a `/bandeja/` y muestra `Bandeja` y `No hay Casos pendientes.` en HTML server-rendered.
- Given el scaffold, when una story posterior conecte el harness, then `tests/README.md` identifica settings, rutas, capas, marcadores CAP-3 y comandos previstos sin exigir cambios al arranque web.
- Given una base nueva, when corren `check` y migraciones, then Django finaliza sin errores y `db.sqlite3` queda fuera de Git.

## Implementation Notes

- 2026-10-03: el usuario redujo el alcance del harness a un contrato de conexión; `tests/README.md` es el único archivo bajo `tests/` y no se instalaron pytest ni Playwright.
- 2026-10-03: Django 5.2.18 aún no estaba publicado; el usuario aprobó usar 5.2.17. `uv.lock` quedó generado con Python 3.13.16 y cinco paquetes resueltos.
- 2026-10-03: se creó el proyecto Django, los cuatro límites importables, el composition root y la Bandeja responsive. `check`, migraciones, imports y rutas `/`, `/bandeja/` y 404 se verificaron correctamente.

## Plan Change Log

## Review Triage Log

- Pass 1 (`thorough`): high 0, medium 5, low 4, false 0, maybe-false 0. `blind-hunter` e `intent-alignment` completaron; `edge-case-hunter` y `verification-gap` informaron que sus archivos de instrucciones renderizados no eran legibles desde el aislamiento del subagente.
- `medium`, rejected/out-of-scope: el SPEC y el ticket aún esperan una prueba base, pero la intención humana congelada prohíbe implementar el harness y modificar otros artefactos BMAD en esta story; `tests/README.md` conserva el contrato para la story posterior.
- `low`, rejected/plan-only: los comandos de Verification no incluyen el smoke HTTP. La ejecución se comprobó con Django Client y quedó registrada en Implementation Notes; corregir este hallazgo solo editaría el plan o introduciría el harness expresamente excluido.
- `medium`, defer: Architecture Spine y SPEC conservan Django 5.2.18 mientras el código usa 5.2.17 por aprobación humana. La reconciliación se registró en `_bmad-output/implementation-artifacts/deferred-work.md` porque otros artefactos BMAD están fuera del alcance aprobado.
- `medium`, patch: README podía sugerir instalación sin red; ahora distingue ejecución sin servicios externos de instalación mediante red o caché previa.
- `medium`, patch: `cap_3 and unit` no tenía conducta concreta; `tests/README.md` ahora define la guardia AST de AD-2 y el composition root.
- `medium`, patch: el contrato E2E omitía ciclo de vida; ahora fija puerto dinámico, readiness acotada, SQLite temporal y teardown garantizado.
- `low`, patch: README presentaba solo Entrega 1; ahora conserva ese origen y declara el incremento F4 + F1 de Entrega 2.
- `low`, rejected/plan-only: `&&` no funciona en Windows PowerShell 5.1, pero aparece solo en el plan de build; el README ya documenta comandos separados y el workflow prohíbe parchear hallazgos cuyo arreglo sea editar el plan.
- `low`, rejected/plan-only: la lista manual no enumera toda WCAG 2.2 AA. La revisión visual y de accesibilidad confirmó shell responsive, nombres accesibles, disclosure móvil y controles de 44 px; ampliar el checklist solo modificaría el plan.
- `intent-alignment`, accepted: el diff implementa la lectura mínima del scaffold y la postergación estricta del harness; la falta de pruebas ejecutables es una decisión humana explícita, no una divergencia accidental.

## Design Notes

La Bandeja solo comunica estructura y estado vacío; no simula funciones futuras. `tests/README.md` deja el contrato de conexión, pero esta story no crea configuración pytest, navegador Playwright ni pruebas.

## Verification

**Commands:**
- `uv sync --locked` -- expected: Python 3.13.16 y entorno bloqueado.
- `uv run python manage.py check && uv run python manage.py migrate --noinput` -- expected: configuración y migraciones base válidas.
- `git diff --check` -- expected: sin errores.

**Manual checks (if no CLI):**
- Abrir `/bandeja/` en escritorio y móvil; confirmar navegación, foco, ausencia de solapamientos y estado vacío. Revisar que `tests/` solo contenga documentación de conexión.

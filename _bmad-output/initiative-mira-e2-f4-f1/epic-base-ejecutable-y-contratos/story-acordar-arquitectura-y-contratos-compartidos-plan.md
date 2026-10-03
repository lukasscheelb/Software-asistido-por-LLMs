---
title: 'Acordar arquitectura y contratos compartidos'
type: 'chore'
ticket: '1'
created: '2026-10-03'
status: 'built'
route: 'oneshot'
route_source: 'auto'
baseline_revision: '7388525120ef99b50b612ff7c44044028ca2581e'
review: 'quick'
review_source: 'auto'
lenses_ran: ['quick-context-free']
review_loop_iteration: 0
context:
  - '_bmad-output/initiative-mira-e2-f4-f1/architecture-mira-f4-f1/ARCHITECTURE-SPINE.md'
  - '_bmad-output/initiative-mira-e2-f4-f1/epic-base-ejecutable-y-contratos/spec-base-ejecutable-y-contratos/SPEC.md'
  - '_bmad-output/initiative-mira-e2-f4-f1/epic-base-ejecutable-y-contratos/spec-base-ejecutable-y-contratos/domain-contracts.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** OQ-2, OQ-3 y OQ-4 siguen abiertas: sin aceptar el starter y la concurrencia, definir el escenario p95 y fijar el criterio PX-08, las historias de scaffold y verificacion no tienen un contrato ejecutable.

**Approach:** Registrar decisiones fechadas y citables para tecnologia, persistencia, concurrencia, rendimiento y recursos; actualizar las fuentes canonicas y sus copias de traspaso sin implementar aun el scaffold ni las reglas F4/F1. Se acepta Python 3.13.16, Django 5.2.18 LTS, SQLite local, Playwright Python 1.63.0 y concurrencia optimista con `expected_case_version`. NFR-3 medira la apertura del detalle desde la Bandeja con 100 Casos y 3 Evidencias por Caso, Django + SQLite local limitado a 2 vCPU/4 GiB, 5 calentamientos y 30 muestras, con `p95 <= 2 s`. PX-08 medira mediante `psutil` el arbol Django + Chromium durante 30 revisiones Playwright, con RSS maximo `<= 1 GiB` y CPU promedio `<= 1 nucleo logico`.

</frozen-after-approval>

## Implementation Notes

Ruta oneshot: el cambio es documental, afecta pocas fuentes canonicas y se estima en menos de 100 lineas; las decisiones HITL deben cerrarse antes de editar los contratos.

- 2026-10-03: el usuario aprobo las opciones recomendadas 1A, 2A y 3A; OQ-2, OQ-3 y OQ-4 quedan listas para cierre documental.
- 2026-10-03: `ARCHITECTURE-SPINE.md` incorpora AD-15, AD-16 y el registro CAP-1; `SPEC.md`, `domain-contracts.md`, PRD y addendum registran las mismas decisiones fechadas.
- 2026-10-03: las copias de iniciativa se sincronizaron por SHA-256 y el informe de validacion dejo solo las decisiones UX de 1.2 como pendientes.
- 2026-10-03: revision quick completo un lente independiente; cinco hallazgos reales fueron parcheados. Linter de arquitectura: cero hallazgos; siete pares de copias: SHA-256 identico; referencias obsoletas: cero.

## Plan Change Log

## Review Triage Log

- `medium`, patched: AD-16 y los contratos decían “procesos” y podían excluir hijos de Chromium; se fijó “árboles de procesos de Django y Chromium” en todas las fuentes y copias.
- `medium`, patched: los SPEC canónicos de F1 y verificación conservaban OQ-2/OQ-3/OQ-4 abiertas; ahora adoptan explícitamente las decisiones de 1.1 y dejan solo el catálogo UX pendiente.
- `medium`, patched: el índice de supuestos del PRD contradecía sus OQ resueltas; ahora registra el cierre de OQ-2 a OQ-4 y mantiene OQ-1/OQ-5 abiertas.
- `low`, patched: `review-rubric.md` conservaba un blocker histórico de rendimiento y recursos; quedó marcado como resuelto por AD-15/AD-16.
- `low`, patched: el addendum agrupaba la marca para supervisor bajo decisiones resueltas; quedó separada como decisión técnica diferida.

## Verification

**Commands:**
- `python .agents/skills/bmad-architecture/scripts/lint_spine.py --workspace _bmad-output/planning-artifacts/architecture/architecture-Software-asistido-por-LLMs-2026-10-03` -- expected: `ok: true` y cero hallazgos.
- `uv run _bmad/method/scripts/tickets.py --project-root . find 1.1` -- expected: el plan se resuelve desde el ticket 1.1 y cita las decisiones cerradas.

**Manual checks (if no CLI):**
- Confirmar que OQ-2, OQ-3 y OQ-4 tienen decision, fecha, responsable y el mismo texto en fuentes canonicas y copias de traspaso.

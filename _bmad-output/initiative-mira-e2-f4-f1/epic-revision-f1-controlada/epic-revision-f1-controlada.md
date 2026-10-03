---
type: epic
title: "Revisión F1 controlada"
parent: initiative-mira-e2-f4-f1
covers: [FR-7, FR-8, FR-9, FR-10, FR-11, FR-12, FR-13, FR-14, FR-15, FR-16, FR-17, FR-19, NFR-2, NFR-3, NFR-4, NFR-5, NFR-6]
after: [epic-base-ejecutable-y-contratos, epic-politica-f4-explicable]
assignee: ""
risk: high
---

# Revisión F1 controlada

## Description

Entrega la Bandeja y el detalle de Caso para revisión humana significativa. Recibe Salidas F4 reales, ordena el contexto antes del Puntaje y protege motivos, Correcciones, concurrencia y plazos.

## Outcome

Marco resuelve los escenarios PF-05 y PF-14 desde la interfaz, mientras Sebastián comprueba que ESCALADO es prioridad humana y nunca rechazo automático.

## Requirements

La fuente numerada es `spec-revision-f1-controlada/SPEC.md`; `review-cases.md` fija flujos y corpus.

- CAP-1 → FR-7.
- CAP-2 → FR-8, NFR-3 y NFR-4.
- CAP-3 → FR-9, NFR-2 y NFR-6.
- CAP-4 → FR-10 y FR-11.
- CAP-5 → FR-12, FR-14 y FR-17.
- CAP-6 → FR-13 y FR-17.
- CAP-7 → FR-15, FR-16 y NFR-5.
- CAP-8 → FR-7, FR-8, FR-9, FR-10, FR-11, FR-12, FR-13, FR-14, FR-15, FR-16, FR-19, NFR-2, NFR-5 y NFR-6.

## Done when

1. CC-F1-01 a CC-F1-06 se completan desde la interfaz con los resultados del PRD.
2. REVISIÓN y ESCALADO aparecen con prioridad y marca correctas a partir de Salidas F4 reales.
3. Evidencia y razones aparecen antes del Puntaje en el detalle.
4. Motivos, Correcciones, Discrepancias y concurrencia preservan la procedencia.
5. La suite E2E demuestra una Decisión humana, una Corrección, un conflicto de versión y un vencimiento.
6. F1 queda integrada en la versión candidata ejecutable del repositorio.

## Boundaries

Incluye lista, detalle y acciones del Operador. No incluye panel agregado del supervisor, revisión del equipo de modelos, nueva Evidencia ni cierre por falta de antecedentes.

## References

- parent — _bmad-output/initiative-mira-e2-f4-f1/initiative-mira-e2-f4-f1.md
- spec — _bmad-output/initiative-mira-e2-f4-f1/epic-revision-f1-controlada/spec-revision-f1-controlada/SPEC.md
- companion — _bmad-output/initiative-mira-e2-f4-f1/epic-revision-f1-controlada/spec-revision-f1-controlada/review-cases.md
- ux — _bmad-output/initiative-mira-e2-f4-f1/ux-mira-f4-f1/DESIGN.md y EXPERIENCE.md
- architecture — _bmad-output/initiative-mira-e2-f4-f1/architecture-mira-f4-f1/ARCHITECTURE-SPINE.md
- prd — _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/prd-mira-f4-f1.md, sección 4.2 y §9.2
- design decision — epic-base-ejecutable-y-contratos, entrada 2
- baseline — LLM - MIRA_E2_Baseline_F4_F1.md, PF-05 y PF-14

## Notes

- Waits on epic-base-ejecutable-y-contratos because: necesita UX, catálogo de motivos, contratos y shell.
- Waits on epic-politica-f4-explicable because: consume Salida F4 y explicación reales.
- Decision: CC-F1-03 es el tracer bullet de F1 (2026-10-03).
- Decision: los flujos de datos y estado se implementan en una sola secuencia para evitar colisiones (2026-10-03).
- Decision: el SPEC de la épica es la fuente de CAP-1 a CAP-8 y las historias citan esos IDs estables (2026-10-03).
- Decision: el refactor sweep precede a la suite E2E final (2026-10-03).
- High-risk check: Sebastián revisa la suite PF-05/PF-14 y una sesión de concurrencia antes de aceptar la épica.

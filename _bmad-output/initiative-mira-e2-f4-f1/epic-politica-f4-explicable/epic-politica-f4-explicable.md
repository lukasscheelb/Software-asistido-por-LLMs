---
type: epic
title: "Política F4 explicable"
parent: initiative-mira-e2-f4-f1
covers: [FR-1, FR-2, FR-3, FR-4, FR-5, FR-6, FR-17, FR-19, NFR-1, NFR-5]
after: [epic-base-ejecutable-y-contratos]
assignee: ""
risk: medium
---

# Política F4 explicable

## Description

Implementa la Política F4 determinista sobre Puntaje y Señales simuladas, con precedencia exacta, configuración versionada y explicación reutilizable por F1.

## Outcome

Sebastián ejecuta la matriz PF-04 y cada Caso produce la Salida F4 y la razón esperadas sin rechazo automático.

## Requirements

La fuente numerada es `spec-politica-f4-explicable/SPEC.md`; `policy-cases.md` fija precedencia y corpus.

- CAP-1 → FR-1.
- CAP-2 → FR-2 y NFR-1.
- CAP-3 → FR-3 y NFR-1.
- CAP-4 → FR-4 y NFR-1.
- CAP-5 → FR-5 y NFR-5.
- CAP-6 → FR-6 y FR-17.
- CAP-7 → FR-1, FR-2, FR-3, FR-4, FR-5, FR-6, FR-19 y NFR-5.

## Done when

1. CC-F4-01 a CC-F4-09 producen exactamente los resultados del PRD.
2. Ninguna ruta produce rechazo automático.
3. Cada Evaluación conserva Versión de política, entradas y explicación.
4. F1 puede consumir la Salida F4 y sus razones sin duplicar reglas.
5. La suite E2E demuestra al menos APROBADO AUTOMÁTICAMENTE, REVISIÓN, ESCALADO y ERROR / DERIVACIÓN.
6. F4 queda integrada en la versión candidata ejecutable del repositorio.

## Boundaries

Incluye la política y su presentación mínima. No incluye scoring real, edición visual de umbrales ni decisiones humanas F1.

## References

- parent — _bmad-output/initiative-mira-e2-f4-f1/initiative-mira-e2-f4-f1.md
- spec — _bmad-output/initiative-mira-e2-f4-f1/epic-politica-f4-explicable/spec-politica-f4-explicable/SPEC.md
- companion — _bmad-output/initiative-mira-e2-f4-f1/epic-politica-f4-explicable/spec-politica-f4-explicable/policy-cases.md
- ux — _bmad-output/initiative-mira-e2-f4-f1/ux-mira-f4-f1/DESIGN.md y EXPERIENCE.md
- architecture — _bmad-output/initiative-mira-e2-f4-f1/architecture-mira-f4-f1/ARCHITECTURE-SPINE.md
- prd — _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/prd-mira-f4-f1.md, sección 4.1 y §9.1
- baseline — LLM - MIRA_E2_Baseline_F4_F1.md, secciones 7 y 12

## Notes

- Waits on epic-base-ejecutable-y-contratos because: necesita contratos, shell, harness y fixtures.
- Decision: CC-F4-02 es el tracer bullet de la épica (2026-10-03).
- Decision: las reglas se implementan en el orden del PRD; no se combinan en una fórmula (2026-10-03).
- Decision: el SPEC de la épica es la fuente de CAP-1 a CAP-7 y las historias citan esos IDs estables (2026-10-03).
- Decision: el refactor sweep precede a la suite E2E final (2026-10-03).

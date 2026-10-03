---
type: epic
title: "Verificación y entrega trazable"
parent: initiative-mira-e2-f4-f1
covers: [FR-17, FR-18, FR-19, FR-20, NFR-1, NFR-2, NFR-3, NFR-4, NFR-5, NFR-6]
after: [epic-politica-f4-explicable, epic-revision-f1-controlada]
assignee: ""
risk: medium
---

# Verificación y entrega trazable

## Description

Integra el corpus controlado, la evidencia de calidad, el README y la aceptación del representante del cliente. Convierte el incremento funcional en una entrega reproducible y auditable.

## Outcome

Un evaluador clona, ejecuta, prueba y demuestra F4 + F1 en menos de 15 minutos, y puede rastrear cada requisito Must hasta su evidencia.

## Requirements

La fuente numerada es `spec-verificacion-entrega-trazable/SPEC.md`; `verification-matrix.md` fija la evidencia.

- CAP-1 → FR-17, FR-18, NFR-5 y NFR-6.
- CAP-2 → FR-20.
- CAP-3 → FR-19 y NFR-6.
- CAP-4 → NFR-2.
- CAP-5 → NFR-1, NFR-3, NFR-4 y NFR-5.
- CAP-6 → FR-19, FR-20, NFR-1 y NFR-2.
- CAP-7 → FR-17, FR-18, FR-19, FR-20, NFR-5 y NFR-6.

## Done when

1. El catálogo CC-F4 y CC-F1 completo pasa en pruebas automatizadas y E2E.
2. El README levanta el sistema y carga datos desde un clon limpio en menos de 15 minutos.
3. PX-05, PX-08 y PX-09 tienen resultados y evidencia reproducible.
4. Sebastián acepta o rechaza cada funcionalidad contra criterios registrados.
5. La trazabilidad de todos los Must llega a commit y prueba sin enlaces rotos.
6. La versión candidata integrada queda ejecutable desde un clon limpio del repositorio.

## Boundaries

Incluye verificación, documentación operativa y aceptación del incremento. No añade nuevas funcionalidades ni resuelve temas del addendum fuera del alcance.

## References

- parent — _bmad-output/initiative-mira-e2-f4-f1/initiative-mira-e2-f4-f1.md
- spec — _bmad-output/initiative-mira-e2-f4-f1/epic-verificacion-entrega-trazable/spec-verificacion-entrega-trazable/SPEC.md
- companion — _bmad-output/initiative-mira-e2-f4-f1/epic-verificacion-entrega-trazable/spec-verificacion-entrega-trazable/verification-matrix.md
- ux — _bmad-output/initiative-mira-e2-f4-f1/ux-mira-f4-f1/DESIGN.md y EXPERIENCE.md
- architecture — _bmad-output/initiative-mira-e2-f4-f1/architecture-mira-f4-f1/ARCHITECTURE-SPINE.md
- prd — _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/prd-mira-f4-f1.md, secciones 9–12
- assignment — Contexto-fase1-bmad/LLM - Entrega_2_MIRA_SDD_BMAD.pdf, secciones 1.3, 4.3, 4.4 y 6.5

## Notes

- Waits on epic-politica-f4-explicable because: necesita F4 completa y su suite E2E.
- Waits on epic-revision-f1-controlada because: necesita F1 completa y su suite E2E.
- Decision: no se crea una épica separada para documentación; README y trazabilidad son parte de la entrega integrada (2026-10-03).
- Decision: después de 4.1, trazabilidad, verificación del README y mediciones trabajan en artefactos separados; por eso 4.2, 4.3 y 4.5 pueden avanzar en paralelo (2026-10-03).
- Decision: el SPEC de la épica es la fuente de CAP-1 a CAP-7 y las historias citan esos IDs estables (2026-10-03).
- Decision: el refactor sweep precede a la suite E2E integral (2026-10-03).

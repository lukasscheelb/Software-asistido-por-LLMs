---
type: epic
title: "Base ejecutable y contratos compartidos"
parent: initiative-mira-e2-f4-f1
covers: [FR-5, FR-17, FR-18, FR-19, FR-20, NFR-3, NFR-4, NFR-5, NFR-6]
after: []
assignee: ""
risk: medium
---

# Base ejecutable y contratos compartidos

## Description

Resuelve las decisiones que vinculan F4, F1 y QA; crea el esqueleto web, el harness automatizado, el modelo de dominio y los primeros Casos controlados. Las épicas funcionales parten de contratos compartidos en vez de inventar sus propios formatos.

## Outcome

El equipo puede iniciar la aplicación, ejecutar una prueba base y recorrer un Caso ficticio a través de un contrato estable de Caso, Política, Evaluación y Salida F4.

## Requirements

La fuente numerada es `spec-base-ejecutable-y-contratos/SPEC.md`; `domain-contracts.md` completa el contrato.

- CAP-1 → FR-5, FR-17, NFR-3, NFR-4 y NFR-5.
- CAP-2 → FR-19 y NFR-6.
- CAP-3 → FR-19, FR-20 y NFR-6.
- CAP-4 → FR-5, FR-17 y NFR-5.
- CAP-5 → FR-18, FR-19, NFR-5 y NFR-6.

## Done when

1. Las decisiones OQ-1 a OQ-5 tienen respuesta o un bloqueo explícito con dueño.
2. La aplicación web y la suite de pruebas arrancan desde un clon del repositorio.
3. Un Caso controlado se carga y atraviesa un stub F4 → F1 visible en la interfaz.
4. Los contratos compartidos registran Política y Versión del caso sin elegir una fórmula de scoring.
5. Los datos de prueba son ficticios, deterministas y no exponen secretos.
6. La base queda integrada en la versión candidata del repositorio y es ejecutable desde un clon limpio.

## Boundaries

Incluye decisiones compartidas, scaffold, contratos, harness y fixtures mínimos. No implementa todavía todas las reglas F4 ni los flujos completos F1.

## References

- parent — _bmad-output/initiative-mira-e2-f4-f1/initiative-mira-e2-f4-f1.md
- spec — _bmad-output/initiative-mira-e2-f4-f1/epic-base-ejecutable-y-contratos/spec-base-ejecutable-y-contratos/SPEC.md
- companion — _bmad-output/initiative-mira-e2-f4-f1/epic-base-ejecutable-y-contratos/spec-base-ejecutable-y-contratos/domain-contracts.md
- ux — _bmad-output/initiative-mira-e2-f4-f1/ux-mira-f4-f1/DESIGN.md y EXPERIENCE.md
- architecture — _bmad-output/initiative-mira-e2-f4-f1/architecture-mira-f4-f1/ARCHITECTURE-SPINE.md
- prd — _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/prd-mira-f4-f1.md, secciones 3–6 y 13
- addendum — _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/addendum.md, decisiones técnicas

## Notes

- Decision: el tracer usa el Caso CC-F4-02 y termina en solicitud de antecedentes (2026-10-03).
- Decision: las decisiones compartidas viven en las entradas 1 y 2; las épicas posteriores dependen de ellas (2026-10-03).
- Unknown: stack, persistencia y mecanismo de concurrencia; entrada 1.
- Unknown: categorías de motivo y presentación de ERROR / DERIVACIÓN; entrada 2.
- Decision: el SPEC de la épica es la fuente de CAP-1 a CAP-5 y las historias citan esos IDs estables (2026-10-03).
- Decision: plan de arranque — 1.1 y 1.2 avanzan en paralelo; luego 1.3, 1.4, 1.5 y 1.6 siguen su cadena de dependencias (2026-10-03).
- Decision: las épicas F4, F1 y verificación permanecen planificadas fuera de la primera ola hasta cerrar la base compartida (2026-10-03).
- Decision: el refactor sweep cierra la épica antes de que F4/F1 amplíen la base (2026-10-03).

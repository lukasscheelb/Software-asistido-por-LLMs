---
type: initiative
title: "Incremento demostrable MIRA F4 + F1"
parent: none
covers: [FR-1, FR-2, FR-3, FR-4, FR-5, FR-6, FR-7, FR-8, FR-9, FR-10, FR-11, FR-12, FR-13, FR-14, FR-15, FR-16, FR-17, FR-18, FR-19, FR-20, NFR-1, NFR-2, NFR-3, NFR-4, NFR-5, NFR-6]
after: []
assignee: ""
risk: high
---

# Incremento demostrable MIRA F4 + F1

## Description

Entrega una aplicación web en español que aplica la Política F4 sobre Casos controlados y deriva a F1 los Casos en REVISIÓN o ESCALADOS. El Operador revisa Evidencia, registra una Decisión humana y conserva la trazabilidad exigida por el PRD 1.0.

## Outcome

Sebastián Rodríguez puede recorrer F4 → F1 con datos ficticios, verificar las fronteras de decisión y seguir cada requisito Must hasta una prueba y un commit.

## Requirements

El PRD 1.0 copiado en `prd-mira-f4-f1/prd-mira-f4-f1.md` es la fuente numerada de FR-1 a FR-20 y NFR-1 a NFR-6. Las épicas conservan esos IDs en `covers` y especifican qué parte entregan cuando un requisito es compartido.

## Done when

1. Los Casos controlados recorren F4 y F1 desde la interfaz en español sin herramientas de desarrollo.
2. Las fronteras, excepciones, decisiones humanas, concurrencia y plazos producen los resultados del PRD.
3. Un clon limpio se levanta siguiendo el README en menos de 15 minutos.
4. Las pruebas automatizadas cubren los requisitos Must, un E2E por funcionalidad y los escenarios PF/PX aplicables.
5. Sebastián registra la aceptación de F4 y F1, y cada requisito Must llega a código, prueba y commit.

## Boundaries

La iniciativa cubre el incremento académico F4 + F1, no el producto MIRA completo. No incluye scoring real, datos personales reales, rechazo automático, F2-F3, F5-F9, multitenencia, facturación ni despliegue productivo.

- Touch point: configuración de Política — consumida como datos versionados; owner: epic-politica-f4-explicable.
- Touch point: marca para supervisor — producida en F1 sin panel agregado; owner: epic-revision-f1-controlada.
- Touch point: artefactos BMAD y Git — enlazados por la evidencia de entrega; owner: epic-verificacion-entrega-trazable.

Tracer path: un Caso controlado con Puntaje `60` produce REVISIÓN en F4, aparece en F1, muestra Evidencia antes del Puntaje y termina en una solicitud de antecedentes motivada.

## References

- prd — _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/prd-mira-f4-f1.md, secciones 1–15
- addendum — _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/addendum.md
- ux — _bmad-output/initiative-mira-e2-f4-f1/ux-mira-f4-f1/DESIGN.md y EXPERIENCE.md
- architecture — _bmad-output/initiative-mira-e2-f4-f1/architecture-mira-f4-f1/ARCHITECTURE-SPINE.md
- baseline — LLM - MIRA_E2_Baseline_F4_F1.md
- decision log — LLM - MIRA_Entrega2_bitacora_decisiones.md, sección 13

## Notes

- Decision: usar el backend repo de BMAD ticketing y la iniciativa `initiative-mira-e2-f4-f1` (2026-10-03).
- Decision: la primera épica es la base compartida porque no existe código del incremento (2026-10-03).
- Decision: UX y arquitectura pendientes se resuelven como trabajo HITL antes de las historias que dependen de ellas (2026-10-03).
- Decision: en este incremento académico, entrega integrada significa incorporada a la versión candidata del repositorio y ejecutable desde un clon limpio; el despliegue productivo está fuera de alcance (2026-10-03).
- Decision: la arquitectura fast path fue aceptada en 1.1; los `[ASSUMPTION]` y Deferred de UX requieren aceptación antes de cerrar 1.2 (2026-10-03).
- High-risk check: Sebastián valida el recorrido integrado y la matriz de trazabilidad antes de aceptar la iniciativa.
- Open question: OQ-1 a OQ-5 del PRD se asignan a las entradas 1.1 y 1.2.

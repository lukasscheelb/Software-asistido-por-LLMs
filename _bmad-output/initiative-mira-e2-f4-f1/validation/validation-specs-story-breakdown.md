# Validación de bmad-spec por épica y Story Breakdown

Fecha: 2026-10-03  
Specs canónicos: `_bmad-output/specs/`  
Handoff: una copia exacta de cada spec vive dentro de su épica y actúa como fuente numerada para ticketing.

## Resultado

- Estado: aprobado para revisión humana antes de publicar.
- Specs: 4.
- Capacidades: 27 en total; 5 de base, 7 de F4, 8 de F1 y 7 de verificación.
- Companions: 4; contratos de dominio, matriz F4, flujos F1 y matriz de verificación.
- Historias: 33, con los mismos IDs, títulos, orden y dependencias de la iteración anterior.
- Cobertura: cada `CAP-N` tiene al menos una historia y cada `covers` de historia resuelve en el SPEC de su épica.
- Trazabilidad parental: cada capacidad está mapeada a los `FR/NFR` declarados por la épica, sin faltantes ni IDs ajenos.
- Dependencias: `tickets.py status` termina correctamente y reporta `unpinned_after = 0`.
- Handoff: SPEC, companion y `.memlog.md` dentro de cada épica coinciden por SHA-256 con el spec canónico.

## Contratos creados

1. `spec-base-ejecutable-y-contratos`: CAP-1 a CAP-5 y `domain-contracts.md`.
2. `spec-politica-f4-explicable`: CAP-1 a CAP-7 y `policy-cases.md`.
3. `spec-revision-f1-controlada`: CAP-1 a CAP-8 y `review-cases.md`.
4. `spec-verificacion-entrega-trazable`: CAP-1 a CAP-7 y `verification-matrix.md`.

## Story Breakdown reconciliado

- Las historias ya no citan directamente `FR/NFR` en `covers`; citan capacidades estables del spec local.
- Cada épica conserva en `Requirements` el mapa explícito `CAP-N → FR/NFR`.
- Los tracers siguen siendo 1.3/1.5 para la base, 2.1 para F4 y 3.1 para F1.
- Los sweeps de refactor y suites E2E permanecen al final de cada secuencia.
- Las ramas paralelas 4.2, 4.3 y 4.5 mantienen ownership separado de trazabilidad, README y mediciones.

## Preguntas abiertas preservadas

- Base CAP-1: stack, persistencia, concurrencia, escenario p95 y criterio PX-08.
- Base CAP-2: catálogo de motivos y presentación de `ERROR / DERIVACIÓN`.
- F4: superficie visual de `ERROR / DERIVACIÓN` sin cambiar su semántica.
- F1: catálogo de motivos, mediciones de Bandeja y mecanismo de concurrencia.
- Verificación CAP-5: consume las decisiones p95/PX-08 de la historia HITL 1.1.

No se inventaron respuestas para estas preguntas. Las dependencias existentes mantienen bloqueado el trabajo que las necesita.

## Spec Law

- Coherencia: todas las capacidades tienen `intent` y `success`; cada spec contiene restricciones, no objetivos y señal verificable.
- Preservación: los requisitos, guardrails, matrices y Casos controlados de las fuentes están en el kernel o en un companion.
- Memoria: cada spec tiene `.memlog.md` append-only con capacidades, restricciones, preguntas, contenido ceremonial descartado y ambos veredictos de validación.

La revisión independiente mediante subagentes no estaba disponible en este entorno; se realizó revisión manual completa más validación determinista de forma, cobertura, referencias, hashes y dependencias.

## Publicación

Los artefactos permanecen sin commit. En el store repo de BMAD, el commit publica el Story Breakdown y requiere aprobación explícita.

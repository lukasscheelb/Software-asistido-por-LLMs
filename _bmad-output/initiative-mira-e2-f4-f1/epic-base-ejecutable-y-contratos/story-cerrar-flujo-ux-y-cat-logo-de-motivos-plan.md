---
title: 'Cerrar flujo UX y catálogo de motivos'
type: 'chore'
ticket: '2'
created: '2026-10-03'
status: done
route: 'oneshot'
route_source: 'auto'
baseline_revision: 'f386bf6d501200369d8cb3ea2936990251d1bc77'
review: 'quick'
review_source: 'auto'
lenses_ran: ['quick-context-free']
review_loop_iteration: 0
context:
  - '_bmad-output/initiative-mira-e2-f4-f1/ux-mira-f4-f1/DESIGN.md'
  - '_bmad-output/initiative-mira-e2-f4-f1/ux-mira-f4-f1/EXPERIENCE.md'
  - '_bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/prd-mira-f4-f1.md'
  - '_bmad-output/initiative-mira-e2-f4-f1/epic-base-ejecutable-y-contratos/spec-base-ejecutable-y-contratos/SPEC.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** OQ-1 y OQ-5 siguen abiertas: el selector de motivos no tiene valores implementables y `ERROR / DERIVACIÓN` conserva una superficie visual asumida, por lo que F1 y los recorridos F4 todavía pueden divergir.

**Approach:** Registrar un catálogo inicial estable y compatible con cada acción humana, decidir la superficie de `ERROR / DERIVACIÓN` y sincronizar PRD, SPEC, UX y contratos consumidores sin implementar todavía la interfaz. Se acepta un catálogo específico por acción: aprobar (`Requisitos cumplidos`, `Evidencia consistente`), rechazar (`Requisitos no cumplidos`, `Evidencia inconsistente`), solicitar antecedentes (`Antecedentes incompletos`, `Evidencia ilegible`, `Aclaración requerida`) y corregir (`Error de extracción`, `Dato no coincide con la Evidencia`); todas incluyen `Otro` con comentario obligatorio. `ERROR / DERIVACIÓN` permanece inline en Resultado F4, conserva entradas, identifica campo y causa, ofrece `Corregir entradas` y nunca crea una fila F1.

</frozen-after-approval>

## Implementation Notes

Ruta oneshot: el cambio es documental, coherente y mecánico; se estima en menos de 100 líneas útiles. La búsqueda independiente confirmó que ninguna fuente Markdown, historial o PDF contiene los valores faltantes ni una decisión final de superficie.

- 2026-10-03: el usuario aprobó las opciones recomendadas 1A y 2A; OQ-1 y OQ-5 quedan listas para cierre documental.
- 2026-10-03: PRD, UX, Architecture Spine y los SPEC de base, F4 y F1 adoptan códigos estables, compatibilidad por acción, `other` con comentario obligatorio y `ERROR / DERIVACIÓN` inline.
- 2026-10-03: las fuentes canónicas se sincronizaron con sus copias de iniciativa y el memlog UX registró las decisiones de forma append-only.
- 2026-10-03: revisión quick completó un lente independiente; cuatro hallazgos medios fueron parcheados. Linter: cero hallazgos; nueve pares de copias: SHA-256 idéntico; referencias obsoletas: cero.

## Plan Change Log

## Review Triage Log

- `medium`, patched: `base/CAP-2` seguía gobernada por decisiones UX diferidas; el mapa ahora cita AD-9 y AD-13.
- `medium`, patched: la iniciativa seguía nombrando OQ-1 a OQ-5 como abiertas; ahora registra su cierre en 1.1/1.2 y separa supuestos visuales no bloqueantes.
- `medium`, patched: `Corregir entradas` no tenía transición implementable; EXPERIENCE define retorno al mismo borrador, foco, edición transitoria, fixture inmutable y reejecución.
- `medium`, patched: PF-05 no cubría categoría incompatible ni `other` vacío; CC-F1-02a/b/c fijan ambos rechazos y sus códigos de error.

## Verification

**Commands:**
- `git diff --check` -- expected: sin errores de formato.
- Búsqueda de OQ-1/OQ-5 y `[ASSUMPTION] ERROR / DERIVACIÓN` -- expected: las fuentes canónicas registran las decisiones y solo mantienen pendientes visuales no bloqueantes.

**Manual checks (if no CLI):**
- Confirmar que catálogo, compatibilidad por acción, regla de `Otro`, estados, acciones y validaciones coinciden entre PRD, UX y SPEC consumidores.

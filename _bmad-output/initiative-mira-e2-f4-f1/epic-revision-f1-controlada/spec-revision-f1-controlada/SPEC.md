---
id: SPEC-revision-f1-controlada
companions: [review-cases.md]
sources:
  - _bmad-output/initiative-mira-e2-f4-f1/epic-revision-f1-controlada/epic-revision-f1-controlada.md
  - _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/prd-mira-f4-f1.md
---

> **Canonical contract.** Este SPEC y los archivos en `companions:` son el contrato completo y validado para construir, probar y revisar esta épica.

# Revisión F1 controlada

## Why

Los Casos no resueltos por F4 requieren revisión humana significativa. F1 debe priorizar riesgo sin convertir la sugerencia de la plataforma en una decisión, y debe conservar motivos, Correcciones, concurrencia y plazos para que la intervención sea auditable.

## Capabilities

- **CAP-1**
  - **intent:** F1 enruta `REVISIÓN` con prioridad normal y `ESCALADO` con prioridad alta y marca para supervisor.
  - **success:** `APROBADO AUTOMÁTICAMENTE` no entra en la Bandeja y cada Caso derivado recibe la prioridad correcta.
- **CAP-2**
  - **intent:** La Bandeja muestra contexto operativo y habilita las mediciones acordadas de respuesta y recursos.
  - **success:** Identificador, Salida F4, razón, prioridad, estado y ambos plazos permiten distinguir prioridades y vencidos sin abrir el detalle.
- **CAP-3**
  - **intent:** El detalle presenta Evidencia, razón y Ubicación del hallazgo antes del Puntaje.
  - **success:** PDF e imagen ficticios señalan ubicaciones comprensibles y el Puntaje aparece después de la Evidencia y razones.
- **CAP-4**
  - **intent:** El Operador puede aprobar, rechazar o solicitar antecedentes con una Categoría de motivo.
  - **success:** Falta de motivo bloquea la acción y `Otro` exige comentario.
- **CAP-5**
  - **intent:** El Operador puede registrar Correcciones y Discrepancias sin borrar originales ni alterar la Decisión humana.
  - **success:** Valor original, corregido, motivo, autor, fecha y Versión del caso permanecen reconstruibles.
- **CAP-6**
  - **intent:** F1 protege la Decisión vigente frente a intervenciones basadas en una Versión del caso obsoleta.
  - **success:** El intento se rechaza, la Decisión vigente se conserva y el Operador recibe una indicación para recargar.
- **CAP-7**
  - **intent:** F1 calcula y alerta Plazo interno y contractual con calendario reproducible.
  - **success:** Los `3` y `5` días hábiles en `America/Santiago` se repiten con fecha controlada; el Caso vencido sigue abierto y prioritario.
- **CAP-8**
  - **intent:** Un evaluador puede completar el corpus F1 desde la interfaz.
  - **success:** CC-F1-01 a CC-F1-06 preservan estado, motivo, procedencia, concurrencia y alertas según `review-cases.md`.

## Constraints

- La sugerencia de la plataforma nunca sustituye el criterio del Operador.
- Evidencia, razón y Ubicación del hallazgo preceden al Puntaje; casos por hora no es una meta.
- Toda Decisión humana y Corrección exige Categoría de motivo.
- Solo se usan datos ficticios y fechas controladas.
- La implementación no incluye panel agregado del supervisor, revisión del equipo de modelos ni cierre por falta de antecedentes.

## Non-goals

- Crear nueva Evidencia o reabrir completamente Casos.
- Implementar F2, F3 o F5-F9.
- Automatizar rechazo o invalidar una Decisión humana por Discrepancia.

## Success signal

PF-05 y PF-14 pasan desde la interfaz: el Operador decide con Evidencia primero y el sistema conserva motivos, originales, Decisión vigente, plazos y alertas.

## Open Questions

### Resolved in story 1.1

- CAP-2 adopta AD-15 y AD-16: apertura Bandeja → detalle con 100 Casos, 3 Evidencias por Caso, 2 vCPU/4 GiB, 5 calentamientos, 30 muestras y `p95 ≤ 2 s`; PX-08 ejecuta 30 revisiones Playwright y mide con `psutil` los árboles de procesos de Django y Chromium, con RSS máximo agregado `≤ 1 GiB` y CPU promedio agregado `≤ 1 núcleo lógico`.
- CAP-6 adopta AD-4 y AD-11: Django 5.2.17 LTS sobre SQLite local y concurrencia optimista por `expected_case_version` dentro de una transacción.

### Resolved in story 1.2

- CAP-4 y CAP-5 adoptan el catálogo por acción de `domain-contracts.md`: aprobar (`requirements_met`, `evidence_consistent`), rechazar (`requirements_not_met`, `evidence_inconsistent`), solicitar antecedentes (`information_incomplete`, `evidence_unreadable`, `clarification_required`), corregir (`extraction_error`, `evidence_value_mismatch`) y `other` para todas con comentario obligatorio.


> Reconciliación 2026-10-04: runtime efectivo Django 5.2.17 aprobado por usuario en story 1.3 y plan de cierre; el historial original permanece en Git.

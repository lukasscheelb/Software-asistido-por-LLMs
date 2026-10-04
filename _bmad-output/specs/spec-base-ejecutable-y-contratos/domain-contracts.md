# Contratos de dominio compartidos

Este archivo fija el significado observable de los contratos y las decisiones técnicas de CAP-1.

| Concepto | Contrato observable |
|---|---|
| Caso | Unidad identificable que agrupa Versiones del caso, Evaluaciones e Intervenciones humanas. |
| Versión del caso | Revisión concreta sobre la que se evalúa o decide; una versión obsoleta no puede sobrescribir la vigente. |
| Política | Conjunto ordenado, configurable y versionado de reglas y parámetros. |
| Evaluación | Vincula una Versión del caso, una Versión de política, entradas simuladas, parámetros efectivos, Salida F4 y explicación. |
| Salida F4 | Uno de `ERROR / DERIVACIÓN`, `ESCALADO`, `APROBADO AUTOMÁTICAMENTE` o `REVISIÓN`. |
| Evidencia | PDF o imagen ficticia con una Ubicación del hallazgo comprensible. |
| Categoría de motivo | Código estable compatible con una acción humana, etiqueta visible en español y regla de comentario. |
| Intervención humana | Decisión humana o Corrección registrada sobre una Versión del caso, con autor y fecha controlada. |
| Corrección | Conserva valor original, valor corregido, motivo, autor, fecha y Versión del caso. |

## Catálogo inicial de Categorías de motivo

| Acción | Código | Etiqueta |
|---|---|---|
| Aprobar | `requirements_met` | Requisitos cumplidos |
| Aprobar | `evidence_consistent` | Evidencia consistente |
| Rechazar | `requirements_not_met` | Requisitos no cumplidos |
| Rechazar | `evidence_inconsistent` | Evidencia inconsistente |
| Solicitar antecedentes | `information_incomplete` | Antecedentes incompletos |
| Solicitar antecedentes | `evidence_unreadable` | Evidencia ilegible |
| Solicitar antecedentes | `clarification_required` | Aclaración requerida |
| Corregir | `extraction_error` | Error de extracción |
| Corregir | `evidence_value_mismatch` | Dato no coincide con la Evidencia |
| Todas | `other` | Otro |

Las categorías predefinidas admiten comentario opcional. `other` exige comentario no vacío después de eliminar espacios. Una categoría incompatible con la acción se rechaza como `invalid_input`.

## Invariantes

- Cambiar una Política no reescribe Evaluaciones previas.
- Una Intervención humana no borra entradas, Evidencia ni resultados anteriores.
- F1 consume la Salida F4 y su explicación sin recalcular la Política.
- `ERROR / DERIVACIÓN` se presenta inline en Resultado F4, conserva entradas y no crea una fila F1.
- Fixtures y tiempos de prueba son deterministas.
- Django persiste mediante repositorios sobre SQLite local; el dominio no depende del ORM.
- Toda Decisión o Corrección compara `expected_case_version` con la Versión vigente dentro de una transacción y responde `stale_version` sin escribir cuando difieren.

## Contrato de verificación CAP-1

- **Tecnología:** Python 3.13.16, Django 5.2.17 LTS, SQLite local y Playwright Python 1.63.0.
- **NFR-3:** apertura Bandeja → detalle con 100 Casos, 3 Evidencias por Caso, 2 vCPU/4 GiB, 5 calentamientos y 30 muestras; `p95 ≤ 2 s`.
- **PX-08:** 30 revisiones Playwright medidas con `psutil` sobre los árboles de procesos de Django y Chromium; RSS máximo agregado `≤ 1 GiB` y CPU promedio agregado `≤ 1 núcleo lógico`.
- **Decisión:** OQ-2, OQ-3 y OQ-4 cerradas el 2026-10-03 por sus responsables definidos en el PRD.


> Reconciliación 2026-10-04: runtime efectivo Django 5.2.17 aprobado por usuario en story 1.3 y plan de cierre; el historial original permanece en Git.


## DEC-E2-08 — Semántica efectiva de Discrepancia

El Operador declara desacuerdo explícito y explica el motivo en comentario. Una Corrección marca Discrepancia; aprobar o rechazar por sí solo no la implica. La marca no invalida la Decisión humana.

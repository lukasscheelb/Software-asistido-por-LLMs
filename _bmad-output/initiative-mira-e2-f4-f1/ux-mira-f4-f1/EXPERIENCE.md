---
name: MIRA F4 + F1
status: final
sources:
  - _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/prd-mira-f4-f1.md
  - _bmad-output/specs/spec-politica-f4-explicable/SPEC.md
  - _bmad-output/specs/spec-revision-f1-controlada/SPEC.md
updated: 2026-10-03
---

# MIRA F4 + F1 — Experience Spine

## Foundation

[ASSUMPTION] Aplicación web responsive en español, optimizada primero para laptop/escritorio y utilizable en tablet. No existe sistema UI confirmado; `DESIGN.md` gobierna la identidad visual y esta spine gobierna comportamiento. F4 y F1 comparten navegación, vocabulario y estados.

## Information Architecture

| Superficie | Acceso | Propósito |
|---|---|---|
| Bandeja | Inicio / navegación | Casos `REVISIÓN` y `ESCALADO`, prioridad, estado y plazos. |
| Ejecutar F4 | Navegación / `Corregir entradas` | Seleccionar un Caso controlado, revisar o editar un borrador transitorio de Puntaje y Señales, y ejecutar la Política versionada sin modificar el fixture. |
| Resultado F4 | Después de ejecutar | Salida, regla, razones, parámetros, acceso al Caso derivado cuando aplica y retorno al borrador cuando la entrada es inválida. |
| Detalle de Caso | Fila de Bandeja | Evidencia y hallazgos antes de Puntaje; historial y acciones humanas. |
| Decisión | Panel del detalle | Aprobar, rechazar o solicitar antecedentes con motivo obligatorio. |
| Corrección | Acción del detalle | Registrar original, corregido, motivo y procedencia. |

La Bandeja es el inicio operativo. Un resultado `REVISIÓN` o `ESCALADO` ofrece “Abrir en Bandeja”; `APROBADO AUTOMÁTICAMENTE` termina en el resultado. `ERROR / DERIVACIÓN` permanece inline en Resultado F4 como excepción y no crea una fila en Bandeja. `Corregir entradas` vuelve a Ejecutar F4 con el mismo Caso y borrador transitorio, conserva los valores y enfoca el primer campo inválido. Los cambios del borrador no modifican el fixture versionado; una nueva ejecución vuelve a validar y reemplaza el resultado inline.

## Voice and Tone

Microcopy neutral, directa y no persuasiva. La plataforma describe; el Operador decide.

| Usar | Evitar |
|---|---|
| `Requiere revisión humana.` | `Recomendamos rechazar.` |
| `Fraude detectado: Sí. Caso escalado.` | `Caso fraudulento.` |
| `La versión cambió. Recarga antes de decidir.` | `Error de concurrencia 409.` |
| `Selecciona una categoría de motivo.` | `Campo inválido.` |
| `La decisión vigente no fue modificada.` | `Operación fallida.` |

## Component Patterns

| Componente | Uso | Reglas de comportamiento |
|---|---|---|
| App shell | Global | Conserva navegación y nombre de superficie; una sola sección aparece activa. |
| Primary button | Formularios y acciones | Ejecuta una acción confirmable; se deshabilita solo con una explicación asociada. |
| Queue table | Bandeja | Fila completa abre detalle. Orden inicial: prioridad, vencimiento, ingreso. Encabezados permiten ordenar; filtros nunca ocultan su estado activo. |
| Status badge | Bandeja, resultado y detalle | Siempre combina texto y estado visual; `ESCALADO` se anuncia como revisión prioritaria. |
| Evidence panel | Detalle | PDF muestra página y campo/región; imagen muestra región y coordenadas cuando existen. Mantiene la ubicación al navegar Evidencia. |
| F4 explanation | Resultado y detalle | Orden fijo: Salida, razón principal, regla, parámetros efectivos y Señales. No recalcula. |
| Decision panel | Detalle | Acción segmentada o radio; selector limitado a categorías compatibles; `Otro` revela comentario obligatorio; confirmación resume el nuevo estado. Cambiar de acción limpia una categoría incompatible. |
| Correction dialog | Detalle | Original es solo lectura. Corregido y categoría son obligatorios. Confirmar no cambia la Decisión humana. |
| Deadline marker | Bandeja y detalle | Muestra fecha y estado: vigente, vence próximo día hábil o vencido. Vencimiento no cierra el Caso. |

## Reason Category Catalog

| Acción | Código estable | Etiqueta visible |
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

Las categorías predefinidas admiten comentario opcional. `other` exige un comentario no vacío después de eliminar espacios. El backend valida la compatibilidad entre acción y código; la UI no presenta combinaciones inválidas.

## State Patterns

| Estado | Superficie | Tratamiento |
|---|---|---|
| Cargando | Bandeja / detalle | Skeleton con dimensiones estables y etiqueta accesible `Cargando`. |
| Caso no seleccionado | Ejecutar F4 | Selector de Caso controlado y resumen del corpus; ejecutar permanece inactivo con instrucción asociada. |
| Ejecutando Política | Ejecutar F4 | Conserva el Caso visible, bloquea una segunda ejecución y anuncia progreso sin temporizador. |
| Entrada inválida | Ejecutar F4 / resultado | Identifica el campo o Señal, conserva los valores y produce `ERROR / DERIVACIÓN`. |
| Bandeja vacía | Bandeja | `No hay Casos pendientes.` Sin acción inventada. |
| `REVISIÓN` | Resultado / Bandeja | Prioridad normal y razón principal. |
| `ESCALADO` | Resultado / Bandeja | Prioridad alta, marca para supervisor y texto `Revisión prioritaria`. |
| `APROBADO AUTOMÁTICAMENTE` | Resultado | Resultado final del piloto; no ofrece Decisión F1. |
| `ERROR / DERIVACIÓN` | Resultado F4 inline | Conserva Caso y borrador transitorio, identifica campo o Señal, muestra causa y formato o rango esperado, y ofrece `Corregir entradas`; no crea Decisión ni fila F1. |
| Versión obsoleta | Decisión / Corrección | Bloquea confirmación, conserva la Decisión vigente y ofrece `Recargar Caso`. |
| Guardado fallido | Decisión / Corrección | Mantiene datos introducidos, muestra causa comprensible y permite reintentar. |
| Vencido | Bandeja / detalle | Sigue abierto, eleva prioridad contractual y conserva marca para supervisor. |

## Interaction Primitives

- `Tab` recorre controles en orden de lectura; `Enter` activa el control enfocado; `Esc` cierra un único diálogo sin guardar.
- Filas de Bandeja se abren con clic o `Enter`. No hay acciones solo por hover.
- Confirmaciones destructivas o adversas nombran Caso, acción y motivo antes de ejecutar.
- El foco vuelve al disparador al cerrar diálogo y pasa al mensaje de conflicto cuando una versión queda obsoleta.
- Cambiar filtro, orden o página conserva contexto al volver desde el detalle.
- No usar drag-and-drop, infinite scroll, temporizadores visuales ni animaciones celebratorias.

## Accessibility Floor

- WCAG 2.2 AA para la superficie responsive.
- Estados, prioridades y vencimientos incluyen texto; nunca dependen solo de los tokens de color de `DESIGN.md`.
- Foco visible con `{components.focus-ring}` y objetivos interactivos de al menos 44 × 44 px.
- Tabla expone encabezados, orden actual y conteo de resultados; en móvil se transforma en lista semántica, no en tabla recortada.
- Mensajes de validación se asocian al campo y el resumen recibe foco al confirmar.
- El orden del DOM mantiene Evidencia y razones antes de Puntaje, igual que el orden visual.

## Responsive & Platform

| Ancho | Comportamiento |
|---|---|
| `≥ 1100 px` | Navegación fija; Bandeja en tabla; detalle en dos columnas con Evidencia dominante y acciones laterales. |
| `768–1099 px` | Navegación compacta; tabla reduce columnas secundarias; detalle apila acciones bajo Evidencia. |
| `< 768 px` | Navegación en menú; Bandeja como lista de filas apiladas; acciones a ancho completo y sin paneles paralelos. |

La demo primaria es laptop/escritorio. Móvil permite consultar y decidir sin pérdida funcional, pero no optimiza densidad de supervisión.

## Key Flows

### UJ-4 — Sebastián valida la política y el recorrido F4 → F1

1. Sebastián abre `Ejecutar F4` y selecciona CC-F4-02.
2. Ejecuta la Política versionada.
3. Resultado F4 muestra `REVISIÓN`, razón, regla y parámetros efectivos.
4. Selecciona `Abrir en Bandeja`.
5. El Caso aparece con prioridad normal y ambos plazos.
6. Abre el detalle y encuentra Evidencia y ubicación antes del Puntaje.
7. **Clímax:** registra `Solicitar antecedentes` con Categoría de motivo y ve el estado `ESPERANDO ANTECEDENTES`, con procedencia intacta.

Fallo: una entrada inválida produce `ERROR / DERIVACIÓN`, explica el campo y no crea un Caso F1. Sebastián selecciona `Corregir entradas`, vuelve al mismo borrador con foco en el primer campo inválido, corrige y reejecuta sin alterar el fixture versionado.

### UJ-1 — Marco resuelve un caso en revisión con la evidencia a la vista

1. Marco abre la Bandeja y encuentra un `ESCALADO` arriba, con marca para supervisor.
2. Abre el Caso y revisa Evidencia, razón y ubicación.
3. Consulta Puntaje y Señales después de entender el hallazgo.
4. Elige una acción humana y una Categoría de motivo.
5. Revisa el resumen de confirmación.
6. **Clímax:** confirma y ve la Decisión humana registrada sin que `ESCALADO` se haya tratado como rechazo automático.

Fallo: sin categoría, la confirmación permanece deshabilitada y el campo explica qué falta.

### UJ-2 — Marco corrige un dato sin borrar el original

1. Marco abre una Corrección y ve `120000` como valor original.
2. Introduce `100000`, selecciona motivo y revisa la comparación.
3. Confirma la Corrección.
4. El detalle vuelve a mostrar el valor original, el corregido, autor, fecha y Versión del caso.
5. **Clímax:** la Discrepancia queda visible sin alterar la Decisión humana ni la Evidencia original.

Fallo: si falta categoría, el formulario conserva los valores y explica el requisito pendiente.

### UJ-3 — Marco recibe una advertencia de concurrencia

1. Marco abre un Caso y prepara una Decisión o Corrección.
2. Otro proceso crea una nueva Versión del caso.
3. Marco confirma sobre la versión anterior.
4. La aplicación bloquea la intervención y ofrece `Recargar Caso`.
5. Marco recarga y revisa la Versión vigente.
6. **Clímax:** la Decisión vigente permanece intacta y Marco puede rehacer la acción sobre la versión actual.

Fallo: si la recarga no está disponible, los datos introducidos se conservan localmente sin habilitar la confirmación.

## Open Questions

- Confirmar identidad de marca, tipografía o modo oscuro antes de sustituir los supuestos visuales de `DESIGN.md`.


## Actualización propuesta del 17 de octubre de 2026

Existe un delta de UX pendiente de aprobación en `_bmad-output/planning-artifacts/ux-designs/ux-mira-mejora-frontend-2026-10-17/PROPUESTA-UX.md`, con borradores DESIGN y EXPERIENCE. Este contrato conserva su vigencia hasta la aprobación y reconciliación del delta.


## Delta aprobado e implementado del 17 de octubre de 2026

La propuesta enlazada anteriormente fue aprobada explícitamente. Para la presentación vigente prevalecen DESIGN.md y EXPERIENCE.md de `ux-mira-mejora-frontend-2026-10-17`; el contrato histórico conserva las reglas no modificadas. Los patrones aspiracionales históricos no cubiertos por el delta no se declaran implementados.

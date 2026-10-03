# Flujos y Casos controlados F1

## Enrutamiento y presentación

- `REVISIÓN` entra con prioridad normal.
- `ESCALADO` entra con prioridad alta y marca para supervisor.
- `APROBADO AUTOMÁTICAMENTE` no entra en la Bandeja.
- La lista muestra identificador, Salida F4, razón principal, prioridad, estado, Plazo interno y Plazo contractual.
- El detalle ordena Evidencia, razón y Ubicación del hallazgo antes de Puntaje y Señales.

## Intervención humana

- Aprobar cambia el estado a `APROBADO`.
- Rechazar cambia el estado a `RECHAZADO` y solo puede ser una Decisión humana.
- Solicitar antecedentes cambia el estado a `ESPERANDO ANTECEDENTES`.
- Toda Decisión y Corrección exige Categoría de motivo; `Otro` exige comentario.
- Una Corrección conserva original, corregido, motivo, Operador, fecha controlada y Versión del caso.
- Una Discrepancia marca la diferencia con la sugerencia sin alterar la Decisión humana.
- Una intervención sobre una versión obsoleta se rechaza sin sobrescribir la vigente.

## Plazos

- Plazo interno: `3` días hábiles desde el ingreso controlado.
- Plazo contractual: `5` días hábiles desde el ingreso controlado.
- Calendario: lunes a viernes en `America/Santiago`.
- Alerta: un día hábil antes y al vencer cada plazo.
- El vencimiento contractual mantiene el Caso abierto, eleva prioridad y conserva la marca para supervisor.

## Matriz PF-05 / PF-14

| ID | Escenario | Resultado esperado |
|---|---|---|
| CC-F1-01 | Corrección `120000 → 100000` | Conserva ambos valores y el motivo. |
| CC-F1-02 | Rechazo sin Categoría de motivo | Bloquea la confirmación. |
| CC-F1-03 | Solicitud de antecedentes con motivo | Cambia a `ESPERANDO ANTECEDENTES`. |
| CC-F1-04 | Decisión sobre Versión obsoleta | Rechaza el intento y conserva la vigente. |
| CC-F1-05 | Próximo al Plazo interno | Alerta un día hábil antes. |
| CC-F1-06 | Plazo contractual vencido | Sigue abierto, eleva prioridad y mantiene marca. |

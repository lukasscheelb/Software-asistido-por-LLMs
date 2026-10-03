# Política y Casos controlados F4

## Orden de evaluación

1. Un Puntaje no numérico o fuera de `[0,100]`, o una Señal numérica presente fuera de rango, produce un error identificable como `ERROR / DERIVACIÓN`.
2. Fraude detectado o Puntaje menor que `60` produce `ESCALADO`.
3. `APROBADO AUTOMÁTICAMENTE` exige automatización `ON`, Puntaje mayor que `90`, Autenticidad al menos `70`, Coherencia al menos `70` y ausencia de fraude.
4. Todo Caso válido restante produce `REVISIÓN`; una Señal requerida ausente nunca cuenta como favorable.

## Matriz PF-04

| ID | Puntaje | Autenticidad | Coherencia | Fraude | Auto | Resultado esperado |
|---|---:|---:|---:|---|---|---|
| CC-F4-01 | 59,99 | 80 | 80 | No | ON | `ESCALADO` |
| CC-F4-02 | 60 | 80 | 80 | No | ON | `REVISIÓN` |
| CC-F4-03 | 90 | 80 | 80 | No | ON | `REVISIÓN` |
| CC-F4-04 | 90,01 | 70 | 70 | No | ON | `APROBADO AUTOMÁTICAMENTE` |
| CC-F4-05 | 95 | 90 | 90 | Sí | ON | `ESCALADO` |
| CC-F4-06 | 95 | 69,99 | 90 | No | ON | `REVISIÓN` |
| CC-F4-07 | 95 | Ausente | 90 | No | ON | `REVISIÓN` |
| CC-F4-08 | 95 | 90 | 90 | No | OFF | `REVISIÓN` |
| CC-F4-09 | 101 | 90 | 90 | No | ON | `ERROR / DERIVACIÓN` |

Cada Evaluación conserva Caso, Versión del caso, entradas recibidas, Versión de política, parámetros efectivos, regla aplicada, razones y Salida F4.

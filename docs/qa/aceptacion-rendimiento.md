# Aceptación del rendimiento observado — MIRA, Entrega 2

## Objeto y evidencia

Se registra la aceptación por parte del cliente del rendimiento actual de la implementación, sin observaciones.

La evidencia técnica es [measurements.json](measurements.json), registrada sobre la revisión `ab745aff3347e6c68e6e7976c474bf1aee049a1a`. La versión actual de referencia es `v2.0-rc1`, commit `0ccb92f0ffae7ca6b1ad4af4f1d19263a0437327`.

## Resultados considerados

| Indicador | Resultado observado | Umbral de referencia | Evaluación técnica |
|---|---|---|---|
| Latencia p95 | 0,5228 segundos | ≤ 2 segundos | Cumple en el entorno medido. |
| Memoria RSS máxima | 837.009.408 bytes (798,2 MiB) | ≤ 1 GiB | Cumple en el entorno medido. |
| CPU promedio | 1,3237 núcleos | ≤ 1 núcleo | Supera el umbral aproximadamente un 32,4 %. Desviación aceptada por el cliente. |

La medición incluye 30 muestras de latencia, cinco calentamientos y 84 muestras de recursos; el conjunto de datos contiene 100 casos con tres evidencias por caso. El cómputo de recursos incluye Django y los árboles de procesos de Playwright/Chromium, según el registro técnico.

## Decisión del cliente

El cliente acepta el resultado de rendimiento actual sin problemas y considera aceptable la implementación presentada, incluida la desviación observada de CPU. Esta aceptación se registra como una excepción al umbral de CPU. Los umbrales originales y las mediciones se conservan para mantener la trazabilidad.

El fundamento de la aceptación es la conformidad del cliente con el resultado actual, junto con el cumplimiento observado de los umbrales de latencia y memoria.

## Entorno y alcance de la conclusión

El registro identifica Windows, Python 3.13.16, 12 procesadores lógicos y 34.224.758.784 bytes de RAM del equipo anfitrión.

## Conclusiones

- La latencia y la memoria cumplen sus umbrales en el entorno medido.
- El cliente acepta expresamente la desviación de CPU y el rendimiento actual sin observaciones.
- No se modifican los resultados originales ni se presenta una nueva medición.

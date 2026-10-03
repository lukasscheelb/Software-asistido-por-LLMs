# Addendum: asuntos diferidos del producto completo

Este addendum conserva decisiones y tensiones relevantes para trabajos posteriores sin ampliar el alcance del incremento F4 + F1.

## Decisiones técnicas resueltas en arquitectura

- **OQ-4 (2026-10-03):** Python 3.13.16, Django 5.2.18 LTS, SQLite local y Playwright Python 1.63.0; concurrencia optimista por `expected_case_version` dentro de una transacción.
- **OQ-2 (2026-10-03):** apertura Bandeja → detalle con 100 Casos, 3 Evidencias por Caso, 2 vCPU/4 GiB, 5 calentamientos y 30 muestras; `p95 ≤ 2 s`.
- **OQ-3 (2026-10-03):** 30 revisiones Playwright medidas con `psutil` sobre los árboles de procesos de Django y Chromium; RSS máximo agregado `≤ 1 GiB` y CPU promedio agregado `≤ 1 núcleo lógico`.

## Decisiones técnicas diferidas

- Forma de representar la marca para supervisor sin construir su panel agregado.

## Tensiones del producto completo fuera del incremento

- **Retención de Evidencia:** la descripción menciona `90` días, mientras cumplimiento plantea plazos de `5` a `10` años. Requiere decisión legal y de producto.
- **Residencia y transferencia de datos:** el contrato del piloto exige datos en Chile, pero algunos proveedores externos pueden procesar fuera del país.
- **Gobierno de umbrales:** cumplimiento propone doble aprobación para cambios de apetito de riesgo; la interfaz de gestión corresponde a F5.
- **Facturación:** no existe una definición acordada de qué procesamiento constituye una validación cobrable.
- **Cierre por falta de antecedentes:** el estado existe en DEC-08, pero sus reglas y plazos no están cerrados para este incremento.

## Alternativas no adoptadas

- Implementar una fórmula de scoring: descartado porque Entrega 2 entrega Puntaje y componentes simulados.
- Rechazar automáticamente Puntajes bajos: descartado por control humano y DEC-01.
- Incorporar el panel del supervisor: diferido para evitar convertir la marca de escalamiento en una tercera funcionalidad.
- Incluir administración visual de umbrales: diferido a F5; F4 consume una Política configurable por datos de prueba.

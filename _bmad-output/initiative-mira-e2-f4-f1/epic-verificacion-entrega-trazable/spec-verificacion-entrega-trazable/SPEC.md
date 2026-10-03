---
id: SPEC-verificacion-entrega-trazable
companions: [verification-matrix.md]
sources:
  - _bmad-output/initiative-mira-e2-f4-f1/epic-verificacion-entrega-trazable/epic-verificacion-entrega-trazable.md
  - _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/prd-mira-f4-f1.md
---

> **Canonical contract.** Este SPEC y los archivos en `companions:` son el contrato completo y validado para construir, probar y revisar esta épica.

# Verificación y entrega trazable

## Why

El incremento solo es entregable si otra persona puede reproducirlo, demostrarlo y auditarlo sin depender del entorno del equipo. La evidencia debe separar resultados esperados de comportamiento accidental y mantener cada requisito Must conectado con su implementación.

## Capabilities

- **CAP-1**
  - **intent:** QA puede ejecutar el catálogo ficticio completo con resultados esperados independientes de la implementación.
  - **success:** CC-F4-01 a CC-F4-09 y CC-F1-01 a CC-F1-06 cubren fronteras, errores, decisiones, concurrencia y plazos.
- **CAP-2**
  - **intent:** Un evaluador puede rastrear cada requisito Must hasta artefacto BMAD, historia, código, prueba y commit.
  - **success:** Cada ruta y referencia citada existe y permite reconstruir el cambio.
- **CAP-3**
  - **intent:** Una persona externa puede levantar y demostrar F4 → F1 desde un clon limpio siguiendo solo el README.
  - **success:** Llega a la demo con datos cargados en menos de `15` minutos.
- **CAP-4**
  - **intent:** Una persona externa puede completar una tarea F4 y una F1 sin instrucciones previas.
  - **success:** PX-05 registra finalización, tiempo y dificultades, y confirma Evidencia y razones antes del Puntaje.
- **CAP-5**
  - **intent:** QA puede ejecutar PX-09, p95 y PX-08 sobre corpus y entorno acordados.
  - **success:** Cada informe registra configuración, datos, resultado y veredicto; PX-09 fallido impide ampliar automatización.
- **CAP-6**
  - **intent:** Sebastián puede aceptar o rechazar F4 y F1 contra criterios registrados.
  - **success:** Existe un acta fechada con resultado y observaciones por funcionalidad.
- **CAP-7**
  - **intent:** La versión candidata puede ejecutar una suite E2E integrada F4 → F1.
  - **success:** La suite cubre aprobación, revisión, escalamiento, Corrección, conflicto de versión y vencimiento desde la interfaz.

## Constraints

- Las pruebas usan Evidencia ficticia, fixtures estables y fechas controladas.
- La automatización permanece limitada a la Política y corpus del piloto si PX-09 falla.
- Los resultados esperados se derivan de PF/PX y los Casos controlados, no del código implementado.
- Entrega integrada significa versión candidata ejecutable desde un clon limpio; no incluye despliegue productivo.

## Non-goals

- Añadir funcionalidad, ampliar automatización o resolver alcance productivo diferido.
- Medir casos resueltos por hora como objetivo de éxito.
- Sustituir la aceptación de Sebastián por una métrica automática.

## Success signal

Un evaluador externo clona, ejecuta y demuestra el recorrido F4 → F1 en menos de `15` minutos, mientras todos los Must conservan evidencia verificable hasta commit.

## Open Questions

- ¿Qué interacción, volumen y entorno se usarán para p95? Debe provenir de la historia HITL 1.1 antes de ejecutar CAP-5.
- ¿Qué métrica, herramienta y umbral se usarán para PX-08? Debe provenir de la historia HITL 1.1 antes de ejecutar CAP-5.

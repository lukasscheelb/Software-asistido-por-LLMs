---
id: SPEC-base-ejecutable-y-contratos
companions: [domain-contracts.md]
sources:
  - _bmad-output/initiative-mira-e2-f4-f1/epic-base-ejecutable-y-contratos/epic-base-ejecutable-y-contratos.md
  - _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/prd-mira-f4-f1.md
  - _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/addendum.md
---

> **Canonical contract.** Este SPEC y los archivos en `companions:` son el contrato completo y validado para construir, probar y revisar esta épica.

# Base ejecutable y contratos compartidos

## Why

F4, F1 y QA necesitan una base común antes de avanzar en paralelo. Sin decisiones técnicas, flujo UX, contratos y fixtures compartidos, cada épica podría crear formatos incompatibles y la demo dejaría de ser reproducible.

## Capabilities

- **CAP-1**
  - **intent:** Arquitectura, QA y Sebastián pueden fijar stack, persistencia, concurrencia, escenario p95 y criterio PX-08 para todo el incremento.
  - **success:** Las decisiones están fechadas, tienen responsable y pueden citarse desde F4, F1 y verificación.
- **CAP-2**
  - **intent:** UX, PM y Sebastián pueden fijar navegación, presentación de `ERROR / DERIVACIÓN` y catálogo inicial de motivos.
  - **success:** El tracer define pantallas, estados, acciones y validaciones sin decisiones visuales pendientes que bloqueen su implementación.
- **CAP-3**
  - **intent:** El equipo puede iniciar una aplicación web en español y su harness automatizado desde un clon limpio.
  - **success:** La pantalla inicial abre y una prueba base termina correctamente con los comandos documentados.
- **CAP-4**
  - **intent:** F4, F1 y QA comparten contratos trazables para Caso, Política, Evaluación, Salida F4, Evidencia e Intervención humana.
  - **success:** Un Caso versionado conserva la Política, las entradas y el resultado que lo originaron según `domain-contracts.md`.
- **CAP-5**
  - **intent:** El equipo puede cargar fixtures ficticios y deterministas para CC-F4-02 y el tracer F4 → F1.
  - **success:** Los mismos fixtures se repiten sin secretos y el Caso controlado aparece en la interfaz.

## Constraints

- La solución no calcula scoring ni define una fórmula; consume Puntaje y Señales simulados.
- Los datos y Evidencias son ficticios y el repositorio no contiene secretos.
- Las decisiones OQ-1 a OQ-5 se registran antes de implementar las historias que dependen de ellas.
- La entrega integrada es una versión candidata ejecutable desde un clon limpio; no incluye despliegue productivo.

## Non-goals

- Implementar todas las reglas F4 o los flujos completos F1.
- Definir autenticación, multitenencia, facturación, residencia o retención productiva.
- Elegir una fórmula de scoring o procesar archivos reales.

## Success signal

Un clon limpio inicia la aplicación y las pruebas; CC-F4-02 atraviesa contratos compartidos y llega a un stub visible de F1 con datos ficticios y trazables.

## Open Questions

- ¿Qué catálogo inicial de motivos y qué superficie visual se usarán para `ERROR / DERIVACIÓN`? Responsable: PM, UX y Sebastián; historias 1.2 y posteriores.
- ¿Qué interacción, volumen y entorno definen el p95? Responsable: Arquitectura y Sebastián; historia 1.1.
- ¿Qué métrica, herramienta y umbral definen PX-08? Responsable: QA y Arquitectura; historia 1.1.
- ¿Qué stack, persistencia y mecanismo de concurrencia implementarán los contratos? Responsable: Arquitectura; historia 1.1.

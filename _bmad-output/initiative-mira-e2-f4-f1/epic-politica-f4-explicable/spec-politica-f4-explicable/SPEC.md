---
id: SPEC-politica-f4-explicable
companions: [policy-cases.md]
sources:
  - _bmad-output/initiative-mira-e2-f4-f1/epic-politica-f4-explicable/epic-politica-f4-explicable.md
  - _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/prd-mira-f4-f1.md
---

> **Canonical contract.** Este SPEC y los archivos en `companions:` son el contrato completo y validado para construir, probar y revisar esta épica.

# Política F4 explicable

## Why

El piloto necesita demostrar decisiones automáticas acotadas, reproducibles y auditables sin convertir una señal simulada en una decisión adversa. La precedencia exacta y la explicación son el control que permite usar F4 y entregar su resultado a F1.

## Capabilities

- **CAP-1**
  - **intent:** F4 valida Puntaje y Señales antes de decidir.
  - **success:** Entradas inválidas producen `ERROR / DERIVACIÓN` y una ausencia nunca favorece una aprobación.
- **CAP-2**
  - **intent:** F4 aplica fraude y Puntaje menor que `60` con precedencia.
  - **success:** Ambos casos producen `ESCALADO` y nunca rechazo o cierre automático.
- **CAP-3**
  - **intent:** F4 aprueba automáticamente solo cuando se cumplen todas las barreras configuradas.
  - **success:** Automatización `ON`, Puntaje mayor que `90`, ambas Señales al menos `70` y ausencia de fraude son necesarias y suficientes.
- **CAP-4**
  - **intent:** F4 deriva a `REVISIÓN` todo Caso válido no capturado por una regla anterior.
  - **success:** Puntajes de `60` a `90`, barreras insuficientes, Señales ausentes y automatización `OFF` producen `REVISIÓN` cuando no corresponde escalar.
- **CAP-5**
  - **intent:** Cada Evaluación usa una Política identificada y conserva su versión y parámetros efectivos.
  - **success:** Dos versiones pueden evaluarse sin reescribir resultados previos.
- **CAP-6**
  - **intent:** Cada Salida F4 conserva una explicación y procedencia consumibles por F1.
  - **success:** La interfaz y F1 muestran regla, valores y razones sin recalcular la Evaluación.
- **CAP-7**
  - **intent:** Un evaluador puede ejecutar por interfaz el corpus F4 controlado.
  - **success:** CC-F4-01 a CC-F4-09 producen exactamente las salidas de `policy-cases.md` y cubren las cuatro clases de resultado.

## Constraints

- La precedencia es validar, fraude, Puntaje bajo, barreras de aprobación y fallback a revisión.
- Nunca existe rechazo automático; `ESCALADO` es revisión humana prioritaria.
- `T=90` y mínimos `70/100` son parámetros versionados del piloto, no constantes definitivas del producto.
- El motor multimodal se simula; F4 no calcula Puntaje ni infiere sobre archivos reales.
- La automatización no se amplía fuera del corpus y Política del piloto antes de PX-09 exitoso.

## Non-goals

- Calcular Puntaje, entrenar modelos o administrar umbrales desde F5.
- Implementar decisiones humanas F1.
- Establecer una tasa objetivo de aprobación automática.

## Success signal

La matriz completa PF-04 pasa con resultados deterministas, ninguna ruta rechaza automáticamente y cada resultado puede reconstruirse desde su Caso y Versión de política.

## Resolved Input

- **Story 1.2:** `ERROR / DERIVACIÓN` se muestra inline en Resultado F4, conserva las entradas, identifica campo y causa y no crea una fila F1. `Corregir entradas` vuelve al mismo borrador transitorio, enfoca el primer campo inválido y permite reejecutar sin modificar el fixture versionado.

# Validación de épicas e historias MIRA F4 + F1

Fecha: 2026-10-03  
Workflow: `bmad-preview-ticketing`, reemplazo oficial de `bmad-create-epics-and-stories` en BMAD v7.  
Fuente: PRD 1.0 y addendum copiados en `prd-mira-f4-f1/`.

## Resultado

- Estado: aprobado para revisión humana antes de publicar.
- Estructura: 1 iniciativa, 4 épicas y 33 historias planificadas.
- Distribución: 6 historias de base, 9 de F4, 10 de F1 y 8 de verificación.
- Cobertura: FR-1 a FR-20 y NFR-1 a NFR-6, sin IDs faltantes ni desconocidos.
- Dependencias: grafo resoluble, sin ciclos detectados y `unpinned_after = 0`.
- Ownership: cada requisito declarado por una épica tiene al menos una historia responsable.
- Refactor: cada épica con más de tres historias contiene un `Refactor sweep` previo a su E2E final.
- Árbol: no existen historias directamente bajo la iniciativa.
- Fuentes: las copias de PRD y addendum coinciden por SHA-256 con sus originales.

## Revisión aplicada

1. Se asignó `FR-17` a las épicas F4 y F1 donde se conserva procedencia.
2. Se asignó `FR-19` a los recorridos E2E de F4 y F1.
3. Se asignaron `NFR-3` y `NFR-4` a la historia 3.2 para habilitar las mediciones de Bandeja.
4. El tracer F4 usa la regla real de fallback a REVISIÓN y no una implementación temporal.
5. Los elementos de riesgo alto nombran una comprobación externa adicional.
6. Se documentó que entrega integrada significa versión candidata ejecutable desde un clon limpio; el despliegue productivo permanece fuera de alcance.
7. Se documentaron las ramas paralelas 4.2, 4.3 y 4.5 con ownership de artefactos separado.

## Preguntas abiertas asignadas

- Historia 1.1, HITL: stack, persistencia, concurrencia, escenario p95 y métrica/umbral PX-08.
- Historia 1.2, HITL: catálogo de categorías y presentación de ERROR / DERIVACIÓN.

Estas preguntas no se resolvieron por inferencia. Las historias dependientes están bloqueadas por 1.1 o 1.2 según corresponda.

## Evidencia de validación

El comando `tickets.py status` reconoció las 33 historias como `planned`, generó una cadena restante válida y reportó cero referencias `after` sin fijar. Un control estructurado adicional comprobó campos obligatorios, riesgos, referencias, cobertura global y por épica, sweeps de refactor y copias de fuentes con resultado `ERRORS=0`.

La revisión independiente mediante subagentes no estaba disponible en este entorno; se realizó revisión manual completa más controles deterministas locales.

## Publicación

Los tickets permanecen sin commit. En el store repo de BMAD, el commit de estos archivos constituye la publicación y requiere aprobación explícita.

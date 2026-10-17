---
name: MIRA front-end F4 y F1
status: final
updated: 2026-10-17
sources:
  - PROPUESTA-UX.md
  - ../../../implementation-artifacts/frontend-mira-2026-10-17/HISTORIAS.md
---

# Experiencia del incremento de UX

## Foundation

Aplicación local Django en español con datos ficticios. DESIGN.md de esta carpeta define la identidad; ARCHITECTURE-SPINE.md e HISTORIAS.md del incremento definen límites y criterios. No se implementan automáticamente todos los patrones aspiracionales de los contratos históricos.

## Information Architecture

F1 - Revisión humana asistida es la bandeja. F4 - Evaluación automática de casos permite seleccionar y evaluar. El resultado derivado abre detalle: evidencia → explicación y señales → decisión → corrección → historial. Se conservan rutas y enlaces existentes.

## Voice and Tone

Instrucciones breves y neutrales. «Evaluar caso», «Abrir evidencia» y «Revisa los datos antes de continuar». Los datos son ficticios y la identidad del operador es declarada.

## Component Patterns

Navegación con estado activo también en móvil. Tabla con encabezados conservados en el árbol accesible y filas apiladas en móvil. Evidencia con alternativa al visor. Formularios de decisión y corrección separados. Los errores del servidor se muestran en resumen asociado al control correspondiente; JavaScript mejora foco y asociaciones sin interceptar envíos.

## State Patterns

Resultado inicial, aprobación automática, revisión, escalado, entrada inválida, sin coincidencias, sin pendientes, decisión guardada, corrección guardada y conflicto conservan sus reglas. La aprobación es verde; rechazo rojo; antecedentes ámbar. Un resultado automático no habilita revisión si las reglas existentes no lo permiten.

## Interaction Primitives

Tab y Shift+Tab recorren controles; skip link enfoca el contenido. Tras error se enfoca el resumen después de restaurar fragmentos; sus enlaces enfocan campos. Texto, operador y discrepancia se conservan al rechazar un envío. No se bloquean reintentos ni se introducen modales.

## Accessibility Floor

Foco visible de {components.focus-ring.width} en controles, incluido textarea; objetivos principales de 44 px; estados con texto. Encabezados y roles de tabla explícitos; objetos PDF con título; imágenes con contexto. Verificaciones específicas registradas en QA, sin afirmar certificación WCAG o una nueva prueba humana.

## Responsive & Platform

Se verificaron las tres pantallas a 320, 360, 390, 768 y 1366 px sin desbordamiento global. Móvil muestra evidencia antes de acciones. PDF incrustado puede depender del navegador; el enlace al archivo permanece disponible.

## Key Flows

1. Operador de prueba evalúa los nueve casos F4, comprueba salida/razón y corrige el borrador inválido. Resultado: nueva evaluación válida sin alterar fixture original.
2. Operador abre un caso F1, consulta PDF/PNG y solicita antecedentes con categoría compatible. Resultado: estado esperado e historial.
3. Operador corrige importe de 120000 a 100000. Resultado: original conservado y decisión sin cambio.
4. Dos sesiones intentan decidir sobre la misma versión. Resultado: segunda intervención bloqueada; primera conservada.
5. Operador envía motivo Otro sin comentario o importe negativo. Resultado: resumen enfocado, campo identificado y valores conservados; puede corregir y continuar.

Estos recorridos fueron ejecutados en navegador con base de pruebas aislada; no representan sesiones nuevas con participantes humanos.

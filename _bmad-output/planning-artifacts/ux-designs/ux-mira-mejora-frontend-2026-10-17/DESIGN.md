---
name: MIRA front-end F4 y F1
status: final
updated: 2026-10-17
colors:
  surface-base: '#f4f7f8'
  surface-raised: '#ffffff'
  surface-subtle: '#eef3f4'
  ink-primary: '#14242b'
  ink-secondary: '#465b65'
  border: '#cbd7db'
  border-strong: '#788b95'
  action: '#006b5b'
  action-hover: '#005449'
  focus: '#1d4ed8'
  approved-bg: '#dcfce7'
  approved-ink: '#166534'
  review-bg: '#fff4cc'
  review-ink: '#76530a'
  escalated-bg: '#ffe5e5'
  escalated-ink: '#9a2525'
  error-bg: '#eee9ff'
  error-ink: '#5b36a8'
typography:
  body:
    fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif'
    fontSize: 16px
    lineHeight: '1.5'
  label:
    fontSize: 14px
rounded:
  sm: 4px
  md: 6px
  lg: 8px
spacing:
  base: 4px
components:
  primary-button:
    background: '{colors.action}'
    foreground: '#FFFFFF'
  focus-ring:
    color: '{colors.focus}'
    width: 3px
---

## Brand & Style

Interfaz operativa sobria, en español. Se conserva la identidad existente. Diseño aprobado por el usuario el 17 de octubre de 2026, implementado localmente sin commit ni push.

## Colors

Acciones usan {colors.action}; fondo {colors.surface-base}; paneles {colors.surface-raised}; texto principal {colors.ink-primary}. Los estados llevan etiqueta y color: verde aprobado, ámbar revisión/antecedentes, rojo escalado/rechazo y violeta error. Escalar no implica rechazar. Contraste medido de pares principales en el registro QA; no equivale a auditoría integral.

## Typography

Cuerpo de 16 px, etiquetas de formulario de 14 px, títulos adaptables de 25–32 px y metadatos de 12–13 px. Nombres completos con salto de línea y sin insignias de tamaño fijo. Sin descarga de fuentes.

## Layout & Spacing

Navegación de escritorio y menú móvil bajo 768 px. F4 pasa a una columna bajo 1100 px y detalle bajo 1200 px. Tabla con ocho columnas y desplazamiento local cuando falta espacio; datos apilados bajo 768 px. Espaciado de 4 px como base. Evidencia precede puntaje y acciones en lectura.

## Elevation & Depth

Jerarquía mediante bordes, fondo y espaciado; sombra solo en menú superpuesto.

## Shapes

Radios de 4, 6 y 8 px; controles principales de 44 px de alto. Radios y casillas de 20 px con etiqueta asociada y área suficiente.

## Components

- Navegación: nombres F4 - Evaluación automática de casos y F1 - Revisión humana asistida; sección activa visible y `aria-current`.
- Evaluación: selección, acción Evaluar caso y resultado legible; estado vacío con símbolo neutro y explicación.
- Bandeja: prioridad, estado, motivo, plazos y Abrir; sin ordenación nueva.
- Evidencia: nombre, archivo, ubicación, hallazgo y alternativa al visor PDF.
- Decisión y corrección: grupos separados, motivos existentes y checkbox propio.
- Errores: borde y resumen rojo con foco, enlaces a campos y atributos ARIA.
- Historial: secciones delimitadas por borde con información existente.

## Do's and Don'ts

Mantener etiquetas textuales y evidencia primero. No colocar nombres largos en cuadrados pequeños, usar verde para todos los estados ni alterar los datos originales para adaptar la presentación.

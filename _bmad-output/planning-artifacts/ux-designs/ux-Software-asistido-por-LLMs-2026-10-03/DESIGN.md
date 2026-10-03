---
name: MIRA F4 + F1
description: Interfaz operativa en español para evaluación explicable y revisión humana con Evidencia primero.
status: final
sources:
  - _bmad-output/initiative-mira-e2-f4-f1/prd-mira-f4-f1/prd-mira-f4-f1.md
  - _bmad-output/specs/spec-politica-f4-explicable/SPEC.md
  - _bmad-output/specs/spec-revision-f1-controlada/SPEC.md
updated: 2026-10-03
colors:
  surface-base: '#F6F8FA'
  surface-raised: '#FFFFFF'
  surface-subtle: '#EEF2F5'
  ink-primary: '#17212B'
  ink-secondary: '#52606D'
  ink-disabled: '#8A96A3'
  border: '#CBD5DF'
  action: '#075E54'
  on-action: '#FFFFFF'
  focus: '#1D4ED8'
  approved-bg: '#DCFCE7'
  approved-ink: '#166534'
  review-bg: '#FEF3C7'
  review-ink: '#854D0E'
  escalated-bg: '#FEE2E2'
  escalated-ink: '#991B1B'
  error-bg: '#EDE9FE'
  error-ink: '#5B21B6'
typography:
  page-title:
    fontFamily: 'system-ui, sans-serif'
    fontSize: 24px
    fontWeight: '650'
    lineHeight: '1.25'
    letterSpacing: 0
  section-title:
    fontFamily: 'system-ui, sans-serif'
    fontSize: 18px
    fontWeight: '650'
    lineHeight: '1.35'
    letterSpacing: 0
  body:
    fontFamily: 'system-ui, sans-serif'
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: 0
  label:
    fontFamily: 'system-ui, sans-serif'
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: 0
  meta:
    fontFamily: 'system-ui, sans-serif'
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.4'
    letterSpacing: 0
rounded:
  sm: 4px
  md: 6px
  lg: 8px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 24px
  '6': 32px
components:
  button-primary:
    background: '{colors.action}'
    foreground: '{colors.on-action}'
    radius: '{rounded.md}'
  evidence-panel:
    background: '{colors.surface-raised}'
    border: '{colors.border}'
    radius: '{rounded.md}'
  decision-panel:
    background: '{colors.surface-subtle}'
    border: '{colors.border}'
    radius: '{rounded.md}'
  focus-ring:
    color: '{colors.focus}'
    width: 2px
---

## Brand & Style

[ASSUMPTION] MIRA usa una estética operativa, sobria y de alta legibilidad porque no existe una identidad visual confirmada. Debe sentirse como una herramienta de decisión cuidadosa: información densa pero ordenada, Evidencia visible y estados inequívocos. No usa composición de marketing, ilustraciones decorativas ni jerarquías basadas en tarjetas flotantes.

## Colors

- `{colors.surface-base}` sostiene el shell; `{colors.surface-raised}` contiene tablas, Evidencia y formularios.
- `{colors.action}` se reserva para la acción primaria confirmable. `{colors.focus}` identifica foco de teclado y selección, nunca una decisión.
- Los estados usan pares fondo/texto: aprobado, revisión, escalado y error. Siempre incluyen etiqueta o icono con texto; el color nunca comunica por sí solo.
- `ESCALADO` usa rojo solo para prioridad humana, no para insinuar rechazo. `ERROR / DERIVACIÓN` usa violeta para separarlo de una decisión adversa.
- No usar gradientes, fondos oscuros dominantes ni una paleta monocromática.

## Typography

La tipografía del sistema evita dependencias y mantiene lectura rápida. `{typography.page-title}` se limita al título de la superficie; tablas, formularios y paneles usan `{typography.body}`, `{typography.label}` y `{typography.meta}`. Los números de Puntaje no superan visualmente a Evidencia o razones.

## Layout & Spacing

La escala 4/8/12/16/24/32 mantiene densidad media. Escritorio usa shell estable con navegación de 232 px, contenido flexible y ancho máximo de 1440 px. La Bandeja prioriza tabla; el detalle usa dos columnas solo cuando caben Evidencia y acciones sin comprimir. En pantallas estrechas todo se apila en orden de lectura.

## Elevation & Depth

La jerarquía depende de bandas, bordes y espaciado. Sombras solo en diálogos y menús superpuestos; paneles de página permanecen planos. Un panel no contiene otra tarjeta decorativa.

## Shapes

Controles y paneles usan radios de 4 a 8 px. Badges de estado pueden usar `{rounded.sm}`; no se usan pills grandes ni botones redondeados como cápsulas. Iconos familiares acompañan acciones cuando aportan reconocimiento y siempre tienen tooltip accesible.

## Components

- **App shell:** navegación persistente a Bandeja y Ejecutar F4; nombre de superficie y acciones globales en una barra compacta.
- **Primary button:** `{components.button-primary}`; una sola acción sólida por contexto, con altura estable y foco visible.
- **Queue table:** filas de altura estable, columnas para Caso, Salida F4, razón, prioridad, estado y plazos. Selección por fila completa; prioridad y vencimiento tienen texto visible.
- **Status badge:** combina etiqueta y color para `REVISIÓN`, `ESCALADO`, `APROBADO AUTOMÁTICAMENTE` y `ERROR / DERIVACIÓN`.
- **Evidence panel:** `{components.evidence-panel}`; muestra archivo ficticio, vista o miniatura y Ubicación del hallazgo antes de Puntaje.
- **F4 explanation:** bloque plano con Salida, razón, regla, parámetros y Señales; Puntaje usa tipografía de cuerpo, no de título.
- **Decision panel:** `{components.decision-panel}`; agrupa acción, selector de Categoría de motivo compatible, comentario condicional y confirmación.
- **Correction dialog:** compara valor original y corregido en columnas alineadas; motivo y procedencia permanecen visibles.
- **Deadline marker:** texto de fecha, tipo de plazo y estado temporal. No depende de reloj o icono aislado.

## Do's and Don'ts

| Do | Don't |
|---|---|
| Mostrar Evidencia, razón y ubicación antes del Puntaje | Abrir el detalle con un número dominante |
| Usar etiquetas y color para todos los estados | Comunicar prioridad solo con rojo |
| Mantener tabla y acciones compactas, estables y escaneables | Convertir cada dato en una tarjeta |
| Separar claramente sugerencia F4 y Decisión humana | Presentar la sugerencia como recomendación vinculante |
| Conservar original y corregido en paralelo | Sustituir visualmente el valor original |
| Mostrar una acción primaria por contexto | Competir con varias acciones sólidas del mismo peso |

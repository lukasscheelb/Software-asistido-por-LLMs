# Propuesta de mejora del front-end de MIRA

Fecha: 17 de octubre de 2026. Rol: UX Expert. Estado: aprobada explícitamente por el usuario el 17 de octubre de 2026; implementación local completada.

Grupo conformado por: Francisca Meyer, Lukas Scheel y Sebastián Rodríguez

## Objetivo y alcance

Mejorar orientación, lectura y accesibilidad de F4 y F1 con Django, plantillas HTML y CSS existentes. No se modifican reglas, rutas, base de datos ni la versión entregada v2.0. Sin commit ni push. Architect, SM, Dev y QA comenzarán después de aprobar esta propuesta.

## Fuentes y alcance de la revisión

Se revisaron `_bmad/config.toml`, los contratos UX de la iniciativa F4/F1, las plantillas `base.html`, `bandeja.html`, `ejecutar_f4.html`, `detalle_caso.html`, `styles.css`, el contexto de las vistas y `docs/qa/usabilidad-px05.md`. La inspección fue documental y del código: no constituye una evaluación visual en navegador ni una prueba nueva con participantes. Las diferencias visuales se comprobarán en la siguiente etapa.

El acta actual registra que Fernanda necesitó orientación para reconocer botones y entender secciones; Ximena completó las tareas sin ayuda. Se utiliza esta evidencia para priorizar orientación, sin generalizar por edad ni afirmar que las mejoras ya resolvieron esas dificultades.

## Hallazgos y prioridades

| ID | Prioridad | Evidencia actual | Mejora propuesta | Criterio de comprobación |
|---|---|---|---|---|
| UX-01 | Alta | `.result-placeholder > span` tiene 56 × 56 px, pero contiene todo el nombre de F4. | Separar nombre y elemento visual; usar texto flexible. | Nombre completo legible, sin recorte o superposición en los anchos objetivo. |
| UX-02 | Alta | Bandeja tiene ocho columnas; CSS fija porcentajes solo en las seis primeras, que ya suman 100 %. | Repartir las ocho columnas y evitar cabeceras excesivamente largas; conservar etiquetas completas en navegación y títulos. | Ninguna columna ni acción queda comprimida u oculta en escritorio; móvil conserva todos los datos. |
| UX-03 | Alta | Dos pruebas históricas identifican dificultad para ubicar botones y comprender secciones; F1 repite nombre en kicker y título. | Explicar el propósito y el siguiente paso; reducir repetición; acción principal «Evaluar caso» en F4. | Una acción principal clara por formulario y enlace explícito hacia la siguiente etapa cuando procede. |
| UX-04 | Alta | La columna lateral reúne explicación, puntajes, decisión, corrección e historial; evidencia debe ir primero según contrato. | Dar mayor ancho a acciones al ser necesario, separar grupos y mantener evidencia primero. | En escritorio y móvil se puede revisar evidencia y completar acciones sin campos estrechos ni cambio de orden semántico. |
| UX-05 | Alta | `input` general aplica ancho 100 % y alto mínimo 44 px; solo radios tienen excepción, no la casilla de discrepancia. | Estilo específico de checkbox y etiqueta asociada. | Casilla alineada y operable por etiqueta y teclado; no ocupa ancho completo. |
| UX-06 | Alta | Foco CSS no incluye textarea; errores no están asociados sistemáticamente a controles y corrección no muestra todos los errores de campo. | Asociar ayudas/errores por ID, foco y resumen accesible. | Error visible y anunciado, valores conservados; Tab y Shift+Tab permiten corregir y enviar. |
| UX-07 | Alta | Estado de decisión usa siempre `status--approved`, incluso para otras acciones. | Estilo semántico por estado con etiqueta explícita. | Aprobar, rechazar y solicitar antecedentes se distinguen sin insinuar aprobación de todos los estados. |
| UX-08 | Media | El objeto PDF de evidencia no tiene título; microcopy usa términos técnicos y mayúsculas inconsistentes. | Nombre accesible, acceso alternativo al archivo y vocabulario claro. | Cada evidencia tiene nombre, ubicación y enlace; lector de pantalla identifica el objeto PDF. |
| UX-09 | Media | Móvil cambia tabla a bloques y oculta `thead`; navegación móvil omite `aria-current`. | Conservar relaciones semánticas y señalar destino activo. | Verificación del árbol accesible y teclado, además de capturas; sin depender de pseudoelementos para etiquetas accesibles. |
| UX-10 | Media | Contrato visual y CSS difieren en colores, medidas y tamaños. | Unificar tokens conservando la paleta actual, tras aprobación. | Una fuente coherente de decisiones visuales; contraste medido en QA, sin afirmar conformidad previa. |

## Dirección visual propuesta

Conservar la identidad operativa actual: fondo claro, paneles blancos, verde para acción y colores de estado con significado. Aumentar legibilidad de etiquetas y espacio entre grupos; dar jerarquía mediante títulos y separación, sin añadir decoración o dependencias. Esta dirección es una propuesta, no una decisión ya aprobada.

### Distribución propuesta para F4

```text
Navegación | F4 - Evaluación automática de casos
           | Breve instrucción sobre la evaluación
           | Selección del caso  | Resultado y razón
           | [Evaluar caso]     | Señales y parámetros
           | Política vigente   | [Ir a revisión humana] si corresponde
```

En móvil: título → selector y acción → resultado → siguiente paso. Sin un nombre largo dentro de una insignia de tamaño fijo.

### Distribución propuesta para F1

```text
Navegación | F1 - Revisión humana asistida
           | Resumen de pendientes y filtros
           | Casos con motivo, prioridad, estado y plazos

Detalle    | Evidencia, archivo y hallazgo | Explicación de la evaluación
           |                             | Decisión humana
           |                             | Corrección diferenciada
           | Historial de intervenciones
```

En móvil se apila: contexto → evidencia y hallazgo → explicación/señales → decisión → corrección → historial. La alternativa de ubicar historial bajo el área principal se validará por Architect; no cambia su contenido ni persistencia.

## Condiciones que se conservan

- Nombres exactos: «F4 - Evaluación automática de casos» y «F1 - Revisión humana asistida».
- Política, umbrales, precedencia de fraude y prohibición de rechazo automático sin cambios.
- Motivo y comentario condicional, discrepancia explícita, conservación del original, historial y control de versión.
- Identidad declarada de demo y datos ficticios; sin añadir autenticación o análisis real.
- Django, HTML y CSS; JavaScript local solo si una interacción aprobada lo necesita y conserva validación de servidor. No se propone SPA, CDN, framework visual ni instalación de paquetes.

## Secuencia BMAD después de la aprobación

1. Architect: contrastar el delta con las vistas, formularios, estados y contratos; concretar cambios presentacionales y sus límites.
2. SM: derivar historias de UX-01 a UX-10 con referencias a contratos y criterios de aceptación; no se crean historias ejecutables antes de la aprobación.
3. Dev: implementar por recorridos conservando reglas y datos existentes.
4. QA: comprobar las 33 pruebas Django existentes, adaptar verificaciones de textos cuando corresponda y recorrer F4 normal/error y F1 decisión/corrección/conflicto en base de datos aislada. Verificar teclado, contraste, árbol accesible y capturas en los anchos objetivo.

## Decisión solicitada

Aprobar la dirección visual y las prioridades UX-01 a UX-10, o indicar ajustes. La implementación queda pendiente de aprobación explícita. Los contratos de esta carpeta son borradores; los contratos finales anteriores siguen vigentes hasta su reconciliación posterior. No se ejecutaron fases Architect, SM, Dev o QA de implementación.


## Cierre de la propuesta

La solicitud de aprobación anterior se conserva como registro de la propuesta inicial. El usuario la aprobó y se completaron Architect, SM, Dev y las comprobaciones QA documentadas en `docs/qa/frontend-2026-10-17/QA.md`. DESIGN y EXPERIENCE de esta carpeta contienen el delta implementado. No se realizó commit, push ni movimiento de v2.0.

---
title: "Product Brief V2: MIRA - Incremento F4 + F1"
status: final
version: "2.0"
created: 2026-09-27
updated: 2026-09-27
supersedes: "../brief-Software-asistido-por-LLMs-2026-09-27/brief.md"
---

# Product Brief V2: MIRA - Incremento F4 + F1

## Resumen ejecutivo

MIRA es la apuesta de DPRIME por convertir soluciones de automatización hechas a medida en una plataforma operable por sus clientes. Su promesa combina tres objetivos en tensión: automatizar decisiones, mantenerlas confiables y permitir que un tercero reconstruya por qué se tomaron. Los pilotos previos mostraron que automatizar sin explicación no elimina trabajo: lo desplaza al operador y reduce la confianza.

La Entrega 2 aborda esa tensión mediante un incremento web, acotado y demostrable que conecta **F4 - Puntaje y decisión por umbrales** con **F1 - Bandeja de revisión asistida**. F4 aplica una política conservadora sobre casos simulados que ya contienen puntaje y señales. Los casos no aptos para aprobación automática llegan a F1, donde una persona revisa evidencia, comprende la razón de derivación y registra una decisión motivada.

Esta V2 conserva las decisiones de la baseline F4 + F1 e incorpora el contexto original de MIRA y las condiciones del entregable BMAD. No afirma que el producto completo esté listo para producción: demuestra control humano, explicabilidad y trazabilidad desde requisitos de la Entrega 1 hasta artefactos, código, pruebas y commits.

## Contexto, problema y oportunidad

DPRIME ha construido pilotos funcionales, pero todavía depende de configuraciones e integraciones artesanales. La versión existente fue concebida para demostrar capacidades, no para operar con niveles de servicio, auditoría reproducible y múltiples clientes. En particular, la revisión humana quedó fuera del diseño: los casos derivados llegan sin contexto suficiente y el operador debe buscar datos en varios sistemas.

El analista liquidador del piloto identifica que su mayor costo no es decidir, sino encontrar la información. Un puntaje aislado no explica si existe evidencia ilegible, una inconsistencia o una señal de fraude. Además, mostrar la recomendación demasiado pronto puede sesgar la decisión y convertir el control humano en una formalidad.

La oportunidad del incremento es probar una automatización responsable: resolver automáticamente solo los casos favorables que superen todas las barreras y entregar al resto una revisión útil, comprensible y auditable. Esto atiende **H-01**, **H-02** y **H-15** sobre umbrales, rechazo automático y mínimos por señal, y **H-16** y **H-18** sobre plazos y usabilidad verificable.

## Usuarios y principios de diseño

- **Operador de revisión:** necesita evidencia y hallazgos localizados antes del puntaje, razones claras y acciones que no obliguen a abrir otros sistemas.
- **Supervisor:** necesita visibilidad de vencimientos y escalamiento de casos atrasados; el incremento no incluye su panel agregado.
- **Responsable de riesgo o cumplimiento:** exige intervención humana significativa, ausencia de rechazo automático y decisiones justificables.
- **Equipo de modelos de DPRIME:** necesita identificar discrepancias y correcciones para aprendizaje posterior, sin alterar la decisión humana.
- **Persona afectada:** no usa MIRA, pero sus datos y patrimonio pueden verse afectados; esto obliga a conservar explicaciones y control humano.

Principios heredados: la evidencia y las razones preceden a la sugerencia; una señal ausente nunca es favorable; el fraude tiene precedencia; toda intervención queda motivada; las correcciones conservan el original; y ninguna salida automática puede ser un rechazo. Estos principios concretan **DEC-01**, **DEC-08**, **DEC-10** y **DEC-11**.

## Solución propuesta

### F4 - Política de decisión

Cada caso ficticio contiene puntaje `0-100`, autenticidad documental `0-100`, coherencia entre evidencias `0-100`, fraude detectado `Sí/No` y automatización `ON/OFF`. F4 no inventa ni calcula una fórmula de scoring; consume los valores del motor simulado y aplica, en orden, la política vigente:

1. Puntaje inválido o fuera de rango: **ERROR / DERIVACIÓN**.
2. Fraude detectado: **ESCALADO**.
3. Puntaje menor que `60`: **ESCALADO**.
4. Automatización `ON`, puntaje mayor que `90` y ambas señales numéricas mayores o iguales que `70`: **APROBADO AUTOMÁTICAMENTE**.
5. Cualquier otro caso: **REVISIÓN**.
6. Nunca existe rechazo automático.

El umbral `T=90` y los mínimos `70/100` son configurables y válidos para este incremento, no parámetros definitivos de MIRA (**DEC-E2-01** a **DEC-E2-04**).

### F1 - Bandeja de revisión asistida

Los casos con salida **REVISIÓN** ingresan a una bandeja web en español. La pantalla presenta evidencia, razones y ubicación de hallazgos antes del puntaje; luego muestra señales, plazos y discrepancias. Para PDF, la ubicación usa página y campo o región; para imagen, nombre de región y coordenadas opcionales.

El operador puede aprobar, rechazar, solicitar antecedentes o corregir un dato. Cada acción exige una categoría de motivo; el comentario es obligatorio al elegir `Otro`. Una corrección conserva el valor original y una decisión sobre una versión obsoleta se bloquea sin sobrescribir la vigente (**DEC-E2-05** y **DEC-E2-06**).

Los plazos usan `America/Santiago`, calendario de lunes a viernes, meta interna de `3` días hábiles, compromiso de `5`, alerta un día hábil antes y al vencer. Un caso vencido permanece abierto y escala (**DEC-E2-07**).

## Gobierno de fuentes y conflictos resueltos

La descripción original contiene alternativas incompatibles: umbrales `80/85`, tramo bajo con posible rechazo y mínimos por señal pendientes. Para este incremento prevalecen la bitácora y la baseline E2: `T=90`, mínimo `70`, fraude como veto y rechazo exclusivamente humano. La frase del entregable que asigna a F4 el "cálculo del puntaje" se interpreta junto con su regla de motor simulado: los casos ya traen puntaje y componentes; F4 aplica la decisión.

Otros conflictos del producto completo, como retención de evidencia, residencia de datos, gobierno dual de cambios de umbral y definición de facturación, permanecen fuera de este incremento. Deben llegar al PRD o a arquitectura como decisiones abiertas, no asumirse resueltos.

## Alcance del incremento

**Incluye:** interfaz y lógica conectadas para F4 y F1; al menos tres casos ficticios con evidencia de ejemplo; política versionada y configurable; decisiones humanas motivadas; correcciones sin pérdida del original; fechas controladas para pruebas; recorrido completo sin herramientas de desarrollo; y trazabilidad con IDs heredados de E1.

**Excluye:** motor multimodal real, fórmula de scoring, datos personales reales, rechazo automático, funcionalidades F2-F3 y F5-F9, despliegue productivo, panel agregado de supervisor, resolución regulatoria integral y decisiones de arquitectura aún no tomadas.

## Trazabilidad prioritaria

| Capacidad | Requisitos E1 | Decisiones y hallazgos | Historia | Verificación base |
|---|---|---|---|---|
| Política F4 | RQF-003, RQF-004, RQF-008, RQNF-009 | DEC-01; H-01, H-02, H-15 | HU-03 | PF-04, PX-09 |
| Revisión F1 | RQF-005, RQF-014, RQNF-005, RQNF-008 | DEC-08, DEC-10, DEC-11; H-08, H-16, H-18 | HU-04 | PF-05, PF-14, PX-05, PX-08 |
| Rendimiento | RQNF-001 | Aplicabilidad por confirmar | Por confirmar | Umbral medible por definir en arquitectura |

## Criterios de éxito

- Las fronteras de F4 se verifican: `59,99` escala; `60..90` revisa; `90,01` solo aprueba con automatización activa, sin fraude y con ambas señales sobre el mínimo.
- Fraude, señal ausente o valor menor que `70` impiden la aprobación automática; nunca se genera rechazo automático.
- F1 permite resolver el flujo completo desde la interfaz, bloquea el rechazo sin motivo y protege la decisión vigente ante concurrencia.
- El escenario `120000 -> 100000` conserva el original y registra la corrección.
- PF-14 reproduce meta, compromiso, alerta y escalamiento mediante fechas controladas.
- La evidencia y las razones aparecen antes del puntaje; una prueba de usabilidad con una persona externa registra éxito, tiempo y dificultades.
- Existen pruebas automatizadas de los Must, excepciones y al menos una prueba E2E por funcionalidad, derivadas de PF y PX en vez del comportamiento accidental del código.
- Un evaluador clona el repositorio, sigue el README y ejecuta ambas funcionalidades con los datos de prueba en menos de `15` minutos.
- Cada requisito incluido se puede seguir hasta artefacto BMAD, historia o tarea, commit y prueba.

## Riesgos y decisiones pendientes

- **Adopción:** una interfaz que priorice velocidad sobre criterio puede inducir aceptación automática de la sugerencia.
- **Explicabilidad:** barras o porcentajes no sustituyen una razón comprensible ni la ubicación del hallazgo.
- **Calidad:** PX-09 debe demostrar calidad suficiente antes de ampliar automatización; los parámetros del piloto no se generalizan.
- **Arquitectura:** stack, persistencia, concurrencia y aplicabilidad exacta de `p95 <= 2 s` requieren decisión posterior.
- **Demostración:** deben fijarse los casos, evidencias ficticias y resultados esperados antes de implementar las pruebas.
- **Gobierno:** cualquier cambio posterior se agrega a la bitácora y no reescribe decisiones anteriores.

## Continuidad BMAD

Este brief es la entrada del rol Analyst y debe ser validado por Sebastián Rodríguez, representante del cliente E2, antes de avanzar. El siguiente artefacto es el PRD, que debe conservar IDs de E1, asignar ID y fuente a requisitos nuevos, y trasladar los asuntos diferidos sin convertirlos en supuestos silenciosos.

## Fuentes

- `LLM - MIRA_Entrega2_bitacora_decisiones.md`
- `LLM - MIRA_E2_Baseline_F4_F1.md`
- `Contexto-fase1-bmad/LLM - Descripción del proyecto.pdf`
- `Contexto-fase1-bmad/LLM - Entrega_2_MIRA_SDD_BMAD.pdf`

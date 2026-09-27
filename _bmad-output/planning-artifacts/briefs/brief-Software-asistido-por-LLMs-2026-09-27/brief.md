---
title: "Product Brief: MIRA - Incremento F4 + F1"
status: final
created: 2026-09-27
updated: 2026-09-27
---

# Product Brief: MIRA - Incremento F4 + F1

## Resumen ejecutivo

La Entrega 2 de MIRA transforma la línea base de requisitos de la Entrega 1 en un incremento funcional, demostrable y trazable. El equipo seleccionó dos funcionalidades conectadas: **F4 - Puntaje y decisión por umbrales** y **F1 - Bandeja de revisión asistida**. F4 aplica una política a datos simulados; los casos que requieren revisión pasan a F1 para que un operador examine la evidencia y registre una decisión fundamentada.

El incremento prioriza el control humano. No implementa el motor multimodal real ni inventa una fórmula de scoring: consume puntajes, componentes y señales incluidos en los casos de prueba. La aprobación automática exige que la automatización esté habilitada y que se cumplan todas las barreras del piloto. El rechazo siempre requiere una decisión humana y un motivo.

El objetivo es demostrar el recorrido F4 -> F1 y mantener continuidad entre requisitos, decisiones, pruebas, artefactos BMAD, implementación y commits. Los parámetros adoptados son válidos para este incremento, no valores definitivos de MIRA.

## Problema y oportunidad

Una decisión pierde confiabilidad si no se pueden explicar las señales que la produjeron, reconstruir la política aplicada o distinguir el dato original de una corrección. También existe riesgo cuando un sistema aprueba sin barreras suficientes, rechaza automáticamente o permite decidir sobre una versión obsoleta.

F4 convierte puntajes y señales ya calculados en una salida conservadora y verificable. F1 entrega al operador evidencia, razones, hallazgos y plazos para resolver los casos que no deben automatizarse. Juntas permiten demostrar automatización acotada con supervisión humana, explicabilidad y trazabilidad.

## Actores y gobierno

- **Operador de revisión:** revisa evidencia y plazos; aprueba, rechaza, solicita antecedentes o corrige un dato con motivo obligatorio y sin borrar el original.
- **Responsable de riesgo:** necesita decisiones explicadas y conservadoras que eviten aprobaciones sin sustento.
- **Supervisor:** controla casos próximos a vencer o atrasados; los vencidos permanecen abiertos y escalan.
- **Equipo:** Lukas Scheel, Francisca Meyer y Sebastián Rodríguez.
- **Representante del cliente E2:** Sebastián Rodríguez valida las decisiones funcionales del incremento.

Las decisiones nuevas se agregan a la bitácora sin borrar las anteriores. Los IDs heredados de E1 se conservan.

## Solución propuesta

### F4 - Política de decisión

Cada caso simulado contiene puntaje `0-100`, autenticidad documental `0-100`, coherencia entre evidencias `0-100`, fraude detectado `Sí/No` y automatización `ON/OFF`. F4 aplica estas reglas, sin calcular el puntaje:

1. Puntaje inválido o fuera de rango: **ERROR / DERIVACIÓN**.
2. Fraude detectado: **ESCALADO**.
3. Puntaje menor que `60`: **ESCALADO**.
4. Automatización `ON`, puntaje mayor que `90` y ambas señales numéricas mayores o iguales que `70`: **APROBADO AUTOMÁTICAMENTE**.
5. Cualquier otro caso: **REVISIÓN**.
6. Nunca existe rechazo automático.

El umbral `T=90` y los mínimos `70/100` son configurables y válidos sólo para este incremento y sus datos de prueba.

### F1 - Bandeja de revisión asistida

Los casos con salida **REVISIÓN** ingresan a una bandeja que muestra evidencia y razones antes del puntaje, señales, ubicación de hallazgos, vencimientos, alertas y discrepancias entre la plataforma y el operador.

El operador puede aprobar, rechazar, solicitar antecedentes o corregir un dato. Cada acción exige una categoría de motivo; el comentario es opcional salvo al seleccionar `Otro`. Una corrección conserva el valor original. Una decisión sobre una versión obsoleta se bloquea sin sobrescribir la decisión vigente.

La ubicación de hallazgos se almacena estructuradamente y se muestra de forma comprensible: página y campo o región para PDF; nombre de región y coordenadas opcionales para imagen.

## Alcance

### Incluido

- interfaz y lógica de negocio para F4 y F1;
- casos, puntajes, componentes, señales y evidencia simulados;
- política versionada y configurable y conexión F4 -> F1;
- decisiones humanas motivadas y correcciones que conservan el original;
- meta interna de `3` días hábiles y compromiso de `5` días hábiles;
- calendario de lunes a viernes en `America/Santiago`;
- alertas un día hábil antes y al vencer;
- escalamiento de vencidos sin cierre automático;
- fechas controladas para pruebas y demostración reproducibles;
- trazabilidad con requisitos, decisiones, historias y pruebas de E1.

### Fuera de alcance

- implementar el motor multimodal real o una fórmula de scoring;
- presentar `T=90` o los mínimos `70/100` como parámetros definitivos;
- habilitar rechazo automático;
- modificar retroactivamente los artefactos de E1;
- implementar funcionalidades distintas de F4 y F1;
- cerrar decisiones de arquitectura correspondientes a una etapa BMAD posterior.

## Requisitos y trazabilidad clave

| Capacidad | Requisitos | Historia | Verificación base |
|---|---|---|---|
| Política de decisión F4 | RQF-003, RQF-004, RQF-008, RQNF-009 | HU-03 | PF-04, PX-09 |
| Revisión asistida F1 | RQF-005, RQF-014, RQNF-005, RQNF-008 | HU-04 | PF-05, PF-14, PX-05, PX-08 |
| Rendimiento transversal | RQNF-001 | Por confirmar | Aplicabilidad pendiente de arquitectura |

## Criterios de éxito

- **Política correcta:** `59,99` escala; los valores entre `60` y `90`, incluidos, revisan; `90,01` sólo aprueba con automatización activa, sin fraude y con ambas señales sobre sus mínimos.
- **Barreras conservadoras:** fraude escala; una señal ausente o bajo `70` impide la aprobación automática; nunca hay rechazo automático.
- **Revisión controlada:** se bloquea el rechazo sin motivo y una decisión sobre una versión obsoleta no sobrescribe la vigente.
- **Corrección trazable:** el escenario `120000 -> 100000` conserva el dato original y registra el motivo.
- **Plazos reproducibles:** PF-14 verifica meta interna, compromiso, alerta previa, vencimiento y escalamiento con fechas controladas.
- **Control humano:** la evidencia aparece antes del puntaje; PX-05 evalúa usabilidad y PX-09 calidad de decisión antes de ampliar la automatización.
- **Trazabilidad completa:** cada cambio se vincula con requisitos, decisiones, pruebas, artefactos BMAD, implementación y commits.

## Riesgos y decisiones pendientes

- Tecnología, arquitectura y persistencia no están definidas en estas fuentes.
- La aplicabilidad de RQNF-001, incluida la pantalla `p95 <= 2 s`, debe confirmarse en BMAD Architect.
- F1 necesita un catálogo inicial de categorías de motivo.
- Debe definirse el conjunto final de casos y evidencias simuladas para la demostración.
- Las reglas del estado `cerrado por falta de antecedentes` deben delimitarse sin ampliar el alcance.
- La activación de la automatización requiere gobierno explícito y permanece restringida a las condiciones del piloto.

## Visión de continuidad

Este incremento crea una base verificable para evolucionar MIRA sin perder control humano. Cualquier avance hacia automatización real deberá apoyarse en calibración, calidad de decisión comprobada y aprobación explícita, manteniendo configurables los umbrales y las reglas.

## Fuentes autorizadas

- `LLM - MIRA_Entrega2_bitacora_decisiones.md`
- `LLM - MIRA_E2_Baseline_F4_F1.md`

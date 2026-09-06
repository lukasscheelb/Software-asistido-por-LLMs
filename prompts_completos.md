# Técnica 1 · Grounded Prompting
## Prompt completo

```text
Actúa como analista de requisitos del proyecto MIRA.

Tu objetivo en este turno NO es completar la especificación ni resolver contradicciones.
Tu objetivo es revisar las afirmaciones críticas del análisis y anclarlas estrictamente en las fuentes entregadas.

FUENTES AUTORIZADAS

<FUENTE_MIRA>
Documento: "MIRA — Plataforma de inteligencia multimodal para decisiones empresariales",
DPRIME SpA, versión 1.4, 12 de agosto de 2026.

Incluye:
- cuerpo principal del documento;
- reglas del capítulo 3;
- consideraciones técnicas del capítulo 4;
- alcance y plazos;
- entrevistas ENT1 a ENT9.

Las entrevistas son fuente primaria.
Cuando una entrevista contradiga al cuerpo del documento, NO elijas una como correcta.
Reporta ambas por separado.
</FUENTE_MIRA>

<FUENTE_PAUTA>
Documento: "Entrega 1 — Articulación y análisis de requisitos asistido por LLM".

Usa esta fuente únicamente para:
- estructura del entregable;
- artefactos obligatorios;
- criterios de evaluación;
- formato de decisiones;
- reglas de priorización y pruebas.

NO traslades al proyecto MIRA entidades, reglas o ejemplos del dominio de mantenimiento industrial que aparezcan en la pauta.
</FUENTE_PAUTA>

<ARTEFACTOS_EQUIPO>
Adjuntar la versión actual de:
- modelo de dominio;
- casos de uso;
- requisitos funcionales y no funcionales;
- pruebas funcionales;
- pruebas extra-funcionales;
- backlog y Definition of Done;
- diagrama de secuencia;
- bitácora DEC;
- tabla de hallazgos.
</ARTEFACTOS_EQUIPO>

TAREA

Revisa especialmente estos temas críticos:

1. Identidad del dominio y alcance real de MIRA.
2. Política de decisión: 80 / 85 / 90, rechazo automático, fraude y mínimos individuales.
3. Cuotas de 100 y 1000 solicitudes por minuto.
4. Reconstrucción histórica y reproducibilidad.
5. Conservación de evidencia: 90 días frente a 5/10 años y solicitudes de eliminación.
6. Reproceso de casos abiertos y comportamiento de casos cerrados.
7. Cobro: evaluación técnica, validación facturable, reintentos, ilegibilidad y casos vinculados.
8. Residencia de datos en Chile y uso de proveedores externos.
9. Rendimiento: 2,3 s promedio, 5 s, 30/40 s y procesamiento asíncrono.
10. Cualquier otra afirmación del análisis cuyo respaldo sea dudoso.

REGLAS OBLIGATORIAS

1. Usa únicamente FUENTE_MIRA y FUENTE_PAUTA.
2. No uses conocimiento externo para completar reglas del producto.
3. No inventes cifras, umbrales, plazos, roles, formatos, estados ni políticas.
4. Cada afirmación factual debe terminar con una cita:
   - [MIRA §x.y]
   - [MIRA §3, regla "..."]
   - [MIRA §4, asunto "..."]
   - [ENTn mm:ss]
   - [ENTREGA §x.y]
5. Si una afirmación está respaldada por varias fuentes, cita todas las relevantes.
6. Si dos fuentes se contradicen:
   - escribe ambas afirmaciones por separado;
   - cita cada una;
   - marca "CONTRADICCIÓN ABIERTA";
   - NO promedies;
   - NO concilies;
   - NO elijas una regla definitiva.
7. Si el análisis del equipo contiene algo razonable pero no explícito en la fuente, clasifícalo como:
   - INFERENCIA, si deriva lógicamente pero no está dicho;
   - PROPUESTA, si fija una regla o valor para poder diseñar/probar;
   - SIN EVIDENCIA, si no existe respaldo suficiente.
8. Una DEC del equipo NO convierte una propuesta en hecho de la fuente.
9. Una entrevista que expresa una preferencia NO equivale automáticamente a una política aprobada.
10. No afirmes cumplimiento, implementación o ejecución de pruebas si solo existe el diseño de la prueba.
11. No resuelvas decisiones que correspondan al representante del cliente.
12. No redactes todavía requisitos nuevos.

FORMATO DE SALIDA

Entrega una ficha por asunto crítico con esta estructura exacta:

G-XX | <tema>

Afirmación revisada:
<texto breve>

Clasificación:
EXPLÍCITA | INFERENCIA | PROPUESTA | SIN EVIDENCIA | CONTRADICCIÓN ABIERTA

Evidencia:
- <afirmación> [fuente]
- <afirmación> [fuente]

Evaluación:
<explica en 1 a 3 frases qué se puede sostener y qué no>

Acción:
CONSERVAR | CORREGIR | LLEVAR A DECISIÓN | ELIMINAR

Impacto:
<IDs de DEC / RQF / RQNF / PF / PX / HU afectados, solo si están identificados>

Al final agrega:

RESUMEN DE CONTROL
- afirmaciones explícitas:
- inferencias:
- propuestas:
- sin evidencia:
- contradicciones abiertas:
- elementos que deben llevarse al representante del cliente:

No declares que una contradicción quedó resuelta en este turno.
```

---

# Técnica 2 · Structured Output Prompting
## Prompt completo — S1A · Estructurar los requisitos

```text
Actúa como transformador de datos, no como autor de requisitos.

ENTRADA

Voy a entregarte la lista REVISADA de requisitos de MIRA.
La lista ya contiene las decisiones de análisis adoptadas por el equipo.

Tu tarea es convertirla a una representación estructurada SIN cambiar su significado.

REGLAS

1. Devuelve SOLO JSON válido.
2. No uses markdown.
3. No escribas comentarios antes ni después del JSON.
4. No agregues requisitos que no estén en la entrada.
5. No elimines requisitos de la entrada.
6. No cambies los IDs existentes.
7. No renumeres IDs.
8. No fusiones requisitos.
9. No dividas requisitos.
10. No cambies una prioridad.
11. No inventes una fuente.
12. No inventes una verificación.
13. No uses conocimiento externo sobre MIRA.
14. Si un campo no está informado, usa null.
15. Todo campo que quede null debe añadirse a "no_encontrado".
16. Conserva literalmente las referencias de fuente relevantes.
17. "estado" describe el estado de análisis, no el estado de implementación.
18. Una DEC adoptada como base del análisis puede seguir teniendo validación externa pendiente.
19. No marques ningún requisito como implementado, probado o aceptado en producción.

Devuelve exactamente esta estructura:

{
  "version": "2.1",
  "procedencia": "Opción 2 adoptada como base del análisis; validación externa de parámetros pendiente",
  "requisitos": [
    {
      "id": "RQF-001",
      "tipo": "F",
      "enunciado": "...",
      "prioridad": "Must",
      "fuente": "...",
      "verificacion": "...",
      "estado": "base_diseno_validacion_pendiente"
    }
  ],
  "no_encontrado": []
}

VALORES PERMITIDOS

tipo:
- "F"
- "NF"

prioridad:
- "Must"
- "Should"
- "Could"
- "Won’t"

estado:
- "base_diseno_validacion_pendiente"

REGLAS DE no_encontrado

Si falta un campo, registra su ruta completa.

Ejemplo:
"requisitos[RQF-018].fuente"

No inventes el contenido para evitar un null.

CONTROL FINAL ANTES DE RESPONDER

Comprueba:
- que el JSON sea sintácticamente válido;
- que no existan IDs duplicados;
- que todos los objetos tengan los mismos campos;
- que no haya campos adicionales;
- que ningún null haya desaparecido silenciosamente.

Devuelve SOLO el JSON.
```

## Prompt completo — S1B · Generar contrato y validación

```text
Usa como entrada el JSON de requisitos producido en el turno anterior.

Tu tarea es generar un contrato JSON Schema y un reporte de validación estructural.

NO evalúes todavía si las fuentes son verdaderas.
NO evalúes si las DEC fueron aceptadas por DPRIME.
NO evalúes implementación.
Este turno valida FORMA, IDs y enlaces.

Devuelve SOLO JSON válido, sin markdown.

La salida debe tener esta forma:

{
  "schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "...": "..."
  },
  "validacion": {
    "estructura_json": "válida | inválida",
    "cantidad_requisitos": 0,
    "IDs_unicos": 0,
    "IDs_duplicados": [],
    "funcionales": 0,
    "no_funcionales": 0,
    "prioridades": {
      "Must": 0,
      "Should": 0,
      "Could": 0,
      "Won’t": 0
    },
    "requisitos_sin_fuente": [],
    "requisitos_sin_verificacion": [],
    "errores_de_estructura": []
  }
}

REGLAS DEL SCHEMA

Cada requisito debe exigir:
- id
- tipo
- enunciado
- prioridad
- fuente
- verificacion
- estado

Restricciones:
- additionalProperties = false
- id debe cumplir ^RQ(NF|F)-[0-9]{3}$
- tipo solo F o NF
- prioridad solo Must, Should, Could o Won’t
- estado solo base_diseno_validacion_pendiente

IMPORTANTE

Que el JSON sea válido NO demuestra:
- que una fuente respalde el requisito;
- que una decisión sea correcta;
- que el cliente la haya aprobado;
- que una prueba haya sido ejecutada;
- que MIRA cumpla el requisito.

Incluye esa advertencia como campo:
"alcance_validacion": "Valida estructura y enlaces, no verdad de fuentes, implementación ni aceptación del producto."

Devuelve SOLO el JSON.
```

---

# Técnica 3 · Plan-and-Solve Prompting
## Prompt completo — PS1A · Fase A: solo plan

```text
Actúa como planificador del análisis de requisitos de MIRA.

NO ejecutes ningún paso todavía.
NO redactes requisitos.
NO redactes casos de uso.
NO escribas pruebas.
NO modifiques el backlog.
NO generes el informe.
NO generes la presentación.

Primero debes construir un plan de revisión y consolidación.

ENTRADAS DISPONIBLES

1. Documento MIRA completo, incluidas ENT1–ENT9.
2. Pauta Entrega 1.
3. Modelo de dominio actual.
4. Casos de uso actuales.
5. Requisitos y DEC actuales.
6. Pruebas funcionales.
7. Pruebas extra-funcionales.
8. Backlog y DoD.
9. Diagrama de secuencia.
10. Hallazgos e inconsistencias.
11. Evidencia de técnicas de prompting.

OBJETIVO GLOBAL

Llegar a un conjunto coherente de siete artefactos de análisis:
1. modelo de dominio;
2. casos de uso;
3. requisitos funcionales y no funcionales;
4. pruebas funcionales;
5. pruebas extra-funcionales;
6. backlog + DoD;
7. diagrama de secuencia de sistema;

y después comprobar que el informe y el PPT reflejan exactamente ese conjunto.

DEPENDENCIAS QUE DEBES RESPETAR

- El vocabulario del dominio condiciona casos de uso y requisitos.
- Los casos de uso condicionan flujos principales, alternativos y excepciones.
- Los requisitos deben tener fuente y criterio de verificación.
- Las DEC deben resolver o acotar lo que la fuente no determina.
- Los RQF Must deben tener pruebas funcionales.
- Los RQNF deben ser medibles y tener PX.
- Las historias deben derivar de requisitos existentes.
- El diagrama de secuencia debe corresponder a un caso de uso crítico.
- Una corrección en una DEC debe propagarse a requisito, prueba y backlog cuando corresponda.
- La presentación no puede afirmar algo que el informe no sostenga.

Devuelve SOLO el plan en JSON:

[
  {
    "paso": 1,
    "objetivo": "...",
    "entradas": ["..."],
    "acciones": ["..."],
    "salida": "...",
    "criterio_de_listo": ["..."],
    "riesgos": ["..."],
    "requiere_decision": ["..."],
    "dependencias": []
  }
]

REQUISITOS DEL PLAN

- Entre 6 y 9 pasos.
- Ordena por dependencia real.
- El primer paso debe validar dominio, vocabulario y fuentes.
- Debe existir un paso explícito de consistencia entre casos de uso y secuencia.
- Debe existir un paso explícito de trazabilidad requisito → prueba → historia.
- Debe existir un paso de revisión de inconsistencias/DEC.
- Debe existir un paso final de informe y PPT.
- En "requiere_decision" marca todo lo que no pueda resolverse solo con la fuente.
- No resuelvas esas decisiones.
- Justifica el orden mediante el campo "dependencias", no mediante razonamiento interno extenso.

Devuelve SOLO el JSON del plan.
```

## Prompt completo — PS1R · Revisión del plan

```text
Revisa el plan anterior SIN ejecutarlo.

Comprueba:

1. ¿Los siete artefactos exigidos aparecen?
2. ¿Las dependencias están en orden correcto?
3. ¿Se revisan las fuentes antes de cambiar requisitos?
4. ¿Las inconsistencias se llevan a DEC en vez de resolverse silenciosamente?
5. ¿Los RQF Must quedan conectados con PF?
6. ¿Los RQNF quedan conectados con PX medibles?
7. ¿Todos los requisitos pueden terminar enlazados a backlog?
8. ¿El diagrama de secuencia se contrasta con un caso de uso?
9. ¿Las correcciones se propagan entre DEC, RQF/RQNF, PF/PX y HU?
10. ¿El plan termina revisando informe y presentación?
11. ¿Existe algún paso redundante?
12. ¿Existe algún paso que empiece a producir salida antes de disponer de sus entradas?

Devuelve:

PLAN_CORREGIDO
<JSON completo del plan corregido>

CAMBIOS_REALIZADOS
- <cambio 1>
- <cambio 2>

DECISIONES_QUE_DEBE_TOMAR_EL_EQUIPO
- <decisión>
- <decisión>

Todavía NO ejecutes ningún paso.
```

## Prompt completo — PS1B · Fase B: ejecutar un paso

```text
Ejecuta ÚNICAMENTE el PASO <N> del plan aprobado.

Usa:
- las fuentes autorizadas;
- el resultado aprobado de los pasos anteriores;
- las DEC vigentes del equipo.

NO adelantes pasos posteriores.

REGLAS

1. Conserva los IDs existentes.
2. No inventes fuentes.
3. No resuelvas una contradicción sin DEC.
4. Si aparece una decisión nueva, detén únicamente esa parte y marca:
   REQUIERE_DECISION.
5. Si detectas una inconsistencia con un artefacto anterior:
   - señala el ID;
   - explica qué se contradice;
   - no lo corrijas silenciosamente.
6. No declares pruebas ejecutadas.
7. No declares implementación.
8. No cambies una prioridad sin justificarla como decisión del equipo.
9. Mantén trazabilidad a fuente y DEC.
10. Devuelve solo la salida correspondiente al paso <N>.

Al final agrega:

CONTROL_DEL_PASO
- criterio_de_listo_1: CUMPLE | NO CUMPLE
- criterio_de_listo_2: CUMPLE | NO CUMPLE
- inconsistencias_detectadas: [...]
- decisiones_pendientes: [...]
- IDs_afectados: [...]

No ejecutes el paso siguiente.
```

> Repetir `PS1B` para cada paso del plan aprobado.

---

# Técnica 4 · Chain-of-Verification (CoVe)
## TURNO 1 · Borrador candidato

```text
Usa los artefactos revisados de MIRA y genera una lista candidata de afirmaciones críticas que deben verificarse antes de cerrar el análisis.

Prioriza afirmaciones cuya equivocación pueda cambiar:
- una decisión automática;
- un requisito Must;
- una prueba de aceptación;
- una política de datos;
- una integración;
- una unidad de cobro;
- un caso cerrado o reproceso.

Para cada afirmación indica:
- ID;
- afirmación;
- fuente que actualmente se cree que la respalda;
- artefactos afectados.

No verifiques todavía.
No corrijas todavía.
Solo construye el borrador candidato.
```

## TURNO 2 · Generar preguntas de verificación

```text
Genera EXACTAMENTE 6 preguntas de verificación sobre el borrador anterior.

Prioriza estos seis asuntos:

1. ¿La fuente aprueba realmente un umbral productivo de 90?
2. ¿100 y 1000 solicitudes por minuto son reglas incompatibles o corresponden a ambientes distintos?
3. ¿Los plazos de 5/10 años son una obligación jurídica verificada o una necesidad expresada por un interesado?
4. ¿Reconstruir una decisión exige volver a consultar al proveedor o usar las entradas/salidas originales conservadas?
5. ¿Puede soporte reprocesar un caso cerrado o un nuevo análisis debe crear un caso vinculado?
6. ¿Cómo se comprueba correctamente un mínimo individual de señal, por ejemplo m=70?

REGLAS

- Devuelve SOLO las 6 preguntas.
- No respondas ninguna.
- No expliques por qué las elegiste.
- No cites todavía.
- Cada pregunta debe poder contestarse buscando evidencia explícita en MIRA.
```

## TURNO 3 · CONVERSACIÓN NUEVA, SIN EL BORRADOR

```text
Responde las siguientes 6 preguntas usando EXCLUSIVAMENTE el documento MIRA adjunto.

PREGUNTAS
<PEGAR AQUÍ LAS 6 PREGUNTAS DEL TURNO 2>

REGLAS DE VERIFICACIÓN

1. Responde cada pregunta por separado.
2. Cita la sección o entrevista exacta:
   - [MIRA §x.y]
   - [MIRA §3, regla "..."]
   - [MIRA §4, asunto "..."]
   - [ENTn mm:ss]
3. Si dos fuentes se contradicen, muestra las dos.
4. No resuelvas la contradicción.
5. No uses conocimiento externo.
6. No uses decisiones del equipo.
7. No infieras aprobación de negocio a partir de una preferencia.
8. Si la respuesta NO está respaldada por evidencia explícita suficiente, responde exactamente:
   SIN EVIDENCIA
9. Si existe evidencia parcial, escribe:
   EVIDENCIA PARCIAL
   y explica qué parte está respaldada y cuál no.
10. No inventes valores.

FORMATO

CV-01
Respuesta: ...
Evidencia:
- ... [fuente]
Conclusión: RESPALDADO | CONTRADICCIÓN | EVIDENCIA PARCIAL | SIN EVIDENCIA

Repite hasta CV-06.
```

## TURNO 4 · Reconstrucción después de la verificación

```text
Vuelve al borrador original y usa las respuestas independientes CV-01 a CV-06.

TAREA

Para cada afirmación del borrador:

- CONSERVAR si la verificación la respalda.
- CORREGIR si la verificación demuestra que está mal formulada.
- ACOTAR si solo una parte está respaldada.
- LLEVAR A DECISIÓN si las fuentes se contradicen o dejan el valor abierto.
- ELIMINAR si no existe evidencia y tampoco corresponde a una decisión explícita del equipo.

REGLAS

1. No cambies algo que la verificación confirmó.
2. No presentes una propuesta como hecho.
3. No conviertas "SIN EVIDENCIA" en una cifra inventada.
4. Si una corrección afecta una DEC, identifica el impacto.
5. Propaga una corrección a todos los artefactos afectados:
   - DEC;
   - RQF/RQNF;
   - PF/PX;
   - HU;
   - CU o secuencia, si corresponde.
6. Conserva IDs existentes.
7. No afirmes que DPRIME aprobó una regla si solo fue adoptada como base de análisis por el equipo.

FORMATO

CV-01
Resultado: CONSERVAR | CORREGIR | ACOTAR | LLEVAR A DECISIÓN | ELIMINAR
Cambio:
...
Impacto:
...

...

VERSIÓN FINAL RECONSTRUIDA
<texto corregido>

PROPAGACIÓN
- DEC afectadas:
- requisitos afectados:
- pruebas afectadas:
- historias afectadas:
- otros artefactos afectados:
```

---

# Técnica 5 · LLM-as-a-Judge
## Prompt completo

```text
LLM-AS-A-JUDGE — EVALUACIÓN DE LA ENTREGA 1 DE MIRA

Actúa exclusivamente como JUEZ de los artefactos entregados.

NO generes una nueva entrega desde cero.
NO reescribas requisitos para hacerlos pasar.
NO completes silenciosamente información faltante.
NO asumas que los artefactos son correctos.
NO otorgues una nota académica global.

FUENTES AUTORIZADAS PARA JUZGAR

1. Pauta "Entrega 1 — Articulación y análisis de requisitos asistido por LLM".
2. Documento MIRA completo.
5. Bitácora DEC.
6. Requisitos.
7. Pruebas funcionales y extra-funcionales.
8. Backlog y DoD.
9. Modelo de dominio.
10. Casos de uso.
11. Diagrama de secuencia.
12. Evidencia de las cinco técnicas de prompting.

CRITERIOS DE LA RÚBRICA

C1 — COMPLETITUD Y COHERENCIA DE ARTEFACTOS
Debe existir:
- modelo de dominio;
- casos de uso;
- requisitos funcionales y no funcionales;
- pruebas funcionales;
- pruebas extra-funcionales;
- backlog + DoD;
- diagrama de secuencia de sistema.

Además:
- deben usar vocabulario compatible;
- los IDs deben ser consistentes;
- una regla corregida debe propagarse a los artefactos dependientes.

C2 — PRECISIÓN Y TRAZABILIDAD
Toda afirmación relevante debe poder vincularse a:
- sección MIRA;
- entrevista;
- DEC explícita;
- o pauta, cuando corresponda.

Una cita inexistente o que no respalde lo afirmado es incumplimiento.

C3 — DETECCIÓN Y RESOLUCIÓN DE INCONSISTENCIAS
Los hallazgos deben:
- tener cita verificable;
- usar la taxonomía de la pauta;
- mostrar las fuentes en conflicto;
- enlazar a una DEC cuando requieran resolución;
- distinguir decisión del equipo de validación externa de DPRIME.

C4 — PRUEBAS FUNCIONALES Y EXTRA-FUNCIONALES
Para RQF Must:
- debe existir PF correspondiente;
- debe haber precondición, pasos/datos y resultado observable;
- los casos de uso críticos deben incluir al menos una excepción/alternativa probada.

Para RQNF:
- debe existir escenario;
- carga o condición;
- umbral medible;
- PX asociada.

No aceptar RNF vagos.

C5 — BACKLOG UTILIZABLE
Las historias deben:
- derivar de requisitos;
- tener criterios de aceptación verificables;
- tener prioridad;
- tener tamaño relativo;
- estar ordenadas por valor/riesgo;
- incluir DoD de 6 a 10 controles binarios.

C6 — TÉCNICAS DE PROMPTING
Deben existir al menos cinco técnicas efectivamente aplicadas.

Para cada técnica comprobar:
- nombre formal;
- tarea concreta;
- por qué era apropiada;
- antes/después o efecto observable;
- prompt real;
- salida real;
- límites de la aplicación.

Comprobar específicamente:
- Grounded: fuentes separadas, citas y vacíos marcados.
- Structured Output: esquema fijo y ausencias visibles.
- Plan-and-Solve: plan antes de ejecución.
- CoVe: preguntas, conversación nueva para verificar y reconstrucción.
- LLM-as-a-Judge: rúbrica explícita, evidencia y sin nota global.

C7 — DOCUMENTACIÓN DE DECISIONES
Cada DEC debe incluir:
- ID;
- fecha;
- asunto;
- contexto con fuentes;
- al menos dos alternativas;
- decisión;
- justificación;
- quién la validó;
- impacto.

El representante del cliente del equipo debe estar identificado.
No confundir validación del representante académico con aprobación real de DPRIME.

C8 — PRESENTACIÓN ORAL Y RESPUESTAS
Este criterio NO puede juzgarse completamente a partir de archivos.

Solo se puede revisar en los archivos:
- que el PPT exista;
- que sea coherente con el informe;
- que cubra el contenido exigido;
- que no afirme resultados inexistentes.

La exposición y respuestas reales deben marcarse:
NO EVALUABLE DESDE ARCHIVOS.

REGLA DE EVALUACIÓN

Para C1 a C7 responde solo:
CUMPLE
o
NO CUMPLE

Para C8 puede utilizarse:
CUMPLE EN ARTEFACTO
NO CUMPLE EN ARTEFACTO
NO EVALUABLE DESDE ARCHIVOS

Cada NO CUMPLE debe incluir evidencia concreta.
Cada CUMPLE debe incluir al menos una evidencia verificable.
No uses escalas 1-7.
No uses porcentajes de cumplimiento.
No entregues nota global.
No promedies criterios.
No compenses un incumplimiento con fortalezas de otro criterio.

FORMATO OBLIGATORIO

C1 — COMPLETITUD Y COHERENCIA
Resultado: CUMPLE | NO CUMPLE
Evidencia:
- <archivo/sección/ID>
Incumplimientos:
- <solo si existen>
Acción correctiva:
- <acción mínima necesaria>

C2 — PRECISIÓN Y TRAZABILIDAD
...

Repite hasta C8.

Después entrega:

HALLAZGOS CRÍTICOS
1. ...
2. ...
3. ...

CAMBIOS MÍNIMOS ANTES DE ENTREGAR
1. ...
2. ...
3. ...

LIMITACIONES DEL JUICIO
- El juez evalúa artefactos, no implementación.
- El juez no sustituye revisión humana.
- Si el mismo modelo participó en la creación de la entrega, existe riesgo de autopreferencia.
- La presentación oral real no puede evaluarse antes de que ocurra.

NO entregues una nota académica global.
```
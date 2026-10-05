---
title: "PRD: MIRA - Incremento F4 + F1"
status: final
version: "1.0"
created: 2026-10-03
updated: 2026-10-03
source_brief: "../../briefs/brief-Software-asistido-por-LLMs-2026-09-27-v2/brief.md"
---

# PRD: MIRA - Incremento F4 + F1

## 0. Propósito del documento

Este PRD convierte el Product Brief V2 validado en requisitos funcionales y no funcionales para el incremento académico de MIRA formado por **F4 - Política de decisión** y **F1 - Bandeja de revisión asistida**. Está dirigido al representante del cliente, UX, arquitectura, desarrollo y QA. Conserva los identificadores de la Entrega 1 como origen y asigna IDs `FR-N` estables para los workflows posteriores. Define capacidades y resultados verificables; las decisiones técnicas se reservan para arquitectura y el addendum.

## 1. Visión y tesis del incremento

MIRA busca automatizar decisiones sobre evidencia sin sacrificar confianza ni auditabilidad. Este incremento prueba una tesis concreta: la automatización solo aporta valor cuando aprueba de forma conservadora los casos que superan todas las barreras y entrega al operador suficiente contexto para resolver el resto con criterio propio.

F4 consume casos ficticios que ya contienen puntaje, componentes y señales; no calcula scoring. Aplica una política versionada y produce una salida explicable. F1 recibe los casos en **REVISIÓN** y los **ESCALADOS**, presenta evidencia y razones antes del puntaje y permite registrar una decisión humana motivada. Un caso **ESCALADO** es una revisión prioritaria con marca para supervisor, nunca un rechazo ni un cierre automático.

El resultado esperado no es una versión productiva de MIRA. Es una aplicación web en español, reproducible y trazable, que permite demostrar ambas funcionalidades de extremo a extremo con datos ficticios controlados.

## 2. Usuarios y trabajos por realizar

### 2.1 Usuarios principales

- **Operador de revisión:** necesita localizar la evidencia relevante, comprender por qué se derivó un caso y resolverlo sin consultar varios sistemas.
- **Responsable de riesgo o representante del cliente:** necesita comprobar que las aprobaciones automáticas respetan todas las barreras y que nunca existe rechazo automático.
- **Supervisor:** necesita que los casos de riesgo o vencidos queden marcados para atención prioritaria; su panel agregado no forma parte de este incremento.
- **Evaluador o QA:** necesita ejecutar casos controlados, reconstruir el resultado y seguir cada requisito hasta su prueba y commit.

### 2.2 No usuarios de este incremento

- La persona cuyos datos representa la evidencia no interactúa con la aplicación.
- El equipo de modelos no configura ni entrena modelos reales en este incremento.
- Administradores de clientes no gestionan módulos, umbrales o flujos mediante interfaces propias.

### 2.3 Recorridos de usuario

#### UJ-1. Marco resuelve un caso en revisión con la evidencia a la vista

Marco, operador de la aseguradora piloto, abre la Bandeja y selecciona un caso en **REVISIÓN**. Ve primero la evidencia, la razón de derivación y la ubicación del hallazgo; después consulta el Puntaje y las Señales. Decide solicitar antecedentes, selecciona una Categoría de motivo y confirma. El Caso cambia a **ESPERANDO ANTECEDENTES** y conserva la Evaluación que originó la revisión.

#### UJ-2. Marco corrige un dato sin borrar el original

Marco abre un Caso cuyo monto fue leído como `120000`. Desde la evidencia localizada confirma que el valor correcto es `100000`, registra la Corrección y selecciona su Categoría de motivo. La interfaz muestra ambos valores y la Intervención humana queda asociada a la Versión del caso vigente.

#### UJ-3. Marco recibe una advertencia de concurrencia

Marco abre una Versión del caso mientras otra sesión registra una decisión sobre una versión más reciente. Cuando intenta guardar, el sistema rechaza la operación, conserva la Decisión humana vigente y le indica que debe recargar el Caso.

#### UJ-4. Sebastián valida la política y el recorrido F4 → F1

Sebastián, representante del cliente E2, ejecuta los Casos controlados. Comprueba las fronteras de la Política, observa que un Caso **ESCALADO** ingresa a F1 con prioridad y marca para supervisor, y completa una Decisión humana desde la interfaz sin editar datos manualmente ni usar herramientas de desarrollo.

## 3. Glosario

- **Caso:** unidad de trabajo identificable que agrupa entradas, Evaluaciones e Intervenciones humanas.
- **Versión del caso:** revisión concreta del Caso sobre la que se intenta decidir; una versión obsoleta no puede sobrescribir la vigente.
- **Evidencia:** PDF o imagen ficticia asociada a un Caso controlado.
- **Señal:** resultado simulado que acompaña al Puntaje; en este incremento son Autenticidad documental, Coherencia entre evidencias y Fraude detectado.
- **Puntaje:** valor simulado entre `0` y `100`; F4 lo consume y no lo calcula.
- **Política:** conjunto ordenado y versionado de reglas y parámetros que transforma Puntaje y Señales en una Salida F4.
- **Evaluación:** aplicación de una Versión de política a una Versión del caso.
- **Salida F4:** uno de `ERROR / DERIVACIÓN`, `ESCALADO`, `APROBADO AUTOMÁTICAMENTE` o `REVISIÓN`.
- **Bandeja:** superficie de F1 con Casos en `REVISIÓN` o `ESCALADO` pendientes de Decisión humana.
- **Decisión humana:** acción del Operador: aprobar, rechazar o solicitar antecedentes.
- **Categoría de motivo:** opción obligatoria que justifica una Decisión humana o Corrección.
- **Corrección:** cambio trazable de un dato interpretado, conservando el valor original.
- **Ubicación del hallazgo:** referencia estructurada a página y campo o región en PDF, o a región y coordenadas opcionales en imagen.
- **Intervención humana:** Decisión humana o Corrección registrada sobre una Versión del caso.
- **Discrepancia:** diferencia entre la sugerencia de la plataforma y la Decisión humana.
- **Plazo interno:** meta de `3` días hábiles desde el ingreso controlado.
- **Plazo contractual:** compromiso de `5` días hábiles desde el ingreso controlado.
- **Caso controlado:** fixture ficticio y reproducible con entradas y resultado esperado.

## 4. Funcionalidades y requisitos

### 4.1 F4 - Política de decisión

F4 realiza una Evaluación determinista sobre un Caso controlado. La precedencia de reglas es parte del requisito: validar entradas, aplicar fraude, aplicar el límite inferior, comprobar las barreras de aprobación y enviar cualquier otro Caso a revisión.

#### FR-1. Validar Puntaje y Señales (origen: RQF-004)

El sistema debe validar el Puntaje y las Señales requeridas antes de aplicar la Política.

**Consecuencias verificables:**
- Un Puntaje no numérico o fuera de `[0,100]` produce `ERROR / DERIVACIÓN`.
- Una Señal numérica presente fuera de `[0,100]` impide la aprobación automática y produce un error identificable.
- Una Señal requerida ausente nunca se interpreta como favorable.
- `ERROR / DERIVACIÓN` aparece inline en Resultado F4, conserva entradas, identifica campo y causa, ofrece `Corregir entradas` y no crea una fila F1. La acción vuelve a Ejecutar F4 con el mismo Caso y borrador transitorio, enfoca el primer campo inválido y permite reejecutar sin modificar el fixture versionado.

#### FR-2. Aplicar precedencia de fraude y Puntaje bajo (origen: RQF-004, DEC-01)

El sistema debe producir `ESCALADO` si Fraude detectado es verdadero o si el Puntaje es menor que `60`.

**Consecuencias verificables:**
- Fraude detectado prevalece sobre Puntaje, mínimos y automatización.
- `59,99` produce `ESCALADO`; `60` no activa esta regla.
- `ESCALADO` nunca produce rechazo ni cierre automático.

#### FR-3. Aprobar solo con todas las barreras cumplidas (origen: RQF-004, RQNF-009)

El sistema debe producir `APROBADO AUTOMÁTICAMENTE` únicamente cuando automatización está `ON`, Puntaje es mayor que `90`, Autenticidad documental es al menos `70`, Coherencia entre evidencias es al menos `70` y no existe fraude.

**Consecuencias verificables:**
- `90` produce `REVISIÓN`; `90,01` puede aprobar.
- `69,99` en cualquiera de las Señales numéricas impide la aprobación.
- Automatización `OFF` impide la aprobación aunque las demás barreras se cumplan.

#### FR-4. Derivar los demás Casos a revisión (origen: RQF-004, RQF-005)

El sistema debe producir `REVISIÓN` para todo Caso válido que no cumpla una regla anterior.

**Consecuencias verificables:**
- Los Puntajes de `60` a `90`, ambos incluidos, producen `REVISIÓN` si no existe fraude.
- Una Señal requerida ausente o bajo su mínimo produce `REVISIÓN` cuando no corresponde `ESCALADO`.
- No existe una ruta de rechazo automático.

#### FR-5. Usar una Política configurable y versionada (origen: RQF-004, RQF-008)

El sistema debe leer `T=90`, mínimos `70/100` y estado de automatización desde una Política identificada por versión.

**Consecuencias verificables:**
- Cada Evaluación registra la Versión de política aplicada y sus parámetros efectivos.
- Cambiar parámetros en la configuración de prueba no reescribe Evaluaciones anteriores.
- La interfaz de administración de umbrales de F5 no forma parte de este incremento.

#### FR-6. Explicar la Salida F4 (origen: RQF-003, RQF-008)

El sistema debe acompañar cada Salida F4 con Puntaje, Señales, regla aplicada y razones comprensibles.

**Consecuencias verificables:**
- La explicación permite distinguir fraude, Puntaje bajo, barrera insuficiente y automatización desactivada.
- La salida conserva los valores simulados recibidos; no inventa componentes ni fórmula de scoring.
- F1 puede presentar la razón sin recalcular la Evaluación.

### 4.2 F1 - Bandeja de revisión asistida

F1 recibe Casos en `REVISIÓN` con prioridad normal y Casos `ESCALADOS` con prioridad alta y marca para supervisor. La Bandeja facilita una revisión significativa y evita que la sugerencia de la plataforma sustituya el criterio del Operador.

#### FR-7. Enrutar Casos a la Bandeja (origen: RQF-005; validación posterior al brief)

El sistema debe ingresar a la Bandeja los Casos con Salida F4 `REVISIÓN` o `ESCALADO`.

**Consecuencias verificables:**
- `REVISIÓN` ingresa con prioridad normal.
- `ESCALADO` ingresa con prioridad alta y marca para supervisor.
- `APROBADO AUTOMÁTICAMENTE` no ingresa a la Bandeja.

#### FR-8. Mostrar contexto operativo en la lista (origen: RQF-005, RQF-014)

La Bandeja debe mostrar para cada Caso su identificador, Salida F4, razón principal, prioridad, estado, Plazo interno y Plazo contractual.

**Consecuencias verificables:**
- Los Casos prioritarios y vencidos se distinguen sin abrir el detalle.
- La lista no expone datos personales reales.

#### FR-9. Presentar Evidencia y razones antes del Puntaje (origen: RQF-005, DEC-11)

El detalle debe presentar Evidencia, razón de derivación y Ubicación del hallazgo antes del Puntaje y las Señales.

**Consecuencias verificables:**
- Un PDF muestra página y campo o región.
- Una imagen muestra nombre de región y, si existen, coordenadas.
- El Operador puede comprender qué revisar antes de ver la sugerencia numérica.

#### FR-10. Registrar Decisiones humanas (origen: RQF-005)

El Operador debe poder aprobar, rechazar o solicitar antecedentes desde el detalle de un Caso pendiente.

**Consecuencias verificables:**
- Aprobar cambia el estado a `APROBADO`.
- Rechazar cambia el estado a `RECHAZADO` y nunca puede originarse en F4.
- Solicitar antecedentes cambia el estado a `ESPERANDO ANTECEDENTES`.

#### FR-11. Exigir una Categoría de motivo (origen: RQF-005, DEC-E2-05)

Toda Decisión humana y Corrección debe incluir una Categoría de motivo.

**Consecuencias verificables:**
- La confirmación se bloquea si falta la Categoría de motivo.
- El comentario es opcional para categorías predefinidas.
- Si la categoría es `Otro`, el comentario es obligatorio.

**Catálogo inicial por acción:**
- Aprobar: `requirements_met` — Requisitos cumplidos; `evidence_consistent` — Evidencia consistente.
- Rechazar: `requirements_not_met` — Requisitos no cumplidos; `evidence_inconsistent` — Evidencia inconsistente.
- Solicitar antecedentes: `information_incomplete` — Antecedentes incompletos; `evidence_unreadable` — Evidencia ilegible; `clarification_required` — Aclaración requerida.
- Corregir: `extraction_error` — Error de extracción; `evidence_value_mismatch` — Dato no coincide con la Evidencia.
- Todas: `other` — Otro; exige comentario no vacío y las combinaciones incompatibles se rechazan.

#### FR-12. Corregir sin borrar el original (origen: RQF-005, DEC-11)

El Operador debe poder registrar una Corrección con valor original, valor corregido y motivo.

**Consecuencias verificables:**
- El escenario `120000 → 100000` conserva ambos valores.
- La Corrección registra Operador, fecha controlada y Versión del caso.
- Una Corrección no modifica silenciosamente la Evidencia original.

#### FR-13. Proteger la Decisión vigente (origen: RQF-005, DEC-08)

El sistema debe rechazar una Intervención humana basada en una Versión del caso obsoleta.

**Consecuencias verificables:**
- La Decisión humana vigente no se sobrescribe.
- El Operador recibe una indicación para recargar el Caso.
- El intento fallido queda distinguible de una Decisión humana confirmada.

#### FR-14. Marcar Discrepancias (origen: RQF-005, DEC-11)

El sistema debe marcar cuando la Decisión humana difiere de la sugerencia de la plataforma.

**Consecuencias verificables:**
- La marca no altera ni invalida la Decisión humana.
- La Discrepancia queda asociada a la Evaluación y a la Intervención humana.
- La revisión posterior por el equipo de modelos queda fuera del incremento.

#### FR-15. Calcular plazos reproducibles (origen: RQF-014, DEC-E2-07)

El sistema debe calcular Plazo interno y Plazo contractual usando `America/Santiago`, calendario de lunes a viernes y fecha de ingreso controlada.

**Consecuencias verificables:**
- El Plazo interno vence a los `3` días hábiles.
- El Plazo contractual vence a los `5` días hábiles.
- Fines de semana no consumen días hábiles.

#### FR-16. Alertar proximidad y vencimiento (origen: RQF-014)

El sistema debe mostrar una alerta un día hábil antes de cada vencimiento y otra al vencer.

**Consecuencias verificables:**
- Las alertas se derivan de la fecha controlada, no del reloj real durante las pruebas.
- Un Caso vencido permanece abierto.
- El vencimiento contractual eleva la prioridad y mantiene la marca para supervisor.

### 4.3 Trazabilidad y demostración controlada

#### FR-17. Conservar la procedencia de cada resultado (origen: RQF-008)

El sistema debe conservar para cada Caso controlado las entradas simuladas, Versión de política, Salida F4, explicación e Intervenciones humanas.

**Consecuencias verificables:**
- Un evaluador puede reconstruir qué Política y datos originaron una salida.
- Las Intervenciones humanas no borran entradas ni resultados previos.
- El alcance no exige implementar el expediente completo de F6.

#### FR-18. Proveer Casos controlados ficticios (origen: Entrega 2 §4.3)

El repositorio debe incluir Casos controlados con Evidencia ficticia y resultados esperados.

**Consecuencias verificables:**
- No se incluyen datos personales reales.
- Los Casos cubren las fronteras, excepciones y recorridos definidos en §9.
- Las mismas entradas producen los mismos resultados en ejecución local y pruebas automatizadas.

#### FR-19. Permitir el recorrido completo desde la interfaz (origen: Entrega 2 §4.4)

Un evaluador debe poder ejecutar F4, abrir los Casos derivados en F1 y registrar una Intervención humana sin editar la base de datos ni usar herramientas de desarrollo.

**Consecuencias verificables:**
- La interfaz está en español.
- F4 y F1 están conectadas por los mismos Casos controlados.
- El README permite levantar el sistema y cargar los datos de prueba.

#### FR-20. Mantener trazabilidad de desarrollo (origen: Entrega 2 §1.3 y §3.3)

Cada requisito Must incluido debe poder seguirse desde su ID E1 hasta artefacto BMAD, historia o tarea, código, prueba y commit.

**Consecuencias verificables:**
- Los artefactos posteriores citan los IDs `FR-N` y los IDs E1 de origen.
- Las pruebas nombran el requisito o criterio que verifican.
- Las correcciones humanas a artefactos generados quedan visibles en commits separados cuando corresponda.

## 5. Requisitos no funcionales

### NFR-1. Calidad de decisión antes de ampliar automatización (origen: RQNF-009, Must)

La automatización debe permanecer restringida a la Política del piloto y al corpus controlado hasta que PX-09 demuestre los resultados esperados. No existe una meta de tasa de aprobación automática.

### NFR-2. Usabilidad de revisión significativa (origen: RQNF-005, Should)

Una persona externa al equipo debe completar una tarea de F4 y una de F1 sin instrucciones previas. Se registran finalización, tiempo y dificultades; la Evidencia y las razones deben aparecer antes del Puntaje.

### NFR-3. Rendimiento de pantalla (origen: RQNF-001, Must)

La apertura del detalle desde la Bandeja debe alcanzar `p95 ≤ 2 s` con 100 Casos y 3 Evidencias por Caso, Django + SQLite local limitado a 2 vCPU/4 GiB, 5 ejecuciones de calentamiento y 30 muestras medidas.

### NFR-4. Consumo de recursos (origen: RQNF-008, Should)

PX-08 debe ejecutar 30 revisiones Playwright y medir con `psutil` los árboles de procesos de Django y Chromium durante toda la sesión. El criterio es RSS máximo agregado `≤ 1 GiB` y CPU promedio agregado `≤ 1 núcleo lógico`.

### NFR-5. Determinismo y reproducibilidad

La misma Versión de política y el mismo Caso controlado deben producir la misma Salida F4. Las pruebas de plazos deben usar fechas controladas.

### NFR-6. Seguridad y privacidad del incremento

Los datos de demostración deben ser ficticios. Credenciales o secretos no deben incluirse en Casos controlados, registros ni repositorio.

## 6. Restricciones y salvaguardas

### 6.1 Seguridad de decisión

- Nunca existe rechazo automático.
- Fraude detectado y Puntaje menor que `60` producen revisión prioritaria, no decisión adversa automática.
- Una Señal ausente nunca se interpreta como favorable.
- Una Versión del caso obsoleta nunca sobrescribe la Decisión humana vigente.

### 6.2 Control humano

- Evidencia, razón y Ubicación del hallazgo preceden al Puntaje.
- Toda Decisión humana y Corrección requiere una Categoría de motivo.
- Medir casos por hora no es un objetivo del incremento.

### 6.3 Datos y pruebas

- Solo se usan Evidencias ficticias.
- Los tiempos de prueba se controlan explícitamente.
- El motor multimodal se simula; no se realizan inferencias sobre archivos reales.

## 7. No objetivos

- Calcular el Puntaje o entrenar un modelo multimodal.
- Presentar `T=90` o mínimos `70/100` como parámetros definitivos de MIRA.
- Implementar rechazo automático.
- Construir F2, F3 o F5-F9, incluido el panel agregado del supervisor y el expediente completo.
- Resolver autenticación, multitenencia, facturación, residencia o retención productiva de datos.
- Definir stack, persistencia o despliegue dentro del PRD.
- Modificar retroactivamente artefactos de la Entrega 1.

## 8. Alcance MVP

### 8.1 Incluido

- Política F4 completa y versionada sobre datos simulados.
- Bandeja F1 con lista, detalle, evidencia localizada, razones, plazos y acciones humanas.
- Entrada prioritaria de Casos `ESCALADOS` con marca para supervisor.
- Correcciones trazables, Discrepancias y protección contra Versión del caso obsoleta.
- Casos controlados, fechas controladas, pruebas automatizadas y recorridos E2E.
- README reproducible y trazabilidad hasta commits.

### 8.2 Fuera del MVP

- Gestión de nueva Evidencia y reapertura completa de Casos según DEC-08.
- Cierre por falta de antecedentes: requiere reglas adicionales y no es necesario para demostrar F4 → F1.
- Integraciones API, correo o sistemas centrales del cliente.

## 9. Catálogo mínimo de Casos controlados

### 9.1 Casos F4 derivados de PF-04

| ID | Puntaje | Autenticidad | Coherencia | Fraude | Auto | Resultado esperado |
|---|---:|---:|---:|---|---|---|
| CC-F4-01 | 59,99 | 80 | 80 | No | ON | `ESCALADO` |
| CC-F4-02 | 60 | 80 | 80 | No | ON | `REVISIÓN` |
| CC-F4-03 | 90 | 80 | 80 | No | ON | `REVISIÓN` |
| CC-F4-04 | 90,01 | 70 | 70 | No | ON | `APROBADO AUTOMÁTICAMENTE` |
| CC-F4-05 | 95 | 90 | 90 | Sí | ON | `ESCALADO` |
| CC-F4-06 | 95 | 69,99 | 90 | No | ON | `REVISIÓN` |
| CC-F4-07 | 95 | Ausente | 90 | No | ON | `REVISIÓN` |
| CC-F4-08 | 95 | 90 | 90 | No | OFF | `REVISIÓN` |
| CC-F4-09 | 101 | 90 | 90 | No | ON | `ERROR / DERIVACIÓN` |

### 9.2 Casos F1 derivados de PF-05 y PF-14

- **CC-F1-01:** Corrección `120000 → 100000`; conserva original, valor corregido y motivo.
- **CC-F1-02:** Rechazo sin Categoría de motivo; la confirmación se bloquea.
- **CC-F1-03:** Solicitud de antecedentes con motivo; cambia a `ESPERANDO ANTECEDENTES`.
- **CC-F1-04:** Decisión sobre Versión del caso obsoleta; se rechaza sin sobrescribir la vigente.
- **CC-F1-05:** Fecha controlada próxima al Plazo interno; muestra alerta un día hábil antes.
- **CC-F1-06:** Plazo contractual vencido; el Caso sigue abierto, eleva prioridad y mantiene marca para supervisor.

## 10. Métricas de éxito

### Primarias

- **SM-1:** `100 %` de los Casos controlados F4 produce el resultado esperado. Valida FR-1 a FR-6.
- **SM-2:** `100 %` de los escenarios PF-05 conserva motivos, originales y Decisión humana vigente. Valida FR-10 a FR-14.
- **SM-3:** `100 %` de los escenarios PF-14 calcula y alerta correctamente con calendario L-V y fechas controladas. Valida FR-15 y FR-16.
- **SM-4:** Un evaluador clona el repositorio, sigue el README y ejecuta F4 → F1 en menos de `15` minutos. Valida FR-18 y FR-19.
- **SM-5:** `100 %` de los requisitos Must del alcance tiene vínculo verificable con artefacto, código, prueba y commit. Valida FR-20.

### Secundarias

- **SM-6:** Una persona externa completa una tarea de F4 y una de F1 sin instrucciones previas; se registran tiempo y dificultades. Valida NFR-2.
- **SM-7:** Ningún Caso produce rechazo automático. Valida FR-2 a FR-4 y el guardrail de decisión.

### Contramétricas

- **SM-C1:** No maximizar la proporción de aprobaciones automáticas; ampliar automatización sin PX-09 exitoso se considera fallo.
- **SM-C2:** No optimizar casos resueltos por hora a costa de la lectura de Evidencia y razones.
- **SM-C3:** No reducir tiempos eliminando motivo, procedencia o protección de concurrencia.

## 11. Responsables y aprobaciones

- **Sebastián Rodríguez, representante del cliente E2:** valida este PRD y acepta o rechaza las funcionalidades contra sus criterios.
- **Grupo conformado por: Francisca Meyer, Lukas Scheel y Sebastián Rodríguez.** El equipo revisa cada artefacto BMAD antes de avanzar.
- **UX:** convierte UJ-1 a UJ-4 y FR-7 a FR-16 en especificación de interfaz en español.
- **Arquitectura:** resuelve stack, persistencia, control de concurrencia y aplicabilidad de NFR-3/NFR-4.
- **QA:** deriva pruebas automatizadas de PF-04, PF-05, PF-14, PX-05, PX-08 y PX-09 sin copiar el comportamiento accidental de la implementación.

## 12. Riesgos y mitigaciones

- **Sesgo de automatización:** mostrar primero Evidencia y razones; medir usabilidad, no velocidad aislada.
- **Aprobación indebida:** aplicar precedencia estricta, límites exactos y automatización desactivable.
- **Concurrencia:** bloquear Intervenciones humanas sobre versiones obsoletas y conservar la vigente.
- **Deriva de alcance:** mantener F5-F9 y decisiones productivas en No objetivos y addendum.
- **Pruebas autorreferentes:** derivar resultados de PF/PX y Casos controlados antes del código.
- **Demo no reproducible:** usar fechas y Evidencias fijas, más README verificable desde un clon limpio.

## 13. Preguntas abiertas

1. **OQ-1 - Categorías de motivo — RESUELTA 2026-10-03:** catálogo específico por acción definido en FR-11 y `domain-contracts.md`; `other` exige comentario. Responsables: PM + Sebastián.
2. **OQ-2 - Rendimiento — RESUELTA 2026-10-03:** apertura Bandeja → detalle; 100 Casos y 3 Evidencias por Caso; Django + SQLite local en 2 vCPU/4 GiB; 5 calentamientos y 30 muestras; `p95 ≤ 2 s`. Responsables: Arquitectura + Sebastián.
3. **OQ-3 - Recursos — RESUELTA 2026-10-03:** 30 revisiones Playwright, medición de los árboles de procesos de Django y Chromium con `psutil`, RSS máximo agregado `≤ 1 GiB` y CPU promedio agregado `≤ 1 núcleo lógico`. Responsables: QA + Arquitectura.
4. **OQ-4 - Tecnología — RESUELTA 2026-10-03:** Python 3.13.16, Django 5.2.18 LTS, SQLite local, Playwright Python 1.63.0 y concurrencia optimista por `expected_case_version`. Responsable: Arquitectura.
5. **OQ-5 - Error / Derivación — RESUELTA 2026-10-03:** resultado inline en Resultado F4, con entradas conservadas, campo y causa, acción `Corregir entradas` hacia el mismo borrador transitorio y sin fila F1 ni mutación del fixture. Responsables: UX + PM.

## 14. Índice de supuestos y notas

- No se introducen supuestos funcionales no confirmados: las decisiones de política, plazos, conexión F4 → F1 y alcance provienen del brief, baseline y validación posterior.
- OQ-2 a OQ-4 quedaron resueltas el 2026-10-03 en la story 1.1 y sus criterios ejecutables viven en NFR-3, NFR-4 y la Architecture Spine.
- OQ-1 a OQ-5 quedaron resueltas; identidad de marca, tipografía y modo oscuro permanecen como decisiones visuales no bloqueantes fuera de estos requisitos funcionales.

## 15. Fuentes

- `_bmad-output/planning-artifacts/briefs/brief-Software-asistido-por-LLMs-2026-09-27-v2/brief.md`
- `LLM - MIRA_Entrega2_bitacora_decisiones.md`, incluida la sección 13 de validación.
- `LLM - MIRA_E2_Baseline_F4_F1.md`
- `Contexto-fase1-bmad/LLM - Entrega_2_MIRA_SDD_BMAD.pdf`

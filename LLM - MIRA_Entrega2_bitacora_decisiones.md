# Bitácora resumida de decisiones — MIRA Entrega 2

> Documento de trazabilidad resumida del trabajo realizado para la Entrega 2.  
> Se actualizará durante el proyecto con nuevas decisiones, aclaraciones y cambios relevantes.

## 1. Revisión inicial de antecedentes
- Se revisaron como contexto:
  - Descripción original del proyecto MIRA.
  - Enunciado de la Entrega 1.
  - Enunciado de la Entrega 2.
- Se determinó que la Entrega 2 exige transformar la línea base de requisitos de la Entrega 1 en un incremento funcional y trazable.
- Se identificó como foco principal de la Entrega 2 la trazabilidad entre requisitos, artefactos del método, implementación, commits y pruebas.
- Se estableció que deben implementarse dos funcionalidades conectadas entre sí, con interfaz y lógica de negocio.
- Se confirmó que el motor multimodal real no se implementará; se utilizarán casos y datos simulados según el enunciado.

## 2. Validación de la Entrega 1 como línea base
- Se recibió y analizó la Entrega 1 final del equipo.
- Integrantes confirmados:
  - Lukas Scheel.
  - Francisca Meyer.
  - Sebastián Rodríguez.
- Representante del cliente en Entrega 1: Lukas Scheel.
- Se confirmó que las decisiones DEC-01 a DEC-16 fueron aceptadas y ratificadas.
- Se confirmó que la Entrega 1 obtuvo una evaluación muy buena y se tomará como línea base correcta para la Entrega 2.
- Decisión: no se modificarán retroactivamente los artefactos de la Entrega 1; cualquier cambio posterior se registrará como evolución o nueva decisión.

## 3. Evaluación de funcionalidades para el incremento
- Se compararon las combinaciones posibles de funcionalidades F1–F9 según:
  - Trazabilidad con requisitos de la Entrega 1.
  - Decisiones y hallazgos asociados.
  - Historias de usuario y pruebas reutilizables.
  - Conexión funcional entre módulos.
  - Complejidad de implementación.
  - Claridad para la demostración.
- Se identificaron como combinaciones más convenientes:
  - F4 + F1.
  - F5 + F4.
  - F1 + F6.
- Decisión final: implementar **F4 + F1**.

## 4. Alcance funcional seleccionado
- **F4 — Puntaje y decisión por umbrales**
  - Calcula la decisión a partir del puntaje, componentes, mínimos por señal y precedencia de fraude.
- **F1 — Bandeja de revisión asistida**
  - Recibe casos derivados, muestra señales/evidencia y permite al operador tomar una decisión fundamentada.
- Relación definida:
  - F4 produce la decisión automática.
  - Los casos que requieren revisión son consumidos por F1.
- Se identificó H-15 (mínimos individuales de señales) como un punto especialmente relevante para reabrir o precisar durante la aplicación de BMAD.

## 5. Método de desarrollo
- Se evaluaron SDD y BMAD.
- Decisión final del equipo: utilizar **BMAD** para la Entrega 2.
- Los artefactos deberán generarse y revisarse siguiendo los roles/fases de BMAD y mantenerse versionados en el repositorio.

## 6. Representante del cliente para Entrega 2
- La Entrega 2 exige rotación del representante del cliente.
- Como Lukas ejerció el rol en Entrega 1, no puede repetirlo.
- Decisión final: **Sebastián Rodríguez será el representante del cliente en la Entrega 2**.

## 7. Regla de trabajo para la trazabilidad
- Decisión: mantener esta bitácora `.md` durante todo el desarrollo.
- Toda decisión relevante dada por el equipo o tomada durante el trabajo se añadirá cronológicamente.
- El registro será resumido, en formato de punteo, evitando detalle excesivo.
- Cuando una decisión anterior cambie, se registrará la nueva decisión sin borrar la anterior.

## 8. Construcción de baseline específica para F4 + F1
- Se extrajeron de la Entrega 1 los artefactos directamente relacionados con el incremento.
- Requisitos funcionales directos seleccionados:
  - F4: RQF-004.
  - F1: RQF-005 y RQF-014.
- Requisitos de apoyo identificados:
  - RQF-003 y RQF-008.
  - RQNF-009 para F4.
  - RQNF-005 y RQNF-008 para F1.
  - RQNF-001 queda como requisito transversal candidato a confirmar en arquitectura.
- Decisiones E1 de referencia: DEC-01, DEC-08, DEC-10 y DEC-11.
- Hallazgos principales: H-01, H-02, H-08, H-15, H-16 y H-18.
- Historias de origen: HU-03 y HU-04.
- Pruebas de origen principales: PF-04, PF-05, PF-14, PX-05, PX-08 y PX-09.
- Se confirmó la relación funcional **F4 → F1**: F4 determina la salida del caso y F1 consume los casos derivados a revisión.
- Se decidió no inventar información faltante durante esta extracción; los vacíos se convertirán en preguntas BMAD para Sebastián.
- Se identificó H-15 como el principal vacío activo: los mínimos concretos por señal no están definidos.
- Se detectó una aclaración adicional necesaria: E2 entrega el puntaje y componentes en los casos simulados, por lo que debe confirmarse que F4 consume ese puntaje y aplica la política, sin inventar una fórmula de scoring.

## 9. Resolución de aclaraciones funcionales para F4 + F1
- Se resolvieron las preguntas abiertas detectadas antes de construir el Project Brief de BMAD.
- **DEC-E2-01 — Mínimos por señal:** para este incremento se fija un mínimo de **70/100** para cada señal numérica obligatoria. La referencia proviene de PF-04 de la Entrega 1, que ya prueba el límite `m=70`. La señal de fraude no usa mínimo numérico: funciona como veto/precedencia.
- **DEC-E2-02 — Umbral operativo:** se adopta **T=90** como umbral operativo del incremento y de los datos de prueba. Se mantiene configurable y se declara válido solo para este incremento/piloto; no se presenta como valor definitivo del producto completo.
- **DEC-E2-03 — Responsabilidad de F4:** F4 **no calcula el puntaje**. Consume el puntaje, sus componentes y señales entregados por el motor simulado y aplica exclusivamente la política de decisión. No se inventará una fórmula de scoring no especificada en E1.
- **DEC-E2-04 — Señales obligatorias del incremento:** se utilizarán dos señales numéricas obligatorias: **autenticidad documental** y **coherencia entre evidencias**, ambas en escala 0–100 y con mínimo 70. Además se utilizará **fraude detectado** como señal booleana de precedencia: si es verdadera, el caso escala independientemente del puntaje.
- **DEC-E2-05 — Motivo de decisión humana:** F1 exigirá un motivo obligatorio para **aprobar, rechazar y solicitar antecedentes**. También se exigirá motivo para corregir un dato. Para reducir fricción, el motivo se registrará mediante una categoría obligatoria y un comentario opcional; si se elige “Otro”, el comentario será obligatorio.
- **DEC-E2-06 — Ubicación del hallazgo:** la ubicación se almacenará de forma estructurada y se mostrará de forma comprensible. Para PDF: **página + campo/región**. Para imagen: **nombre de región + coordenadas opcionales**. La interfaz priorizará la descripción legible por una persona.
- **DEC-E2-07 — Plazos de revisión:** se mantienen los criterios ratificados de E1 para el incremento: **3 días hábiles como meta interna**, **5 días hábiles como compromiso contractual**, zona horaria **America/Santiago**, calendario **lunes a viernes**, alerta **1 día hábil antes** y al vencimiento; un caso vencido permanece abierto y escala, sin cierre automático.
- Para pruebas y demo, las fechas de ingreso serán datos controlados/fijos para que los resultados sean reproducibles.
- Con estas aclaraciones se considera suficiente la baseline para pasar al **Project Brief del rol Analyst de BMAD**.

## 10. Sincronización documental previa a BMAD Analyst
- Se actualizó `MIRA_E2_Baseline_F4_F1.md` con las decisiones DEC-E2-01 a DEC-E2-07.
- Las preguntas Q-01 a Q-07 quedaron marcadas como resueltas y vinculadas a sus decisiones.
- Se incorporó a la baseline la política operativa vigente de F4.
- La baseline F4 + F1 queda cerrada como entrada oficial para el rol **Analyst** de BMAD.
- Próximo paso confirmado: construir el **Project Brief**.

## 11. Preparación del repositorio para BMAD
- Se subieron al repositorio de GitHub los archivos:
  - `MIRA_E2_Baseline_F4_F1.md`.
  - `MIRA_Entrega2_bitacora_decisiones.md`.
- Estos documentos quedan disponibles como insumos iniciales para la carga en BMAD.
- Próxima acción operativa: un integrante del equipo realizará la carga/configuración en BMAD e iniciará el rol **Analyst** para generar el **Project Brief**.
- Regla: conservar en el repositorio la salida original generada por BMAD y cualquier corrección humana posterior como evidencia separada.

## 12. Confirmación del primer workflow BMAD
- Se revisó el material de clases de BMAD.
- En BMAD, `bmad-product-brief` pertenece a la fase de **Análisis** y produce `brief.md` (y eventualmente `addendum.md`).
- Aunque la fase de análisis puede ser opcional en proyectos pequeños, para esta Entrega 2 **sí se utilizará**, porque el enunciado exige explícitamente que el rol Analyst produzca un **Project Brief** construido desde la Entrega 1.
- Decisión: el primer workflow BMAD del proyecto será **`bmad-product-brief`**.
- Después de revisar y aceptar el `brief.md`, el siguiente workflow será **`bmad-prd`**.

## 13. Validación del Product Brief V2 y ajustes para PRD

- Se revisó el Product Brief V2 generado por BMAD.
- Se valida como base suficiente para avanzar al PRD.
- Se mantiene el alcance F4 + F1.
- Se confirma que F4 consume puntaje y señales simuladas; no calcula scoring.
- Se confirma que no existe rechazo automático.
- Se confirma T=90 y mínimos 70/100 como parámetros del incremento, configurables y no definitivos del producto completo.
- Se decide que ESCALADO significa revisión prioritaria con marca para supervisor, sin cierre automático.
- Se decide que la primera implementación usará datos ficticios controlados para demo y pruebas.
- Se decide que el PRD deberá fijar casos de prueba controlados antes de implementar.
- Representante del cliente E2: Sebastián Rodríguez.
- Estado: brief validado con observaciones para PRD.


## 14. Candidato local persistente y cierre técnico — 2026-10-04

- DEC-E2-08: desacuerdo declarado con motivo; Corrección marca Discrepancia, decisión sola no.
- Implementación local en main `a59ab9c52324c0812eea0433966a70ed7a05024f`: SQLite, CAS transaccional, snapshots y append-only por repositorio/modelos, corpus F4/F1, evidencia PDF/PNG y UI versionada.
- Runtime aprobado Django 5.2.17 reconciliado en contratos efectivos; historial previo conservado.
- 25 pruebas Django y 4 pytest verifican persistencia, carrera, fronteras, errores, corrección y navegador.
- Medición registrada diagnóstica: p95 0.4871s, RSS 842932224 bytes, CPU 1.2759 núcleos. CPU excede umbral; hardware AD-15 no acreditado.
- Sesiones externas, aceptación de Sebastián y v2.0 final pendientes. Número de grupo dejado en blanco por instrucción del usuario.


## 15. Auditoría de la entrega y aprobación del cierre BMAD — 2026-10-04

- Se revisaron los enunciados y el repositorio frente a la rúbrica de E2, con foco en implementación funcional, trazabilidad, pruebas, reproducibilidad y documentos de entrega.
- Se priorizaron la persistencia de intervenciones, el control de concurrencia, la Corrección auditada, la evidencia visible y el cierre verificable del incremento F4 + F1.
- Se versionó el plan BMAD en `_bmad-output/implementation-artifacts/plan-cierre-mira-e2-f4-f1.md` y se conservaron los artefactos y decisiones de E1.
- El usuario aprobó las correcciones con opción A y solicitó integrar la rama de preparación en `main`; se realizó la integración fast-forward y el trabajo posterior continuó directamente en `main` (aprobación registrada en `1cd0378`).
- Se ratificó DEC-E2-08: el desacuerdo debe declararse con motivo; una Corrección registra Discrepancia y una Decisión, por sí sola, no implica desacuerdo.

## 16. Implementación y correcciones posteriores a la revisión — 2026-10-04

- Se completó F4 → F1 con SQLite, snapshots de evaluación y política, control transaccional por versión y eventos append-only en repositorio/modelos. `load_demo` conserva intervenciones al repetirse.
- Se incorporaron 15 Casos ficticios, evidencia PDF/PNG visible, historial persistente, Corrección de importe que conserva el original y la Decisión humana, motivos obligatorios y comentario obligatorio para `Otro`.
- Se mantuvieron los parámetros del piloto (T=90, mínimos 70), precedencia de fraude, reloj controlado de Santiago y plazos de 3/5 días hábiles; los vencidos y las solicitudes de antecedentes permanecen abiertos.
- Se conservaron snapshots antiguos sin reescribir evaluaciones, se hizo coherente la lectura del detalle y se bloquearon ambos formularios ante `stale_version` hasta recargar.
- Se corrigieron entradas decimales localizadas, NaN/Infinity, duplicación de borradores, retención de datos al fallar una Corrección, mensajes de confirmación y rutas de modificación ORM de snapshots.
- La revisión BMAD documentó cuatro lentes, su clasificación de hallazgos y los parches; todos los hallazgos enviados a corrección quedaron cerrados. Evidencia: `docs/qa/review-bmad.md` y `docs/qa/review-fixes.md`.
- Commits de referencia: implementación `a59ab9c`, compatibilidad histórica `422e777`, correcciones de revisión `0166caa` y cierre candidato `f426957`.

## 17. Verificación final y límites del candidato — 2026-10-04

- La verificación final registrada pasó instalación bloqueada (`uv sync --locked`), comprobación Django, migraciones y carga del corpus; runtime reconciliado: Python 3.13.16 y Django 5.2.17.
- Resultado final: **33 pruebas Django y 8 pytest aprobadas**. Este registro actualiza los conteos intermedios de la sección 14 y conserva su evidencia histórica.
- Se verificaron persistencia entre procesos, concurrencia por versión, fronteras F4, errores sin efectos laterales, evidencia, Corrección, historial y flujos Chromium. Se completó la matriz Must con historias, código, pruebas, commits y hashes de fuentes actuales.
- Se corrigió el muestreo CPU para capturar contadores iniciales/finales y declarar brechas. Medición final diagnóstica: p95 **0,5228 s**, RSS máximo **837.009.408 bytes** (aprox. 798,2 MiB), CPU promedio **1,3237 núcleos**, sin brechas observadas de contadores.
- p95 y memoria cumplen sus umbrales observados; CPU supera el límite de 1 núcleo. El hardware no acredita AD-15, por lo que estos resultados no certifican aceptación de rendimiento. Fuente: `docs/qa/measurements.json`; medición anterior conservada por separado.
- Se registró reproducción técnica desde una exportación Git limpia con caché local (8,65 s); no equivale a una sesión de instalación realizada por una persona externa.
- Siguen pendientes PX-05/usabilidad humana, sesión externa de reproducción, aceptación de Sebastián Rodríguez y resolución/acreditación de CPU y entorno AD-15. Actas: `docs/qa/actas-pendientes.md`.
- Se creó la etiqueta candidata **`v2.0-rc1`** sobre `5b4c9fe`; `v2.0` final queda reservada para el cierre validado.

## 18. Informe, presentación y versión Word editable — 2026-10-04

- Se prepararon el informe 6.1–6.8, matriz de trazabilidad Must, comparativa, guion, capturas y documentos de QA.
- Se incorporaron `entrega/MIRA-Meyer-Scheel-Rodriguez.pdf` (12 páginas) y `entrega/MIRA-Entrega2.pptx` (13 diapositivas), con registros de revisión e integridad en `docs/qa/artifacts.json`.
- Por instrucción del usuario, el número de grupo quedó en blanco para completarlo manualmente; debe ajustarse la portada y el nombre requerido antes de entregar.
- Se convirtió el informe a `entrega/MIRA-Meyer-Scheel-Rodriguez.docx` y se enlazó desde README (commit `64bb6c6`): texto y tres tablas editables, cinco imágenes y grupo en blanco.
- La conversión verificó contenido de la fuente e integridad del paquete DOCX. La paginación visual de Word no pudo verificarse en este entorno; debe revisarse al abrirlo en Word.

## 19. Autorización de publicación en GitHub — 2026-10-04

- El usuario solicitó actualizar esta bitácora y realizar commit y push de todo el trabajo de la sesión al repositorio `lukasscheelb/Software-asistido-por-LLMs`.
- Esta autorización posterior reemplaza la restricción operativa de no hacer push del plan inicial. La publicación debe conservar el historial y los hashes, subir `main` y la etiqueta candidata `v2.0-rc1`, sin forzar referencias.
- La aceptación humana y la acreditación de rendimiento siguen pendientes aunque se publique el candidato. El resultado del push se verificará contra las referencias remotas.


## 20. Identidad Git y reescritura autorizada — 2026-10-04

- A solicitud del usuario, con acuerdo comunicado de sus colaboradores, se reescribieron autor y committer de los 16 commits de esta sesión como **Lukas Scheel Belmar**, correo `227247263+lukasscheelb@users.noreply.github.com`.
- Se conservaron fechas, mensajes y árboles de cada commit; la línea base anterior a la sesión permanece intacta. El respaldo recuperable se guardó fuera del repositorio.
- Correspondencia entre hashes originales y nuevos: `docs/qa/commit-author-map.json`. La identidad Git no cambia la procedencia real: el código y los parches generados por el agente siguen declarados como tales.
- Se actualizaron referencias del historial, matrices y documentos derivados; FR-20 se enlaza a la versión actual del informe y se conserva la prueba de hashes del árbol actual.
- La publicación reescrita usa leases explícitos de main y v2.0-rc1 para impedir sobrescribir cambios concurrentes. La etiqueta candidata incorpora mantenimiento documental y nueva verificación; v2.0 final no se declara aceptada.
- Siguen pendientes PX-05 humano, aceptación de Sebastián y acreditación/rendimiento AD-15. Cambiar la identidad de Git no sustituye esas evidencias.
- Verificación posterior: check Django válido, **33 Django y 8 pytest aprobadas**, incluida FR-20; código, pruebas, fixtures y dependencias sin cambios. PDF (12 páginas) y PPTX (13 diapositivas) revisados; integridad Word verificada, paginación nativa Word no disponible. Registro: `docs/qa/identity-rewrite-verification.json`.

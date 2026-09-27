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

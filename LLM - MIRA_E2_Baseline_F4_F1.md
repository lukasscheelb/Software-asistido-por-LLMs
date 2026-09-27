# Baseline de alcance E1 → E2 — F4 + F1

## 1. Alcance confirmado
- Método: **BMAD**.
- Funcionalidades:
  - **F4 — Puntaje y decisión por umbrales**.
  - **F1 — Bandeja de revisión asistida**.
- Representante del cliente E2: **Sebastián Rodríguez**.
- Línea base: artefactos de la Entrega 1 ratificados por el equipo.
- Regla de continuidad: los IDs de E1 se conservan; cualquier cambio en E2 se registra como evolución o nueva decisión.

## 2. Requisitos funcionales directos

### F4
- **RQF-004 — Must:** Aplicar política versionada: aprobar si habilitada, p>T, sin fraude y con mínimos cumplidos; restantes casos revisan o escalan, sin rechazo automático.
  - Fuente E1: §2.6; §3; DEC-01.
  - Verificación E1: PF-04.

### F1
- **RQF-005 — Must:** Resolver casos con evidencia y motivos visibles; registrar aprobación, rechazo, solicitud de antecedentes y corrección sin borrar el original.
  - Fuente E1: §2.7; §3; DEC-08/11.
  - Verificación E1: PF-05.
- **RQF-014 — Must:** Mostrar vencimientos interno/contractual y alertar ingreso, proximidad y atraso; escalar vencidos sin cierre automático no autorizado.
  - Fuente E1: §2.7; §2.15; ENT4 [00:13:46]; DEC-10.
  - Verificación E1: PF-14.

## 3. Requisitos de apoyo que afectan el incremento
- **RQF-003 — Must:** aporta señales, ubicación de hallazgos y explicación de errores consumidas por F1/F4; en E2 el motor se simula.
- **RQF-008 — Must:** aporta la conservación de entradas/salidas, señales, reglas, versiones e intervenciones originales; útil para mantener explicación y trazabilidad del caso.
- **RQNF-009 — Must:** calidad de decisión previa a automatización; asociada a HU-03/F4 y verificada por PX-09.
- **RQNF-005 — Should:** usabilidad de revisión humana; asociada a HU-04/F1 y verificada por PX-05.
- **RQNF-008 — Should:** consumo de recursos de la interfaz de revisión; asociada a HU-04/F1 y verificada por PX-08.
- **RQNF-001 — Must (transversal):** incluye pantalla p95 <=2 s. Se mantiene como requisito transversal candidato para la arquitectura; su aplicabilidad exacta al incremento se confirmará en BMAD Architect.

## 4. Decisiones E1 directamente aplicables
- **DEC-01 — Política de decisión y gobierno**
  - T=90 quedó definido como candidato, no como valor aprobado definitivo.
  - Aprobación solo con automatización habilitada, p>T, sin fraude y con señales obligatorias presentes y sobre sus mínimos.
  - Fraude escala.
  - p<60 escala.
  - Casos restantes pasan a revisión.
  - Nunca existe rechazo automático.
  - Puntajes inválidos o fuera de [0,100] derivan como error.
- **DEC-08 — Identidad y estados del caso**
  - Evidencia nueva en caso abierto mantiene el caso y crea nueva evaluación.
  - Tras cierre, la nueva evidencia crea un caso vinculado.
  - Estados relevantes para F1: revisión, esperando antecedentes, aprobado, rechazado y cerrado por falta de antecedentes.
  - Transiciones terminales requieren resultado y motivo.
- **DEC-10 — Plazos y alertas de revisión**
  - Meta interna propuesta: 3 días hábiles.
  - Compromiso: 5 días hábiles.
  - Alertar un día hábil antes y al vencer.
  - Caso vencido se mantiene abierto y escala al supervisor.
- **DEC-11 — Revisión humana y usabilidad**
  - Mostrar evidencia y razones antes del puntaje.
  - Exigir decisión humana con motivo.
  - Conservar corrección junto al valor original.
  - Mostrar desacuerdos entre operador y plataforma.

## 5. Hallazgos E1 relevantes
- **H-01:** existían umbrales 80/85/90 y fronteras ambiguas → resuelto con T=90 como candidato y automatización apagada hasta calibración.
- **H-02:** conflicto por rechazo automático y cambios unilaterales → resuelto con rechazo solo humano y gobierno de cambios.
- **H-08:** ambigüedad sobre reevaluar el mismo caso o crear uno nuevo → resuelto por DEC-08.
- **H-15:** mínimos individuales de señales no definidos → permanece como punto que debe precisarse antes de habilitar automatización.
- **H-16:** ambigüedad entre meta de 3 días y compromiso de 5 → resuelto por DEC-10.
- **H-18:** “intuitiva/sin capacitación” no era verificable → resuelto mediante prueba de usabilidad definida en DEC-11.

## 6. Historias de usuario de origen
- **HU-03 — Must:** Como responsable de riesgo quiero una decisión explicada y conservadora para evitar aprobaciones sin sustento.
  - Requisitos: RQF-003/004/008; RQNF-009.
  - Criterios: PF-03/04/08 y PX-09; automatización permanece apagada sin aprobación.
  - Tamaño E1: 13.
- **HU-04 — Must:** Como operador quiero revisar evidencia y plazos para resolver con criterio propio.
  - Requisitos: RQF-005/014; RQNF-005/008.
  - Criterios: PF-05/14 y PX-05/08; no sobrescribir decisión concurrente.
  - Tamaño E1: 8.

## 7. Pruebas E1 que deben derivar a pruebas E2
- **PF-04 — F4**
  - T=90; mínimo m=70; automatización habilitada; sin fraude.
  - Fronteras: 59,99 / 60 / 80 / 85 / 89,99 / 90 / 90,01.
  - Variantes: fraude, señal ausente, señal=69,99, automatización deshabilitada.
  - Resultado: 59,99 escala; 60..90 revisan; 90,01 aprueba solo si todas las barreras se cumplen; fraude escala; demás fallos revisan; nunca rechazo automático.
- **PF-05 — F1**
  - Corregir monto 120000→100000.
  - Rechazo sin motivo debe bloquearse.
  - Solicitud de antecedentes cambia estado.
  - Decisión sobre versión obsoleta debe rechazarse sin sobrescribir la decisión vigente.
- **PF-14 — F1**
  - Calendario L-V.
  - Verificar vencimiento interno, contractual, alerta previa, vencimiento y escalamiento sin cierre automático.
- **PX-09 — F4**
  - Calidad de decisión; umbrales definidos en E1 sobre corpus controlado.
- **PX-05 — F1**
  - Usabilidad y control humano; evidencia antes del puntaje.
- **PX-08 — F1**
  - Consumo de recursos durante una sesión de revisión.

## 8. Conexión F4 → F1
1. El caso de prueba ya contiene señales, puntaje y componentes del motor simulado.
2. F4 aplica la política de decisión.
3. Si la salida es **REVISIÓN**, el caso ingresa a F1.
4. F1 muestra evidencia, razones/señales, hallazgos y plazos.
5. El operador decide y registra motivo/corrección cuando corresponda.
6. La interfaz marca si existe discrepancia entre la decisión del operador y la salida de la plataforma.

## 11. Decisiones E2 vigentes incorporadas a la baseline

### DEC-E2-01 — Mínimos por señal
- Para este incremento se fija un mínimo de **70/100** para cada señal numérica obligatoria.
- La referencia proviene de PF-04 de la Entrega 1, que ya prueba el límite `m=70`.
- La señal de fraude no usa mínimo numérico: actúa como condición de precedencia.

### DEC-E2-02 — Umbral operativo
- Se adopta **T=90** como umbral operativo del incremento y de los datos de prueba.
- Se mantiene configurable.
- Su validez se limita a este incremento/piloto y no se presenta como umbral definitivo de MIRA.

### DEC-E2-03 — Responsabilidad de F4
- F4 **no calcula el puntaje**.
- Consume el puntaje, sus componentes y señales entregados por el motor simulado.
- F4 aplica exclusivamente la política de decisión.
- No se inventará una fórmula de scoring no especificada en la Entrega 1.

### DEC-E2-04 — Señales obligatorias
- **Autenticidad documental:** escala 0–100, mínimo 70.
- **Coherencia entre evidencias:** escala 0–100, mínimo 70.
- **Fraude detectado:** señal booleana con precedencia; si es verdadera, el caso escala independientemente del puntaje.

### DEC-E2-05 — Motivo de decisión humana
- F1 exigirá motivo obligatorio para:
  - aprobar;
  - rechazar;
  - solicitar antecedentes;
  - corregir un dato.
- Se usará una categoría de motivo obligatoria y un comentario opcional.
- Si se selecciona **Otro**, el comentario será obligatorio.

### DEC-E2-06 — Ubicación del hallazgo
- La ubicación se almacenará de forma estructurada y se mostrará de forma comprensible.
- Para PDF: **página + campo/región**.
- Para imagen: **nombre de región + coordenadas opcionales**.
- La interfaz priorizará la descripción entendible para una persona no técnica.

### DEC-E2-07 — Plazos de revisión
- Meta interna: **3 días hábiles**.
- Compromiso contractual: **5 días hábiles**.
- Zona horaria: **America/Santiago**.
- Calendario: **lunes a viernes**.
- Alerta: **1 día hábil antes** y al vencimiento.
- Un caso vencido permanece abierto y escala; no existe cierre automático por vencimiento.
- Para pruebas y demo se usarán fechas de ingreso fijas/controladas para obtener resultados reproducibles.

## 12. Política operativa vigente de F4
Entrada:
- puntaje `0–100`;
- autenticidad documental `0–100`;
- coherencia entre evidencias `0–100`;
- fraude detectado `Sí/No`;
- automatización `ON/OFF`.

Reglas:
1. Puntaje inválido o fuera de rango → **ERROR / DERIVACIÓN**.
2. Fraude detectado = Sí → **ESCALADO**.
3. Puntaje < 60 → **ESCALADO**.
4. Automatización = ON, puntaje > 90, autenticidad >= 70 y coherencia >= 70 → **APROBADO AUTOMÁTICAMENTE**.
5. Cualquier otro caso → **REVISIÓN**.
6. Nunca existe rechazo automático.

## 13. Aclaraciones BMAD resueltas
- **Q-01:** Resuelta por DEC-E2-01.
- **Q-02:** Resuelta por DEC-E2-02.
- **Q-03:** Resuelta por DEC-E2-03.
- **Q-04:** Resuelta por DEC-E2-04.
- **Q-05:** Resuelta por DEC-E2-05.
- **Q-06:** Resuelta por DEC-E2-06.
- **Q-07:** Resuelta por DEC-E2-07.

## 14. Estado de la baseline
- La baseline F4 + F1 se considera **cerrada y vigente para iniciar BMAD Analyst**.
- Las decisiones DEC-E2-01 a DEC-E2-07 pasan a formar parte de la entrada oficial de la Entrega 2.
- Si posteriormente alguna decisión cambia, no se borrará: se registrará una nueva decisión en la bitácora y se actualizará esta baseline indicando la nueva regla vigente.
- Próximo artefacto: **Project Brief del rol Analyst de BMAD**.

# Revision BMAD del candidato

Lentes: blind-hunter, edge-case-hunter, verification-gap, intent-alignment. Revisor independiente del implementador; hallazgos verificados en BD aislada. Revision de todos los hallazgos antes de agrupar.

| ID | Veredicto | Ruta | Evidencia y decision |
|---|---|---|---|
| H1 | medium | patch | GET puede mostrar decision anterior con version nueva: intercalacion comprobada con Client y guardado entre case_detail y snapshot. Leer el contexto relacionado coherentemente. |
| H2 | medium | patch | POST obsoleto vuelve a mostrar formulario de Correccion con version nueva; prueba de intercalacion/stale confirmada. Requerir recarga antes de otro envio. |
| H3 | high | patch | 69.99 se renderiza como 69,99 en value y Decimal no lo acepta. Reproducido en POST de borrador; comparte causa de formato con E2. |
| H4 | medium | patch | Dos POST identicos de borrador crean dos casos: recuento 15->17 en BD aislada. Identidad estable de borrador evita duplicados sin nueva ruta publica. |
| H5 | medium | patch | Otro vacio borra importe, categoria, comentario y operador de Correccion; comprobado contenido de respuesta. Retener datos y errores junto al formulario. |
| H6 | low | patch | Correccion exitosa confirma una Decision, reproducido. Corregir texto directamente y expectativa de prueba. |
| H7 | medium | patch | _base_manager.update y bulk_create(update_conflicts=True) sobrescribieron snapshots en BD aislada. Proteger mismas operaciones existentes; no exigir defensa SQL admin. |
| H8 | medium | patch | test_traceability compara blobs historicos entre si, no fuentes actuales: puede certificar matriz antigua tras cambios. Comprobar hashes actuales normalizados y actualizar matriz del candidato. |
| H9 | low | rechazado | N+1 y escaneo estan presentes, pero corpus de demo es 15 y p95 observado con100 es0.4871s<2. No demuestra que provoquen exceso CPU; el refactor excede correccion directa para un defecto despreciable en uso actual. |
| H10 | medium | patch | Sampler fija primer contador cuando ya inicio trabajo y no captura final: omite consumo de bordes. Capturar baseline/final y declarar huecos de ciclo de vida; mantener diagnostico. |
| E1 | high | patch | POST scoreNaN respondio500 por numberformat de Django; salida dominioERROR no basta. Renderizar valor sin localizacion de Decimal no finito, conservando entrada. |
| E2 | high | patch | Confirmado value69,99 en borrador con autenticidad69.99. Mismo defecto de H3; usar strings canonicos/raw para inputs. |
| E3 | false | rechazado | La UI ya no ofrece otra Decision tras request_info; SPEC excluye nueva evidencia/reapertura y exige no cerrar por falta de antecedentes. Espera abierta es intencional; aprobar de nuevo sin nuevo flujo no es comportamiento anunciado. |
| G1 | medium | patch | Gap pre-verificado: solo100000 valido en pruebas de Correccion; finitos F4 no ejercitan comando. Agregar negativas/NaN/Infinity/malformadas y estado intacto. |
| G2 | medium | patch | Gap pre-verificado: E2E mira REVISIÓN transitoria y no sigue link generado; ausencia de seed pasaria. Seguir detalle persistido y conservar snapshot original. |
| I1 | low | rechazado | Reinicio se prueba entre procesos de composicion y no navegador: diferencia real de superficie, pero no se reclama sesion humana ni recuperacion UI en esa prueba; mismo adaptador durable ya ejercido. |
| I2 | false | rechazado | Conexiones concurrentes y pestañas secuenciales aportan evidencia complementaria declarada; no afirma simultaneidad de clicks Chromium. |
| I3 | false | rechazado | Correccion especificada120000->100000 se implementa sobre importe. No se reclama editor general; borrador nuevo conserva original. No hay divergencia con matriz aprobada. |
| I4 | false | rechazado | Prueba garantiza disponibilidad/orden; informe deja PX05 humano pendiente. No se declara comprension/legibilidad evaluada externamente. |
| I5 | false | rechazado | SQL administrativo se declara fuera de demo; no se reclama inmutabilidad frente a SQL. H7 sigue siendo un defecto distinto dentro de ORM y se corrige. |
| I6 | false | rechazado | Informe no certifica hardware/CPU/aceptacion. El usuario aprobo candidato con sesiones pendientes, no actas falsas. |
| I7 | low | rechazado | Main corroborado con git branch/log. Test de cadena es tecnico, no demostracion semantica total; pruebas PF/PX complementan. H8 especifico sobre archivos actuales si se corrige. |
| I8 | false | rechazado | Intencion aislada no enumera auditoria, pero plan aprobado contextualiza prioridades y matriz. No constituye un defecto del diff ni requiere inventar una nueva lista. |

Rutas patch conservan la superficie publica; se reengage el implementador. NaN/formato se agrupan; los otros defectos conservan su resultado especifico. No se amplian reapertura, SQL administrativo ni aceptacion humana.


## Cierre de parches y verificación

Parches `beca2cb`, grafo `632dc13`. Todos los hallazgos enviados a parche quedaron corregidos; no se difirió ninguno. Verificación independiente: uv sync --locked, check, migrate, load_demo; 33 pruebas Django y 8 pytest OK, ejecutados secuencialmente porque comparten la base temporal por defecto. El navegador comprobó NaN corregible, adopción de borrador, evidencia, corrección 120000→100000 y bloqueo de ambas acciones ante versión obsoleta hasta recarga.

Nueva medición en `measurements.json`: p95 0.5228s, RSS 837009408 bytes, CPU 1.3237 núcleos, sin brechas de contadores observadas; CPU excede umbral. Diagnóstico en entorno no acreditado. La medición anterior se conserva. PX-05 y aceptación no se realizaron.

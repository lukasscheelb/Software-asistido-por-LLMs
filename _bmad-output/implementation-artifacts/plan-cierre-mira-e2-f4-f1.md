---
title: 'Cerrar correcciones MIRA F4 y F1'
type: 'bugfix'
ticket: ''
created: '2026-10-04'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'thorough'
review_source: 'auto'
lenses_ran: ['blind-hunter', 'edge-case-hunter', 'verification-gap', 'intent-alignment']
review_loop_iteration: 0
baseline_revision: '4337a3a5f6dff92f8eddb20947b2f34a1e80f001'
context:
  - '_bmad-output/specs/spec-revision-f1-controlada/SPEC.md'
  - '_bmad-output/specs/spec-politica-f4-explicable/SPEC.md'
  - '_bmad-output/specs/spec-verificacion-entrega-trazable/SPEC.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** F4/F1 pierde intervenciones al reiniciar, admite decisiones concurrentes y carece de correcciones, evidencia visible y cierre verificable.

**Approach:** Completar el incremento contra sus contratos BMAD, conservando IDs E1 y commits trazables directamente en `main`. El usuario solicita todas las correcciones prioritarias de la auditoría como una versión candidata coherente.

## Boundaries & Constraints

**Always:** SQLite, CAS por versión, historial append-only, política persistida, Decimal, español, datos ficticios, reloj Santiago inyectable. Conservar barreras F4 y Django 5.2.17 aprobado; reconciliar contratos. Derivar pruebas de PF-04/05/14 y PX aplicables.

**Never:** Motor real, funciones fuera de F4/F1, servicios productivos o publicación remota. Inventar aceptación, usabilidad externa, autoría humana o límites de hardware. Identificar candidato local; reservar v2.0 final para cierre validado.

## I/O & Edge-Case Matrix

| Escenario | Entrada | Resultado | Error |
|---|---|---|---|
| F4 | Fronteras/fraude | Resultado y parámetros conservados | Inválidos/NaN: ERROR |
| Decisión | Motivo y versión vigente | Evento durable | Sin motivo: bloqueo |
| Corrección | 120000→100000 | Original y corregido auditables | Otro exige comentario |
| Concurrencia | Misma versión, dos comandos | Una confirmación | stale_version, recarga |
| Reinicio | Intervención guardada | Historial intacto | Sin pérdida |
| Plazos | L-V, reloj controlado | 3/5 días, alertas | Vencido sigue abierto |

</frozen-after-approval>

## Code Map

- `src/mira/domain/`: reutilizar reglas y categorías; ampliar intervención, corrección y validación finita.
- `src/mira/composition.py`: reemplazar diccionario/fechas divergentes; consumir evaluaciones históricas.
- `src/mira/infrastructure/review_store.py`: sustituir memoria por SQLite transaccional.
- `src/mira/application/services.py`: comandos/versiones y proyección operativa.
- `src/mira/web/`: conservar navegación, estética y orden evidencia primero.
- `_bmad-output/initiative-mira-e2-f4-f1/`: contratos e historias 2.x/3.x/4.x existentes.

## Tasks & Acceptance

**Execution:**
- [x] `domain/review.py`, `application/ports.py`, `application/services.py`: comandos de decisión/corrección y conflictos.
- [x] `infrastructure/models.py`, `infrastructure/migrations/`, `review_store.py`: casos/versiones/evaluaciones e intervenciones append-only, CAS atómico.
- [x] `composition.py`, `domain/policy.py`, `infrastructure/clock.py`: ensamblaje, reloj compartido y entradas finitas.
- [x] `fixtures/`, `web/management/commands/load_demo.py`: corpus F4/F1 idempotente y evidencia PDF/imágenes visible.
- [x] `web/views.py`, `web/urls.py`, `web/templates/`, `web/static/`: formularios versionados, historial, correcciones, supervisor, estados y ambos plazos.
- [x] `web/tests.py`, `tests/`, `pyproject.toml`, `uv.lock`: persistencia, carrera, errores, E2E y mediciones con configuración/resultados reales.
- [x] `docs/`, `README.md`, bitácora E2 y `_bmad-output/`: matriz Must con hashes, comparativa, QA, runtime coherente y cierre escrito/presentación; actas humanas pendientes.

Las rutas de código anteriores son relativas a `src/mira/`, excepto fixtures/tests/docs, dependencias y documentos BMAD.

**Acceptance Criteria:**
- Dado el corpus, cuando se recorre F4→F1, entonces se inspecciona evidencia y decide/corrige desde UI.
- Dada una intervención, cuando reinicia el proceso, entonces conserva resultado y política original.
- Dados dos operadores con igual versión, cuando confirman, entonces solo uno guarda.
- Dado un Must, cuando se consulta su matriz, entonces existen historia/código/prueba/commit.
- Dada una sesión humana no realizada, cuando se consulta el cierre, entonces figura pendiente.

## Implementation Notes

- 2026-10-04: el usuario aprueba todo el plan con opción A y pide unir la rama a main. Merge fast-forward completado; implementar directamente en main. DEC-E2-08: el operador declara desacuerdo con motivo; una corrección registra discrepancia; una decisión por sí sola no implica desacuerdo.
- Runtime local disponible: `.venv/Scripts/python.exe` en raíz del repo. uv: `C:/Users/lukas/Documents/Codex/2026-10-04/nece/work/audit-env/Scripts/uv.exe`. Variables de runtime/cache escribibles: UV_CACHE_DIR=`C:/Users/lukas/Documents/Codex/2026-10-04/nece/work/uv-cache`, UV_PYTHON_INSTALL_DIR=`C:/Users/lukas/Documents/Codex/2026-10-04/nece/work/uv-python`.
- Git necesita `-c safe.directory=C:/Users/lukas/Documents/Codex/2026-10-04/nece/work/repo-actual`; identidad por comando `-c user.name=Codex -c user.email=codex@local`. Commits locales por grupo coherente están autorizados; no hacer push.
- Fuera del repo, salidas para usuario solo en `C:/Users/lukas/Documents/Codex/2026-10-04/nece/outputs`; intermediarios en work.

## Plan Change Log

## Review Triage Log

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

## Verification

- `uv sync --locked`, `manage.py check`, `migrate --noinput`: instalación/esquema válidos.
- `uv run python manage.py test mira.web` y `uv run pytest tests`: suites y navegador aislado.
- `uv run python tests/quality/measure.py`: p95/recursos con muestras; si no se acredita el entorno AD-15, resultado diagnóstico.
- Navegador: evidencia, historial, corrección y conflicto entre pestañas. Externo PX-05 y aceptación de Sebastián siguen siendo sesiones humanas.


## Implementación y verificación registrada — 2026-10-04

- Candidato técnico local en main: `a59ab9c52324c0812eea0433966a70ed7a05024f`; documentación/QA: `aa824fc` (hash completo en matriz). No se realizó push.
- SQLite, snapshots de evaluación/política, versión CAS y eventos append-only por repositorio/modelos; correcciones preservan decisión y originales. Corpus de 15 casos con PDF/PNG ficticios.
- `manage.py check`, migraciones y carga idempotente válidas; 27 pruebas Django, 5 pytest (incluye cadena verificable de rutas/historias/pruebas/hashes/commits), navegador Chromium y reinicio mediante procesos nuevos.
- Medición real del commit técnico: p95 0,4871s; RSS máx 842932224 bytes; CPU promedio 1,2759 núcleos, supera ≤1. Hardware 12 lógicos/34224758784 bytes RAM, no acredita 2vCPU/4GiB: diagnóstico, no aceptación AD-15.
- Reproducción técnica git archive limpio con caché: 8,65s; sesión externa de clon limpio pendiente.
- Fuentes informe 6.1–6.8, comparativa dos tablas/indicadores propuestos, guion y actas pendientes en docs. Número de grupo en blanco por instrucción humana.
- Pendientes de cierre final: revisión BMAD del candidato, PX-05 externo, aceptación de Sebastián y medición acreditada AD-15/PX-08/resolución de CPU. v2.0 final reservada; no se inventa ninguna aceptación o sesión humana.



## Verificación final del candidato

Parches 0166caa y grafo ab745af revisados. 33 Django y 8 pytest pasan; instalación bloqueada, esquema y fixtures válidos. Navegador: NaN, borrador persistido, evidencia, corrección e historial; versión obsoleta bloquea formularios hasta recarga. Medición actual: p95 0.5228s, RSS 837009408 bytes, CPU 1.3237 núcleos (excede ≤1); sin brechas de contadores. Resultado diagnóstico, AD-15/PX-05/aceptación humana pendientes. Cuatro lentes finalizados y parches cerrados, sin hallazgos diferidos.


## Cambio de identidad Git autorizado — 2026-10-04

El usuario autorizó cambiar autor y committer de los 16 commits de esta sesión a Lukas Scheel Belmar y su correo GitHub noreply, actualizar trazabilidad/documentos y publicar con protección de referencias. Esta autorización posterior reemplaza las instrucciones operativas de identidad Codex/no push de las notas históricas; se conserva el intento funcional aprobado y la procedencia del trabajo asistido por agentes. La etiqueta candidata incluye el mantenimiento documental y la verificación posterior; v2.0 final sigue pendiente.

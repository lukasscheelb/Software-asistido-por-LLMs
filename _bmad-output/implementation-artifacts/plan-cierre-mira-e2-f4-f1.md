---
title: 'Cerrar las correcciones prioritarias de MIRA F4 y F1'
type: 'bugfix'
ticket: ''
created: '2026-10-04'
status: 'draft'
route: 'full'
route_source: 'auto'
review: ''
review_source: ''
lenses_ran: []
review_loop_iteration: 0
baseline_revision: '4337a3a5f6dff92f8eddb20947b2f34a1e80f001'
context:
  - '_bmad-output/specs/spec-revision-f1-controlada/SPEC.md'
  - '_bmad-output/specs/spec-politica-f4-explicable/SPEC.md'
  - '_bmad-output/specs/spec-verificacion-entrega-trazable/SPEC.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** El incremento ejecuta F4/F1, pero pierde decisiones al reiniciar, admite escrituras concurrentes incompatibles y no implementa correcciones ni evidencia visual. La entrega carece de verificación completa y documentación del resultado.

**Approach:** Cerrar el incremento académico existente contra sus contratos BMAD; conservar IDs E1, registrar decisiones y versionar cambios coherentes en la rama local `fix/mira-e2-bmad`. El usuario pidió el conjunto de correcciones prioritarias de la auditoría; el objetivo común es una versión candidata ejecutable y trazable.

## Boundaries & Constraints

**Always:** SQLite transaccional; capas AD-2; historial append-only; política versionada; puntajes Decimal; evidencia ficticia; español; reloj inyectable America/Santiago; preservar F4 sin rechazo automático. Reutilizar Django 5.2.17 ya instalado y reconciliar sus contratos con la decisión registrada en deferred-work. Derivar pruebas de PF-04/05/14 y PX aplicables.

**Never:** Implementar el motor real, F2/F3/F5–F9, servicios productivos o autenticación. Afirmar sesiones humanas, autoría del equipo o límites de hardware no observados. Publicar cambios remotos sin instrucción. Emitir `v2.0` como entrega aceptada antes de registrar los pendientes humanos; usar una versión candidata local.

## I/O & Edge-Case Matrix

| Escenario | Entrada/estado | Resultado esperado | Error |
|---|---|---|---|
| F4 | Fronteras y fraude del corpus | Salida y parámetros persistidos, nunca rechazo | Entrada inválida y NaN producen ERROR |
| Decidir | Caso derivado, motivo y versión vigente | Evento durable y nuevo estado | Falta de motivo bloquea |
| Corregir | 120000 → 100000 | Ambos valores, autor, motivo, fecha y versión | Otro exige comentario |
| Concurrencia | Dos comandos con la misma versión | Solo uno confirma; original intacto | stale_version y recarga |
| Reiniciar | Intervención ya confirmada | Mismo historial y política original | Sin pérdida |
| Plazos | Reloj controlado L-V | 3/5 días, tiempo restante y alerta | Vencido sigue abierto |

</frozen-after-approval>

## Code Map

- `src/mira/domain/{policy,review,deadlines}.py`: reglas puras existentes; reutilizar barreras y categorías.
- `src/mira/composition.py`: reemplazar estado global y fechas divergentes por adaptadores; no duplicar reglas.
- `src/mira/infrastructure/review_store.py`: diccionario actual sin persistencia; sustituir por repositorio SQLite.
- `src/mira/application/services.py`: proyección de bandeja; incorporar estado/plazos desde resultados conservados.
- `src/mira/web/{views.py,templates/mira_web/}`: formularios y orden evidencia primero; preservar estilo y navegación.
- `_bmad-output/initiative-mira-e2-f4-f1/`: historias 2.x, 3.x, 4.x y arquitectura aprobadas; conservar sus fuentes y registrar evolución.

## Tasks & Acceptance

**Execution:**
- [ ] `src/mira/domain/review.py`, `application/ports.py`, `application/services.py`: entidades de intervención/corrección, errores y comandos con versión.
- [ ] `src/mira/infrastructure/{models.py,migrations/,review_store.py}`: esquema, eventos append-only y comparación/escritura atómica; historial de evaluaciones y parámetros.
- [ ] `src/mira/composition.py`, `domain/policy.py`, `infrastructure/clock.py`: ensamblaje, reloj compartido y validación de valores finitos.
- [ ] `fixtures/`, `web/management/commands/load_demo.py`: corpus F4/F1 idempotente y PDF/imágenes ficticios visibles.
- [ ] `web/views.py`, `web/urls.py`, `templates/mira_web/`, `static/mira_web/styles.css`: decisiones/correcciones, versión del formulario, historial, estados/plazos y supervisor para ESCALADO.
- [ ] `src/mira/web/tests.py`, `tests/{unit,integration,e2e}/`, `pyproject.toml`, `uv.lock`: conservar pruebas útiles y añadir reinicio, carrera, correcciones, errores y recorridos UI.
- [ ] `tests/quality/`, `docs/verification/`: ejecutar corpus y medir p95/recursos con muestras y configuración; separar diagnóstico de cumplimiento si el entorno no acredita AD-15.
- [ ] `docs/{traceability,comparativa,aceptacion,usabilidad}.md`: matriz con hashes reales, cambios y responsables conocidos; formatos humanos pendientes.
- [ ] `README.md`, `LLM - MIRA_Entrega2_bitacora_decisiones.md`, `_bmad-output/`: sincronizar runtime, alcance y resultados; revisar QA independiente.
- [ ] `docs/entrega2/`: preparar informe y presentación con evidencia real y pendientes visibles; versionar cada grupo y versión candidata.

**Acceptance Criteria:**
- Dado el corpus cargado, cuando se recorre F4→F1 por UI, entonces se inspecciona evidencia y se decide/corrige sin editar la base.
- Dada una intervención guardada, cuando se reinicia o cambia la política, entonces se conserva su resultado original y su procedencia.
- Dados dos operadores con la misma versión, cuando confirman, entonces uno obtiene conflicto y ninguna decisión se sobrescribe.
- Dado un Must del alcance, cuando se consulta la matriz, entonces existen historia, código, prueba y commit citados.
- Dadas sesiones humanas no realizadas, cuando se consulta el cierre, entonces figuran pendientes y no resultados inventados.

## Open Questions

1. **Discrepancia:** F4 emite REVISIÓN/ESCALADO, no recomienda aprobar/rechazar. Opción A: el operador declara explícitamente desacuerdo con un motivo; corregir un dato marca discrepancia, sin interpretar toda decisión como desacuerdo. Opción B: conservar la convención actual que marca aprobar/rechazar como discrepancia frente a la derivación, documentándola y probándola. A evita confundir resolución con desacuerdo; B mantiene el comportamiento existente. Esta decisión se registrará como DEC-E2 nueva antes de implementar.

## Implementation Notes

## Plan Change Log

## Review Triage Log

## Verification

**Commands:**
- `uv sync --locked`: instalación reproducible.
- `uv run python manage.py check` y `migrate --noinput`: esquema válido.
- `uv run python manage.py test mira.web`: reglas y persistencia.
- `uv run pytest tests`: suites unitarias/integración/E2E con base aislada.
- `uv run python tests/quality/measure.py`: resultados y entorno explícitos.
- `git status --short`: solo cambios intencionales antes de cada commit.

**Manual checks:** navegación, evidencia, corrección e historial desde el navegador; confirmación del conflicto entre dos pestañas. Las sesiones externas y aceptación de Sebastián son responsabilidad humana.

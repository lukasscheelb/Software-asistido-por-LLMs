---
title: 'Cerrar correcciones MIRA F4 y F1'
type: 'bugfix'
ticket: ''
created: '2026-10-04'
status: 'in-progress'
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
- [ ] `domain/review.py`, `application/ports.py`, `application/services.py`: comandos de decisión/corrección y conflictos.
- [ ] `infrastructure/models.py`, `infrastructure/migrations/`, `review_store.py`: casos/versiones/evaluaciones e intervenciones append-only, CAS atómico.
- [ ] `composition.py`, `domain/policy.py`, `infrastructure/clock.py`: ensamblaje, reloj compartido y entradas finitas.
- [ ] `fixtures/`, `web/management/commands/load_demo.py`: corpus F4/F1 idempotente y evidencia PDF/imágenes visible.
- [ ] `web/views.py`, `web/urls.py`, `web/templates/`, `web/static/`: formularios versionados, historial, correcciones, supervisor, estados y ambos plazos.
- [ ] `web/tests.py`, `tests/`, `pyproject.toml`, `uv.lock`: persistencia, carrera, errores, E2E y mediciones con configuración/resultados reales.
- [ ] `docs/`, `README.md`, bitácora E2 y `_bmad-output/`: matriz Must con hashes, comparativa, QA, runtime coherente y cierre escrito/presentación; actas humanas pendientes.

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

## Verification

- `uv sync --locked`, `manage.py check`, `migrate --noinput`: instalación/esquema válidos.
- `uv run python manage.py test mira.web` y `uv run pytest tests`: suites y navegador aislado.
- `uv run python tests/quality/measure.py`: p95/recursos con muestras; si no se acredita el entorno AD-15, resultado diagnóstico.
- Navegador: evidencia, historial, corrección y conflicto entre pestañas. Externo PX-05 y aceptación de Sebastián siguen siendo sesiones humanas.

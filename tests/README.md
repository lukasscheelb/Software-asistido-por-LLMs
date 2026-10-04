# Pruebas del candidato F4 + F1

Las expectativas se derivan de PF-04, PF-05, PF-14 y del corpus de los SPEC BMAD; no sustituyen aceptación humana.

## Ejecución

Desde la raíz del repositorio, después de `uv sync --locked`:

```powershell
uv run python manage.py test mira.web
$env:PLAYWRIGHT_BROWSERS_PATH="$PWD/.cache/playwright"
uv run python -m playwright install chromium
uv run pytest tests
uv run python tests/quality/measure.py
```

Django cubre reglas F4, motivos, correcciones, CAS, plazos, persistencia y rutas. La prueba concurrente usa conexiones SQLite distintas contra una base de archivo temporal.

`tests/test_contracts.py` compara el corpus versionado con resultados esperados. `test_e2e.py` inicia servidor y Chromium, recorre F4 y F1, inspecciona evidencia y verifica conflictos desde la interfaz. `test_restart.py` escribe y lee desde procesos nuevos. `test_traceability.py` comprueba la cadena de artefactos, commits y hashes de fuentes actuales. Las bases y puertos de estas pruebas son temporales; no se usa la base de la demo compartida.

Los fixtures en `fixtures/` son ficticios. `load_demo` es idempotente y conserva intervenciones. Los scripts y dependencias ejecutables están fijados en `uv.lock`.

## Medición y aceptación

`tests/quality/measure.py` registra configuración, muestras, p95 de latencia, RSS y CPU en `docs/qa/measurements.json`. Se ejecuta como diagnóstico local: no acredita por sí solo el equipo de 2 vCPU/4 GiB de AD-15. El JSON declara límites de hardware y muestreo.

PX-05 requiere un integrante externo, y la aceptación requiere al representante del cliente. Registrar tareas, resultados, tiempos y criterios en `docs/qa/actas-pendientes.md`; las pruebas automatizadas no completan esas actas.

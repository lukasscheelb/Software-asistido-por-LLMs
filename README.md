# MIRA — Análisis de Requisitos Asistido por LLM

Este repositorio nació como la **Entrega 1** del curso **Taller de Desarrollo de Software Conducido por Agentes de IA** de la Universidad de Valparaíso y conserva ese análisis como base histórica. Actualmente incorpora el incremento académico **MIRA F4 + F1** de la Entrega 2.

## Aplicación local CAP-3

La ejecución local usa Python 3.13.16, Django 5.2.17 y SQLite, y no se conecta a
servicios externos. La instalación requiere [`uv`](https://docs.astral.sh/uv/) y
acceso de red para descargar el runtime y los paquetes, salvo que ya estén en caché.

Desde la raíz del repositorio:

```powershell
uv sync --locked
uv run python manage.py check
uv run python manage.py migrate --noinput
uv run python manage.py load_demo
uv run python manage.py test mira.web
uv run python manage.py runserver
```

Abrir `http://127.0.0.1:8000/`. La ruta inicial redirige a `/bandeja/`.
`uv` lee `.python-version`, instala Python 3.13.16 cuando no está disponible y
reproduce las dependencias de `uv.lock`. La base `db.sqlite3` se crea localmente y
no se versiona.

La demo incluye quince Casos ficticios (nueve F4 y seis F1) para la matriz F4. La Bandeja permite buscar
y filtrar los que requieren revisión, `Ejecutar F4` aplica la Política
determinista del piloto y el detalle presenta la Evidencia antes del Puntaje. En
F1 el operador puede registrar una decisión humana mínima con acción, categoría de
motivo obligatoria y comentario obligatorio cuando el motivo es `Otro`. Los plazos
de F1 se calculan con una fecha controlada del piloto, calendario lunes a viernes,
meta interna de 3 días hábiles y compromiso contractual de 5 días hábiles. No se
usan datos personales reales.

La verificación automatizada se ejecuta con `uv run python manage.py test mira.web`.
Las pruebas adicionales con pytest y Playwright se ejecutan con los comandos
indicados al final de este archivo; los contratos están en `tests/README.md`.
Este incremento es para desarrollo y verificación local; no incluye configuración
productiva.

## Descripción

El proyecto aborda el análisis de requisitos de **MIRA**, una plataforma de inteligencia artificial multimodal orientada al procesamiento de evidencia digital y apoyo a la toma de decisiones empresariales.

El trabajo consiste en transformar una descripción inicial de necesidades en un conjunto de artefactos de análisis que permitan comprender el dominio, identificar requisitos, detectar inconsistencias y preparar una base para el desarrollo posterior.

## Objetivos

- Analizar y estructurar las necesidades descritas en la documentación del proyecto.
- Identificar requisitos funcionales y no funcionales.
- Modelar los principales conceptos e interacciones del sistema.
- Detectar contradicciones, ambigüedades y decisiones pendientes.
- Mantener trazabilidad entre fuentes, decisiones, requisitos, pruebas y backlog.
- Aplicar técnicas de prompting para apoyar y verificar el proceso de análisis.

## Técnicas de prompting utilizadas

Durante el trabajo se utilizaron distintas técnicas de prompting para apoyar tareas específicas del análisis:

- **Grounded Prompting**
- **Structured Output Prompting**
- **Plan-and-Solve Prompting**
- **Chain-of-Verification (CoVe)**
- **LLM-as-a-Judge**

Los prompts completos se encuentran documentados dentro del repositorio.

## Equipo

- Francisca Meyer
- Lukas Scheel
- Sebastián Rodríguez

**Representante del cliente E1:** Lukas Scheel. **E2:** Sebastián Rodríguez.

## Consideraciones

Las herramientas de IA se utilizaron como apoyo al proceso de análisis. Las decisiones del proyecto, la revisión de inconsistencias y la validación de los artefactos corresponden al equipo.

Este repositorio mantiene el historial de trabajo y los principales archivos utilizados para la preparación de la entrega.


## Candidato local y pruebas integradas

Estado: candidato publicado; v2.0 final pendiente de validación externa y aceptación humana. [Informe](docs/informe-candidato.md), [matriz Must](docs/trazabilidad-must.md), [guion](docs/guion-presentacion.md), [actas pendientes](docs/qa/actas-pendientes.md).

`load_demo` es idempotente: no borra intervenciones. SQLite conserva evaluación, entradas, política efectiva e historial al reiniciar. Los comandos exigen la versión esperada del Caso; un conflicto muestra `stale_version` y pide recargar. Una Corrección del importe conserva original, valor corregido, motivo, operador declarado y fecha controlada; no altera la Decisión humana. El desacuerdo se declara explícitamente con comentario (DEC-E2-08). Antecedentes solicitados siguen visibles como abiertos.

Para Chromium y pytest en PowerShell:

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH="$PWD/.cache/playwright"
uv run python -m playwright install chromium
uv run pytest tests
uv run python tests/quality/measure.py
```

Las mediciones son diagnósticas si no se acredita el equipo AD-15 de 2 vCPU/4 GiB. La ejecución registrada observa p95 y RSS bajo umbral, CPU sobre umbral; consultar JSON con las 30 muestras. PX-05 y aceptación de Sebastián siguen pendientes. El operador demo se declara, sin autenticación productiva. Fecha compartida: 2026-10-06 12:00 America/Santiago, inyectable mediante `ControlledClock`; calendario L-V, sin feriados adicionales.

Demo: ejecutar CC-F4-04/05/09, corregir el borrador de error, abrir CC-F1-01 y su evidencia, corregir 120000→100000, solicitar antecedentes en CC-F1-03, abrir CC-F1-04 en dos pestañas y confirmar una misma versión; consultar alertas CC-F1-05/06 y reiniciar para comprobar historial.

## Archivos de entrega candidata

Etiqueta candidata publicada: `v2.0-rc1`, sobre `main`. [Informe PDF](entrega/MIRA-Meyer-Scheel-Rodriguez.pdf), [informe Word editable](entrega/MIRA-Meyer-Scheel-Rodriguez.docx) y [presentación editable](entrega/MIRA-Entrega2.pptx). El grupo se dejó en blanco por instrucción del usuario; completar portada y renombrar el PDF como `NUMEROGRUPO-MIRA-Meyer-Scheel-Rodriguez.pdf` antes de entregar. Fuentes: `docs/informe-candidato.md` y `docs/guion-presentacion.md`.

La revisión BMAD terminó con los parches cerrados y sin hallazgos diferidos: `docs/qa/review-bmad.md`. Verificación: 33 Django y 8 pytest OK. La etiqueta v2.0 final queda reservada para el cierre validado; completar las actas reales pendientes, revisar la reflexión personal y resolver/acreditar recursos. La publicación en GitHub fue autorizada por el usuario.

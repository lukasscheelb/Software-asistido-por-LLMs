# MIRA — Análisis de Requisitos Asistido por LLM

Repositorio de GitHub: [Software-asistido-por-LLMs](https://github.com/lukasscheelb/Software-asistido-por-LLMs).

Este repositorio nació como la **Entrega 1** del curso **Taller de Desarrollo de Software Conducido por Agentes de IA** de la Universidad de Valparaíso y conserva ese análisis como base histórica. Actualmente incorpora el incremento académico **MIRA F4 + F1** de la Entrega 2.

## Aplicación local CAP-3

La ejecución local usa Python 3.13.16, Django 5.2.17 y SQLite, y no se conecta a
servicios externos. La instalación requiere [`uv`](https://docs.astral.sh/uv/) y
acceso de red para descargar el runtime y los paquetes, salvo que ya estén en caché.

### 1. Requisitos iniciales

La guía principal está pensada para Windows con PowerShell. Necesitas Git ya
instalado, un navegador (Edge, Chrome o Firefox) y conexión a Internet durante la
primera instalación. Si el repositorio es privado, tu cuenta de GitHub debe tener
acceso y Git debe estar autenticado.

No necesitas instalar Python, Django o SQLite manualmente: `uv` prepara Python y
las dependencias del proyecto. Tampoco se necesitan Node.js, Docker, un servidor
de base de datos, claves de API ni extensiones de un editor para ejecutar MIRA.
VS Code y sus extensiones son opcionales.

### 2. Instalar uv

Abre **PowerShell** y ejecuta el instalador oficial:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Cierra y vuelve a abrir PowerShell para que reconozca el comando. Comprueba:

```powershell
uv --version
git --version
```

Si `uv` no se reconoce después de reiniciar la terminal, comprueba la ruta que
mostró el instalador y que esté incluida en `PATH`. Con la ruta predeterminada,
puedes comprobar el ejecutable directamente con:

```powershell
& "$env:USERPROFILE\.local\bin\uv.exe" --version
```

Referencia: [instalación oficial de uv](https://docs.astral.sh/uv/getting-started/installation/).

En macOS o Linux, instala `uv` con `curl -LsSf https://astral.sh/uv/install.sh | sh`
y reinicia la terminal. Los comandos Git y `uv` de los pasos siguientes son los
mismos; los ejemplos de variables de entorno del apartado de pruebas son para
PowerShell. La comprobación de instalación registrada se realizó en Windows.

### 3. Clonar y entrar al proyecto

Desde la carpeta donde quieras guardar el proyecto:

```powershell
git clone https://github.com/lukasscheelb/Software-asistido-por-LLMs.git
cd Software-asistido-por-LLMs
```

Ejecuta los pasos restantes desde esta carpeta: debe contener `manage.py`,
`pyproject.toml` y `uv.lock`. Para reproducir específicamente el candidato
publicado, en una copia nueva puedes ejecutar `git checkout v2.0-rc1`; para
trabajar con los cambios más recientes, conserva `main`.

### 4. Preparar Python, dependencias y base de datos

Ejecuta cada comando por separado y continúa solo si termina sin errores:

```powershell
uv sync --locked
uv run python manage.py check
uv run python manage.py migrate --noinput
uv run python manage.py load_demo
```

`uv` lee `.python-version`, instala Python 3.13.16 cuando no está disponible y
reproduce las dependencias de `uv.lock`. La base `db.sqlite3` se crea localmente y
no se versiona. También crea `.venv`; no es necesario activarlo porque `uv run`
usa el entorno del proyecto. La descarga inicial requiere Internet y puede tardar
según la conexión.

Los paquetes se instalan automáticamente: Django y sus dependencias para la
aplicación; pytest, pytest-django, Playwright y psutil para las pruebas. Las
versiones exactas y las dependencias transitivas están fijadas en `uv.lock`.
SQLite forma parte de Python. No ejecutes instalaciones manuales con `pip` ni
necesitas un archivo `requirements.txt` para seguir esta guía.

Resultados esperados: `check` indica que no hay problemas, `migrate` aplica las
migraciones y `load_demo` informa **15 Casos ficticios disponibles**. El último
comando conserva las decisiones e intervenciones existentes; no reinicia los datos.

### 5. Iniciar y utilizar MIRA

```powershell
uv run python manage.py runserver 127.0.0.1:8000
```

Deja esa terminal abierta y entra en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
La ruta inicial redirige a `/bandeja/`. No se requiere iniciar sesión.
Para una primera comprobación, abre **Ejecutar F4**, selecciona **CC-F4-02**,
pulsa **Ejecutar Política** y luego **Abrir detalle** para acceder a la evidencia
y a la revisión humana F1.

Para detener el servidor, pulsa **Ctrl+C** en su terminal. Para volver a usarlo,
entra nuevamente en la carpeta del proyecto y ejecuta el mismo comando de
`runserver`; no es necesario reinstalar ni volver a cargar la demo. Los datos se
conservan en `db.sqlite3`.

### 6. Problemas frecuentes

| Problema | Solución |
|---|---|
| `uv` no se reconoce | Reinicia PowerShell y comprueba la ruta del instalador y `PATH`, como se explica en el paso 2. |
| GitHub devuelve `Repository not found` o deniega el acceso | Comprueba la URL y que tu cuenta tenga acceso al repositorio si es privado; autentica Git con tu cuenta. |
| La carpeta de destino ya existe al clonar | Usa una carpeta distinta o entra en la copia existente; no la elimines si contiene trabajo propio. |
| No se encuentra `manage.py` o `pyproject.toml` | Ejecuta `cd Software-asistido-por-LLMs` desde su carpeta padre. |
| Falla la descarga de Python o paquetes | Comprueba Internet, proxy o certificados de tu red y repite `uv sync --locked`. |
| Falta una tabla de SQLite | Detén el servidor y ejecuta `uv run python manage.py migrate --noinput`. |
| No aparecen casos demo | Ejecuta `uv run python manage.py load_demo` y recarga la Bandeja. |
| El puerto 8000 está ocupado | Ejecuta `uv run python manage.py runserver 127.0.0.1:8001` y abre `http://127.0.0.1:8001/`. |
| El navegador no conecta | Comprueba que el servidor siga ejecutándose y que la URL use el puerto indicado en la terminal. |
| Aparece un conflicto `stale_version` | Recarga el detalle del caso, revisa su estado actualizado y vuelve a realizar la operación. |

### 7. Verificación opcional

Para comprobar la aplicación con las pruebas de Django, desde la raíz del proyecto:

```powershell
uv run python manage.py test mira.web
```

Las pruebas adicionales de navegador se explican en **Candidato local y pruebas
integradas**. Chromium de Playwright se descarga aparte únicamente para esas
pruebas y para la medición; no hace falta para usar MIRA en tu navegador habitual.

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

Grupo conformado por: Francisca Meyer, Lukas Scheel y Sebastián Rodríguez.

**Representante del cliente E1:** Lukas Scheel. **E2:** Sebastián Rodríguez.

## Consideraciones

Las herramientas de IA se utilizaron como apoyo al proceso de análisis. Las decisiones del proyecto, la revisión de inconsistencias y la validación de los artefactos corresponden al equipo.

Este repositorio mantiene el historial de trabajo y los principales archivos utilizados para la preparación de la entrega.


## Candidato local y pruebas integradas

Estado: versión de entrega publicada; informe y actas actualizados localmente. F4/F1 aceptadas por el cliente; v2.0 final pendiente de cierre y acreditaciones. [Informe](docs/informe-entrega.md), [matriz Must](docs/trazabilidad-must.md), [estado de validaciones](docs/qa/actas-pendientes.md).

`load_demo` es idempotente: no borra intervenciones. SQLite conserva evaluación, entradas, política efectiva e historial al reiniciar. Los comandos exigen la versión esperada del Caso; un conflicto muestra `stale_version` y pide recargar. Una Corrección del importe conserva original, valor corregido, motivo, operador declarado y fecha controlada; no altera la Decisión humana. El desacuerdo se declara explícitamente con comentario (DEC-E2-08). Antecedentes solicitados siguen visibles como abiertos.

Para Chromium y pytest en PowerShell:

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH="$PWD/.cache/playwright"
uv run python -m playwright install chromium
uv run pytest tests
uv run python tests/quality/measure.py
```

Las mediciones son diagnósticas si no se acredita el equipo AD-15 de 2 vCPU/4 GiB. La ejecución registrada observa p95 y RSS bajo umbral, CPU sobre umbral; consultar JSON con las 30 muestras. El cliente acepta el rendimiento con esa desviación y Sebastián acepta F4/F1. Se registraron dos sesiones de usabilidad; quedan por acreditar las condiciones formales de PX-05. El operador demo se declara, sin autenticación productiva. Fecha compartida: 2026-10-06 12:00 America/Santiago, inyectable mediante `ControlledClock`; calendario L-V, sin feriados adicionales.

Demo: ejecutar CC-F4-04/05/09, corregir el borrador de error, abrir CC-F1-01 y su evidencia, corregir 120000→100000, solicitar antecedentes en CC-F1-03, abrir CC-F1-04 en dos pestañas y confirmar una misma versión; consultar alertas CC-F1-05/06 y reiniciar para comprobar historial.

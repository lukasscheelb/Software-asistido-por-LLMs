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
uv run python manage.py test mira.web
uv run python manage.py runserver
```

Abrir `http://127.0.0.1:8000/`. La ruta inicial redirige a `/bandeja/`.
`uv` lee `.python-version`, instala Python 3.13.16 cuando no está disponible y
reproduce las dependencias de `uv.lock`. La base `db.sqlite3` se crea localmente y
no se versiona.

La demo incluye cuatro Casos ficticios: la Bandeja permite buscar y filtrar los que
requieren revisión, `Ejecutar F4` aplica la Política determinista del piloto y el
detalle presenta la Evidencia antes del Puntaje. No se usan datos personales reales.

La verificación automatizada base se ejecuta con `uv run python manage.py test mira.web`.
El contrato de ampliación hacia pytest y Playwright, capas, marcadores CAP-3 y
comandos previstos está documentado en `tests/README.md`.
Este starter es solo para desarrollo y verificación local; no incluye configuración
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

**Representante del cliente:** Lukas Scheel

## Consideraciones

Las herramientas de IA se utilizaron como apoyo al proceso de análisis. Las decisiones del proyecto, la revisión de inconsistencias y la validación de los artefactos corresponden al equipo.

Este repositorio mantiene el historial de trabajo y los principales archivos utilizados para la preparación de la entrega.

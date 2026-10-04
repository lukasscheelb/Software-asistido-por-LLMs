# Contrato del harness de pruebas

Esta story deja solo los puntos de conexión de CAP-3. Este directorio no contiene
pruebas ejecutables, configuración de pytest ni navegadores de Playwright. La story
que conecte el harness deberá mantener el arranque web actual sin cambios.

## Puntos de conexión

- Settings de Django: `mira.settings` mediante `DJANGO_SETTINGS_MODULE`.
- Entrada de comandos: `uv run python manage.py ...`.
- Ruta inicial: `GET /` responde con una redirección temporal a `/bandeja/`.
- Bandeja: `GET /bandeja/` responde `200` y renderiza los Casos controlados
  `CC-F4-02` y `CC-F4-03` sin depender de JavaScript.
- Ejecución F4: `GET /ejecutar-f4/` presenta el selector de Casos y
  `POST /ejecutar-f4/` devuelve una de las cuatro salidas deterministas de la
  Política.
- Detalle: `GET /casos/<case_id>/` muestra primero la Evidencia y después el
  Puntaje y las Señales; un identificador desconocido responde `404`.
- Composition root: `mira.composition`; solo este módulo ensamblará adaptadores
  concretos cuando existan.
- Capas: `tests/unit` cubrira `mira.domain`, `tests/integration` cubrira puertos y
  adaptadores entre `mira.application` y `mira.infrastructure`, y `tests/e2e`
  recorrera `mira.web` desde el navegador.

La dirección que debe conservar el harness es
`web/infrastructure -> application -> domain`. Las pruebas unitarias no usaran
Django ni SQLite. Las de integración usarán una base SQLite temporal administrada
por Django. Las E2E iniciarán el servidor local y usarán Chromium contra las rutas
públicas.

## Ciclo de vida E2E previsto

La fixture E2E reservará un puerto dinámico asignado por el sistema en
`127.0.0.1` y publicará la URL base al navegador. Esperará como máximo 10 segundos,
mediante consultas a `GET /bandeja/`, hasta recibir `200`; si no ocurre, abortará
con los diagnósticos del proceso web. Un módulo de settings de prueba derivado de
`mira.settings` apuntará SQLite a un directorio temporal único por ejecución o
worker, sin usar `db.sqlite3`.

El servidor, el contexto de Chromium y la base temporal se gestionarán con
`try/finally`: el teardown detendrá el proceso web, cerrará el navegador y eliminará
el directorio temporal incluso cuando una prueba falle o sea interrumpida.

## Fixtures previstos

Los fixtures futuros viviran en `fixtures/`, seran ficticios, versionados e
idempotentes. Las pruebas podrán construir datos temporales propios, pero no
alterarán esos archivos ni compartirán `db.sqlite3` entre ejecuciones.

## Marcadores CAP-3 previstos

La configuración futura de pytest registrará `cap_3`, `unit`, `integration` y
`e2e`. La prueba base de CAP-3 comprobará la redirección, el estado HTTP, el HTML
server-rendered, los filtros de la Bandeja y las cuatro salidas controladas de F4.
También verificará el orden Evidencia antes de Puntaje en el detalle. Los nombres
de las pruebas citaran CAP-3.

En concreto, `cap_3 and unit` ejecutará una guardia estática sobre el AST de imports
de `src/mira`: rechazará dependencias contrarias a
`web/infrastructure -> application -> domain`, verificará que todos los límites
sean importables y comprobará que `mira.composition` sea el único módulo autorizado
a importar simultáneamente puertos de `application` y adaptadores concretos de
`infrastructure`.

## Comandos previstos

Estos comandos documentan el contrato futuro; todavía no están disponibles en
esta story:

```powershell
uv run playwright install chromium
uv run pytest -m "cap_3 and unit"
uv run pytest -m "cap_3 and integration"
uv run pytest -m "cap_3 and e2e"
```

Playwright for Python se fijará en `1.63.0`. La versión exacta de pytest deberá
aprobarse y bloquearse en `uv.lock` al implementar el harness; no se incorpora
ninguna dependencia de pruebas en esta story.

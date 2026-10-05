# Comprobación de instalación del README

Fecha de revisión: 4 de octubre de 2026. Código de referencia: `0ccb92f0ffae7ca6b1ad4af4f1d19263a0437327`, etiqueta `v2.0-rc1`.

## Procedimiento y resultados

Se creó una copia Git limpia local, sin reutilizar `.venv` ni `db.sqlite3` de la copia de trabajo. Se utilizaron Python y paquetes disponibles en la caché de uv; la instalación se ejecutó con `uv sync --locked --offline`. Las variables de directorios de caché y Python apuntaron a los recursos disponibles en este entorno.

| Paso | Resultado |
|---|---|
| Clonar la copia Git local | Correcto. |
| Sincronizar dependencias bloqueadas | Correcto; entorno nuevo y 17 paquetes instalados. |
| `uv run python manage.py check` | Sin problemas. |
| `uv run python manage.py migrate --noinput` | Migraciones aplicadas correctamente. |
| `uv run python manage.py load_demo` | 15 casos ficticios disponibles. |
| `uv run python manage.py test mira.web` | 33 pruebas aprobadas. |
| Iniciar servidor local | Correcto; se usó el puerto 8001 para no interferir con la aplicación existente en 8000. |
| Abrir raíz, Bandeja, Ejecutar F4 y detalle CC-F4-02 | Respuestas HTTP 200; la raíz redirige a Bandeja. |
| Detener el servidor de comprobación | Correcto. |

## Mejoras del README

Se documentaron requisitos, instalación oficial de uv, verificación de comandos, clonación y entrada al repositorio, instalación automática de Python y dependencias, migraciones y demo, inicio y detención del servidor, persistencia, puerto alternativo, problemas frecuentes y pruebas opcionales. No se requieren extensiones de editor ni instalación manual de paquetes.

## Alcance

La comprobación valida instalación y arranque en Windows desde una copia limpia con caché. No verifica descarga desde GitHub o instalación del ejecutable uv desde cero, ni acredita una sesión realizada por una persona externa en menos de 15 minutos. Las instrucciones de instalación de uv se cotejaron con su documentación oficial. La comprobación histórica de `reproducibility.json` se conserva por separado.

# Verificación del incremento de front-end

Fecha: 17 de octubre de 2026. Alcance: propuesta UX-01 a UX-10 aprobada. No es una evaluación académica del informe.

## Resultados

- 33 pruebas Django de `mira.web`: aprobadas.
- Siete pruebas pytest seleccionadas: aprobadas (`test_frontend_ux.py`, `test_e2e.py`, `test_contracts.py`, `test_restart.py`, `test_measure_counters.py`). Se usó una carpeta temporal nueva para evitar permisos de cachés anteriores y `PLAYWRIGHT_BROWSERS_PATH` apuntando a los binarios locales ya existentes.
- Tres pantallas a cinco anchos: 320, 360, 390, 768 y 1366 px; sin desbordamiento horizontal global. La tabla puede desplazarse dentro de su contenedor en tablet.
- Navegación móvil con sección activa; encabezados de tabla presentes en el árbol accesible; objetivos de casilla, orden evidencia/puntaje y título del objeto PDF comprobados.
- Prueba de Tab/Shift+Tab, skip link, foco de textarea y resumen de errores. Se corrigió la restauración de fragmento que retiraba foco al resumen.
- Borrador F4, decisión con Otro/desacuerdo sin comentario y corrección negativa: errores asociados y valores conservados. Estados aprobado y rechazado verificados visualmente por clase y texto. El recorrido integrado verifica antecedentes y conflicto entre sesiones.
- PDF y PNG servidos y comprobados por firma. El visor PDF incrustado no renderiza en este Chromium headless; se verificó el archivo y el enlace alternativo.
- Ocho pares de contraste medidos en `contrast.json`; texto ≥4,5:1 y borde de control ≥3:1. Esto no constituye auditoría integral WCAG.

## Capturas

Se inspeccionaron capturas de F1, F4 y detalle en 390 y 1366 px. Son pantallas de base de pruebas aislada. No se modificaron fixtures ni la base de trabajo del usuario. Los archivos `f1-390.png`, `f4-390.png`, `detalle-390.png` y sus equivalentes de escritorio documentan la presentación. Los resultados son técnicos; no se declara una nueva validación humana de usabilidad.

## Límites

No se ejecutó auditoría de lector de pantalla real, zoom nativo de navegador ni evaluación de todas las combinaciones de contraste. No se certifica conformidad WCAG completa. La nueva apariencia requiere validación humana si se desea acreditar mejoría de usabilidad. No se renovó la evidencia FR-20 ligada a commits porque el usuario prohibió commit y push. No se movió v2.0. Los informes PDF/DOCX históricos no se modificaron.

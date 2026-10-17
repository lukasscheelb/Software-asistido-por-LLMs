# Historias de mejora del front-end

Rol SM. Fuente: propuesta UX aprobada del 17 de octubre de 2026 y ARCHITECTURE-SPINE.md de esta carpeta. Se conserva la vinculación de origen HU-03/04 de F4/F1 sin crear requisitos de negocio nuevos.

| Historia | Hallazgos | Criterios de aceptación | Evidencia de cierre |
|---|---|---|---|
| UX-HU-01 Orientación y evaluación | UX-01, UX-03 | Nombres completos; estado vacío legible; botón Evaluar caso; resultado y borrador de error conservan funcionamiento. | `test_e2e.py`, `test_frontend_ux.py`, capturas F4. |
| UX-HU-02 Bandeja adaptable | UX-02, UX-09 | Ocho columnas dimensionadas; acción Abrir disponible; encabezados accesibles en móvil; sin desbordamiento global entre 320 y 1366 px. | Matriz de 15 vistas y capturas F1. |
| UX-HU-03 Revisión y corrección legibles | UX-04, UX-05, UX-07, UX-08 | Evidencia antes del puntaje; archivos con acceso alternativo y nombre accesible; checkbox propio; estado coherente con acción; decisión y corrección separadas. | E2E PDF/PNG, intervención, corrección y conflicto; prueba UX de checkbox y rechazo. |
| UX-HU-04 Errores y teclado | UX-06, UX-09 | Foco visible en textarea; resumen enfocado tras error, incluso tras usar skip link; mensajes asociados; conservar operador, discrepancia y valores inválidos. | Prueba UX de Tab/Shift+Tab, foco y errores de decisión/borrador/corrección. |
| UX-HU-05 Consistencia visual | UX-10 | Paleta existente reconciliada con tokens; contraste medido en pares principales; documentos y bitácora actualizados. | DESIGN.md, resultados de contraste y capturas revisadas. |

Estado: implementadas y verificadas con el alcance documentado en el registro QA. La validación humana de usabilidad del nuevo diseño y una auditoría integral de accesibilidad permanecen fuera de estas pruebas automáticas.

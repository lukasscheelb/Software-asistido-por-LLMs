# Compatibilidad técnica del incremento de UX

Rol Architect. Fecha: 17 de octubre de 2026. Propuesta aprobada explícitamente por el usuario. Alcance: presentación de F4/F1 dentro del monolito Django existente.

## Decisiones

- AD-UX-01 [ADOPTED]: mantener plantillas renderizadas en servidor, CSS local y las rutas actuales. No agregar frameworks, paquetes, CDN ni servicios.
- AD-UX-02 [ADOPTED]: el servidor conserva todas las validaciones, escritura de intervenciones y control CAS. El delta de `views.py` solo retiene datos introducidos y asocia errores existentes a controles; no decide aprobación ni corrige valores de negocio.
- AD-UX-03 [ADOPTED]: JavaScript local y progresivo para asociaciones ARIA y foco del resumen de errores. No interceptar envíos ni bloquear reintentos. El foco se establece tras restaurar fragmentos de navegación.
- AD-UX-04 [ADOPTED]: mantener evidencia y ubicación antes del puntaje en el DOM. Separar grupos dentro del detalle, conservando decisión, corrección e historial sin diálogos nuevos.
- AD-UX-05 [ADOPTED]: tabla de ocho columnas en escritorio con desplazamiento contenido si falta ancho; representación apilada en móvil con roles y encabezados accesibles. Nunca permitir desbordamiento horizontal de toda la página.
- AD-UX-06 [ADOPTED]: estilos de decisión según acción registrada, sin tratar rechazo o antecedentes como aprobación. La etiqueta textual es obligatoria.

## Límites

No cambia política, umbrales, precedencia de fraude, datos de prueba, modelos, migraciones, persistencia, autenticación ni plazos. No se altera `v2.0`. No se agregan ordenación, filtros nuevos o confirmaciones modales. El historial permanece en la sección diferenciada del panel para evitar reorganizar sus contratos de datos. PDFs incrustados dependen del visor del navegador y conservan acceso alternativo al archivo.

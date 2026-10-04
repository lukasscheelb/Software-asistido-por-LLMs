# Correcciones de revisión del candidato

- Detalle materializado desde una transacción de lectura coherente, después del comando. `stale_version` bloquea decisión y corrección hasta recargar por GET.
- F4 usa valores de presentación/edición string sin localización numérica; NaN/sNaN/Infinity/-Infinity son ERROR corregible. Borradores válidos repetidos tienen identificador estable por contenido e inputs originales sin sobrescribir fixture.
- Corrección inválida conserva importe, categoría, comentario y operador junto a sus errores. Mensaje de éxito propio de Corrección.
- ORM append-only protege base manager y bulk upsert; migración 0002 conserva opciones de manager. No se amplía a administración SQL directa.
- Trazabilidad contrasta hashes normalizados del árbol actual y blobs del commit. Cambiar fuente actual invalida la prueba.
- Muestreo CPU registra contadores iniciales antes del trabajo y finales antes de cerrar navegador; procesos nuevos/salidos y lecturas fallidas se declaran. Los datos anteriores de measurements.json corresponden al método/commit allí identificado: no representan medición nueva del sampler corregido. Hardware AD-15 sigue sin acreditación.
- Regresiones: importes negativos/no finitos/malformados conservan versión, valor, decisión e historial; navegador abre detalle del caso corregido y la lectura persistida conserva original CC-F4-09 ERROR/101.

Verificación focalizada: `manage.py test mira.web` 33 pruebas OK; pytest de e2e y counters 3 passed. Validator de trazabilidad se ejecuta tras fijar commit y actualizar manifiestos. Verificación completa/medición nueva a cargo de la revisión final; no se inventa resultado.

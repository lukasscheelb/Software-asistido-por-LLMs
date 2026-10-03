# Contratos de dominio compartidos

Este archivo fija el significado observable de los contratos. La forma física se decide en CAP-1.

| Concepto | Contrato observable |
|---|---|
| Caso | Unidad identificable que agrupa Versiones del caso, Evaluaciones e Intervenciones humanas. |
| Versión del caso | Revisión concreta sobre la que se evalúa o decide; una versión obsoleta no puede sobrescribir la vigente. |
| Política | Conjunto ordenado, configurable y versionado de reglas y parámetros. |
| Evaluación | Vincula una Versión del caso, una Versión de política, entradas simuladas, parámetros efectivos, Salida F4 y explicación. |
| Salida F4 | Uno de `ERROR / DERIVACIÓN`, `ESCALADO`, `APROBADO AUTOMÁTICAMENTE` o `REVISIÓN`. |
| Evidencia | PDF o imagen ficticia con una Ubicación del hallazgo comprensible. |
| Intervención humana | Decisión humana o Corrección registrada sobre una Versión del caso, con autor y fecha controlada. |
| Corrección | Conserva valor original, valor corregido, motivo, autor, fecha y Versión del caso. |

## Invariantes

- Cambiar una Política no reescribe Evaluaciones previas.
- Una Intervención humana no borra entradas, Evidencia ni resultados anteriores.
- F1 consume la Salida F4 y su explicación sin recalcular la Política.
- Fixtures y tiempos de prueba son deterministas.
- Los contratos no prescriben base de datos, framework ni mecanismo de concurrencia hasta resolver CAP-1.

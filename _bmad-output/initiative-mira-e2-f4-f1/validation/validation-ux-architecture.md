# Validación de bmad-ux y bmad-architecture

Fecha: 2026-10-03  
Modo: fast path con supuestos explícitos y revisión determinista.

## Resultado

- Estado: parcial, listo para revisión humana.
- UX: `DESIGN.md` y `EXPERIENCE.md` finalizados como contrato de trabajo.
- Cobertura UX: UJ-1 a UJ-4 tienen flujo independiente, protagonista, pasos, clímax y fallo.
- Componentes: 9 nombres alineados entre apariencia y comportamiento.
- Tokens: 17 referencias `{path.to.token}` resuelven en `DESIGN.md`.
- Arquitectura: 14 decisiones `AD-N` con `Binds`, `Prevents` y `Rule`.
- Linter oficial: cero hallazgos.
- Reviewer Gate: versión tecnológica y compatibilidad adversarial revisadas; los hallazgos altos fueron corregidos.
- Ticketing: 33 historias intactas y `unpinned_after = 0`.
- Handoff: las copias UX y arquitectura dentro de la iniciativa coinciden por SHA-256 con los originales.

## UX

- Superficie web responsive en español, primero laptop/escritorio.
- Bandeja operativa, ejecución F4, resultado, detalle, Decisión y Corrección.
- Evidencia, razón y ubicación preceden al Puntaje en orden visual y DOM.
- Estados de F4, concurrencia, plazos, carga, vacío y fallo están definidos.
- WCAG 2.2 AA, teclado completo, foco visible y estados no dependientes solo del color.

Supuestos pendientes de aceptación:

- Lenguaje visual operativo con tipografía del sistema, tema claro y densidad media.
- `ERROR / DERIVACIÓN` como estado inline en Resultado F4.
- Identidad de marca y modo oscuro no definidos.

## Arquitectura

- Paradigma: monolito modular con límites hexagonales.
- Starter propuesto: Python 3.13.16, Django 5.2.18 LTS, SQLite local y Playwright Python 1.63.0.
- Dominio puro para F4; mutaciones solo por application services.
- Concurrencia optimista con `expected_case_version`.
- Evaluaciones, Decisiones y Correcciones append-only.
- Política inmutable por versión; reloj y calendario inyectables.
- Fixtures ficticios versionados e idempotentes.
- Vocabulario compartido propiedad de `domain`.
- Bandeja como proyección de lectura, nunca segunda fuente de verdad.

Supuestos y decisiones pendientes:

- Aceptar o sustituir el starter antes de iniciar 1.3.
- Definir interacción, volumen y entorno del p95.
- Definir métrica, herramienta y umbral PX-08.
- Definir catálogo inicial de motivos y superficie final de `ERROR / DERIVACIÓN`.

## Reviewer Gate

- `review-rubric.md`: cobertura estructural completa; pendientes correctamente diferidos.
- `review-current-technology.md`: corrigió Django 5.2.8 a 5.2.18.
- `review-incompatible-units.md`: añadió AD-13 para vocabulario común y AD-14 para ownership de Bandeja.

No se usaron subagentes porque no estaban disponibles; los tres lentes se ejecutaron secuencialmente y dejaron evidencia escrita.

## Publicación

No se iniciaron historias ni se creó commit. Los artefactos aún deben ser adoptados por `bmad-spec` o aceptados como companions antes de cerrar las historias HITL 1.1 y 1.2.

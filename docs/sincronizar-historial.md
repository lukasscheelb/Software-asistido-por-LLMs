# Sincronizar después de la reescritura de autoría

Los 16 commits de la sesión del 4 de octubre de 2026 tienen nuevos hashes e identidad Git de Lukas Scheel Belmar. La línea base anterior se conserva. No se debe mezclar el main antiguo en el nuevo mediante merge/pull normal, porque volvería a introducir el historial anterior.

## Copia sin trabajo propio pendiente

Desde la raíz del repositorio, comprobar primero `git status`. Si hay cambios o commits propios, seguir el apartado siguiente antes de continuar.

```powershell
git branch respaldo-main-antes-reescritura main
git fetch origin
git switch main
git reset --hard origin/main
```

La rama de respaldo conserva el main anterior. El reset sustituye el estado de main; ejecutarlo únicamente después de verificar que no se pierde trabajo propio.

Para actualizar la etiqueta candidata existente, después de sincronizar main:

```powershell
git fetch origin +refs/tags/v2.0-rc1:refs/tags/v2.0-rc1
```

Comprobar `git status`, `git log -5 --oneline` y el destino de `v2.0-rc1`. El nuevo destino incluye mantenimiento de trazabilidad/documentos y su verificación; no declara aceptación de v2.0 final.

## Copia con cambios o commits propios

- Guardar los cambios no comprometidos con un commit en una rama propia o `git stash push -u -m "Respaldo antes de reescritura"`. El stash con `-u` conserva también archivos no rastreados, pero no archivos ignorados; copiar aparte cualquier archivo ignorado que sea importante.
- Conservar los commits propios en una rama de respaldo antes de reemplazar main.
- Sincronizar main mediante los comandos del apartado anterior.
- Revisar y recuperar únicamente los cambios propios con cherry-pick o aplicar el stash, resolviendo los conflictos si aparecen. No hacer merge del main antiguo completo.

Correspondencia de los commits de la sesión: `docs/qa/commit-author-map.json`. Si no está claro qué commits son propios o hay otras ramas compartidas, revisar el grafo antes del reset y coordinar la recuperación con el equipo.

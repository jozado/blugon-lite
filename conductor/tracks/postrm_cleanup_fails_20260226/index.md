# Subtrack: postrm no elimina directorios con __pycache__

## Estado Actual

**Status:** 🔴 EN INVESTIGACIÓN
**Priority:** MEDIUM

## Resumen

Los directorios `/usr/lib/blugon-lite/tui/widgets` y `modals` no se eliminan porque contienen `__pycache__`.

## Archivos

- [spec.md](./spec.md) - Especificación detallada del problema
- [plan.md](./plan.md) - Plan de acción y seguimiento

## Última Actualización

2026-02-26: Creado subtrack después de que el usuario reportó que los directorios persisten después de `apt purge`.

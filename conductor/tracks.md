# Project Tracks

This file tracks all major tracks for the project. Each track has its own detailed plan in its respective folder.

---

- [x] **Track: Crear blugon-lite.py eliminando características innecesarias y manteniendo funcionalidad core**
  *Link: [./tracks/blugon_lite_20260223/](./tracks/blugon_lite_20260223/)*

- [x] **Track: Crear TUI con urwid y paquete .deb instalable**
  *Link: [./tracks/blugon_deb_20260223/](./tracks/blugon_deb_20260223/)*

---

## Bug Fixes

- [x] **Track: Reparar bugs de input del modal de edición del TUI**
  *Link: [./tracks/tui_modal_input_fix_20260224/](./tracks/tui_modal_input_fix_20260224/)*
  *Parent: blugon_deb_20260223*
  *Priority: HIGH - Bloquea testing del TUI*

---

## Critical Fixes

- [x] **Track: Crear deb funcional**
  *Link: [./tracks/deb_funcional_20260225/](./tracks/deb_funcional_20260225/)*
  *Parent: blugon_deb_20260223*
  *Priority: CRITICAL - Bloquea lanzamiento del paquete .deb*

  **IMPORTANTE:** Este track tiene un archivo `HALLAZGOS_Y_PROBLEMAS.md` que DEBE ser leído antes de comenzar cualquier trabajo.

---

## Bug Fixes Pending

- [x] **Track: Solucionar issues pendientes del deb**
  *Link: [./tracks/deb_issues_20260226/](./tracks/deb_issues_20260226/)*
  *Parent: deb_funcional_20260225*
  *Priority: HIGH - Mejoras críticas post-instalación*

  **Issues a resolver:**
  1. ~~Restaurar gamma de pantalla al detener daemon (TUI)~~ → **SUBTRACK: [gamma_restore_fails_20260226](./tracks/gamma_restore_fails_20260226/)** ✅
  2. ~~Restaurar gamma al desinstalar paquete~~ → **SUBTRACK: [gamma_restore_fails_20260226](./tracks/gamma_restore_fails_20260226/)** ✅
  3. ~~Eliminar autoinicio correctamente al desinstalar~~ → ✅ COMPLETADO
  4. ~~Eliminar directorios residuales al desinstalar~~ → **SUBTRACK: [postrm_cleanup_fails_20260226](./tracks/postrm_cleanup_fails_20260226/)** ✅
  5. ~~Mejorar TUI (UX, validaciones)~~ → ✅ COMPLETADO

  **Archivo de contexto:** `DEBUG_SESSION.md` con toda la información de depuración.

  **SUBTRACKS:**
  - ✅ [gamma_restore_fails_20260226](./tracks/gamma_restore_fails_20260226/) - Gamma no se restaura (CRITICAL) - VERIFICADO POR USUARIO
  - ✅ [postrm_cleanup_fails_20260226](./tracks/postrm_cleanup_fails_20260226/) - postrm no elimina directorios (MEDIUM)
  - ✅ [daemon_sync_5min_20260226](./tracks/daemon_sync_5min_20260226/) - Sincronizar daemon a múltiplos de 5 min (COMPLETADO)

---

## Release

- [ ] **Track: Revisar documentación y subir proyecto a GitHub**
  *Link: [./tracks/github_release_20260227/](./tracks/github_release_20260227/)*
  *Priority: CRITICAL - Lanzamiento oficial v1.0.0*

  **Objetivos:**
  1. Limpieza de archivos temporales
  2. Documentación completa (README, INSTALL, LICENSE)
  3. Crear repositorio en GitHub
  4. Publicar release v1.0.0 con paquete .deb


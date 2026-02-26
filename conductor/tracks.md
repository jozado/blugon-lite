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

- [~] **Track: Solucionar issues pendientes del deb**
  *Link: [./tracks/deb_issues_20260226/](./tracks/deb_issues_20260226/)*
  *Parent: deb_funcional_20260225*
  *Priority: HIGH - Mejoras críticas post-instalación*

  **Issues a resolver:**
  1. Restaurar gamma de pantalla al detener daemon (TUI)
  2. Restaurar gamma al desinstalar paquete
  3. Eliminar autoinicio correctamente al desinstalar
  4. Mejorar TUI ( UX, validaciones )

  **Archivo de contexto:** `DEBUG_SESSION.md` con toda la información de depuración.


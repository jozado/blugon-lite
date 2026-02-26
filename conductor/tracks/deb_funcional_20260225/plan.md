# Implementation Plan: deb_funcional_20260225

## Track: Crear deb funcional

---

## Fase 1: Lectura de Contexto [checkpoint: ]

- [ ] Task: LEER HALLAZGOS_Y_PROBLEMAS.md
    - [ ] Leer completamente el archivo de hallazgos
    - [ ] Comprender causas raíz de cada problema
    - [ ] Identificar archivos afectados
    - [ ] Tomar notas de soluciones intentadas

- [ ] Task: Verificar estado actual del sistema
    - [ ] Ejecutar `dpkg -l blugon-lite`
    - [ ] Verificar si hay procesos corriendo
    - [ ] Limpiar estado si es necesario

- [ ] Task: Conductor - User Manual Verification 'Lectura de Contexto' (Protocol in workflow.md)

---

## Fase 2: Arreglar Desinstalación Sucia [checkpoint: ]

**PROBLEMA IDENTIFICADO:** El script prerm usaba `pkill -f "blugon-lite"` que mataba los propios procesos de apt/dpkg que estaban ejecutando la desinstalación.

**SOLUCIÓN APLICADA:**
- Creada función `kill_blugon_daemon()` que usa `pgrep -f` para obtener PIDs numéricos
- Excluye explícitamente procesos de dpkg, apt, prerm, postrm
- Excluye el propio proceso prerm usando $$
- Logging extensivo a /tmp/blugon-prerm-debug.log

**TESTING:**
- [x] Instalación del paquete funciona
- [x] Daemon inicia correctamente
- [x] Desinstalación con daemon corriendo funciona (EXIT CODE: 0)
- [x] Logs confirman que solo el daemon es eliminado

- [x] Task: Revisar scripts actuales en debian/DEBIAN/
    - [x] Verificar prerm actual
    - [x] Verificar postrm actual
    - [x] Verificar postinst actual

- [x] Task: Corregir prerm
    - [x] Remover `set -e` si existe
    - [x] Agregar `|| true` a todos los comandos
    - [x] Agregar logging a /tmp/blugon-debug.log
    - [x] Manejar caso failed-remove
    - [x] Siempre `exit 0`
    - [x] Crear función kill_blugon_daemon() para evitar matar procesos de dpkg/apt

- [x] Task: Corregir postrm
    - [x] Remover `set -e` si existe
    - [x] Agregar `|| true` a todos los comandos
    - [x] Agregar logging a /tmp/blugon-debug.log
    - [x] Manejar TODOS los casos: purge, remove, failed-remove, abort-install, etc.
    - [x] Siempre `exit 0`

- [x] Task: Corregir postinst
    - [x] Remover `set -e` si existe
    - [x] Agregar `|| true` a comandos de usuario
    - [x] Agregar logging

- [x] Task: Reconstruir paquete .deb
    - [x] Ejecutar build-deb.sh
    - [x] Verificar que scripts están en el .deb

- [x] Task: Probar desinstalación
    - [x] Instalar paquete
    - [x] Ejecutar `sudo apt purge blugon-lite`
    - [x] Verificar que completa sin colgarse (EXIT CODE: 0)
    - [x] Verificar que no queda en estado `rF`

- [x] Task: Conductor - User Manual Verification 'Desinstalación Sucia' (Protocol in workflow.md)

---

## Fase 3: Arreglar Detección del Daemon [checkpoint: ]

**PROBLEMA IDENTIFICADO:** La función `is_daemon_running()` solo buscaba `blugon-lite.py` pero el daemon instalado usa `/usr/bin/blugon-lite`.

**SOLUCIÓN APLICADA:**
- Actualizada función `is_daemon_running()` en `tui/utils.py`
- Ahora busca múltiples patrones: `blugon-lite`, `blugon-lite.py`, `blugon-lite --interval`
- Logging extensivo a /tmp/blugon-tui-debug.log
- Función `toggle_daemon()` también actualizada para usar rutas absolutas

**TESTING:**
- [x] python3 -c "from tui.utils import is_daemon_running; print(is_daemon_running())" retorna True con daemon corriendo

- [x] Task: Analizar función is_daemon_running()
    - [x] Leer tui/utils.py
    - [x] Identificar patrón de búsqueda actual
    - [x] Identificar por qué falla

- [x] Task: Actualizar is_daemon_running()
    - [x] Buscar por "blugon-lite" (comando instalado)
    - [x] Buscar por "blugon-lite.py" (desarrollo)
    - [x] Buscar por argumento "--interval"
    - [x] Usar pgrep -f con múltiples patrones

- [x] Task: Probar detección
    - [x] Iniciar daemon: `blugon-lite --interval 120 &`
    - [x] Abrir TUI: `blugon-lite-tui`
    - [x] Verificar que muestra "Daemon: Activo"
    - [x] Matar daemon y verificar "Daemon: Inactivo"

- [x] Task: Conductor - User Manual Verification 'Detección del Daemon' (Protocol in workflow.md)

---

## Fase 4: Arreglar Servicio Systemd [checkpoint: 756093d]

**ANÁLISIS:** El servicio systemd tiene configuración correcta (Type=simple, ExecStart con ruta absoluta, Environment=DISPLAY=:0) PERO no funciona porque los daemons que necesitan X11 no pueden acceder al servidor X cuando se ejecutan como servicio systemd del sistema.

**SOLUCIÓN APLICADA:**
- Se determinó que el método preferido es autoinicio vía `.desktop` (Freedesktop.org standard)
- El servicio systemd se mantiene pero no se recomienda para este caso de uso
- Método .desktop es compatible con XFCE, GNOME, KDE, MATE, Cinnamon, LXDE/LXQt

**COMPATIBILIDAD:**
- ✅ XFCE, GNOME, KDE, MATE, Cinnamon (X11)
- ⚠️ Wayland: No funciona (blugon-lite usa X11/Xrandr)
- ✅ CLI manual funciona sin autoinicio

- [x] Task: Revisar archivo del servicio
    - [x] Leer debian/blugon-lite.service
    - [x] Verificar que no tiene `User=%i`
    - [x] Verificar ExecStart con ruta absoluta

- [x] Task: Corregir servicio si es necesario
    - [x] El servicio ya está correcto (Type=simple, ruta absoluta, Environment=DISPLAY=:0)
    - [x] Documentar que autoinicio .desktop es el método preferido

- [x] Task: Probar servicio
    - [x] El servicio inicia pero falla por acceso X11
    - [x] Documentar limitación en README

- [x] Task: Conductor - User Manual Verification 'Servicio Systemd' (Protocol in workflow.md)

---

## Fase 5: Arreglar Lanzador de Autoinicio [checkpoint: 756093d]

**SOLUCIÓN APLICADA:**
- blugon-lite-autostart.desktop: Exec con ruta absoluta `/usr/bin/blugon-lite --interval 120`
- postinst: Copia a `/etc/xdg/autostart/blugon-lite.desktop` (autoinicio global)
- postinst: Copia a `~/.config/autostart/` para cada usuario
- postrm purge: Limpia `/etc/xdg/autostart/blugon-lite.desktop`

**TESTING:**
- [x] Instalación copia archivo a /etc/xdg/autostart/
- [x] Instalación copia archivo a ~/.config/autostart/
- [x] Desinstalación (purge) limpia /etc/xdg/autostart/
- [x] Daemon inicia automáticamente al iniciar sesión (XFCE)

- [x] Task: Revisar archivo .desktop
    - [x] Leer blugon-lite-autostart.desktop
    - [x] Verificar que Exec usa ruta absoluta
    - [x] Verificar Terminal=false

- [x] Task: Actualizar postinst para copiar .desktop
    - [x] Copiar a /etc/xdg/autostart/
    - [x] Copiar a ~/.config/autostart/ para cada usuario
    - [x] Establecer permisos correctos (644)

- [x] Task: Probar lanzador
    - [x] Verificar que el archivo se crea en /etc/xdg/autostart/
    - [x] Verificar que el archivo se crea en ~/.config/autostart/
    - [x] Reiniciar sesión y verificar autoinicio

- [x] Task: Conductor - User Manual Verification 'Lanzador de Autoinicio' (Protocol in workflow.md)

- [ ] Task: Conductor - User Manual Verification 'Lanzador de Autoinicio' (Protocol in workflow.md)

---

## Fase 6: Testing Final y Documentación [checkpoint: ]

- [ ] Task: Testing integral
    - [ ] Instalar paquete limpio
    - [ ] Habilitar servicio systemd
    - [ ] Verificar daemon se inicia
    - [ ] Verificar TUI muestra daemon activo
    - [ ] Desinstalar paquete
    - [ ] Verificar desinstalación limpia

- [ ] Task: Actualizar HALLAZGOS_Y_PROBLEMAS.md
    - [ ] Documentar soluciones aplicadas
    - [ ] Agregar comandos de verificación
    - [ ] Listar lecciones aprendidas adicionales

- [ ] Task: Conductor - User Manual Verification 'Testing Final' (Protocol in workflow.md)

---

## Fase 7: Finalización [checkpoint: ]

- [ ] Task: Commit final
    - [ ] Stage todos los cambios
    - [ ] Commit con mensaje descriptivo
    - [ ] Git note con resumen de fixes

- [ ] Task: Marcar track como completo
    - [ ] Update tracks.md
    - [ ] Commit

- [ ] Task: Conductor - User Manual Verification 'Finalización' (Protocol in workflow.md)

---

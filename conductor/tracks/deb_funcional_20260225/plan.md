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

## Fase 4: Arreglar Servicio Systemd [checkpoint: ]

- [ ] Task: Revisar archivo del servicio
    - [ ] Leer debian/blugon-lite.service
    - [ ] Verificar que no tiene `User=%i`
    - [ ] Verificar ExecStart con ruta absoluta

- [ ] Task: Corregir servicio si es necesario
    - [ ] Remover `User=%i`
    - [ ] Asegurar Type=simple
    - [ ] Verificar Environment=DISPLAY=:0

- [ ] Task: Probar servicio
    - [ ] `sudo systemctl daemon-reload`
    - [ ] `sudo systemctl enable blugon-lite`
    - [ ] `sudo systemctl start blugon-lite`
    - [ ] `systemctl status blugon-lite`

- [ ] Task: Conductor - User Manual Verification 'Servicio Systemd' (Protocol in workflow.md)

---

## Fase 5: Arreglar Lanzador de Autoinicio [checkpoint: ]

- [ ] Task: Revisar archivo .desktop
    - [ ] Leer blugon-lite-autostart.desktop
    - [ ] Verificar que Exec usa ruta absoluta
    - [ ] Verificar Terminal=false

- [ ] Task: Actualizar postinst para copiar .desktop
    - [ ] Copiar a /etc/xdg/autostart/
    - [ ] Copiar a ~/.config/autostart/ para cada usuario
    - [ ] Establecer permisos correctos

- [ ] Task: Probar lanzador
    - [ ] Click en "blugon-lite Daemon" en menú
    - [ ] Verificar que inicia proceso
    - [ ] Reiniciar sesión y verificar autoinicio

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

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

- [ ] Task: Revisar scripts actuales en debian/DEBIAN/
    - [ ] Verificar prerm actual
    - [ ] Verificar postrm actual
    - [ ] Verificar postinst actual

- [ ] Task: Corregir prerm
    - [ ] Remover `set -e` si existe
    - [ ] Agregar `|| true` a todos los comandos
    - [ ] Agregar logging a /tmp/blugon-debug.log
    - [ ] Manejar caso failed-remove
    - [ ] Siempre `exit 0`

- [ ] Task: Corregir postrm
    - [ ] Remover `set -e` si existe
    - [ ] Agregar `|| true` a todos los comandos
    - [ ] Agregar logging a /tmp/blugon-debug.log
    - [ ] Manejar TODOS los casos: purge, remove, failed-remove, abort-install, etc.
    - [ ] Siempre `exit 0`

- [ ] Task: Corregir postinst
    - [ ] Remover `set -e` si existe
    - [ ] Agregar `|| true` a comandos de usuario
    - [ ] Agregar logging

- [ ] Task: Reconstruir paquete .deb
    - [ ] Ejecutar build-deb.sh
    - [ ] Verificar que scripts están en el .deb

- [ ] Task: Probar desinstalación
    - [ ] Instalar paquete
    - [ ] Ejecutar `sudo apt purge blugon-lite`
    - [ ] Verificar que completa sin colgarse
    - [ ] Verificar que no queda en estado `rF`

- [ ] Task: Conductor - User Manual Verification 'Desinstalación Sucia' (Protocol in workflow.md)

---

## Fase 3: Arreglar Detección del Daemon [checkpoint: ]

- [ ] Task: Analizar función is_daemon_running()
    - [ ] Leer tui/utils.py
    - [ ] Identificar patrón de búsqueda actual
    - [ ] Identificar por qué falla

- [ ] Task: Actualizar is_daemon_running()
    - [ ] Buscar por "blugon-lite" (comando instalado)
    - [ ] Buscar por "blugon-lite.py" (desarrollo)
    - [ ] Buscar por argumento "--interval"
    - [ ] Usar pgrep -f con múltiples patrones

- [ ] Task: Probar detección
    - [ ] Iniciar daemon: `blugon-lite --interval 120 &`
    - [ ] Abrir TUI: `blugon-lite-tui`
    - [ ] Verificar que muestra "Daemon: Activo"
    - [ ] Matar daemon y verificar "Daemon: Inactivo"

- [ ] Task: Conductor - User Manual Verification 'Detección del Daemon' (Protocol in workflow.md)

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

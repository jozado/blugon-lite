# Implementation Plan: blugon_deb_20260223

## Track: Crear TUI con urwid y paquete .deb instalable

---

## Fase 1: Auto-Configuración del Script [checkpoint: ecd050e]

- [x] Task: Modificar blugon-lite.py con fallback automático
    - [x] Actualizar función read_gamma() para buscar en múltiples ubicaciones
    - [x] Agregar configuración hardcodeada por defecto
    - [x] Mantener compatibilidad con configs existentes
    - [x] Testear que funciona sin ~/.config/blugon/gamma

- [x] Task: Mejorar archivo configs/evening/gamma
    - [x] Agregar comentarios detallados sobre formato
    - [x] Incluir guía de temperaturas (6500K, 4500K, 3000K, 2000K)
    - [x] Ejemplos de cómo agregar/quitar horarios
    - [x] Mantener horario 17:00-08:00 como default

- [x] Task: Conductor - User Manual Verification 'Auto-Configuración' (Protocol in workflow.md)

---

## Fase 2: TUI con urwid [checkpoint: 176153d]

- [x] Task: Configurar entorno de desarrollo para TUI
    - [x] Instalar urwid (pip install urwid)
    - [x] Crear archivo blugon-lite-tui.py básico
    - [x] Implementar ventana principal con título
    - [x] Implementar loop principal de urwid

- [x] Task: Implementar visualización de horarios
    - [x] Leer configuración actual desde ~/.config/blugon/gamma
    - [x] Mostrar lista de horarios con navegación (↑↓)
    - [x] Mostrar gamma actual y próxima transición
    - [x] Resaltar horario seleccionado

- [x] Task: Implementar edición de horarios
    - [x] Dialog para editar hora (HH:MM)
    - [x] Dialog para editar temperatura (Kelvin)
    - [x] Validación de inputs (hora 0-23, temp 1000-20000)
    - [x] Vista previa de cambios antes de guardar

- [x] Task: Implementar agregar/eliminar horarios
    - [x] Dialog para agregar nuevo horario
    - [x] Confirmación antes de eliminar
    - [x] Ordenamiento automático por hora
    - [x] Prevención de duplicados

- [x] Task: Implementar guardado y salida
    - [x] Guardar cambios a ~/.config/blugon/gamma
    - [x] Confirmación si hay cambios sin guardar
    - [x] Mensaje de éxito después de guardar
    - [x] Atajos: 's' guardar, 'q' salir, 'h' ayuda

- [x] Task: Implementar características adicionales
    - [x] Mostrar estado del daemon (corriendo/detenido)
    - [x] Botón para iniciar/detener daemon
    - [x] About screen (tecla 'a')
    - [x] Help screen (tecla 'h')
    - [x] Colores y estilos apropiados

- [x] Task: Crear wrapper ejecutable blugon-lite-tui
    - [x] Script bash que llama a Python
    - [x] Verificar dependencias (python3, urwid)
    - [x] Manejo de errores si faltan dependencias
    - [x] Hacer ejecutable (chmod +x)

- [x] Task: Conductor - User Manual Verification 'TUI con urwid' (Protocol in workflow.md)

---

## Fase 3: Configuraciones Predefinidas [checkpoint: ecd050e]

- [x] Task: Crear config office/gamma
    - [x] Horario típico oficina (9:00-18:00)
    - [x] 5-6 puntos de transición
    - [x] Comentarios específicos para este perfil

- [x] Task: Crear config student/gamma
    - [x] Horarios extendidos (estudiante)
    - [x] Más horas de luz normal
    - [x] Transición más tarde en la noche

- [x] Task: Crear config night-owl/gamma
    - [x] Para usuarios nocturnos
    - [x] Luz normal hasta tarde
    - [x] Transición más tarde

- [x] Task: Crear config minimal/gamma
    - [x] Solo 3 puntos: día, tarde, noche
    - [x] Simple y fácil de entender
    - [x] Ideal para usuarios nuevos

- [x] Task: Actualizar Makefile
    - [x] Incluir nuevas configs en install
    - [x] Actualizar rutas de instalación

- [x] Task: Conductor - User Manual Verification 'Configuraciones Predefinidas' (Protocol in workflow.md)

---

## Fase 4: Testing Manual del Conjunto [checkpoint: ]

**BUG ENCONTRADO:** El modal de edición no permite escribir texto con el teclado, ni usar Backspace/Delete, ni Enter en botones.

*Solución:* Se creó subtrack `tui_modal_input_fix_20260224` para reparar estos bugs antes de continuar con el testing.

- [x] Task: Testing de blugon-lite.py auto-configurable
    - [x] Probar sin ~/.config/blugon/gamma
    - [x] Probar con config de usuario
    - [x] Probar fallback a config del sistema
    - [x] Probar fallback hardcodeado
    - [x] Verificar --once funciona
    - [x] Verificar --interval funciona
    - [x] Verificar --backend funciona

- [~] Task: Testing de blugon-lite-tui (BLOQUEADO por bugs de input)
    - [ ] Probar navegación con teclado
    - [ ] Probar edición de horarios
    - [ ] Probar agregar/eliminar horarios
    - [ ] Probar guardado de configuración
    - [ ] Probar en diferentes tamaños de terminal
    - [ ] Verificar que no crasha

- [ ] Task: Testing de integración
    - [ ] blugon-lite.py y blugon-lite-tui coexisten
    - [ ] Cambios en TUI se reflejan en blugon-lite
    - [ ] Múltiples configs predefinidas cargan bien
    - [ ] Probar flujo completo: instalar → TUI → usar

- [~] Task: Corregir bugs encontrados
    - [x] Listar bugs encontrados (modal input)
    - [ ] Reparar bugs de edición de texto
    - [ ] Reparar bugs de Backspace/Delete
    - [ ] Reparar bugs de Enter en botones
    - [ ] Priorizar por severidad
    - [ ] Corregir bugs críticos
    - [ ] Corregir bugs menores si hay tiempo

- [ ] Task: Conductor - User Manual Verification 'Testing Manual del Conjunto' (Protocol in workflow.md)

---

## Fase 5: Documentación [checkpoint: ]

- [ ] Task: Actualizar README.md
    - [ ] Instrucciones de uso (antes del .deb)
    - [ ] Sección sobre el TUI (cómo usar)
    - [ ] Guía de configuraciones predefinidas
    - [ ] Cómo editar gamma manualmente
    - [ ] Ejemplos para diferentes casos de uso
    - [ ] Solución de problemas comunes
    - [ ] Capturas de pantalla del TUI (ASCII)

- [ ] Task: Crear INSTALL.md
    - [ ] Requisitos del sistema
    - [ ] Instalación desde fuente (paso a paso)
    - [ ] Uso básico después de instalar
    - [ ] Primeros pasos con el TUI

- [ ] Task: Actualizar blugon-lite.1 (man page)
    - [ ] Documentar opción --status (si se agrega)
    - [ ] Documentar blugon-lite-tui
    - [ ] Ejemplos de uso del TUI
    - [ ] Referencia a configuraciones predefinidas

- [ ] Task: Conductor - User Manual Verification 'Documentación' (Protocol in workflow.md)

---

## Fase 6: Paquete .deb [checkpoint: ]

- [ ] Task: Crear estructura debian/
    - [ ] Crear directorio debian/
    - [ ] Crear debian/control con metadatos
    - [ ] Crear debian/compat
    - [ ] Crear debian/source/format

- [ ] Task: Crear archivos de instalación
    - [ ] Crear debian/blugon-lite.install
    - [ ] Crear debian/blugon-lite.docs
    - [ ] Crear debian/conffiles
    - [ ] Crear debian/blugon-lite.maintscript

- [ ] Task: Crear scripts de mantenimiento
    - [ ] Crear debian/postinst (post-instalación)
    - [ ] Crear debian/prerm (pre-remoción)
    - [ ] Crear debian/postrm (post-remoción)
    - [ ] Hacer scripts ejecutables

- [ ] Task: Implementar postinst
    - [ ] Crear ~/.config/blugon/ si no existe
    - [ ] Copiar config por defecto si no existe config de usuario
    - [ ] Ofrecer activar servicio systemd (opcional)
    - [ ] Manejar actualización desde versión previa

- [ ] Task: Implementar prerm/postrm
    - [ ] Detener daemon si está corriendo
    - [ ] Opción de mantener configs del usuario
    - [ ] Limpieza de archivos temporales

- [ ] Task: Construir paquete .deb
    - [ ] Ejecutar dpkg-deb --build debian/
    - [ ] Verificar paquete con dpkg-deb --info
    - [ ] Listar contenido con dpkg-deb --content
    - [ ] Mover .deb a raíz del proyecto

- [ ] Task: Testing del paquete .deb
    - [ ] Instalar en sistema limpio (VM o container)
    - [ ] Verificar postinst se ejecuta
    - [ ] Verificar configs se instalan
    - [ ] Verificar TUI funciona
    - [ ] Verificar blugon-lite funciona
    - [ ] Probar desinstalación

- [ ] Task: Conductor - User Manual Verification 'Paquete .deb' (Protocol in workflow.md)

---

## Fase 7: Finalización [checkpoint: ]

- [ ] Task: Verificar criterios de aceptación
    - [ ] blugon-lite.py funciona sin config manual
    - [ ] blugon-lite-tui es intuitivo y funcional
    - [ ] Múltiples configs predefinidas disponibles
    - [ ] Documentación clara y completa
    - [ ] .deb se instala sin errores

- [ ] Task: Limpieza final
    - [ ] Eliminar archivos temporales
    - [ ] Verificar PEP 8 en código Python
    - [ ] Verificar que no hay código comentado
    - [ ] Optimizar si es necesario

- [ ] Task: Conductor - User Manual Verification 'Finalización' (Protocol in workflow.md)

---

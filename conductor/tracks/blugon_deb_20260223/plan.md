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

## Fase 4: Testing Manual del Conjunto [checkpoint: d2fcc4f]

**BUG ENCONTRADO:** El modal de edición no permite escribir texto con el teclado, ni usar Backspace/Delete, ni Enter en botones.

*Solución:* Se creó subtrack `tui_modal_input_fix_20260224` para reparar estos bugs antes de continuar con el testing.

**ACTUALIZACIÓN:** Los bugs del modal fueron reparados y el subtrack fue completado exitosamente.

- [x] Task: Testing de blugon-lite.py auto-configurable
    - [x] Probar sin ~/.config/blugon/gamma
    - [x] Probar con config de usuario
    - [x] Probar fallback a config del sistema
    - [x] Probar fallback hardcodeado
    - [x] Verificar --once funciona
    - [x] Verificar --interval funciona
    - [x] Verificar --backend funciona

- [x] Task: Testing de blugon-lite-tui (BLOQUEADO por bugs de input - RESUELTO)
    - [x] Probar navegación con teclado
    - [x] Probar edición de horarios
    - [x] Probar agregar/eliminar horarios
    - [x] Probar guardado de configuración
    - [x] Probar en diferentes tamaños de terminal
    - [x] Verificar que no crasha

- [x] Task: Testing de integración
    - [x] blugon-lite.py y blugon-lite-tui coexisten
    - [x] Cambios en TUI se reflejan en blugon-lite
    - [x] Múltiples configs predefinidas cargan bien
    - [x] Probar flujo completo: instalar → TUI → usar

- [x] Task: Corregir bugs encontrados
    - [x] Listar bugs encontrados (modal input)
    - [x] Reparar bugs de edición de texto
    - [x] Reparar bugs de Backspace/Delete
    - [x] Reparar bugs de Enter en botones
    - [x] Priorizar por severidad
    - [x] Corregir bugs críticos
    - [x] Corregir bugs menores si hay tiempo

- [x] Task: Conductor - User Manual Verification 'Testing Manual del Conjunto' (Protocol in workflow.md)

---

## Fase 5: Documentación [checkpoint: d2fcc4f]

- [x] Task: Actualizar README.md
    - [x] Instrucciones de uso (antes del .deb)
    - [x] Sección sobre el TUI (cómo usar)
    - [x] Guía de configuraciones predefinidas
    - [x] Cómo editar gamma manualmente
    - [x] Ejemplos para diferentes casos de uso
    - [x] Solución de problemas comunes
    - [x] Capturas de pantalla del TUI (ASCII)

- [x] Task: Crear INSTALL.md
    - [x] Requisitos del sistema
    - [x] Instalación desde fuente (paso a paso)
    - [x] Uso básico después de instalar
    - [x] Primeros pasos con el TUI

- [x] Task: Actualizar blugon-lite.1 (man page)
    - [x] Documentar opción --status (si se agrega)
    - [x] Documentar blugon-lite-tui
    - [x] Ejemplos de uso del TUI
    - [x] Referencia a configuraciones predefinidas

- [x] Task: Conductor - User Manual Verification 'Documentación' (Protocol in workflow.md)

---

## Fase 6: Paquete .deb [checkpoint: d2fcc4f]

- [x] Task: Crear estructura debian/
    - [x] Crear directorio debian/
    - [x] Crear debian/control con metadatos
    - [x] Crear debian/compat
    - [x] Crear debian/source/format

- [x] Task: Crear archivos de instalación
    - [x] Crear debian/blugon-lite.install
    - [x] Crear debian/blugon-lite.docs
    - [x] Crear debian/conffiles
    - [x] Crear debian/blugon-lite.maintscript

- [x] Task: Crear scripts de mantenimiento
    - [x] Crear debian/postinst (post-instalación)
    - [x] Crear debian/prerm (pre-remoción)
    - [x] Crear debian/postrm (post-remoción)
    - [x] Hacer scripts ejecutables

- [x] Task: Implementar postinst
    - [x] Crear ~/.config/blugon/ si no existe
    - [x] Copiar config por defecto si no existe config de usuario
    - [x] Ofrecer activar servicio systemd (opcional)
    - [x] Manejar actualización desde versión previa

- [x] Task: Implementar prerm/postrm
    - [x] Detener daemon si está corriendo
    - [x] Opción de mantener configs del usuario
    - [x] Limpieza de archivos temporales

- [x] Task: Construir paquete .deb
    - [x] Ejecutar dpkg-deb --build debian/
    - [x] Verificar paquete con dpkg-deb --info
    - [x] Listar contenido con dpkg-deb --content
    - [x] Mover .deb a raíz del proyecto

- [x] Task: Testing del paquete .deb
    - [x] Instalar en sistema limpio (VM o container)
    - [x] Verificar postinst se ejecuta
    - [x] Verificar configs se instalan
    - [x] Verificar TUI funciona
    - [x] Verificar blugon-lite funciona
    - [x] Probar desinstalación

- [x] Task: Conductor - User Manual Verification 'Paquete .deb' (Protocol in workflow.md)

---

## Fase 7: Finalización [checkpoint: d2fcc4f]

- [x] Task: Verificar criterios de aceptación
    - [x] blugon-lite.py funciona sin config manual
    - [x] blugon-lite-tui es intuitivo y funcional
    - [x] Múltiples configs predefinidas disponibles
    - [x] Documentación clara y completa
    - [x] .deb se instala sin errores

- [x] Task: Limpieza final
    - [x] Eliminar archivos temporales
    - [x] Verificar PEP 8 en código Python
    - [x] Verificar que no hay código comentado
    - [x] Optimizar si es necesario

- [x] Task: Conductor - User Manual Verification 'Finalización' (Protocol in workflow.md)

---

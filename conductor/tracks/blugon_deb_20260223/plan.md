# Implementation Plan: blugon_deb_20260223

## Track: Crear TUI con urwid y paquete .deb instalable

---

## Fase 1: Auto-Configuración del Script [checkpoint: ]

- [ ] Task: Modificar blugon-lite.py con fallback automático
    - [ ] Actualizar función read_gamma() para buscar en múltiples ubicaciones
    - [ ] Agregar configuración hardcodeada por defecto
    - [ ] Mantener compatibilidad con configs existentes
    - [ ] Testear que funciona sin ~/.config/blugon/gamma

- [ ] Task: Mejorar archivo configs/evening/gamma
    - [ ] Agregar comentarios detallados sobre formato
    - [ ] Incluir guía de temperaturas (6500K, 4500K, 3000K, 2000K)
    - [ ] Ejemplos de cómo agregar/quitar horarios
    - [ ] Mantener horario 17:00-08:00 como default

- [ ] Task: Conductor - User Manual Verification 'Auto-Configuración' (Protocol in workflow.md)

---

## Fase 2: TUI con urwid [checkpoint: ]

- [ ] Task: Configurar entorno de desarrollo para TUI
    - [ ] Instalar urwid (pip install urwid)
    - [ ] Crear archivo blugon-lite-tui.py básico
    - [ ] Implementar ventana principal con título
    - [ ] Implementar loop principal de urwid

- [ ] Task: Implementar visualización de horarios
    - [ ] Leer configuración actual desde ~/.config/blugon/gamma
    - [ ] Mostrar lista de horarios con navegación (↑↓)
    - [ ] Mostrar gamma actual y próxima transición
    - [ ] Resaltar horario seleccionado

- [ ] Task: Implementar edición de horarios
    - [ ] Dialog para editar hora (HH:MM)
    - [ ] Dialog para editar temperatura (Kelvin)
    - [ ] Validación de inputs (hora 0-23, temp 1000-20000)
    - [ ] Vista previa de cambios antes de guardar

- [ ] Task: Implementar agregar/eliminar horarios
    - [ ] Dialog para agregar nuevo horario
    - [ ] Confirmación antes de eliminar
    - [ ] Ordenamiento automático por hora
    - [ ] Prevención de duplicados

- [ ] Task: Implementar guardado y salida
    - [ ] Guardar cambios a ~/.config/blugon/gamma
    - [ ] Confirmación si hay cambios sin guardar
    - [ ] Mensaje de éxito después de guardar
    - [ ] Atajos: 's' guardar, 'q' salir, 'h' ayuda

- [ ] Task: Implementar características adicionales
    - [ ] Mostrar estado del daemon (corriendo/detenido)
    - [ ] Botón para iniciar/detener daemon
    - [ ] About screen (tecla 'a')
    - [ ] Help screen (tecla 'h')
    - [ ] Colores y estilos apropiados

- [ ] Task: Crear wrapper ejecutable blugon-lite-tui
    - [ ] Script bash que llama a Python
    - [ ] Verificar dependencias (python3, urwid)
    - [ ] Manejo de errores si faltan dependencias
    - [ ] Hacer ejecutable (chmod +x)

- [ ] Task: Conductor - User Manual Verification 'TUI con urwid' (Protocol in workflow.md)

---

## Fase 3: Configuraciones Predefinidas [checkpoint: ]

- [ ] Task: Crear config office/gamma
    - [ ] Horario típico oficina (9:00-18:00)
    - [ ] 5-6 puntos de transición
    - [ ] Comentarios específicos para este perfil

- [ ] Task: Crear config student/gamma
    - [ ] Horarios extendidos (estudiante)
    - [ ] Más horas de luz normal
    - [ ] Transición más tarde en la noche

- [ ] Task: Crear config night-owl/gamma
    - [ ] Para usuarios nocturnos
    - [ ] Luz normal hasta tarde
    - [ ] Transición más tarde

- [ ] Task: Crear config minimal/gamma
    - [ ] Solo 3 puntos: día, tarde, noche
    - [ ] Simple y fácil de entender
    - [ ] Ideal para usuarios nuevos

- [ ] Task: Actualizar Makefile
    - [ ] Incluir nuevas configs en install
    - [ ] Actualizar rutas de instalación

- [ ] Task: Conductor - User Manual Verification 'Configuraciones Predefinidas' (Protocol in workflow.md)

---

## Fase 4: Testing Manual del Conjunto [checkpoint: ]

- [ ] Task: Testing de blugon-lite.py auto-configurable
    - [ ] Probar sin ~/.config/blugon/gamma
    - [ ] Probar con config de usuario
    - [ ] Probar fallback a config del sistema
    - [ ] Probar fallback hardcodeado
    - [ ] Verificar --once funciona
    - [ ] Verificar --interval funciona
    - [ ] Verificar --backend funciona

- [ ] Task: Testing de blugon-lite-tui
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

- [ ] Task: Corregir bugs encontrados
    - [ ] Listar bugs encontrados
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

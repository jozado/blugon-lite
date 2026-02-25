# Implementation Plan: tui_modal_input_fix_20260224

## Track: Reparar bugs de input del modal de edición del TUI

---

## Fase 1: Análisis y Diagnóstico [checkpoint: ]

- [ ] Task: Analizar el flujo actual de entrada de teclas
    - [ ] Revisar input_filter en app.py
    - [ ] Revisar handle_modal_input en app.py
    - [ ] Revisar ModalOverlay.keypress
    - [ ] Identificar dónde se pierden las teclas

- [ ] Task: Identificar bugs específicos
    - [ ] Por qué no funciona escritura de texto
    - [ ] Por qué no funciona Enter en botones
    - [ ] Por qué no funciona Backspace/Delete

- [ ] Task: Documentar diagnóstico en notas del track

---

## Fase 2: Reparar input_filter [checkpoint: ]

- [ ] Task: Refactorizar input_filter para detectar modal
    - [ ] Verificar si modal_open es True
    - [ ] Si modal está abierto, pasar todas las teclas
    - [ ] Si modal está cerrado, usar comportamiento normal

- [ ] Task: Asegurar que ESC siempre funcione
    - [ ] ESC debe cerrar modal desde cualquier lugar
    - [ ] ESC debe manejarse antes que otros inputs

- [ ] Task: Testear input_filter corregido
    - [ ] Abrir modal con 'e'
    - [ ] Verificar que teclas llegan al modal
    - [ ] Verificar que navegación principal no se rompe

---

## Fase 3: Reparar handle_modal_input [checkpoint: ]

- [ ] Task: Manejar caracteres imprimibles para etiqueta
    - [ ] Detectar si key es carácter imprimible (len == 1)
    - [ ] Agregar carácter al valor de etiqueta
    - [ ] Limitar a 20 caracteres máximo

- [ ] Task: Manejar Backspace correctamente
    - [ ] Detectar 'backspace' y 'ctrl h'
    - [ ] Borrar último carácter
    - [ ] Manejar string vacío

- [ ] Task: Manejar Delete correctamente
    - [ ] Detectar 'delete' y 'ctrl d'
    - [ ] Borrar todo el contenido
    - [ ] Resetear a string vacío

- [ ] Task: Manejar Enter para botones
    - [ ] Si campo seleccionado es 4 (Guardar), ejecutar save
    - [ ] Si campo seleccionado es 5 (Cancelar), ejecutar cancel
    - [ ] Retornar después de ejecutar para evitar redibujado extra

- [ ] Task: Mejorar navegación entre campos
    - [ ] Up/Down navegan entre campos (0-5)
    - [ ] Left/Right modifican valores (campos 0-2)
    - [ ] Tab va directo a botón Guardar
    - [ ] Shift+Tab va hacia atrás

---

## Fase 4: Limpieza y Refactorización [checkpoint: ]

- [ ] Task: Eliminar logs de debug
    - [ ] Remover escritura a /tmp/tui_modal.log
    - [ ] Remover escritura a /tmp/tui_label.log

- [ ] Task: Refactorizar código duplicado
    - [ ] Unificar lógica edit/add donde sea posible
    - [ ] Extraer funciones helper si es necesario

- [ ] Task: Agregar docstrings
    - [ ] Documentar input_filter
    - [ ] Documentar handle_modal_input
    - [ ] Documentar funciones auxiliares

---

## Fase 5: Testing Manual [checkpoint: ]

- [ ] Task: Probar edición de etiqueta
    - [ ] Escribir texto "Mi Horario"
    - [ ] Verificar que se muestra correctamente
    - [ ] Guardar y verificar persistencia

- [ ] Task: Probar Backspace
    - [ ] Escribir "Hola"
    - [ ] Borrar con Backspace carácter por carácter
    - [ ] Verificar que se borra correctamente

- [ ] Task: Probar Delete
    - [ ] Escribir "Hola"
    - [ ] Presionar Delete
    - [ ] Verificar que se borra todo

- [ ] Task: Probar Enter en botones
    - [ ] Navegar a "Guardar" con Tab
    - [ ] Presionar Enter
    - [ ] Verificar que guarda
    - [ ] Navegar a "Cancelar"
    - [ ] Presionar Enter
    - [ ] Verificar que cancela

- [ ] Task: Probar navegación completa
    - [ ] Up/Down entre campos
    - [ ] Left/Right en valores numéricos
    - [ ] Tab a botones
    - [ ] ESC cancela

- [ ] Task: Conductor - User Manual Verification (Protocol in workflow.md)

---

## Fase 6: Finalización [checkpoint: ]

- [ ] Task: Actualizar plan.md del track principal
    - [ ] Marcar bugs como corregidos
    - [ ] Agregar nota de la reparación

- [ ] Task: Commit final
    - [ ] Stage todos los cambios
    - [ ] Commit con mensaje descriptivo
    - [ ] Git note con resumen del fix

- [ ] Task: Marcar track como completo
    - [ ] Update tracks.md
    - [ ] Commit

---

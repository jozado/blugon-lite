# Implementation Plan: tui_modal_input_fix_20260224

## Track: Reparar bugs de input del modal de edición del TUI

---

## Fase 1: Análisis y Diagnóstico [checkpoint: f7fb942]

- [x] Task: Analizar el flujo actual de entrada de teclas
    - [x] Revisar input_filter en app.py
    - [x] Revisar handle_modal_input en app.py
    - [x] Revisar ModalOverlay.keypress
    - [x] Identificar dónde se pierden las teclas

- [x] Task: Identificar bugs específicos
    - [x] Por qué no funciona escritura de texto
    - [x] Por qué no funciona Enter en botones
    - [x] Por qué no funciona Backspace/Delete

- [x] Task: Documentar diagnóstico en notas del track

---

## Fase 2: Reparar input_filter [checkpoint: f7fb942]

- [x] Task: Refactorizar input_filter para detectar modal
    - [x] Verificar si modal_open es True
    - [x] Si modal está abierto, pasar todas las teclas
    - [x] Si modal está cerrado, usar comportamiento normal

- [x] Task: Asegurar que ESC siempre funcione
    - [x] ESC debe cerrar modal desde cualquier lugar
    - [x] ESC debe manejarse antes que otros inputs

- [x] Task: Testear input_filter corregido
    - [x] Abrir modal con 'e'
    - [x] Verificar que teclas llegan al modal
    - [x] Verificar que navegación principal no se rompe

---

## Fase 3: Reparar handle_modal_input [checkpoint: f7fb942]

- [x] Task: Manejar caracteres imprimibles para etiqueta
    - [x] Detectar si key es carácter imprimible (len == 1)
    - [x] Agregar carácter al valor de etiqueta
    - [x] Limitar a 20 caracteres máximo

- [x] Task: Manejar Backspace correctamente
    - [x] Detectar 'backspace' y 'ctrl h'
    - [x] Borrar último carácter
    - [x] Manejar string vacío

- [x] Task: Manejar Delete correctamente
    - [x] Detectar 'delete' y 'ctrl d'
    - [x] Borrar todo el contenido
    - [x] Resetear a string vacío

- [x] Task: Manejar Enter para botones
    - [x] Si campo seleccionado es 4 (Guardar), ejecutar save
    - [x] Si campo seleccionado es 5 (Cancelar), ejecutar cancel
    - [x] Retornar después de ejecutar para evitar redibujado extra

- [x] Task: Mejorar navegación entre campos
    - [x] Up/Down navegan entre campos (0-5)
    - [x] Left/Right modifican valores (campos 0-2)
    - [x] Tab va directo a botón Guardar
    - [x] Shift+Tab va hacia atrás

---

## Fase 4: Limpieza y Refactorización [checkpoint: f7fb942]

- [x] Task: Eliminar logs de debug
    - [x] Remover escritura a /tmp/tui_modal.log
    - [x] Remover escritura a /tmp/tui_label.log

- [x] Task: Refactorizar código duplicado
    - [x] Unificar lógica edit/add donde sea posible
    - [x] Extraer funciones helper si es necesario

- [x] Task: Agregar docstrings
    - [x] Documentar input_filter
    - [x] Documentar handle_modal_input
    - [x] Documentar funciones auxiliares

---

## Fase 5: Testing Manual [checkpoint: f7fb942]

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

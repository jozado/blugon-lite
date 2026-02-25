# Track Specification: tui_modal_input_fix_20260224

## Descripción

Reparar los bugs del modal de edición/agregado del TUI relacionados con la entrada de texto y navegación.

**Problemas identificados:**
1. No se puede escribir texto con el teclado en el campo "Etiqueta"
2. No funciona Backspace para borrar carácter por carácter
3. No funciona Delete para borrar todo el contenido
4. Los botones "Guardar"/"Cancelar" no responden a Enter
5. El campo de etiqueta no permite edición textual completa

**Causa raíz:** El `input_filter` del `urwid.MainLoop` está capturando las teclas antes de que lleguen al manejador del modal, y el `handle_modal_input` no está procesando correctamente todas las teclas de texto.

## Alcance

### Características a Reparar

1. **Input Filter Corregido** (Prioridad: ALTA)
   - El input_filter debe detectar si hay un modal abierto
   - Si hay modal abierto, pasar TODAS las teclas al modal (excepto ESC)
   - Si no hay modal, usar el comportamiento normal de navegación

2. **Edición de Texto en Campo Etiqueta** (Prioridad: ALTA)
   - Permitir escribir caracteres imprimibles (a-z, 0-9, espacios, etc.)
   - Backspace borra último carácter
   - Delete borra todo el contenido
   - Máximo 20 caracteres para etiqueta

3. **Botones con Enter** (Prioridad: ALTA)
   - Enter en campo "Guardar" ejecuta guardado
   - Enter en campo "Cancelar" ejecuta cancelación
   - Feedback visual del botón seleccionado

4. **Navegación Mejorada** (Prioridad: MEDIA)
   - Tab navega entre campos
   - Shift+Tab navega hacia atrás
   - Flechas arriba/abajo navegan entre campos (no valores)
   - Flechas izquierda/derecha modifican valores numéricos

### Características NO incluidas en este track

- Cambios en la estructura visual del modal
- Nuevos campos o funcionalidades adicionales
- Cambios en otros modales (theme selector, confirm dialogs)

## Requisitos Técnicos

### Código
- **blugon-lite-tui.py**: Sin cambios
- **tui/app.py**: Refactorizar `input_filter` y `handle_modal_input`
- **Mantener compatibilidad**: No romper navegación existente

### Testing
- Probar escritura de texto en campo etiqueta
- Probar Backspace y Delete
- Probar Enter en botones
- Probar navegación con Tab/flechas

## Entregables

### Código Modificado
1. **tui/app.py** (refactorizado)
   - `input_filter` corregido para modales
   - `handle_modal_input` con manejo completo de teclas
   - `edit_schedule` con campo de etiqueta editable

### Testing
2. **Pruebas manuales completadas**
   - Editar etiqueta con texto personalizado
   - Borrar con Backspace carácter por carácter
   - Borrar con Delete todo el contenido
   - Guardar con Enter
   - Cancelar con Enter

## Criterios de Aceptación

### Funcionalidad
- [ ] Se puede escribir texto en el campo "Etiqueta"
- [ ] Backspace borra último carácter
- [ ] Delete borra todo el contenido
- [ ] Enter en "Guardar" ejecuta guardado
- [ ] Enter en "Cancelar" ejecuta cancelación
- [ ] Tab navega entre campos
- [ ] Flechas arriba/abajo navegan entre campos
- [ ] Flechas izquierda/derecha modifican valores numéricos

### Calidad de Código
- [ ] No hay código duplicado
- [ ] Funciones documentadas con docstrings
- [ ] No hay logs de debug (/tmp/tui_*.log)
- [ ] Código sigue PEP 8

## Notas de Implementación

### Sobre el input_filter
El input_filter de urwid recibe una lista de teclas y debe retornar:
- Lista vacía `[]` si consume las teclas
- Lista con teclas si quiere pasarlas al widget

Para modales, el filter debe:
```python
if modal_open:
    return keys  # Pasar todas las teclas al modal
```

### Sobre handle_modal_input
Debe manejar:
1. Teclas de navegación (up, down, left, right, tab)
2. Teclas de texto (caracteres imprimibles)
3. Teclas de edición (backspace, delete, enter, esc)

### Orden de Implementación
1. Primero: Arreglar input_filter para detectar modal
2. Segundo: Arreglar handle_modal_input para texto
3. Tercero: Arreglar Enter para botones
4. Cuarto: Testing manual completo

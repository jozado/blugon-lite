#!/usr/bin/env python3
"""
Manejador de entrada de teclado para el TUI de blugon-lite.

Este módulo centraliza el procesamiento de todas las entradas de teclado,
tanto para la pantalla principal como para los modales.
"""

import urwid
from .modals import ModalOverlay


class InputHandler:
    """
    Manejador centralizado de entrada de teclado.
    
    Responsable de:
    - Filtrar teclas para la pantalla principal (navegación ↑↓)
    - Pasar teclas al modal cuando está abierto
    - Procesar teclas dentro del modal (edición, navegación, acciones)
    """
    
    def __init__(self, app):
        """
        Inicializar el manejador de input.
        
        Args:
            app: Referencia a la aplicación BlugonLiteTUI principal
        """
        self.app = app
        self.current_modal = None  # Modal activo actual
    
    def set_modal(self, modal):
        """
        Establecer el modal activo.
        
        Args:
            modal: El modal que está actualmente abierto
        """
        self.current_modal = modal
    
    def clear_modal(self):
        """Limpiar la referencia al modal."""
        self.current_modal = None
    
    def create_input_filter(self):
        """
        Crear el input filter para urwid.MainLoop.
        
        El filter decide qué teclas consumir y cuáles pasar al widget.
        
        Returns:
            function: Función input_filter para urwid
        """
        def input_filter(keys, raw):
            # Si hay modal abierto, procesar TODAS las teclas aquí
            if hasattr(self.app, 'modal_open') and self.app.modal_open:
                for key in keys:
                    # Todas las teclas van al handler del modal
                    self.app.handle_modal_input(key)
                # Consumir TODAS las teclas (no pasar ninguna al widget)
                return []

            # Pantalla principal: consumir flechas para navegación
            for key in keys:
                if key in ('up', 'cursor up'):
                    self.app.on_navigate_up()
                    return []
                elif key in ('down', 'cursor down'):
                    self.app.on_navigate_down()
                    return []

            # Pasar otras teclas al handle_input normal
            return keys

        return input_filter
    
    def handle_modal_input(self, key):
        """
        Procesar entrada de teclado dentro del modal.

        Maneja:
        - Navegación entre campos (up, down, tab, shift+tab)
        - Modificación de valores numéricos (left, right)
        - Edición de texto (caracteres imprimibles, backspace, delete)
        - Acciones (enter, escape)

        Args:
            key: La tecla presionada
        """
        # Debug: log de teclas en modal
        with open('/tmp/tui_debug.log', 'a') as f:
            f.write(f'HANDLE_MODAL_INPUT: key={repr(key)}, edit_index={hasattr(self.app, "edit_index")}, add_hour={hasattr(self.app, "add_hour")}, delete_confirm={hasattr(self.app, "delete_confirm_open")}\n')
            f.flush()

        # ESC siempre cierra el modal
        if key in ('esc', 'escape'):
            self._close_modal()
            return

        # Determinar tipo de modal
        is_edit = hasattr(self.app, 'edit_index')
        is_add = hasattr(self.app, 'add_hour')
        is_delete = hasattr(self.app, 'delete_confirm_open')
        is_theme = hasattr(self.app, 'theme_selector_open')

        # Modal de eliminación o temas se maneja directamente
        if (is_delete or is_theme) and not is_edit and not is_add:
            with open('/tmp/tui_debug.log', 'a') as f:
                f.write(f'ES MODAL DE ELIMINACION O TEMAS, DELEGO AL MODAL\n')
                f.write(f'current_modal exists: {hasattr(self.app, "current_modal")}\n')
                f.write(f'current_modal: {self.app.current_modal if hasattr(self.app, "current_modal") else None}\n')
                f.flush()
            if hasattr(self.app, 'current_modal') and self.app.current_modal:
                self.app.current_modal.handle_input(key)
            return

        if not is_edit and not is_add:
            with open('/tmp/tui_debug.log', 'a') as f:
                f.write('NO ES EDIT NI ADD NI DELETE, RETORNO\n')
                f.flush()
            return

        changed = False
        rebuild = False

        # Obtener campo seleccionado
        if is_edit:
            field_selected = getattr(self.app, 'edit_field_selected', 0)
        else:
            field_selected = getattr(self.app, 'add_field_selected', 0)

        with open('/tmp/tui_debug.log', 'a') as f:
            f.write(f'field_selected={field_selected}, is_edit={is_edit}, is_add={is_add}\n')
            f.flush()
        
        # Procesar tecla según el campo y tipo de modal
        if key in ('up', 'cursor up'):
            self._navigate_field(-1, wrap=True)
            changed = True
            rebuild = True
        elif key in ('down', 'cursor down'):
            self._navigate_field(1, wrap=True)
            changed = True
            rebuild = True
        elif key == 'tab':
            # Tab siempre va a la zona de botones (Guardar/Cancelar)
            # Si ya está en botones, alterna entre ellos
            self._go_to_buttons()
            changed = True
            rebuild = True
        elif key == 'shift tab':
            # Shift+Tab va al campo anterior (navegación inversa)
            self._navigate_field(-1, wrap=True)
            changed = True
            rebuild = True
        elif key in ('left', 'cursor left'):
            changed = self._adjust_value(-1)
        elif key in ('right', 'cursor right'):
            changed = self._adjust_value(1)
        elif key == 'enter':
            self._handle_enter()
            return
        elif field_selected == 3:  # Campo de etiqueta
            changed = self._edit_label(key)
        
        if changed:
            self._update_modal()
    
    def _close_modal(self):
        """Cerrar el modal actual."""
        if hasattr(self.app, 'edit_index'):
            self.app.cancel_edit()
        elif hasattr(self.app, 'add_hour'):
            self.app.cancel_add()
        elif hasattr(self.app, 'theme_selector_open'):
            self.app.cancel_theme()
        elif hasattr(self.app, 'delete_confirm_open'):
            self.app.cancel_delete()
        elif hasattr(self.app, 'confirm_exit_open'):
            self.app.confirm_exit_no()
        else:
            self.app.modal_open = False
            self.app.loop.widget = self.app.main_frame
    
    def _navigate_field(self, direction, wrap=True):
        """
        Navegar entre campos del modal.
        
        Args:
            direction: -1 para arriba, 1 para abajo
            wrap: Si True, navegación circular (0-5), si False va directo a botones
        """
        is_edit = hasattr(self.app, 'edit_index')
        max_field = 5  # 0=Hora, 1=Minuto, 2=Temp, 3=Etiqueta, 4=Guardar, 5=Cancelar

        if is_edit:
            current = getattr(self.app, 'edit_field_selected', 0)
            new_field = current + direction
            if wrap:
                new_field = (current + direction) % (max_field + 1)
            else:
                new_field = max(0, min(max_field, new_field))
            self.app.edit_field_selected = new_field
        else:
            current = getattr(self.app, 'add_field_selected', 0)
            new_field = current + direction
            if wrap:
                new_field = (current + direction) % (max_field + 1)
            else:
                new_field = max(0, min(max_field, new_field))
            self.app.add_field_selected = new_field

    def _go_to_buttons(self):
        """
        Ir a la zona de botones (Guardar/Cancelar).
        
        Si ya está en botones, alterna entre Guardar (4) y Cancelar (5).
        Si está en campos de edición (0-3), va directo a Guardar (4).
        """
        is_edit = hasattr(self.app, 'edit_index')
        
        if is_edit:
            current = getattr(self.app, 'edit_field_selected', 0)
            if current >= 4:
                # Ya está en botones, alternar
                self.app.edit_field_selected = 5 if current == 4 else 4
            else:
                # Está en campos, ir a Guardar
                self.app.edit_field_selected = 4
        else:
            current = getattr(self.app, 'add_field_selected', 0)
            if current >= 4:
                # Ya está en botones, alternar
                self.app.add_field_selected = 5 if current == 4 else 4
            else:
                # Está en campos, ir a Agregar
                self.app.add_field_selected = 4
    
    def _adjust_value(self, direction):
        """
        Ajustar valor numérico de campo seleccionado.
        
        Args:
            direction: -1 para disminuir, 1 para aumentar
            
        Returns:
            bool: True si el valor cambió
        """
        is_edit = hasattr(self.app, 'edit_index')
        field = getattr(self.app, 'edit_field_selected' if is_edit else 'add_field_selected', 0)
        
        # Si estamos en botones (campo 4+), mover selección
        if field >= 4:
            if is_edit:
                self.app.edit_field_selected = 5 if direction > 0 else 4
            else:
                self.app.add_field_selected = 5 if direction > 0 else 4
            return True
        
        # Campo de etiqueta no se ajusta con flechas
        if field == 3:
            return False
        
        changed = False
        if is_edit:
            if field == 0:  # Hora
                self.app.edit_hour_val = (self.app.edit_hour_val + direction) % 24
                changed = True
            elif field == 1:  # Minuto
                self.app.edit_minute_val = (self.app.edit_minute_val + direction * 5) % 60
                changed = True
            elif field == 2:  # Temperatura
                new_temp = self.app.edit_temp_val + direction * 100
                self.app.edit_temp_val = max(1000, min(20000, new_temp))
                changed = True
        else:
            if field == 0:  # Hora
                self.app.add_hour = (self.app.add_hour + direction) % 24
                changed = True
            elif field == 1:  # Minuto
                self.app.add_minute = (self.app.add_minute + direction * 5) % 60
                changed = True
            elif field == 2:  # Temperatura
                new_temp = self.app.add_temp + direction * 100
                self.app.add_temp = max(1000, min(20000, new_temp))
                changed = True
        
        return changed
    
    def _handle_enter(self):
        """Manejar tecla Enter según campo seleccionado."""
        is_edit = hasattr(self.app, 'edit_index')
        field = getattr(self.app, 'edit_field_selected' if is_edit else 'add_field_selected', 0)
        
        if field == 4:  # Guardar/Agregar
            if is_edit:
                self.app.save_edit_from_modal()
            else:
                self.app.save_add_from_modal()
        elif field == 5:  # Cancelar
            if is_edit:
                self.app.cancel_edit()
            else:
                self.app.cancel_add()
        elif field < 3:  # Campos numéricos también guardan con Enter
            if is_edit:
                self.app.save_edit_from_modal()
            else:
                self.app.save_add_from_modal()
    
    def _edit_label(self, key):
        """
        Editar campo de etiqueta con teclado.
        
        Args:
            key: La tecla presionada
            
        Returns:
            bool: True si el valor cambió
        """
        is_edit = hasattr(self.app, 'edit_index')
        is_add = hasattr(self.app, 'add_hour')

        if key in ('backspace', 'ctrl h'):
            if is_edit and hasattr(self.app, 'edit_label_val'):
                self.app.edit_label_val = self.app.edit_label_val[:-1]
                return True
            elif is_add and hasattr(self.app, 'add_label_val'):
                self.app.add_label_val = self.app.add_label_val[:-1]
                return True
        elif key in ('delete', 'ctrl d'):
            if is_edit:
                self.app.edit_label_val = ""
                return True
            else:
                self.app.add_label_val = ""
                return True
        elif len(key) == 1 and key.isprintable():
            if is_edit and hasattr(self.app, 'edit_label_val'):
                if len(self.app.edit_label_val) < 20:
                    self.app.edit_label_val += key
                    return True
            elif is_add and hasattr(self.app, 'add_label_val'):
                if len(self.app.add_label_val) < 20:
                    self.app.add_label_val += key
                    return True

        return False
    
    def _update_modal(self):
        """Actualizar vista previa y redibujar modal."""
        is_edit = hasattr(self.app, 'edit_index')

        # Actualizar la vista previa de color
        if is_edit:
            self.app.edit_color_preview.update(self.app.edit_temp_val)
        else:
            self.app.add_color_preview.update(self.app.add_temp)

        # Reconstruir el body del modal actual
        if hasattr(self.app, 'current_modal') and self.app.current_modal:
            new_body = self.app.current_modal.build_body()
            # Reemplazar el body del overlay
            self.app.loop.widget = ModalOverlay(
                new_body,
                self.app.current_modal.title if hasattr(self.app.current_modal, 'title') else "Editar Horario",
                width=('relative', 90),
                height=('relative', 90),
                on_keypress=lambda key: self.app.current_modal.handle_input(key)
            )

        self.app.loop.draw_screen()

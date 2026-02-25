#!/usr/bin/env python3
"""
Modal de confirmación de eliminación para el TUI de blugon-lite.
"""

import urwid
from .base import ModalBuilder


class DeleteConfirmModal:
    """Modal para confirmar eliminación de horario."""
    
    def __init__(self, app, index, schedule):
        """
        Inicializar el modal de confirmación.
        
        Args:
            app: Referencia a la aplicación principal
            index: Índice del horario a eliminar
            schedule: Datos del horario
        """
        self.app = app
        self.index = index
        self.schedule = schedule
        self.body = None
        self.title = "Confirmar Eliminación"
        
        # Establecer este modal como el activo
        self.app.current_modal = self
    
    def build_body(self):
        """Construir el cuerpo del modal."""
        # Incluir la etiqueta en el mensaje
        label = self.schedule.get('label', '')
        if label:
            mensaje = f"¿Eliminar horario \"{label}\" {self.schedule['time_str']} ({self.schedule['temp_str']})?"
        else:
            mensaje = f"¿Eliminar horario {self.schedule['time_str']} ({self.schedule['temp_str']})?"
        
        self.body = urwid.Pile([
            urwid.Text(""),
            urwid.Text(mensaje),
            urwid.Divider(),
            urwid.Button("Sí, eliminar", lambda b: self.confirm()),
            urwid.Button("No, cancelar", lambda b: self.cancel()),
        ])
        self.body.set_focus(3)  # Foco inicial en "Sí, eliminar"
        return self.body
    
    def handle_input(self, key):
        """
        Manejar entrada de teclado en el modal de eliminación.
        
        Args:
            key: Tecla presionada
        """
        # ESC cierra el modal
        if key in ('esc', 'escape'):
            self.cancel()
            return
        
        if self.body is None:
            return
        
        focus = self.body.get_focus()
        
        # Navegación con flechas
        if key in ('up', 'cursor up'):
            if focus == 3:  # Botón "Sí"
                self.body.set_focus(4)  # Ir a "No"
            elif focus == 4:  # Botón "No"
                self.body.set_focus(3)  # Ir a "Sí"
            return
        elif key in ('down', 'cursor down'):
            if focus == 4:  # Botón "No"
                self.body.set_focus(3)  # Ir a "Sí"
            elif focus == 3:  # Botón "Sí"
                self.body.set_focus(4)  # Ir a "No"
            return
        # Enter ejecuta el botón seleccionado
        elif key == 'enter':
            if focus == 3:
                self.confirm()
            elif focus == 4:
                self.cancel()
            return
    
    def confirm(self):
        """Confirmar eliminación."""
        del self.app.schedules[self.index]
        if self.app.selected_index >= len(self.app.schedules):
            self.app.selected_index = max(0, len(self.app.schedules) - 1)
        self.app.refresh_schedule_list()
        self.app.show_message("Horario eliminado", 'success')
        self.app.current_modal = None
        self.app.modal_open = False
        self.app.delete_confirm_open = False
        self.app.loop.widget = self.app.main_frame
        self.app.loop.draw_screen()
        self.app.save_config()
    
    def cancel(self):
        """Cancelar eliminación."""
        self.app.current_modal = None
        self.app.delete_confirm_open = False
        self.app.modal_open = False
        self.app.loop.widget = self.app.main_frame
        self.app.loop.draw_screen()

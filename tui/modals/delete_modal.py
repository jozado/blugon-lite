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
    
    def build_body(self):
        """Construir el cuerpo del modal."""
        self.body = urwid.Pile([
            urwid.Text(""),
            urwid.Text(f"¿Eliminar horario {self.schedule['time_str']} ({self.schedule['temp_str']})?"),
            urwid.Divider(),
            urwid.Button("Sí, eliminar", lambda b: self.confirm()),
            urwid.Button("No, cancelar", lambda b: self.cancel()),
        ])
        self.body.set_focus(3)  # Foco inicial en "Sí, eliminar"
        return self.body
    
    def handle_input(self, key):
        """
        Manejar entrada de teclado.
        
        Args:
            key: Tecla presionada
            
        Returns:
            bool: True si se consumió la tecla
        """
        if self.body is None:
            return False
        
        if key in ('up', 'cursor up'):
            focus = self.body.get_focus()
            if focus == 3:
                self.body.set_focus(4)
            elif focus == 4:
                self.body.set_focus(3)
            return True
        elif key in ('down', 'cursor down'):
            focus = self.body.get_focus()
            if focus == 4:
                self.body.set_focus(3)
            elif focus == 3:
                self.body.set_focus(4)
            return True
        elif key == 'enter':
            focus = self.body.get_focus()
            if focus == 3:
                self.confirm()
            elif focus == 4:
                self.cancel()
            return True
        elif key == 'esc':
            self.cancel()
            return True
        
        return False
    
    def confirm(self):
        """Confirmar eliminación."""
        del self.app.schedules[self.index]
        if self.app.selected_index >= len(self.app.schedules):
            self.app.selected_index = max(0, len(self.app.schedules) - 1)
        self.app.refresh_schedule_list()
        self.app.show_message("Horario eliminado", 'success')
        self.app.modal_open = False
        self.app.delete_confirm_open = False
        self.app.loop.widget = self.app.main_frame
        self.app.loop.draw_screen()
        self.app.save_config()
    
    def cancel(self):
        """Cancelar eliminación."""
        self.app.delete_confirm_open = False
        self.app.modal_open = False
        self.app.loop.widget = self.app.main_frame
        self.app.loop.draw_screen()

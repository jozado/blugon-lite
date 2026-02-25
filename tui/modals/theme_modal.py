#!/usr/bin/env python3
"""
Modal de selección de temas para el TUI de blugon-lite.
"""

import urwid
from ..themes import THEMES


class ThemeSelectorModal:
    """Modal para seleccionar tema de colores."""
    
    def __init__(self, app):
        """
        Inicializar el modal de selección de temas.
        
        Args:
            app: Referencia a la aplicación principal
        """
        self.app = app
        self.title = "Temas"
        self.body = None
        self.selected_index = 0
        
        # Establecer este modal como el activo
        self.app.current_modal = self
        self.app.theme_selector_open = True
    
    def build_body(self):
        """Construir el cuerpo del modal."""
        theme_buttons = []
        for idx, (theme_id, (theme_name, _)) in enumerate(THEMES.items()):
            btn = urwid.Button(theme_name, lambda b, tid=theme_id: self.select_theme(tid))
            theme_buttons.append(urwid.AttrMap(btn, 'default', 'selected'))
        
        self.body = urwid.Pile([
            urwid.AttrMap(urwid.Text("Seleccionar Tema"), 'header'),
            urwid.Divider(),
        ] + theme_buttons + [
            urwid.Divider(),
            urwid.Button("Cancelar", lambda b: self.cancel()),
        ])
        self.body.focus_position = 2  # Primer botón de tema
        
        return self.body
    
    def handle_input(self, key):
        """
        Manejar entrada de teclado en el modal de temas.
        
        Args:
            key: Tecla presionada
        """
        if self.body is None:
            return
        
        # ESC cierra el modal
        if key in ('esc', 'escape'):
            self.cancel()
            return
        
        focus_index = self.body.focus_position
        total_items = len(self.body.contents)
        
        # Navegación con flechas
        if key in ('up', 'cursor up'):
            if focus_index > 2:  # Después del header y divider
                self.body.focus_position = focus_index - 1
            return
        elif key in ('down', 'cursor down'):
            if focus_index < total_items - 1:
                self.body.focus_position = focus_index + 1
            return
        # Enter selecciona el botón enfocado
        elif key == 'enter':
            # Obtener el widget enfocado usando focus_position
            focus_pos = self.body.focus_position
            focus_widget = self.body.contents[focus_pos][0]
            
            if isinstance(focus_widget, urwid.AttrMap):
                focus_widget = focus_widget.original_widget
            if isinstance(focus_widget, urwid.Button):
                # Simular click
                focus_widget._emit('click')
            return
    
    def select_theme(self, theme_id):
        """Seleccionar y aplicar un tema."""
        self.app.theme_selector_open = False
        self.app.current_modal = None
        if theme_id in THEMES:
            self.app.loop.screen.register_palette(THEMES[theme_id][1])
            self.app.current_theme = theme_id
            self.app.show_message(f"Tema cambiado a {theme_id}", 'success')
        self.app.modal_open = False
        self.app.loop.widget = self.app.main_frame
        self.app.loop.draw_screen()
    
    def cancel(self):
        """Cancelar selección de tema."""
        self.app.theme_selector_open = False
        self.app.current_modal = None
        self.app.modal_open = False
        self.app.loop.widget = self.app.main_frame
        self.app.loop.draw_screen()

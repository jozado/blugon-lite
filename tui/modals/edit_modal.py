#!/usr/bin/env python3
"""
Modal de edición de horarios para el TUI de blugon-lite.
"""

import urwid
from ..utils import get_label_for_time
from ..widgets import ColorPreview
from .base import ModalBuilder


class EditScheduleModal:
    """Modal para editar un horario existente."""
    
    def __init__(self, app, index, schedule):
        """
        Inicializar el modal de edición.
        
        Args:
            app: Referencia a la aplicación principal
            index: Índice del horario en la lista
            schedule: Datos del horario a editar
        """
        self.app = app
        self.index = index
        self.schedule = schedule
        self.title = "Editar Horario"
        
        # Establecer este modal como el activo
        self.app.current_modal = self
        
        # Inicializar valores de edición
        self.app.edit_index = index
        self.app.edit_hour_val = schedule['hour']
        self.app.edit_minute_val = schedule['minute']
        self.app.edit_temp_val = int(schedule['temp'])
        self.app.edit_label_val = schedule.get('label', get_label_for_time(schedule['hour'], schedule['minute']))
        self.app.edit_field_selected = 0
        self.app.edit_color_preview = ColorPreview(self.app.edit_temp_val)
    
    def build_body(self):
        """Construir el cuerpo del modal."""
        def highlight_field(value, field_idx, format_str="{}"):
            if self.app.edit_field_selected == field_idx:
                return urwid.AttrMap(
                    urwid.Text(f"[{format_str.format(value)}]", align='center'),
                    'selected'
                )
            return urwid.Text(f"[{format_str.format(value)}]", align='center')
        
        def highlight_label(value, field_idx):
            if self.app.edit_field_selected == field_idx:
                return urwid.AttrMap(
                    urwid.Text(f"[{value}]", align='left'),
                    'selected'
                )
            return urwid.Text(f" {value}", align='left')
        
        instructions_box = urwid.LineBox(
            urwid.Pile([
                urwid.Columns([
                    ('pack', urwid.Text("  ← → ")),
                    ('pack', urwid.Text("ajustar Hora/Min/Temp")),
                ]),
                urwid.Columns([
                    ('pack', urwid.Text("  ↑ ↓  ")),
                    ('pack', urwid.Text("navegar campos")),
                ]),
                urwid.Columns([
                    ('pack', urwid.Text("  Tab  ")),
                    ('pack', urwid.Text("ir a botones")),
                ]),
                urwid.Columns([
                    ('pack', urwid.Text("  Del  ")),
                    ('pack', urwid.Text("borrar Etiqueta")),
                ]),
            ]),
            title=" Navegación "
        )
        
        body = urwid.Pile([
            urwid.Divider(),
            urwid.Columns([
                ('pack', urwid.Text("  Hora:        ")),
                ('pack', highlight_field(f"{self.app.edit_hour_val:02d}", 0)),
            ]),
            urwid.Columns([
                ('pack', urwid.Text("  Minuto:      ")),
                ('pack', highlight_field(f"{self.app.edit_minute_val:02d}", 1)),
            ]),
            urwid.Columns([
                ('pack', urwid.Text("  Temperatura: ")),
                ('pack', highlight_field(f"{self.app.edit_temp_val}", 2, "{}K")),
            ]),
            urwid.Columns([
                ('pack', urwid.Text("  Etiqueta:    ")),
                ('pack', highlight_label(self.app.edit_label_val, 3)),
            ]),
            urwid.Divider(),
            urwid.Text("  ─── Vista Previa ────────────────────"),
            self.app.edit_color_preview,
            urwid.Divider(),
            instructions_box,
            urwid.Divider(),
            urwid.Columns([
                ('pack', urwid.Text("  ")),
                ('pack', highlight_field("Guardar", 4)),
                ('pack', urwid.Text("    ")),
                ('pack', highlight_field("Cancelar", 5)),
                ('pack', urwid.Text("  ")),
            ]),
            urwid.Divider(),
        ])
        
        return body
    
    def handle_input(self, key):
        """
        Manejar entrada de teclado delegando al input_handler.
        
        Args:
            key: Tecla presionada
        """
        self.app.input_handler.handle_modal_input(key)
    
    def save(self):
        """Guardar los cambios."""
        try:
            label = getattr(self.app, 'edit_label_val', 
                          get_label_for_time(self.app.edit_hour_val, self.app.edit_minute_val))
            
            self.app.schedules[self.index] = {
                'hour': self.app.edit_hour_val,
                'minute': self.app.edit_minute_val,
                'temp': self.app.edit_temp_val,
                'time_str': f"{self.app.edit_hour_val:02d}:{self.app.edit_minute_val:02d}",
                'temp_str': f"{self.app.edit_temp_val}K",
                'label': label
            }
            self.app.schedules.sort(key=lambda x: x['hour'] * 60 + x['minute'])
            self.app.refresh_schedule_list()
            self.app.show_message("Horario actualizado", 'success')
        except Exception as e:
            self.app.show_message(f"Error: {e}", 'error')
            return
        
        self._cleanup()
        self.app.current_modal = None
        self.app.modal_open = False
        self.app.loop.widget = self.app.main_frame
        self.app.loop.draw_screen()
        self.app.save_config()
    
    def cancel(self):
        """Cancelar la edición."""
        self._cleanup()
        self.app.current_modal = None
        self.app.modal_open = False
        self.app.loop.widget = self.app.main_frame
        self.app.loop.draw_screen()
    
    def _cleanup(self):
        """Limpiar variables de edición."""
        for var in ['edit_index', 'edit_hour_val', 'edit_minute_val',
                    'edit_temp_val', 'edit_label_val', 'edit_color_preview',
                    'edit_field_selected']:
            if hasattr(self.app, var):
                delattr(self.app, var)

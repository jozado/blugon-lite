#!/usr/bin/env python3
"""
Modal de agregado de horarios para el TUI de blugon-lite.
"""

import urwid
from ..utils import get_label_for_time
from ..widgets import ColorPreview


class AddScheduleModal:
    """Modal para agregar un nuevo horario."""
    
    def __init__(self, app):
        """
        Inicializar el modal de agregado.
        
        Args:
            app: Referencia a la aplicación principal
        """
        self.app = app
        
        # Establecer este modal como el activo
        self.app.current_modal = self
        
        # Inicializar valores de agregado
        self.app.add_hour = 12
        self.app.add_minute = 0
        self.app.add_temp = 6500
        self.app.add_label_val = ""  # Vacío por defecto
        self.app.add_field_selected = 0
        self.app.add_color_preview = ColorPreview(self.app.add_temp)
    
    def build_body(self):
        """Construir el cuerpo del modal."""
        def highlight_field(value, field_idx, format_str="{}"):
            if self.app.add_field_selected == field_idx:
                return urwid.AttrMap(
                    urwid.Text(f"[{format_str.format(value)}]", align='center'),
                    'selected'
                )
            return urwid.Text(f"[{format_str.format(value)}]", align='center')
        
        def highlight_label(value, field_idx):
            if self.app.add_field_selected == field_idx:
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
                ('pack', highlight_field(f"{self.app.add_hour:02d}", 0)),
            ]),
            urwid.Columns([
                ('pack', urwid.Text("  Minuto:      ")),
                ('pack', highlight_field(f"{self.app.add_minute:02d}", 1)),
            ]),
            urwid.Columns([
                ('pack', urwid.Text("  Temperatura: ")),
                ('pack', highlight_field(f"{self.app.add_temp}", 2, "{}K")),
            ]),
            urwid.Columns([
                ('pack', urwid.Text("  Etiqueta:    ")),
                ('pack', highlight_label(self.app.add_label_val, 3)),
            ]),
            urwid.Divider(),
            urwid.Text("  ─── Vista Previa ────────────────────"),
            self.app.add_color_preview,
            urwid.Divider(),
            instructions_box,
            urwid.Divider(),
            urwid.Columns([
                ('pack', urwid.Text("  ")),
                ('pack', highlight_field("Agregar", 4)),
                ('pack', urwid.Text("    ")),
                ('pack', highlight_field("Cancelar", 5)),
                ('pack', urwid.Text("  ")),
            ]),
            urwid.Divider(),
        ])
        
        return body
    
    def handle_input(self, key):
        """
        Manejar entrada de teclado en el modal de agregado.
        
        Args:
            key: Tecla presionada
        """
        # ESC cierra el modal
        if key in ('esc', 'escape'):
            self.cancel()
            return
        
        changed = False
        field = self.app.add_field_selected
        
        # Navegación entre campos
        if key in ('up', 'cursor up'):
            if field > 0:
                self.app.add_field_selected = field - 1
                changed = True
        elif key in ('down', 'cursor down'):
            if field < 5:
                self.app.add_field_selected = field + 1
                changed = True
        elif key == 'tab':
            # Tab va a botones o alterna entre ellos
            if field >= 4:
                self.app.add_field_selected = 5 if field == 4 else 4
            else:
                self.app.add_field_selected = 4
            changed = True
        elif key == 'shift tab':
            # Shift+Tab navega hacia atrás
            if field > 0:
                self.app.add_field_selected = field - 1
            changed = True
        # Ajuste de valores con flechas laterales
        elif key in ('left', 'cursor left'):
            if field >= 4:
                self.app.add_field_selected = 5 if field == 4 else 4
                changed = True
            elif field == 0:  # Hora
                self.app.add_hour = (self.app.add_hour - 1) % 24
                changed = True
            elif field == 1:  # Minuto
                self.app.add_minute = (self.app.add_minute - 5) % 60
                changed = True
            elif field == 2:  # Temperatura
                self.app.add_temp = max(1000, self.app.add_temp - 100)
                changed = True
        elif key in ('right', 'cursor right'):
            if field >= 4:
                self.app.add_field_selected = 4 if field == 5 else 5
                changed = True
            elif field == 0:  # Hora
                self.app.add_hour = (self.app.add_hour + 1) % 24
                changed = True
            elif field == 1:  # Minuto
                self.app.add_minute = (self.app.add_minute + 5) % 60
                changed = True
            elif field == 2:  # Temperatura
                self.app.add_temp = min(20000, self.app.add_temp + 100)
                changed = True
        # Enter para agregar/cancelar
        elif key == 'enter':
            if field == 4:
                self.save()
                return
            elif field == 5:
                self.cancel()
                return
            elif field < 3:
                self.save()
                return
        # Edición de etiqueta (campo 3)
        elif field == 3:
            if key in ('backspace', 'ctrl h'):
                if self.app.add_label_val:
                    self.app.add_label_val = self.app.add_label_val[:-1]
                    changed = True
            elif key in ('delete', 'ctrl d'):
                self.app.add_label_val = ""
                changed = True
            elif len(key) == 1 and key.isprintable():
                if len(self.app.add_label_val) < 20:
                    self.app.add_label_val += key
                    changed = True
        
        if changed:
            self.app.add_color_preview.update(self.app.add_temp)
            self.app.add_schedule()
            self.app.loop.draw_screen()
    
    def save(self):
        """Guardar el nuevo horario."""
        try:
            label = getattr(self.app, 'add_label_val',
                          get_label_for_time(self.app.add_hour, self.app.add_minute))
            
            self.app.schedules.append({
                'hour': self.app.add_hour,
                'minute': self.app.add_minute,
                'temp': self.app.add_temp,
                'time_str': f"{self.app.add_hour:02d}:{self.app.add_minute:02d}",
                'temp_str': f"{self.app.add_temp}K",
                'label': label
            })
            self.app.schedules.sort(key=lambda x: x['hour'] * 60 + x['minute'])
            self.app.refresh_schedule_list()
            self.app.show_message("Horario agregado", 'success')
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
        """Cancelar el agregado."""
        self._cleanup()
        self.app.current_modal = None
        self.app.modal_open = False
        self.app.loop.widget = self.app.main_frame
        self.app.loop.draw_screen()
    
    def _cleanup(self):
        """Limpiar variables de agregado."""
        for var in ['add_hour', 'add_minute', 'add_temp',
                    'add_label_val', 'add_color_preview', 'add_field_selected']:
            if hasattr(self.app, var):
                delattr(self.app, var)

#!/usr/bin/env python3
"""Aplicación principal del TUI para blugon-lite."""

import urwid
from datetime import datetime

from .config import CONFIG_FILE, SYSTEM_CONFIG_FILE, VERSION
from .themes import THEMES, PALETTE_DARK
from .utils import (
    read_gamma_file,
    write_gamma_file,
    get_default_schedules,
    is_daemon_running,
    get_label_for_time,
)
from .widgets import ColorPreview, ScheduleItem, ModalOverlay


class BlugonLiteTUI:
    """Clase principal de la aplicación TUI."""

    def __init__(self):
        self.schedules = []
        self.selected_index = 0
        self.modified = False
        self.unsaved_changes = False
        self.current_theme = 'dark'
        self.daemon_active = False

        self.load_config()
        self.daemon_active = is_daemon_running()
        self.create_widgets()

        # Input filter para interceptar teclas
        def input_filter(keys, raw):
            # Si hay modal abierto, pasar todas las teclas al modal
            # El modal se encarga de procesarlas mediante handle_modal_input
            if hasattr(self, 'modal_open') and self.modal_open:
                # ESC siempre cierra el modal (manejo global)
                for key in keys:
                    if key in ('esc', 'escape'):
                        # Llamar al handler del modal para cierre
                        if hasattr(self, 'handle_modal_input'):
                            self.handle_modal_input(key)
                        return []
                # Pasar todas las demás teclas al widget del modal
                return keys

            # Input filter normal para la pantalla principal
            for key in keys:
                if key in ('up', 'cursor up'):
                    self.on_navigate_up()
                    return []  # Consumir la tecla
                elif key in ('down', 'cursor down'):
                    self.on_navigate_down()
                    return []  # Consumir la tecla
            return keys  # Pasar otras teclas

        self.loop = urwid.MainLoop(
            self.main_frame,
            palette=PALETTE_DARK,
            unhandled_input=self.handle_input,
            input_filter=input_filter,
            handle_mouse=False
        )

    def load_config(self):
        """Cargar configuración gamma."""
        self.schedules = read_gamma_file(CONFIG_FILE)
        if not self.schedules:
            self.schedules = read_gamma_file(SYSTEM_CONFIG_FILE)
        if not self.schedules:
            self.schedules = get_default_schedules()

    def create_widgets(self):
        """Crear widgets principales de la UI."""
        self.header = self._create_header()
        self.info_panel = self._create_info_panel()
        self.footer = self._create_footer()
        self.status = urwid.AttrMap(urwid.Text(" Ready"), 'info')
        self.schedule_list_widget = self._create_schedule_list()

        # Título HORARIOS
        horarios_title = urwid.AttrMap(
            urwid.Text("  ─── HORARIOS ─────────────────────────────"),
            'header'
        )

        # Contenido principal
        main_content_inner = urwid.Pile([
            ('pack', urwid.Text("")),  # Espacio vertical después del header
            ('pack', self.info_panel),
            ('pack', urwid.Text("")),  # Espacio vertical antes de la lista
            ('pack', horarios_title),  # Título HORARIOS
            ('pack', urwid.Text("")),  # Espacio vertical después de HORARIOS
            ('weight', 1, self.schedule_list_widget),  # Lista de horarios
            ('pack', urwid.Text("")),  # Espacio vertical
            ('pack', self.status),
        ])

        # Envolver en LineBox
        self.main_content = urwid.LineBox(
            urwid.Padding(main_content_inner, left=1, right=1),
            title=" blugon-lite TUI "
        )

        self.main_frame = urwid.Frame(
            self.main_content,
            header=self.header,
            footer=self.footer
        )

        self.update_info()

    def _create_header(self):
        """Crear header con estado del daemon."""
        indicator = '[●]' if self.daemon_active else '[○]'
        attr = 'daemon_active' if self.daemon_active else 'daemon_inactive'
        text = 'Activo' if self.daemon_active else 'Inactivo'

        header_text = urwid.Columns([
            ('pack', urwid.Text("  blugon-lite", align='left')),
            urwid.Text(""),  # Espacio flexible
            ('pack', urwid.AttrMap(
                urwid.Text(f"  {indicator} Daemon: {text}  ", align='right'),
                attr
            )),
        ])

        return urwid.AttrMap(header_text, 'header')

    def _create_info_panel(self):
        """Crear panel de información con hora actual, temperatura y próximo cambio."""
        now = datetime.now()
        current_time = now.hour * 60 + now.minute

        current_sched = None
        next_sched = None

        for sched in self.schedules:
            sched_time = sched['hour'] * 60 + sched['minute']
            if sched_time <= current_time:
                current_sched = sched
            elif next_sched is None:
                next_sched = sched

        if next_sched is None and self.schedules:
            next_sched = self.schedules[0]

        temp_info = f"{current_sched['temp_str']} ({current_sched['label']})" if current_sched else "N/A"

        if next_sched:
            next_time = next_sched['hour'] * 60 + next_sched['minute']
            if next_time < current_time:
                next_time += 24 * 60
            diff_minutes = next_time - current_time
            hours, mins = diff_minutes // 60, diff_minutes % 60
            next_info = f"{next_sched['time_str']} → {next_sched['temp_str']} ({hours}h {mins}m)"
        else:
            next_info = "N/A"

        info_widget = urwid.Pile([
            urwid.Text(f"  HORA ACTUAL: {now.strftime('%H:%M')}"),
            urwid.Text(f"  TEMPERATURA: {temp_info}"),
            urwid.Text(f"  PRÓXIMO: {next_info}"),
        ])

        return urwid.AttrMap(
            urwid.Padding(info_widget, left=1, right=1),
            'info_panel'
        )

    def update_info(self):
        """Actualizar panel de información con hora y próxima transición."""
        now = datetime.now()
        current_time = now.hour * 60 + now.minute

        current_sched = None
        next_sched = None

        for sched in self.schedules:
            sched_time = sched['hour'] * 60 + sched['minute']
            if sched_time <= current_time:
                current_sched = sched
            elif next_sched is None:
                next_sched = sched

        if next_sched is None and self.schedules:
            next_sched = self.schedules[0]

        temp_info = f"{current_sched['temp_str']} ({current_sched['label']})" if current_sched else "N/A"

        if next_sched:
            next_time = next_sched['hour'] * 60 + next_sched['minute']
            if next_time < current_time:
                next_time += 24 * 60
            diff_minutes = next_time - current_time
            hours, mins = diff_minutes // 60, diff_minutes % 60
            next_info = f"{next_sched['time_str']} → {next_sched['temp_str']} ({hours}h {mins}m)"
        else:
            next_info = "N/A"

        info_text = urwid.Pile([
            urwid.Text(f"  HORA ACTUAL: {now.strftime('%H:%M')}"),
            urwid.Text(f"  TEMPERATURA: {temp_info}"),
            urwid.Text(f"  PRÓXIMO: {next_info}"),
        ])

        self.info_panel.original_widget = urwid.Padding(info_text, left=1, right=1)

    def _create_schedule_list(self):
        """Crear lista de horarios."""
        self.schedule_items = []
        # Crear los items inicialmente
        total = len(self.schedules)
        for i, sched in enumerate(self.schedules):
            item = ScheduleItem(
                sched, i,
                is_selected=(i == self.selected_index),
                is_first=(i == 0),
                is_last=(i == total - 1),
                total_items=total
            )
            self.schedule_items.append(item)
        
        # Usar SimpleFocusListWalker para que el ListBox se actualice
        self.schedule_walker = urwid.SimpleFocusListWalker(self.schedule_items)
        return urwid.ListBox(self.schedule_walker)
    
    def on_navigate_up(self):
        """Manejar navegación hacia arriba."""
        if self.selected_index > 0:
            self.selected_index -= 1
            self.refresh_schedule_list()
            self.loop.draw_screen()

    def on_navigate_down(self):
        """Manejar navegación hacia abajo."""
        if self.selected_index < len(self.schedules) - 1:
            self.selected_index += 1
            self.refresh_schedule_list()
            self.loop.draw_screen()

    def _create_footer(self):
        """Crear footer con instrucciones."""
        instructions = urwid.Text([
            ('info', "e"), " Editar  ",
            ('info', "a"), " Agregar  ",
            ('info', "d"), " Eliminar  ",
            ('info', "t"), " Tema  ",
            ('info', "q"), " Salir"
        ])

        footer_cols = urwid.Columns([
            ('pack', instructions),
        ])

        return urwid.AttrMap(
            urwid.Padding(footer_cols, left=1, right=1),
            'footer'
        )

    def refresh_schedule_list(self):
        """Actualizar lista de horarios."""
        # Actualizar el estado de selección de cada item
        total = len(self.schedules)
        for i, item in enumerate(self.schedule_items):
            item.is_selected = (i == self.selected_index)
            item.is_first = (i == 0)
            item.is_last = (i == total - 1)
            item.total_items = total
            item._w = item._build_widget()  # Forzar actualización del widget

        # Actualizar el foco del walker
        if hasattr(self, 'schedule_walker') and self.schedule_items:
            self.schedule_walker.set_focus(self.selected_index)

        if self.unsaved_changes:
            self.status.original_widget.set_text(" (* Cambios sin guardar)")
        else:
            self.status.original_widget.set_text(" Ready")

    def update_info(self):
        """Actualizar panel de información con hora y próxima transición."""
        now = datetime.now()
        current_time = now.hour * 60 + now.minute

        current_sched = None
        next_sched = None

        for sched in self.schedules:
            sched_time = sched['hour'] * 60 + sched['minute']
            if sched_time <= current_time:
                current_sched = sched
            elif next_sched is None:
                next_sched = sched

        if next_sched is None and self.schedules:
            next_sched = self.schedules[0]

        temp_info = f"{current_sched['temp_str']} ({current_sched['label']})" if current_sched else "N/A"

        if next_sched:
            next_time = next_sched['hour'] * 60 + next_sched['minute']
            if next_time < current_time:
                next_time += 24 * 60
            diff_minutes = next_time - current_time
            hours, mins = diff_minutes // 60, diff_minutes % 60
            next_info = f"{next_sched['time_str']} → {next_sched['temp_str']} ({hours}h {mins}m)"
        else:
            next_info = "N/A"

        info_text = urwid.Columns([
            ('pack', urwid.Text(f"  HORA: {now.strftime('%H:%M')}  ")),
            ('pack', urwid.Text(f"  TEMP: {temp_info}  ")),
            ('pack', urwid.Text(f"  PRÓXIMO: {next_info}  ")),
        ])

        self.info_panel = urwid.AttrMap(
            urwid.Padding(info_text, left=1, right=1),
            'default'
        )

    def handle_input(self, key):
        """Manejar entrada de teclado global."""
        # Si hay un modal abierto, NO manejar nada aquí (el modal captura las teclas)
        if hasattr(self, 'modal_open') and self.modal_open:
            return

        if key == 'q':
            if self.unsaved_changes:
                self.show_confirm_exit()
            else:
                raise urwid.ExitMainLoop()
        elif key == 's':
            self.save_config()
        elif key == 'a':
            self.add_schedule()
        elif key == 't':
            self.show_theme_selector()
        elif key == 'e':
            if not self.schedules:
                self.show_message("No hay horarios para editar", 'warning')
                return
            self.edit_schedule(self.selected_index)
        elif key == 'd':
            if not self.schedules:
                self.show_message("No hay horarios para eliminar", 'warning')
                return
            self.delete_schedule(self.selected_index)

    def show_message(self, message, style='info'):
        """Mostrar mensaje temporal (toast)."""
        self.status.original_widget.set_text(f" {message}")
        self.status.set_attr_map({None: style})

    def show_confirm_exit(self):
        """Mostrar diálogo de confirmación de salida."""
        body = urwid.Pile([
            urwid.Text("Tienes cambios sin guardar."),
            urwid.Text("¿Estás seguro de que deseas salir?"),
            urwid.Divider(),
            urwid.Button("Sí, salir", lambda b: self.confirm_exit_yes()),
            urwid.Button("No, continuar", lambda b: self.confirm_exit_no()),
        ])

        def modal_keypress(key):
            if key == 'esc':
                self.confirm_exit_no()
                return None
            return key
        
        overlay = ModalOverlay(body, "Confirmar Salida", width=50, height=12, on_keypress=modal_keypress)
        self.loop.widget = overlay
        self.modal_open = True
        self.confirm_exit_open = True

    def confirm_exit_yes(self):
        """Confirmar salida."""
        raise urwid.ExitMainLoop()

    def confirm_exit_no(self):
        """Cancelar salida."""
        self.confirm_exit_open = False
        self.modal_open = False
        self.loop.widget = self.main_frame

    def edit_schedule(self, index=None):
        """Editar un horario."""
        if index is None:
            index = getattr(self, 'edit_index', None)
        if index is None or index < 0 or index >= len(self.schedules):
            self.show_message("Selecciona un horario válido", 'warning')
            return

        sched = self.schedules[index]
        
        # Si no existen las variables de edición, inicializarlas
        if not hasattr(self, 'edit_index'):
            self.edit_index = index
            self.edit_hour_val = sched['hour']
            self.edit_minute_val = sched['minute']
            self.edit_temp_val = int(sched['temp'])
            self.edit_label_val = sched.get('label', get_label_for_time(sched['hour'], sched['minute']))
        
        # Campo seleccionado (0=Hora, 1=Minuto, 2=Temperatura, 3=Etiqueta, 4=Guardar, 5=Cancelar)
        if not hasattr(self, 'edit_field_selected'):
            self.edit_field_selected = 0
        
        self.edit_color_preview = ColorPreview(self.edit_temp_val)
        label = self.edit_label_val
        
        # Determinar qué campo está resaltado
        def highlight_field(value, field_idx, format_str="{}"):
            if self.edit_field_selected == field_idx:
                return urwid.AttrMap(urwid.Text(f"[{format_str.format(value)}]", align='center'), 'selected')
            else:
                return urwid.Text(f"[{format_str.format(value)}]", align='center')
        
        # Widget especial para etiqueta editable
        def highlight_label(value, field_idx):
            if self.edit_field_selected == field_idx:
                return urwid.AttrMap(urwid.Text(f"[{value}]", align='left'), 'selected')
            else:
                return urwid.Text(f" {value}", align='left')

        # Instrucciones en recuadro
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
                ('pack', highlight_field(f"{self.edit_hour_val:02d}", 0)),
            ]),
            urwid.Columns([
                ('pack', urwid.Text("  Minuto:      ")),
                ('pack', highlight_field(f"{self.edit_minute_val:02d}", 1)),
            ]),
            urwid.Columns([
                ('pack', urwid.Text("  Temperatura: ")),
                ('pack', highlight_field(f"{self.edit_temp_val}", 2, "{}K")),
            ]),
            urwid.Columns([
                ('pack', urwid.Text("  Etiqueta:    ")),
                ('pack', highlight_label(label, 3)),
            ]),
            urwid.Divider(),
            urwid.Text("  ─── Vista Previa ────────────────────"),
            self.edit_color_preview,
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

        self.modal_body = body
        # Modal con callback para capturar teclas
        def modal_keypress(key):
            return self.handle_modal_input(key)  # Retorna None si consume, key si no
        
        overlay = ModalOverlay(body, "Editar Horario", width=('relative', 90), height=('relative', 90), on_keypress=modal_keypress)
        self.loop.widget = overlay
        self.modal_open = True

    def handle_modal_input(self, key):
        """
        Manejar entrada de teclado dentro del modal de edición/agregado.
        
        Este método procesa todas las teclas cuando el modal está abierto:
        - Navegación entre campos (up, down, tab)
        - Modificación de valores numéricos (left, right)
        - Edición de texto (caracteres imprimibles, backspace, delete)
        - Acciones (enter para guardar/cancelar, esc para cerrar)
        
        Args:
            key: La tecla presionada (string)
        """
        # ESC siempre cierra el modal
        if key in ('esc', 'escape'):
            if hasattr(self, 'edit_index'):
                self.cancel_edit()
            elif hasattr(self, 'add_hour'):
                self.cancel_add()
            elif hasattr(self, 'theme_selector_open'):
                self.cancel_theme()
            elif hasattr(self, 'delete_confirm_open'):
                self.cancel_delete()
            elif hasattr(self, 'confirm_exit_open'):
                self.confirm_exit_no()
            else:
                self.modal_open = False
                self.loop.widget = self.main_frame
            return

        # Determinar si estamos en modo edición o agregado
        is_edit = hasattr(self, 'edit_index')
        is_add = hasattr(self, 'add_hour')

        if not is_edit and not is_add:
            return

        changed = False
        rebuild = False

        # Determinar campo seleccionado
        if is_edit:
            field_selected = getattr(self, 'edit_field_selected', 0)
        else:
            field_selected = getattr(self, 'add_field_selected', 0)

        # Navegación entre campos con ↑ ↓
        if key in ('up', 'cursor up'):
            if field_selected > 0:
                if is_edit:
                    self.edit_field_selected = field_selected - 1
                else:
                    self.add_field_selected = field_selected - 1
                rebuild = True
            changed = True
        elif key in ('down', 'cursor down'):
            max_field = 5  # 0=Hora, 1=Minuto, 2=Temperatura, 3=Etiqueta, 4=Guardar, 5=Cancelar
            if field_selected < max_field:
                if is_edit:
                    self.edit_field_selected = field_selected + 1
                else:
                    self.add_field_selected = field_selected + 1
                rebuild = True
            changed = True
        # Navegación con Tab hacia adelante
        elif key == 'tab':
            if is_edit:
                self.edit_field_selected = min(4, self.edit_field_selected + 1)
            else:
                self.add_field_selected = min(4, self.add_field_selected + 1)
            rebuild = True
            changed = True
        # Shift+Tab para navegación hacia atrás
        elif key == 'shift tab':
            if is_edit:
                self.edit_field_selected = max(0, self.edit_field_selected - 1)
            else:
                self.add_field_selected = max(0, self.add_field_selected - 1)
            rebuild = True
            changed = True
        # Ajuste de valores con ← →
        elif key in ('left', 'cursor left'):
            if field_selected >= 4:  # Estamos en botones, ir a Cancelar
                if is_edit:
                    self.edit_field_selected = 5
                else:
                    self.add_field_selected = 5
                rebuild = True
                changed = True
            elif is_edit:
                if field_selected == 0:  # Hora
                    self.edit_hour_val = (self.edit_hour_val - 1) % 24
                    changed = True
                elif field_selected == 1:  # Minuto
                    self.edit_minute_val = (self.edit_minute_val - 5) % 60
                    changed = True
                elif field_selected == 2:  # Temperatura
                    self.edit_temp_val = max(1000, self.edit_temp_val - 100)
                    changed = True
                # Nota: field_selected == 3 (Etiqueta) NO se modifica con flechas
            else:
                if field_selected == 0:  # Hora
                    self.add_hour = (self.add_hour - 1) % 24
                    changed = True
                elif field_selected == 1:  # Minuto
                    self.add_minute = (self.add_minute - 5) % 60
                    changed = True
                elif field_selected == 2:  # Temperatura
                    self.add_temp = max(1000, self.add_temp - 100)
                    changed = True
                # Nota: field_selected == 3 (Etiqueta) NO se modifica con flechas
        elif key in ('right', 'cursor right'):
            if field_selected >= 4:  # Estamos en botones, ir a Guardar/Agregar
                if is_edit:
                    self.edit_field_selected = 4
                else:
                    self.add_field_selected = 4
                rebuild = True
                changed = True
            elif is_edit:
                if field_selected == 0:  # Hora
                    self.edit_hour_val = (self.edit_hour_val + 1) % 24
                    changed = True
                elif field_selected == 1:  # Minuto
                    self.edit_minute_val = (self.edit_minute_val + 5) % 60
                    changed = True
                elif field_selected == 2:  # Temperatura
                    self.edit_temp_val = min(20000, self.edit_temp_val + 100)
                    changed = True
                # Nota: field_selected == 3 (Etiqueta) NO se modifica con flechas
            else:
                if field_selected == 0:  # Hora
                    self.add_hour = (self.add_hour + 1) % 24
                    changed = True
                elif field_selected == 1:  # Minuto
                    self.add_minute = (self.add_minute + 5) % 60
                    changed = True
                elif field_selected == 2:  # Temperatura
                    self.add_temp = min(20000, self.add_temp + 100)
                    changed = True
                # Nota: field_selected == 3 (Etiqueta) NO se modifica con flechas
        # Enter para guardar/cancelar o ejecutar acción del botón
        elif key == 'enter':
            if field_selected == 4:  # Guardar/Agregar
                if is_edit:
                    self.save_edit_from_modal()
                else:
                    self.save_add_from_modal()
                return
            elif field_selected == 5:  # Cancelar
                if is_edit:
                    self.cancel_edit()
                else:
                    self.cancel_add()
                return
            # Si estamos en un campo numérico, Enter también guarda
            elif field_selected < 3:
                if is_edit:
                    self.save_edit_from_modal()
                else:
                    self.save_add_from_modal()
                return
        # Teclas de edición de texto para campo Etiqueta (field 3)
        elif field_selected == 3:
            # Backspace borra último carácter
            if key in ('backspace', 'ctrl h'):
                if is_edit and hasattr(self, 'edit_label_val'):
                    if self.edit_label_val:
                        self.edit_label_val = self.edit_label_val[:-1]
                        changed = True
                elif is_add and hasattr(self, 'add_label_val'):
                    if self.add_label_val:
                        self.add_label_val = self.add_label_val[:-1]
                        changed = True
            # Delete borra todo el contenido
            elif key in ('delete', 'ctrl d'):
                if is_edit:
                    self.edit_label_val = ""
                    changed = True
                elif is_add:
                    self.add_label_val = ""
                    changed = True
            # Caracteres imprimibles se agregan al texto (máximo 20 chars)
            elif len(key) == 1 and key.isprintable():
                if is_edit and hasattr(self, 'edit_label_val'):
                    if len(self.edit_label_val) < 20:
                        self.edit_label_val = self.edit_label_val + key
                        changed = True
                elif is_add and hasattr(self, 'add_label_val'):
                    if len(self.add_label_val) < 20:
                        self.add_label_val = self.add_label_val + key
                        changed = True

        if changed:
            # Actualizar vista previa
            if is_edit:
                self.edit_color_preview.update(self.edit_temp_val)
                # Reconstruir el modal
                self.edit_schedule(self.edit_index)
            else:
                self.add_color_preview.update(self.add_temp)
                # Reconstruir el modal
                self.add_schedule()

            # Redibujar
            self.loop.draw_screen()

    def save_edit(self, index, hour_edit, minute_edit, temp_edit):
        """Guardar edición de horario."""
        try:
            hour = int(hour_edit.edit_text) if hour_edit.edit_text else 12
            minute = int(minute_edit.edit_text) if minute_edit.edit_text else 0
            temp = int(temp_edit.edit_text) if temp_edit.edit_text else 6500

            if not (0 <= hour <= 23):
                raise ValueError("Hora debe ser 0-23")
            if not (0 <= minute <= 59):
                raise ValueError("Minuto debe ser 0-59")
            if not (1000 <= temp <= 20000):
                raise ValueError("Temperatura debe ser 1000-20000")

            label = get_label_for_time(hour, minute)
            self.schedules[index] = {
                'hour': hour,
                'minute': minute,
                'temp': temp,
                'time_str': f"{hour:02d}:{minute:02d}",
                'temp_str': f"{temp}K",
                'label': label
            }
            self.schedules.sort(key=lambda x: x['hour'] * 60 + x['minute'])
            self.unsaved_changes = True
            self.refresh_schedule_list()
            self.show_message("Horario actualizado", 'success')
        except ValueError as e:
            self.show_message(f"Error: {e}", 'error')
            return

        self.loop.widget = self.main_frame

    def save_edit_from_modal(self, index=None):
        """Guardar edición desde el modal."""
        if index is None:
            index = getattr(self, 'edit_index', None)
        if index is None:
            self.show_message("Error: no hay índice de edición", 'error')
            return
            
        try:
            hour = self.edit_hour_val
            minute = self.edit_minute_val
            temp = self.edit_temp_val
            label = self.edit_label_val if hasattr(self, 'edit_label_val') else get_label_for_time(hour, minute)
            
            self.schedules[index] = {
                'hour': hour,
                'minute': minute,
                'temp': temp,
                'time_str': f"{hour:02d}:{minute:02d}",
                'temp_str': f"{temp}K",
                'label': label
            }
            self.schedules.sort(key=lambda x: x['hour'] * 60 + x['minute'])
            self.unsaved_changes = True
            self.refresh_schedule_list()
            self.show_message("Horario actualizado", 'success')
        except Exception as e:
            self.show_message(f"Error: {e}", 'error')
            return
        
        # Limpiar variables de edición
        if hasattr(self, 'edit_index'):
            del self.edit_index
        if hasattr(self, 'edit_hour_val'):
            del self.edit_hour_val
        if hasattr(self, 'edit_minute_val'):
            del self.edit_minute_val
        if hasattr(self, 'edit_temp_val'):
            del self.edit_temp_val
        if hasattr(self, 'edit_label_val'):
            del self.edit_label_val
        if hasattr(self, 'edit_color_preview'):
            del self.edit_color_preview
        if hasattr(self, 'edit_field_selected'):
            del self.edit_field_selected
        
        self.modal_open = False
        self.loop.widget = self.main_frame

    def cancel_edit(self):
        """Cancelar edición."""
        if hasattr(self, 'edit_index'):
            del self.edit_index
        if hasattr(self, 'edit_hour_val'):
            del self.edit_hour_val
        if hasattr(self, 'edit_minute_val'):
            del self.edit_minute_val
        if hasattr(self, 'edit_temp_val'):
            del self.edit_temp_val
        if hasattr(self, 'edit_label_val'):
            del self.edit_label_val
        if hasattr(self, 'edit_color_preview'):
            del self.edit_color_preview
        if hasattr(self, 'edit_field_selected'):
            del self.edit_field_selected
        self.modal_open = False
        self.loop.widget = self.main_frame

    def add_schedule(self):
        """Agregar nuevo horario."""
        # Si no existen las variables de agregado, inicializarlas
        if not hasattr(self, 'add_hour'):
            self.add_hour = 12
            self.add_minute = 0
            self.add_temp = 6500
            self.add_label_val = "Mañana"
        
        # Campo seleccionado (0=Hora, 1=Minuto, 2=Temperatura, 3=Etiqueta, 4=Agregar, 5=Cancelar)
        if not hasattr(self, 'add_field_selected'):
            self.add_field_selected = 0
        
        self.add_color_preview = ColorPreview(self.add_temp)
        label = self.add_label_val
        
        # Determinar qué campo está resaltado
        def highlight_field(value, field_idx, format_str="{}"):
            if self.add_field_selected == field_idx:
                return urwid.AttrMap(urwid.Text(f"[{format_str.format(value)}]", align='center'), 'selected')
            else:
                return urwid.Text(f"[{format_str.format(value)}]", align='center')
        
        # Widget especial para etiqueta editable
        def highlight_label(value, field_idx):
            if self.add_field_selected == field_idx:
                return urwid.AttrMap(urwid.Text(f"[{value}]", align='left'), 'selected')
            else:
                return urwid.Text(f" {value}", align='left')

        # Instrucciones en recuadro
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
                ('pack', highlight_field(f"{self.add_hour:02d}", 0)),
            ]),
            urwid.Columns([
                ('pack', urwid.Text("  Minuto:      ")),
                ('pack', highlight_field(f"{self.add_minute:02d}", 1)),
            ]),
            urwid.Columns([
                ('pack', urwid.Text("  Temperatura: ")),
                ('pack', highlight_field(f"{self.add_temp}", 2, "{}K")),
            ]),
            urwid.Columns([
                ('pack', urwid.Text("  Etiqueta:    ")),
                ('pack', highlight_label(label, 3)),
            ]),
            urwid.Divider(),
            urwid.Text("  ─── Vista Previa ────────────────────"),
            self.add_color_preview,
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

        self.modal_body = body
        # Modal con callback para capturar teclas
        def modal_keypress(key):
            self.handle_modal_input(key)
            return None  # Siempre consumir la tecla
        
        overlay = ModalOverlay(body, "Agregar Horario", width=('relative', 90), height=('relative', 90), on_keypress=modal_keypress)
        self.loop.widget = overlay
        self.modal_open = True

    def save_add(self, hour_edit, minute_edit, temp_edit):
        """Guardar nuevo horario."""
        try:
            hour = int(hour_edit.edit_text) if hour_edit.edit_text else 12
            minute = int(minute_edit.edit_text) if minute_edit.edit_text else 0
            temp = int(temp_edit.edit_text) if temp_edit.edit_text else 6500

            if not (0 <= hour <= 23):
                raise ValueError("Hora debe ser 0-23")
            if not (0 <= minute <= 59):
                raise ValueError("Minuto debe ser 0-59")
            if not (1000 <= temp <= 20000):
                raise ValueError("Temperatura debe ser 1000-20000")

            label = get_label_for_time(hour, minute)
            self.schedules.append({
                'hour': hour,
                'minute': minute,
                'temp': temp,
                'time_str': f"{hour:02d}:{minute:02d}",
                'temp_str': f"{temp}K",
                'label': label
            })
            self.schedules.sort(key=lambda x: x['hour'] * 60 + x['minute'])
            self.unsaved_changes = True
            self.refresh_schedule_list()
            self.show_message("Horario agregado", 'success')
        except ValueError as e:
            self.show_message(f"Error: {e}", 'error')
            return

        self.loop.widget = self.main_frame

    def cancel_add(self):
        """Cancelar agregado."""
        if hasattr(self, 'add_hour'):
            del self.add_hour
        if hasattr(self, 'add_minute'):
            del self.add_minute
        if hasattr(self, 'add_temp'):
            del self.add_temp
        if hasattr(self, 'add_label_val'):
            del self.add_label_val
        if hasattr(self, 'add_color_preview'):
            del self.add_color_preview
        if hasattr(self, 'add_field_selected'):
            del self.add_field_selected
        self.modal_open = False
        self.loop.widget = self.main_frame

    def save_add_from_modal(self):
        """Guardar agregado desde el modal."""
        try:
            label = self.add_label_val if hasattr(self, 'add_label_val') else get_label_for_time(self.add_hour, self.add_minute)
            self.schedules.append({
                'hour': self.add_hour,
                'minute': self.add_minute,
                'temp': self.add_temp,
                'time_str': f"{self.add_hour:02d}:{self.add_minute:02d}",
                'temp_str': f"{self.add_temp}K",
                'label': label
            })
            self.schedules.sort(key=lambda x: x['hour'] * 60 + x['minute'])
            self.unsaved_changes = True
            self.refresh_schedule_list()
            self.show_message("Horario agregado", 'success')
        except Exception as e:
            self.show_message(f"Error: {e}", 'error')
            return
        
        # Limpiar variables de agregado
        if hasattr(self, 'add_hour'):
            del self.add_hour
        if hasattr(self, 'add_minute'):
            del self.add_minute
        if hasattr(self, 'add_temp'):
            del self.add_temp
        if hasattr(self, 'add_label_val'):
            del self.add_label_val
        if hasattr(self, 'add_color_preview'):
            del self.add_color_preview
        if hasattr(self, 'add_field_selected'):
            del self.add_field_selected
        
        self.modal_open = False
        self.loop.widget = self.main_frame

    def delete_schedule(self, index):
        """Eliminar horario."""
        if index < 0 or index >= len(self.schedules):
            self.show_message("Selecciona un horario válido", 'warning')
            return

        sched = self.schedules[index]
        body = urwid.Pile([
            urwid.Text(f"¿Eliminar horario {sched['time_str']} ({sched['temp_str']})?"),
            urwid.Divider(),
            urwid.Button("Sí, eliminar", lambda b: self.confirm_delete(index)),
            urwid.Button("No, cancelar", lambda b: self.cancel_delete()),
        ])

        def modal_keypress(key):
            if key == 'esc':
                self.cancel_delete()
                return None
            return key
        
        self.loop.widget = ModalOverlay(body, "Confirmar Eliminación", width=50, height=12, on_keypress=modal_keypress)
        self.modal_open = True
        self.delete_confirm_open = True

    def confirm_delete(self, index):
        """Confirmar eliminación."""
        del self.schedules[index]
        self.unsaved_changes = True
        if self.selected_index >= len(self.schedules):
            self.selected_index = max(0, len(self.schedules) - 1)
        self.refresh_schedule_list()
        self.show_message("Horario eliminado", 'success')
        self.delete_confirm_open = False
        self.modal_open = False
        self.loop.widget = self.main_frame

    def cancel_delete(self):
        """Cancelar eliminación."""
        self.delete_confirm_open = False
        self.modal_open = False
        self.loop.widget = self.main_frame

    def save_config(self):
        """Guardar configuración a archivo."""
        try:
            write_gamma_file(CONFIG_FILE, self.schedules)
            self.unsaved_changes = False
            self.modified = True
            self.refresh_schedule_list()
            self.show_message(f"Guardado en {CONFIG_FILE}", 'success')
        except Exception as e:
            self.show_message(f"Error al guardar: {e}", 'error')

    def show_theme_selector(self):
        """Mostrar selector de temas."""
        theme_buttons = []
        for theme_id, (theme_name, _) in THEMES.items():
            btn = urwid.Button(theme_name, lambda b, tid=theme_id: self.select_theme(tid))
            theme_buttons.append(btn)

        body = urwid.Pile([
            urwid.AttrMap(urwid.Text("Seleccionar Tema"), 'header'),
            urwid.Divider(),
        ] + theme_buttons + [
            urwid.Divider(),
            urwid.Button("Cancelar", lambda b: self.cancel_theme()),
        ])

        def modal_keypress(key):
            if key == 'esc':
                self.cancel_theme()
                return None
            return key
        
        self.loop.widget = ModalOverlay(body, "Temas", width=40, height=14, on_keypress=modal_keypress)
        self.modal_open = True
        self.theme_selector_open = True

    def select_theme(self, theme_id):
        """Seleccionar y aplicar un tema."""
        self.theme_selector_open = False
        self.modal_open = False
        if theme_id in THEMES:
            self.loop.screen.register_palette(THEMES[theme_id][1])
            self.current_theme = theme_id
            self.show_message(f"Tema cambiado a {theme_id}", 'success')
        self.loop.widget = self.main_frame

    def cancel_theme(self):
        """Cancelar selección de tema."""
        self.theme_selector_open = False
        self.modal_open = False
        self.loop.widget = self.main_frame

    def run(self):
        """Ejecutar el TUI."""
        try:
            self.loop.run()
        except KeyboardInterrupt:
            pass

        if self.unsaved_changes and self.modified:
            print("\nAdvertencia: Tienes cambios sin guardar.")


def main():
    """Punto de entrada principal."""
    print("Iniciando blugon-lite TUI...")
    app = BlugonLiteTUI()
    app.run()
    print("¡Adiós!")


if __name__ == "__main__":
    main()

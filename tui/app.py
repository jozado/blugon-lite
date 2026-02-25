#!/usr/bin/env python3
"""
blugon-lite-tui - Text User Interface para configuración de blugon-lite.

Aplicación principal del TUI usando urwid.
"""

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
from .widgets import ColorPreview, ScheduleItem
from .modals import ModalOverlay, EditScheduleModal, AddScheduleModal, DeleteConfirmModal
from .input_handler import InputHandler


class BlugonLiteTUI:
    """
    Clase principal de la aplicación TUI.
    
    Responsable de:
    - Gestionar el estado de la aplicación
    - Crear y mantener la UI principal
    - Coordinar con InputHandler para entrada de teclado
    - Gestionar ciclo de vida de modales
    """

    def __init__(self):
        """Inicializar la aplicación TUI."""
        self.schedules = []
        self.selected_index = 0
        self.modified = False
        self.unsaved_changes = False
        self.current_theme = 'dark'
        self.daemon_active = False
        
        # Inicializar manejador de input
        self.input_handler = InputHandler(self)

        self.load_config()
        self.daemon_active = is_daemon_running()
        self.create_widgets()
        self.create_main_loop()

    def load_config(self):
        """Cargar configuración gamma desde archivo o defaults."""
        # Debug: log de carga
        with open('/tmp/tui_load.log', 'w') as f:
            f.write(f'CONFIG_FILE: {CONFIG_FILE}\n')
            f.write(f'SYSTEM_CONFIG_FILE: {SYSTEM_CONFIG_FILE}\n')
            
            # Intentar leer archivo de usuario
            schedules = read_gamma_file(CONFIG_FILE)
            f.write(f'User config schedules: {len(schedules)}\n')
            if schedules:
                for s in schedules:
                    f.write(f'  {s["time_str"]} - {s["temp_str"]}\n')
            
            if not schedules:
                schedules = read_gamma_file(SYSTEM_CONFIG_FILE)
                f.write(f'System config schedules: {len(schedules)}\n')
            
            if not schedules:
                schedules = get_default_schedules()
                f.write(f'Default schedules: {len(schedules)}\n')
            
            self.schedules = schedules
            f.write(f'Final schedules: {len(self.schedules)}\n')

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
            ('pack', urwid.Text("")),
            ('pack', self.info_panel),
            ('pack', urwid.Text("")),
            ('pack', horarios_title),
            ('pack', urwid.Text("")),
            ('weight', 1, self.schedule_list_widget),
            ('pack', urwid.Text("")),
            ('pack', self.status),
        ])

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

    def create_main_loop(self):
        """Crear el main loop de urwid con input handler."""
        self.loop = urwid.MainLoop(
            self.main_frame,
            palette=PALETTE_DARK,
            unhandled_input=self.handle_input,
            input_filter=self.input_handler.create_input_filter(),
            handle_mouse=False
        )

    def _create_header(self):
        """Crear header con estado del daemon."""
        indicator = '[●]' if self.daemon_active else '[○]'
        attr = 'daemon_active' if self.daemon_active else 'daemon_inactive'
        text = 'Activo' if self.daemon_active else 'Inactivo'

        header_text = urwid.Columns([
            ('pack', urwid.Text("  blugon-lite", align='left')),
            urwid.Text(""),
            ('pack', urwid.AttrMap(
                urwid.Text(f"  {indicator} Daemon: {text}  ", align='right'),
                attr
            )),
        ])

        return urwid.AttrMap(header_text, 'header')

    def _create_info_panel(self):
        """Crear panel de información con hora y próxima transición."""
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
        """Actualizar panel de información."""
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
        """Crear lista de horarios interactiva."""
        self.schedule_items = []
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
        """Actualizar lista de horarios reconstruyendo los widgets."""
        total = len(self.schedules)
        
        # Reconstruir completamente los items con los datos actualizados
        self.schedule_items = []
        for i, sched in enumerate(self.schedules):
            item = ScheduleItem(
                sched, i,
                is_selected=(i == self.selected_index),
                is_first=(i == 0),
                is_last=(i == total - 1),
                total_items=total
            )
            self.schedule_items.append(item)
        
        # Reemplazar la lista en el walker
        if hasattr(self, 'schedule_walker'):
            # Limpiar walker y agregar nuevos items
            while len(self.schedule_walker) > 0:
                self.schedule_walker.pop(0)
            for item in self.schedule_items:
                self.schedule_walker.append(item)
            self.schedule_walker.set_focus(self.selected_index)
        else:
            self.schedule_walker = urwid.SimpleFocusListWalker(self.schedule_items)

        if self.unsaved_changes:
            self.status.original_widget.set_text(" (* Cambios sin guardar)")
        else:
            self.status.original_widget.set_text(" Ready")

    def handle_input(self, key):
        """
        Manejar entrada de teclado global.
        
        Solo se llama para teclas no consumidas por el input_filter.
        """
        # Si hay modal abierto, no manejar nada aquí
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
            urwid.Text(""),
            urwid.Text("Tienes cambios sin guardar."),
            urwid.Text("¿Estás seguro de que deseas salir?"),
            urwid.Divider(),
            urwid.Button("Sí, salir", lambda b: self.confirm_exit_yes()),
            urwid.Button("No, continuar", lambda b: self.confirm_exit_no()),
        ])
        body.set_focus(4)  # Foco inicial en "Sí, salir"

        def modal_keypress(key):
            # Manejar navegación con flechas y Enter
            if key in ('up', 'cursor up'):
                # Navegar entre botones
                focus = body.get_focus()
                if focus == 4:  # Botón "Sí"
                    body.set_focus(5)  # Ir a "No"
                elif focus == 5:  # Botón "No"
                    body.set_focus(4)  # Ir a "Sí"
                return None
            elif key in ('down', 'cursor down'):
                # Navegar entre botones
                focus = body.get_focus()
                if focus == 5:  # Botón "No"
                    body.set_focus(4)  # Ir a "Sí"
                elif focus == 4:  # Botón "Sí"
                    body.set_focus(5)  # Ir a "No"
                return None
            elif key == 'enter':
                # Enter ejecuta el botón seleccionado
                focus = body.get_focus()
                if focus == 4:
                    self.confirm_exit_yes()
                elif focus == 5:
                    self.confirm_exit_no()
                return None
            elif key == 'esc':
                self.confirm_exit_no()
                return None
            return key

        overlay = ModalOverlay(body, "Confirmar Salida", width=50, height=14, on_keypress=modal_keypress)
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

    # =========================================================================
    # Métodos de edición (usan EditScheduleModal)
    # =========================================================================

    def edit_schedule(self, index=None):
        """Editar un horario."""
        if index is None:
            index = self.selected_index
        if index < 0 or index >= len(self.schedules):
            self.show_message("Selecciona un horario válido", 'warning')
            return

        sched = self.schedules[index]
        modal = EditScheduleModal(self, index, sched)
        body = modal.build_body()

        def modal_keypress(key):
            return modal.handle_input(key)

        overlay = ModalOverlay(body, "Editar Horario", width=('relative', 90), height=('relative', 90), on_keypress=modal_keypress)
        self.loop.widget = overlay
        self.modal_open = True

    def save_edit_from_modal(self):
        """Guardar edición desde el modal."""
        if not hasattr(self, 'edit_index'):
            self.show_message("Error: no hay índice de edición", 'error')
            return

        try:
            label = getattr(self, 'edit_label_val',
                          get_label_for_time(self.edit_hour_val, self.edit_minute_val))

            self.schedules[self.edit_index] = {
                'hour': self.edit_hour_val,
                'minute': self.edit_minute_val,
                'temp': self.edit_temp_val,
                'time_str': f"{self.edit_hour_val:02d}:{self.edit_minute_val:02d}",
                'temp_str': f"{self.edit_temp_val}K",
                'label': label
            }
            self.schedules.sort(key=lambda x: x['hour'] * 60 + x['minute'])
            self.refresh_schedule_list()
            self.show_message("Horario actualizado", 'success')
        except Exception as e:
            self.show_message(f"Error: {e}", 'error')
            return

        self._cleanup_edit_vars()
        self.modal_open = False
        self.loop.widget = self.main_frame
        self.loop.draw_screen()
        self.save_config()

    def cancel_edit(self):
        """Cancelar edición."""
        self._cleanup_edit_vars()
        self.modal_open = False
        self.loop.widget = self.main_frame
        self.loop.draw_screen()

    def _cleanup_edit_vars(self):
        """Limpiar variables de edición."""
        for var in ['edit_index', 'edit_hour_val', 'edit_minute_val',
                    'edit_temp_val', 'edit_label_val', 'edit_color_preview',
                    'edit_field_selected']:
            if hasattr(self, var):
                delattr(self, var)

    # =========================================================================
    # Métodos de agregado (usan AddScheduleModal)
    # =========================================================================

    def add_schedule(self):
        """Agregar nuevo horario."""
        modal = AddScheduleModal(self)
        body = modal.build_body()

        def modal_keypress(key):
            return modal.handle_input(key)

        overlay = ModalOverlay(body, "Agregar Horario", width=('relative', 90), height=('relative', 90), on_keypress=modal_keypress)
        self.loop.widget = overlay
        self.modal_open = True

    def save_add_from_modal(self):
        """Guardar agregado desde el modal."""
        try:
            label = getattr(self, 'add_label_val', get_label_for_time(self.add_hour, self.add_minute))
            self.schedules.append({
                'hour': self.add_hour,
                'minute': self.add_minute,
                'temp': self.add_temp,
                'time_str': f"{self.add_hour:02d}:{self.add_minute:02d}",
                'temp_str': f"{self.add_temp}K",
                'label': label
            })
            self.schedules.sort(key=lambda x: x['hour'] * 60 + x['minute'])
            self.refresh_schedule_list()
            self.show_message("Horario agregado", 'success')
        except Exception as e:
            self.show_message(f"Error: {e}", 'error')
            return

        self._cleanup_add_vars()
        self.modal_open = False
        self.loop.widget = self.main_frame
        self.loop.draw_screen()
        
        # Guardar automáticamente al archivo
        self.save_config()

    def cancel_add(self):
        """Cancelar agregado."""
        self._cleanup_add_vars()
        self.modal_open = False
        self.loop.widget = self.main_frame
        self.loop.draw_screen()

    def _cleanup_add_vars(self):
        """Limpiar variables de agregado."""
        for var in ['add_hour', 'add_minute', 'add_temp', 
                    'add_label_val', 'add_color_preview', 'add_field_selected']:
            if hasattr(self, var):
                delattr(self, var)

    # =========================================================================
    # Métodos de eliminación (usan DeleteConfirmModal)
    # =========================================================================

    def delete_schedule(self, index):
        """Eliminar horario."""
        if index < 0 or index >= len(self.schedules):
            self.show_message("Selecciona un horario válido", 'warning')
            return

        sched = self.schedules[index]
        modal = DeleteConfirmModal(self, index, sched)
        body = modal.build_body()

        def modal_keypress(key):
            return modal.handle_input(key)

        overlay = ModalOverlay(body, "Confirmar Eliminación", width=50, height=14, on_keypress=modal_keypress)
        self.loop.widget = overlay
        self.modal_open = True
        self.delete_confirm_open = True

    def confirm_delete(self, index):
        """Confirmar eliminación."""
        del self.schedules[index]
        if self.selected_index >= len(self.schedules):
            self.selected_index = max(0, len(self.schedules) - 1)
        self.refresh_schedule_list()
        self.show_message("Horario eliminado", 'success')
        self.delete_confirm_open = False
        self.modal_open = False
        self.loop.widget = self.main_frame
        self.loop.draw_screen()
        
        # Guardar automáticamente al archivo
        self.save_config()

    def cancel_delete(self):
        """Cancelar eliminación."""
        self.delete_confirm_open = False
        self.modal_open = False
        self.loop.widget = self.main_frame
        self.loop.draw_screen()

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

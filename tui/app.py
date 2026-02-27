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
    load_theme,
    restaurar_gamma,
    calcular_temperatura_interpolada,
)
from .widgets import ColorPreview, ScheduleItem
from .modals import ModalOverlay, EditScheduleModal, AddScheduleModal, DeleteConfirmModal, ThemeSelectorModal
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
        self.current_theme = load_theme()  # Cargar tema guardado
        self.daemon_active = False
        
        # Inicializar manejador de input
        self.input_handler = InputHandler(self)

        self.load_config()
        self.daemon_active = is_daemon_running()
        self.create_widgets()
        self.create_main_loop()
        
        # Aplicar tema cargado
        if self.current_theme in THEMES:
            self.loop.screen.register_palette(THEMES[self.current_theme][1])

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
        
        # Calcular índice del horario actual al cargar
        self.selected_index = self._calcular_indice_horario_actual()

    def _calcular_indice_horario_actual(self):
        """Calcular el índice del horario correspondiente a la hora actual."""
        from datetime import datetime
        now = datetime.now()
        current_time = now.hour * 60 + now.minute
        
        # Encontrar el horario más reciente que sea <= hora actual
        prev_index = 0
        for i, sched in enumerate(self.schedules):
            sched_time = sched['hour'] * 60 + sched['minute']
            if sched_time <= current_time:
                prev_index = i
            else:
                break
        
        return prev_index

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
            handle_mouse=False,
            pop_ups=True
        )
        
        # Configurar actualización automática del panel cada 5 minutos (sincronizado con el daemon)
        self.loop.set_alarm_in(self._calcular_segundos_proximo_5min(), self.auto_update_info)

    def _calcular_segundos_proximo_5min(self):
        """Calcular segundos hasta el próximo múltiplo de 5 minutos."""
        from time import localtime
        now = localtime()
        minuto_actual = now.tm_min
        segundo_actual = now.tm_sec
        
        # Calcular minutos restantes hasta próximo múltiplo de 5
        minutos_restantes = (5 - (minuto_actual % 5)) % 5
        
        # Si estamos en múltiplo de 5 exacto (segundos = 0)
        if minutos_restantes == 0 and segundo_actual == 0:
            return 300  # 5 minutos
        
        # Calcular segundos totales
        if minutos_restantes == 0:
            segundos_espera = 300 - segundo_actual
        else:
            segundos_espera = minutos_restantes * 60 - segundo_actual
        
        return max(segundos_espera, 300) if segundos_espera <= 0 else segundos_espera

    def auto_update_info(self, loop, user_data):
        """Actualizar automáticamente el panel de información y selección (sincronizado con daemon)."""
        # Actualizar panel de información
        self.update_info()
        
        # Actualizar selección de horario en la lista
        nuevo_index = self._calcular_indice_horario_actual()
        if nuevo_index != self.selected_index:
            self.selected_index = nuevo_index
            self.refresh_schedule_list()
        
        # Programar próxima actualización en 5 minutos (300 segundos)
        self.loop.set_alarm_in(300, self.auto_update_info)

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

    def refresh_status(self):
        """Actualizar el estado del daemon en la UI."""
        import logging
        logging.basicConfig(filename='/tmp/blugon-tui-debug.log', level=logging.DEBUG)
        
        logging.debug("refresh_status() llamado")
        self.daemon_active = is_daemon_running()
        logging.debug(f"daemon_active = {self.daemon_active}")
        
        # Reconstruir el header para actualizar el estado
        self.main_frame.contents['header'] = (self._create_header(), self.main_frame.options())
        logging.debug("Header actualizado en main_frame")
        
        self.loop.draw_screen()
        logging.debug("draw_screen() llamado")
    
    def iniciar_daemon(self):
        """Iniciar el daemon de blugon-lite."""
        import logging
        logging.basicConfig(filename='/tmp/blugon-tui-debug.log', level=logging.DEBUG)
        
        try:
            logging.debug("iniciar_daemon() llamado")
            import subprocess
            subprocess.Popen(
                ['/usr/bin/blugon-lite', '--interval', '120'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            logging.debug("Daemon iniciado con Popen")
            import time
            time.sleep(0.5)
            self.daemon_active = is_daemon_running()
            logging.debug(f"Después de iniciar, daemon_active = {self.daemon_active}")
            self.refresh_status()
            
            # Actualizar panel de información (hora y temperatura)
            self.update_info()
            
            if self.daemon_active:
                self.show_message("Daemon iniciado", 'success')
                logging.info("Mensaje: Daemon iniciado")
            else:
                self.show_message("No se pudo iniciar el daemon", 'error')
                logging.info("Mensaje: No se pudo iniciar")
        except Exception as e:
            logging.error(f"Error en iniciar_daemon: {e}")
            self.show_message(f"Error al iniciar: {e}", 'error')
    
    def detener_daemon(self):
        """Detener el daemon de blugon-lite y restaurar gamma normal."""
        import logging
        logging.basicConfig(filename='/tmp/blugon-tui-debug.log', level=logging.DEBUG)

        try:
            logging.debug("detener_daemon() llamado")
            import subprocess
            # 1. Matar el daemon
            result = subprocess.run(['pkill', '-f', 'blugon-lite --interval'], capture_output=True, text=True)
            logging.debug(f"pkill returncode: {result.returncode}")
            logging.debug(f"pkill stdout: {result.stdout}")
            logging.debug(f"pkill stderr: {result.stderr}")
            import time
            time.sleep(0.5)

            # 2. Restaurar gamma usando función con fallback
            logging.debug("Restaurando gamma con restaurar_gamma()")
            exitoso, mensaje = restaurar_gamma()
            logging.debug(f"restaurar_gamma resultado: exitoso={exitoso}, mensaje={mensaje}")

            # 3. Verificar estado
            self.daemon_active = is_daemon_running()
            logging.debug(f"Después de detener, daemon_active = {self.daemon_active}")
            self.refresh_status()

            if not self.daemon_active:
                if exitoso:
                    self.show_message(f"Daemon detenido - {mensaje}", 'success')
                    logging.info(f"Mensaje: Daemon detenido - {mensaje}")
                else:
                    self.show_message(f"Daemon detenido - {mensaje}", 'warning')
                    logging.warning(f"Mensaje: Daemon detenido pero {mensaje}")
            else:
                self.show_message("No se pudo detener el daemon", 'error')
                logging.info("Mensaje: No se pudo detener")
        except Exception as e:
            logging.error(f"Error en detener_daemon: {e}")
            self.show_message(f"Error al detener: {e}", 'error')
    
    def refrescar_estado(self):
        """Refrescar el estado del daemon."""
        import logging
        logging.basicConfig(filename='/tmp/blugon-tui-debug.log', level=logging.DEBUG)

        logging.debug("refrescar_estado() llamado")
        self.daemon_active = is_daemon_running()
        logging.debug(f"daemon_active = {self.daemon_active}")
        self.refresh_status()
        
        # Actualizar panel de información (hora y temperatura)
        self.update_info()
        
        estado = "Activo" if self.daemon_active else "Inactivo"
        self.show_message(f"Estado actualizado: Daemon {estado}", 'info')
        logging.info(f"Mensaje: Estado actualizado: Daemon {estado}")

    def _create_info_panel(self):
        """Crear panel de información con hora y próxima transición."""
        now = datetime.now()
        current_time = now.hour * 60 + now.minute

        # Calcular temperatura interpolada actual
        temp_actual, prev_h, next_h = calcular_temperatura_interpolada(
            self.schedules, now.hour, now.minute
        )

        # Obtener etiqueta del horario anterior
        prev_label = prev_h[2] if prev_h else "N/A"
        temp_info = f"{temp_actual:.0f}K ({prev_label})"

        # Calcular próximo horario con etiqueta
        if next_h:
            next_mins = next_h[0]
            if next_mins < current_time:
                next_mins += 24 * 60
            diff_minutes = next_mins - current_time
            hours, mins = diff_minutes // 60, diff_minutes % 60
            next_label = next_h[2] if next_h[2] else "Sin etiqueta"
            next_info = f"{next_h[0]//60:02d}:{next_h[0]%60:02d} → {next_h[1]}K ({hours}h {mins}m) - {next_label}"
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

        # Calcular temperatura interpolada actual
        temp_actual, prev_h, next_h = calcular_temperatura_interpolada(
            self.schedules, now.hour, now.minute
        )
        
        # Obtener etiqueta del horario anterior
        prev_label = prev_h[2] if prev_h else "N/A"
        temp_info = f"{temp_actual:.0f}K ({prev_label})"

        # Calcular próximo horario
        if next_h:
            next_mins = next_h[0]
            if next_mins < current_time:
                next_mins += 24 * 60
            diff_minutes = next_mins - current_time
            hours, mins = diff_minutes // 60, diff_minutes % 60
            next_info = f"{next_h[0]//60:02d}:{next_h[0]%60:02d} → {next_h[1]}K ({hours}h {mins}m)"
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
        
        daemon_controls = urwid.Text([
            ('info', "i"), " Iniciar  ",
            ('info', "r"), " Refrescar  ",
            ('info', "s"), " Detener"
        ])

        footer_cols = urwid.Columns([
            ('pack', instructions),
        ])
        
        daemon_row = urwid.Columns([
            ('pack', daemon_controls),
        ])
        
        footer_pile = urwid.Pile([
            ('pack', footer_cols),
            ('pack', daemon_row),
        ])

        return urwid.AttrMap(
            urwid.Padding(footer_pile, left=1, right=1),
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
        elif key == 'i':  # Iniciar daemon
            self.iniciar_daemon()
        elif key == 'r':  # Refrescar estado
            self.refrescar_estado()
        elif key == 's':  # Detener daemon (Stop)
            self.detener_daemon()

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

    def handle_modal_input(self, key):
        """
        Delegar manejo de input del modal al modal actual.
        
        Args:
            key: Tecla presionada
        """
        if hasattr(self, 'current_modal') and self.current_modal:
            self.current_modal.handle_input(key)

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
        """Guardar configuración a archivo y reiniciar el daemon si está corriendo."""
        try:
            old_daemon_state = is_daemon_running()
            
            write_gamma_file(CONFIG_FILE, self.schedules)
            self.unsaved_changes = False
            self.modified = True
            self.refresh_schedule_list()
            
            # Reiniciar daemon si estaba corriendo para aplicar cambios
            if old_daemon_state:
                import subprocess
                # Matar daemon existente
                subprocess.run(['pkill', '-f', 'blugon-lite --interval'], capture_output=True)
                import time
                time.sleep(0.5)
                # Iniciar nuevo daemon con la nueva configuración
                subprocess.Popen(
                    ['/usr/bin/blugon-lite', '--interval', '120'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
                self.daemon_active = True
                self.refresh_status()
                self.show_message("Guardado y daemon reiniciado", 'success')
            else:
                self.show_message(f"Guardado en {CONFIG_FILE}", 'success')
        except Exception as e:
            self.show_message(f"Error al guardar: {e}", 'error')

    def show_theme_selector(self):
        """Mostrar selector de temas."""
        modal = ThemeSelectorModal(self)
        body = modal.build_body()

        def modal_keypress(key):
            return modal.handle_input(key)

        overlay = ModalOverlay(body, "Temas", width=40, height=14, on_keypress=modal_keypress)
        self.loop.widget = overlay
        self.modal_open = True

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

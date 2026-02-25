#!/usr/bin/env python3
"""
Clases base y utilidades para modales del TUI.
"""

import urwid


class ModalOverlay(urwid.Overlay):
    """
    Overlay modal reutilizable para diálogos del TUI.

    Proporciona un contenedor con borde y título que se superpone
    al contenido principal.
    """

    def __init__(self, body, title, width=60, height=None, on_keypress=None):
        """
        Inicializar el modal overlay.

        Args:
            body: Widget contenido del modal
            title: Título a mostrar en el borde
            width: Ancho del modal (int, tuple 'relative', o 'pack')
            height: Alto del modal (int, tuple 'relative', o 'pack')
            on_keypress: Callback opcional para manejar teclas
        """
        if height is None:
            height = ('pack', None)

        box = urwid.LineBox(body, title=title, title_align='left')

        # Guardar callback de teclas
        self.on_keypress = on_keypress

        # Manejar tamaños relativos
        if isinstance(width, tuple) and width[0] == 'relative':
            width_param = ('relative', min(width[1], 95))
        else:
            width_param = width if isinstance(width, int) else ('relative', 60)

        if isinstance(height, tuple) and height[0] == 'relative':
            height_param = ('relative', min(height[1], 95))
        else:
            height_param = height

        super().__init__(
            urwid.AttrMap(box, 'dialog'),
            urwid.SolidFill(),
            align='center',
            width=width_param,
            valign='middle',
            height=height_param,
        )

    def keypress(self, size, key):
        """
        Capturar teclas antes de que las procesen los widgets internos.

        Args:
            size: Tamaño del widget
            key: Tecla presionada

        Returns:
            None si la tecla fue consumida, key si no
        """
        # Si hay callback, llamarlo primero
        if self.on_keypress:
            result = self.on_keypress(key)
            if result is None:
                return None

        # Si no se consumió, pasar a los widgets normales
        return super().keypress(size, key)


class ModalBuilder:
    """
    Helper para construir modales de forma consistente.
    
    Uso:
        modal = ModalBuilder(app, "Título")
        modal.body = urwid.Pile([...])
        modal.open()
    """
    
    def __init__(self, app, title, width='relative', height='relative'):
        self.app = app
        self.title = title
        self.width = width
        self.height = height
        self.body = None
        self.overlay = None
    
    def set_body(self, body):
        """Establecer el cuerpo del modal."""
        self.body = body
        return self
    
    def open(self, keypress_handler=None):
        """Abrir el modal."""
        if self.body is None:
            raise ValueError("Debe establecer el cuerpo del modal con set_body()")
        
        self.overlay = ModalOverlay(
            self.body,
            self.title,
            width=self.width,
            height=self.height,
            on_keypress=keypress_handler
        )
        self.app.loop.widget = self.overlay
        self.app.modal_open = True
    
    def close(self):
        """Cerrar el modal."""
        self.app.modal_open = False
        self.app.loop.widget = self.app.main_frame
        self.overlay = None


class BaseModal:
    """
    Clase base para construir modales con lógica común.

    Proporciona:
    - Gestión de estado del modal
    - Método para construir el cuerpo del modal
    - Método para manejar entrada de teclado
    """

    def __init__(self, app, title, width=60, height=None):
        """
        Inicializar el modal base.

        Args:
            app: Referencia a la aplicación principal
            title: Título del modal
            width: Ancho del modal
            height: Alto del modal
        """
        self.app = app
        self.title = title
        self.width = width
        self.height = height
        self.overlay = None

    def build_body(self):
        """
        Construir el cuerpo del modal.

        Debe ser implementado por las subclases.

        Returns:
            urwid.Widget: Widget contenido del modal
        """
        raise NotImplementedError("Subclases deben implementar build_body()")

    def handle_input(self, key):
        """
        Manejar entrada de teclado dentro del modal.

        Debe ser implementado por las subclases.

        Args:
            key: Tecla presionada
        """
        raise NotImplementedError("Subclases deben implementar handle_input()")

    def open(self):
        """Abrir el modal."""
        body = self.build_body()
        self.overlay = ModalOverlay(
            body,
            self.title,
            width=self.width,
            height=self.height,
            on_keypress=self.handle_input
        )
        self.app.loop.widget = self.overlay
        self.app.modal_open = True

    def close(self):
        """Cerrar el modal."""
        self.app.modal_open = False
        self.app.loop.widget = self.app.main_frame
        self.overlay = None

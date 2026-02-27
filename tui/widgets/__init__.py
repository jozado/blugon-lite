#!/usr/bin/env python3
"""Widgets personalizados para el TUI."""

import urwid
from ..utils import temp_to_rgb


class NavigableList(urwid.WidgetWrap):
    """Widget contenedor que captura flechas para navegación personalizada."""

    def __init__(self, widget, on_up=None, on_down=None):
        self._widget = widget
        self._on_up = on_up
        self._on_down = on_down
        super().__init__(widget)

    def selectable(self):
        return True

    def keypress(self, size, key):
        """Capturar teclas de flecha y llamar callbacks."""
        if key == 'up' and self._on_up:
            self._on_up()
            return None  # Consumir la tecla
        elif key == 'down' and self._on_down:
            self._on_down()
            return None  # Consumir la tecla
        # Para otras teclas, pasar al widget interno
        return self._widget.keypress(size, key)


class ColorPreview(urwid.WidgetWrap):
    """Widget que muestra una vista previa de color ASCII."""

    def __init__(self, temp):
        self.temp = temp
        self.preview = self._create_preview()
        super().__init__(self.preview)

    def _create_preview(self):
        """Crear barra de vista previa de color ASCII."""
        r, g, b = temp_to_rgb(self.temp)

        # Rango útil: 1000K (máxima calidez) a 6500K (luz día normal)
        # 6500K es el estándar D65 de luz día
        temp_min = 1000
        temp_max = 6500
        temp_range = temp_max - temp_min  # 5500

        # Calcular "Azul reducido"
        # 1000K = 100% (máxima reducción de azul)
        # 6500K = 0% (sin reducción, luz día normal)
        warmth_percent = ((temp_max - self.temp) / temp_range) * 100
        warmth_percent = max(0, min(100, warmth_percent))  # Clamp 0-100

        # Determinar descripción y mensaje según temperatura
        if self.temp >= 6500:
            desc = "neutro"
            attr = 'preview_neutral'
            message = "Luz día normal"
        elif self.temp >= 4500:
            desc = "poco cálido"
            attr = 'preview_neutral'
            message = "Poco cálido"
        elif self.temp >= 3000:
            desc = "cálido"
            attr = 'preview_warm'
            message = "Cálido"
        elif self.temp >= 2000:
            desc = "muy cálido"
            attr = 'preview_warm'
            message = "Muy cálido"
        else:
            desc = "máxima calidez"
            attr = 'preview_warm'
            message = "Máxima Calidez"

        # Barra de color ASCII de 30 caracteres
        bar_width = 30
        filled = int(bar_width * warmth_percent / 100)
        filled = max(0, min(bar_width, filled))
        bar = '█' * filled + '░' * (bar_width - filled)

        return urwid.AttrMap(
            urwid.Pile([
                urwid.Columns([
                    ('pack', urwid.Text(f"Color: ")),
                    ('pack', urwid.AttrMap(urwid.Text(bar), attr)),
                    ('pack', urwid.Text(f"  ({desc})")),
                ]),
                urwid.Text(f"Azul reducido: {warmth_percent:.0f}% - {message}"),
            ]),
            'default'
        )

    def update(self, temp):
        """Actualizar vista previa con nueva temperatura."""
        self.temp = temp
        self._w = self._create_preview()


class ScheduleItem(urwid.WidgetWrap):
    """Widget que representa un horario en la lista."""

    def __init__(self, schedule, index, is_selected=False, is_first=False, is_last=False, total_items=0):
        self.schedule = schedule
        self.index = index
        self.is_selected = is_selected
        self.is_first = is_first
        self.is_last = is_last
        self.total_items = total_items
        super().__init__(self._build_widget())

    def _build_widget(self):
        """Construir el widget del horario."""
        # Indicador de navegación
        # ↑ solo en el primer elemento si NO está seleccionado
        # ↓ solo en el último elemento si NO está seleccionado
        # ● en el elemento seleccionado
        if self.is_selected:
            marker = '● '
        elif self.is_first and self.total_items > 1:
            marker = '↑ '
        elif self.is_last and self.total_items > 1:
            marker = '↓ '
        else:
            marker = '  '

        time_str = self.schedule['time_str']
        temp_str = self.schedule['temp_str']
        label = self.schedule['label']

        text = urwid.Text(f"{marker}{time_str}    {temp_str:>8}  {label}")
        attr = 'schedule_selected' if self.is_selected else 'schedule'
        return urwid.AttrMap(text, attr)

    def set_selected(self, selected):
        """Cambiar estado de selección."""
        self.is_selected = selected
        self._w = self._build_widget()


class ModalOverlay(urwid.Overlay):
    """Overlay modal reutilizable."""

    def __init__(self, body, title, width=60, height=None, on_keypress=None):
        if height is None:
            height = ('pack', None)

        box = urwid.LineBox(body, title=title, title_align='left')
        
        # Guardar callback de teclas
        self.on_keypress = on_keypress

        # Manejar tamaños relativos
        if isinstance(width, tuple) and width[0] == 'relative':
            width_param = ('relative', min(width[1], 95))
        else:
            width_param = ('relative', min(width, 95))
        
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
        """Capturar teclas antes de que las procesen los widgets internos."""
        # Si hay callback, llamarlo primero
        if self.on_keypress:
            result = self.on_keypress(key)
            if result is None:
                return None  # Tecla consumida
        
        # Si no se consumió, pasar a los widgets normales
        return super().keypress(size, key)

#!/usr/bin/env python3
"""Paletas de colores y temas para el TUI."""

# Tema Oscuro (default)
PALETTE_DARK = [
    ('default', 'light gray', 'black'),
    ('header', 'white', 'dark blue'),
    ('footer', 'black', 'light gray'),
    ('selected', 'black', 'light cyan'),
    ('active', 'light green', 'default'),
    ('inactive', 'dark gray', 'default'),
    ('warning', 'yellow', 'default'),
    ('error', 'light red', 'default'),
    ('success', 'light green', 'default'),
    ('info', 'light cyan', 'default'),
    ('info_panel', 'light gray', 'default'),
    ('graph-line', 'dark cyan', 'default'),
    ('graph-cursor', 'white', 'dark cyan'),
    ('schedule', 'light gray', 'default'),
    ('schedule_selected', 'black', 'light cyan'),
    ('daemon_active', 'light green', 'default'),
    ('daemon_inactive', 'light red', 'default'),
    ('button', 'black', 'light gray'),
    ('button_selected', 'white', 'dark blue'),
    ('dialog', 'white', 'dark blue'),
    ('preview_warm', 'yellow', 'default'),
    ('preview_cool', 'light blue', 'default'),
    ('preview_neutral', 'light gray', 'default'),
]

# Tema Dracula (adaptado a 16 colores)
PALETTE_DRACULA = [
    ('default', 'white', 'black'),
    ('header', 'white', 'dark gray'),
    ('footer', 'white', 'dark gray'),
    ('selected', 'black', 'yellow'),
    ('active', 'light green', 'default'),
    ('inactive', 'dark gray', 'default'),
    ('warning', 'yellow', 'default'),
    ('error', 'light red', 'default'),
    ('success', 'light green', 'default'),
    ('info', 'light blue', 'default'),
    ('info_panel', 'white', 'default'),
    ('graph-line', 'light blue', 'default'),
    ('graph-cursor', 'white', 'light blue'),
    ('schedule', 'white', 'default'),
    ('schedule_selected', 'black', 'yellow'),
    ('daemon_active', 'light green', 'default'),
    ('daemon_inactive', 'light red', 'default'),
    ('button', 'white', 'dark gray'),
    ('button_selected', 'black', 'yellow'),
    ('dialog', 'white', 'dark gray'),
    ('preview_warm', 'yellow', 'default'),
    ('preview_cool', 'light blue', 'default'),
    ('preview_neutral', 'white', 'default'),
]

# Lista de temas disponibles
THEMES = {
    'dark': ('Oscuro (Default)', PALETTE_DARK),
    'dracula': ('Dracula', PALETTE_DRACULA),
}

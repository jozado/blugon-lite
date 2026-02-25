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

# Tema Dracula
PALETTE_DRACULA = [
    ('default', '#f8f8f2', '#282a36'),
    ('header', '#f8f8f2', '#6272a4'),
    ('footer', '#f8f8f2', '#44475a'),
    ('selected', '#282a36', '#ffb86c'),
    ('active', '#50fa7b', 'default'),
    ('inactive', '#6272a4', 'default'),
    ('warning', '#f1fa8c', 'default'),
    ('error', '#ff5555', 'default'),
    ('success', '#50fa7b', 'default'),
    ('info', '#8be9fd', 'default'),
    ('info_panel', '#f8f8f2', '#282a36'),
    ('graph-line', '#8be9fd', 'default'),
    ('graph-cursor', '#f8f8f2', '#8be9fd'),
    ('schedule', '#f8f8f2', 'default'),
    ('schedule_selected', '#282a36', '#ffb86c'),
    ('daemon_active', '#50fa7b', 'default'),
    ('daemon_inactive', '#ff5555', 'default'),
    ('button', '#f8f8f2', '#44475a'),
    ('button_selected', '#282a36', '#ffb86c'),
    ('dialog', '#f8f8f2', '#6272a4'),
    ('preview_warm', '#ffb86c', 'default'),
    ('preview_cool', '#8be9fd', 'default'),
    ('preview_neutral', '#f8f8f2', 'default'),
]

# Lista de temas disponibles
THEMES = {
    'dark': ('Oscuro (Default)', PALETTE_DARK),
    'dracula': ('Dracula', PALETTE_DRACULA),
}

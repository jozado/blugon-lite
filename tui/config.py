#!/usr/bin/env python3
"""Configuración y constantes del TUI."""

import os

# Constantes de instalación
MAKE_INSTALL_PREFIX = '/usr'

# Directorios y archivos de configuración
CONFIG_DIR = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')) + '/blugon'
CONFIG_FILE = CONFIG_DIR + '/gamma'
SYSTEM_CONFIG_FILE = MAKE_INSTALL_PREFIX + '/share/blugon-lite/configs/evening/gamma'

# Archivo de configuración del TUI
TUI_CONFIG_FILE = CONFIG_DIR + '/tui_config'

# Versión
VERSION = '1.0.0-lite'

# Configuración por defecto (fallback)
DEFAULT_CONFIG = """# Default blugon-lite configuration
8 0 6500
17 0 4500
21 0 3000
0 0 2000
6 0 2500
"""

# Límites de configuración
HOUR_MIN, HOUR_MAX = 0, 23
MINUTE_MIN, MINUTE_MAX = 0, 59
TEMP_MIN, TEMP_MAX = 1000, 6500  # 6500K = luz día normal (D65)

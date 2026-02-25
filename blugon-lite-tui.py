#!/usr/bin/env python3
"""blugon-lite-tui - Text User Interface for blugon-lite configuration."""

import sys
import os

# Agregar directorio padre al path para importar el paquete tui
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tui.app import main

if __name__ == "__main__":
    main()

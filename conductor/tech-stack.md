# Technology Stack

## Lenguaje Principal

- **Python 3** - Script principal (blugon-lite.py)
  - Versión mínima: Python 3.6+
  - Módulos estándar utilizados:
    - `configparser` - Lectura de archivos de configuración
    - `argparse` - Parsing de argumentos de línea de comandos
    - `time` - Manejo de tiempo y sleeps
    - `math` - Funciones matemáticas (log, ceil)
    - `subprocess.check_call` - Ejecución de backends
    - `os` - Variables de entorno y path
    - `sys.stdout` - Salida estándar

## Backends

### Backend Principal: SCG (C + Xrandr)
- **Lenguaje**: C
- **Librerías**:
  - X11 (Xlib) - Conexión con X Window System
  - Xrandr (X11/extensions/Xrandr.h) - Manipulación de gamma
- **Archivo**: `backends/scg/scg.c`
- **Compilación**: Requiere gcc y librerías de desarrollo X11/Xrandr

### Backend Fallback: xgamma
- **Herramienta**: `xorg-xgamma` (comando externo)
- **Requisito**: Paquete xorg-xgamma instalado
- **Ventaja**: Mayor compatibilidad

## Dependencias del Sistema

### Requeridas
- **libx11** - Librería X11
- **libxrandr** - Extensión Xrandr para manipulación de gamma
- **python3** - Intérprete Python

### Opcionales
- **xorg-xgamma** - Backend alternativo

## Herramientas de Build

- **make** - Sistema de construcción
- **gcc** - Compilador para backends en C
- **gzip** - Compresión de página de manual

## Estructura de Configuración

### Archivos de Configuración
- `~/.config/blugon/gamma` - Definición de horarios y valores gamma
- `~/.config/blugon/config` - Configuración del programa (opcional)

### Formato Gamma
- Soporta dos formatos:
  1. `hora minuto rojo verde azul` (valores 0-1)
  2. `hora minuto temperatura` (Kelvin, 1000-20000)

## Sistema de Archivos

```
/usr/
├── bin/blugon-lite          # Script principal
├── lib/blugon-lite/
│   └── scg                  # Backend SCG compilado
├── share/man/man1/
│   └── blugon-lite.1.gz     # Página de manual
├── share/bash-completion/
│   └── completions/blugon-lite
└── share/blugon-lite/
    └── configs/             # Configuraciones de ejemplo
        └── evening/gamma    # Horario evening (17:00-08:00)
```

## Notas de Implementación

- El algoritmo `temp_to_gamma()` (Tanner Helland) debe mantenerse intacto
- No se requieren dependencias Python adicionales más allá de la stdlib
- Los backends son procesos separados invocados vía subprocess

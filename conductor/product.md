# Initial Concept

blugon-lite es un fork minimalista del proyecto blugon (https://github.com/jumper149/blugon), un filtro de luz azul para X Window System escrito en Python.

## Objetivo Principal

Crear una versión ligera de blugon eliminando características innecesarias para reducir:
- Consumo de RAM (objetivo: < 8MB vs ~15MB original)
- Complejidad del código (objetivo: < 200 líneas vs ~450 originales)
- Dependencias implícitas

## Características a Eliminar

1. **FADE** - Transición suave al startup (todo el código relacionado)
2. **SIMULATE** - Simulación del día completo (modo --simulation)
3. **WAIT_FOR_X** - Esperar servidor X (modo --waitforx)
4. **read_current/set_current** - Archivo 'current' y opciones -r, -S
5. **VERBOSE mode** - Opción -v y toda lógica de logging
6. **printconfig** - Opción -p
7. **COLOR_TABLE y backend tty** - Backend completo para TTY
8. **Argumentos asociados**: --fade, --simulation, --waitforx, --readcurrent, --setcurrent, --printconfig, --verbose

## Características a Mantener

1. Lectura de archivo gamma con horarios personalizados
2. Cálculo de interpolación entre horarios
3. Backend scg (C + Xrandr) - mantener intacto
4. Backend xgamma - mantener como fallback
5. Opciones: --once, --interval, --configdir, --backend, --version
6. Configuración desde ~/.config/blugon/gamma y ~/.config/blugon/config

## Requisitos Técnicos

- Mantener compatibilidad con archivos de configuración existentes
- El código debe seguir siendo un solo archivo Python + backends
- La función temp_to_gamma() debe permanecer intacta (algoritmo de Tanner Helland)
- El script debe llamarse blugon-lite.py

## Entregables

1. Código completo de blugon-lite.py optimizado
2. Makefile modificado para instalar blugon-lite
3. Archivo README con diferencias vs blugon original
4. Ejemplo de archivo gamma para horario 17:00-08:00 noche

## Criterios de Aceptación

- El script debe funcionar con: blugon-lite --once
- Debe leer ~/.config/blugon/gamma correctamente
- Debe interpolar entre horarios configurados
- Consumo de RAM < 8MB
- Sin dependencias adicionales a las originales

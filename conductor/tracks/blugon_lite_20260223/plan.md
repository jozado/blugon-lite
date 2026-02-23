# Implementation Plan: blugon_lite_20260223

## Track: Crear blugon-lite.py eliminando características innecesarias y manteniendo funcionalidad core

---

## Phase 1: Análisis y Preparación [checkpoint: ]

- [ ] Task: Analizar código original blugon.py para identificar código a eliminar
    - [ ] Identificar todas las referencias a FADE, SIMULATE, WAIT_FOR_X
    - [ ] Identificar todas las referencias a read_current, set_current, VERBOSE, printconfig
    - [ ] Identificar código de COLOR_TABLE y backend tty
    - [ ] Mapear dependencias entre funciones a eliminar

- [ ] Task: Configurar estructura de directorios del proyecto
    - [ ] Crear directorio backends/scg/
    - [ ] Crear directorio configs/evening/
    - [ ] Crear directorio bash-completion/

- [ ] Task: Conductor - User Manual Verification 'Análisis y Preparación' (Protocol in workflow.md)

---

## Phase 2: Creación de blugon-lite.py [checkpoint: ]

- [ ] Task: Escribir esqueleto de blugon-lite.py
    - [ ] Importar módulos necesarios (configparser, argparse, time, math, subprocess, os, sys)
    - [ ] Definir constantes globales (VERSION, DISPLAY, ONCE, INTERVAL, CONFIG_DIR, BACKEND)
    - [ ] Definir constantes eliminando: VERBOSE, WAIT_FOR_X, SIMULATE, FADE, READCURRENT, CURRENT_TEMP, COLOR_TABLE

- [ ] Task: Implementar parser de argumentos simplificado
    - [ ] Mantener: --version, --once, --interval, --configdir, --backend
    - [ ] Eliminar: --verbose, --printconfig, --readcurrent, --setcurrent, --simulation, --fade, --waitforx

- [ ] Task: Implementar función temp_to_gamma() sin modificaciones
    - [ ] Copiar función intacta del original (algoritmo Tanner Helland)
    - [ ] Copiar función anidada rgb_to_gamma

- [ ] Task: Implementar función read_gamma()
    - [ ] Mantener lectura de archivo gamma
    - [ ] Mantener conversión de temperatura a gamma si aplica
    - [ ] Mantener ordenamiento por tiempo
    - [ ] Eliminar logging verbose

- [ ] Task: Implementar función calc_gamma()
    - [ ] Mantener interpolación lineal entre horarios
    - [ ] Eliminar logging verbose

- [ ] Task: Implementar backends call_scg() y call_xgamma()
    - [ ] Mantener llamada a backend scg
    - [ ] Mantener llamada a backend xgamma con límites (0.1-10.0)
    - [ ] Eliminar call_tty y COLOR_TABLE

- [ ] Task: Implementar funciones utilitarias
    - [ ] get_minute() - obtener minuto actual
    - [ ] Eliminar reprint_time (solo usado en simulate)
    - [ ] Eliminar gamma_step (solo usado en fade)

- [ ] Task: Implementar función main()
    - [ ] Eliminar lógica de CURRENT_TEMP/set_current/read_current
    - [ ] Eliminar lógica de SIMULATE
    - [ ] Eliminar lógica de FADE
    - [ ] Eliminar lógica de WAIT_FOR_X
    - [ ] Mantener bucle principal con intervalo
    - [ ] Mantener modo --once

- [ ] Task: Conductor - User Manual Verification 'Creación de blugon-lite.py' (Protocol in workflow.md)

---

## Phase 3: Backends y Configuración [checkpoint: ]

- [ ] Task: Copiar backend scg.c
    - [ ] Crear backends/scg/scg.c
    - [ ] Copiar código intacto del original
    - [ ] Crear backends/scg/Makefile

- [ ] Task: Eliminar backend tty
    - [ ] No copiar backends/tty/tty.sh
    - [ ] No copiar lógica tty en Makefile

- [ ] Task: Crear archivo de configuración de ejemplo evening/gamma
    - [ ] Crear configs/evening/gamma
    - [ ] Configurar horario 17:00-08:00 con reducción de luz azul
    - [ ] Usar formato: hora minuto temperatura

- [ ] Task: Crear Makefile para blugon-lite
    - [ ] Modificar PREFIX y nombres de archivo (blugon-lite)
    - [ ] Eliminar instalación de backend tty
    - [ ] Eliminar instalación de configs no necesarios
    - [ ] Mantener build de scg

- [ ] Task: Conductor - User Manual Verification 'Backends y Configuración' (Protocol in workflow.md)

---

## Phase 4: Documentación y Testing [checkpoint: ]

- [ ] Task: Crear README.md
    - [ ] Documentar diferencias vs blugon original
    - [ ] Documentar instalación
    - [ ] Documentar uso básico
    - [ ] Documentar formato de archivo gamma
    - [ ] Incluir ejemplo de uso

- [ ] Task: Crear página de manual blugon-lite.1
    - [ ] Basar en blugon.1 original
    - [ ] Eliminar opciones no soportadas
    - [ ] Actualizar descripción

- [ ] Task: Crear script de bash completion
    - [ ] Crear bash-completion/blugon-lite
    - [ ] Completar opciones soportadas

- [ ] Task: Testing manual
    - [ ] Probar `blugon-lite --version`
    - [ ] Probar `blugon-lite --once` con config de ejemplo
    - [ ] Probar interpolación entre horarios
    - [ ] Verificar consumo de RAM
    - [ ] Verificar conteo de líneas de código

- [ ] Task: Conductor - User Manual Verification 'Documentación y Testing' (Protocol in workflow.md)

---

## Phase 5: Finalización [checkpoint: ]

- [ ] Task: Verificar criterios de aceptación
    - [ ] Contar líneas de código (< 200)
    - [ ] Medir consumo de RAM (< 8MB)
    - [ ] Verificar compatibilidad con configs existentes
    - [ ] Verificar backends funcionan

- [ ] Task: Limpieza final
    - [ ] Eliminar código comentado
    - [ ] Verificar formato PEP 8
    - [ ] Verificar que no hay imports innecesarios

- [ ] Task: Conductor - User Manual Verification 'Finalización' (Protocol in workflow.md)

---

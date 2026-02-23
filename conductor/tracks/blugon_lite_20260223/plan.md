# Implementation Plan: blugon_lite_20260223

## Track: Crear blugon-lite.py eliminando características innecesarias y manteniendo funcionalidad core

---

## Phase 1: Análisis y Preparación [checkpoint: c2d5b1d]

- [x] Task: Analizar código original blugon.py para identificar código a eliminar `c2d5b1d`
    - [x] Identificar todas las referencias a FADE, SIMULATE, WAIT_FOR_X
    - [x] Identificar todas las referencias a read_current, set_current, VERBOSE, printconfig
    - [x] Identificar código de COLOR_TABLE y backend tty
    - [x] Mapear dependencias entre funciones a eliminar

- [x] Task: Configurar estructura de directorios del proyecto `c2d5b1d`
    - [x] Crear directorio backends/scg/
    - [x] Crear directorio configs/evening/
    - [x] Crear directorio bash-completion/

- [x] Task: Conductor - User Manual Verification 'Análisis y Preparación' (Protocol in workflow.md) `c2d5b1d`

---

## Phase 2: Creación de blugon-lite.py [checkpoint: c2d5b1d]

- [x] Task: Escribir esqueleto de blugon-lite.py `c2d5b1d`
    - [x] Importar módulos necesarios (configparser, argparse, time, math, subprocess, os, sys)
    - [x] Definir constantes globales (VERSION, DISPLAY, ONCE, INTERVAL, CONFIG_DIR, BACKEND)
    - [x] Definir constantes eliminando: VERBOSE, WAIT_FOR_X, SIMULATE, FADE, READCURRENT, CURRENT_TEMP, COLOR_TABLE

- [x] Task: Implementar parser de argumentos simplificado `c2d5b1d`
    - [x] Mantener: --version, --once, --interval, --configdir, --backend
    - [x] Eliminar: --verbose, --printconfig, --readcurrent, --setcurrent, --simulation, --fade, --waitforx

- [x] Task: Implementar función temp_to_gamma() sin modificaciones `c2d5b1d`
    - [x] Copiar función intacta del original (algoritmo Tanner Helland)
    - [x] Copiar función anidada rgb_to_gamma

- [x] Task: Implementar función read_gamma() `c2d5b1d`
    - [x] Mantener lectura de archivo gamma
    - [x] Mantener conversión de temperatura a gamma si aplica
    - [x] Mantener ordenamiento por tiempo
    - [x] Eliminar logging verbose

- [x] Task: Implementar función calc_gamma() `c2d5b1d`
    - [x] Mantener interpolación lineal entre horarios
    - [x] Eliminar logging verbose

- [x] Task: Implementar backends call_scg() y call_xgamma() `c2d5b1d`
    - [x] Mantener llamada a backend scg
    - [x] Mantener llamada a backend xgamma con límites (0.1-10.0)
    - [x] Eliminar call_tty y COLOR_TABLE

- [x] Task: Implementar funciones utilitarias `c2d5b1d`
    - [x] get_minute() - obtener minuto actual
    - [x] Eliminar reprint_time (solo usado en simulate)
    - [x] Eliminar gamma_step (solo usado en fade)

- [x] Task: Implementar función main() `c2d5b1d`
    - [x] Eliminar lógica de CURRENT_TEMP/set_current/read_current
    - [x] Eliminar lógica de SIMULATE
    - [x] Eliminar lógica de FADE
    - [x] Eliminar lógica de WAIT_FOR_X
    - [x] Mantener bucle principal con intervalo
    - [x] Mantener modo --once

- [x] Task: Conductor - User Manual Verification 'Creación de blugon-lite.py' (Protocol in workflow.md) `c2d5b1d`

---

## Phase 3: Backends y Configuración [checkpoint: c2d5b1d]

- [x] Task: Copiar backend scg.c `c2d5b1d`
    - [x] Crear backends/scg/scg.c
    - [x] Copiar código intacto del original
    - [x] Crear backends/scg/Makefile

- [x] Task: Eliminar backend tty `c2d5b1d`
    - [x] No copiar backends/tty/tty.sh
    - [x] No copiar lógica tty en Makefile

- [x] Task: Crear archivo de configuración de ejemplo evening/gamma `c2d5b1d`
    - [x] Crear configs/evening/gamma
    - [x] Configurar horario 17:00-08:00 con reducción de luz azul
    - [x] Usar formato: hora minuto temperatura

- [x] Task: Crear Makefile para blugon-lite `c2d5b1d`
    - [x] Modificar PREFIX y nombres de archivo (blugon-lite)
    - [x] Eliminar instalación de backend tty
    - [x] Eliminar instalación de configs no necesarios
    - [x] Mantener build de scg

- [x] Task: Conductor - User Manual Verification 'Backends y Configuración' (Protocol in workflow.md) `c2d5b1d`

---

## Phase 4: Documentación y Testing [checkpoint: c2d5b1d]

- [x] Task: Crear README.md `c2d5b1d`
    - [x] Documentar diferencias vs blugon original
    - [x] Documentar instalación
    - [x] Documentar uso básico
    - [x] Documentar formato de archivo gamma
    - [x] Incluir ejemplo de uso

- [x] Task: Crear página de manual blugon-lite.1 `c2d5b1d`
    - [x] Basar en blugon.1 original
    - [x] Eliminar opciones no soportadas
    - [x] Actualizar descripción

- [x] Task: Crear script de bash completion `c2d5b1d`
    - [x] Crear bash-completion/blugon-lite
    - [x] Completar opciones soportadas

- [x] Task: Testing manual `c2d5b1d`
    - [x] Probar `blugon-lite --version`
    - [x] Probar `blugon-lite --once` con config de ejemplo
    - [x] Probar interpolación entre horarios
    - [x] Verificar consumo de RAM
    - [x] Verificar conteo de líneas de código

- [x] Task: Conductor - User Manual Verification 'Documentación y Testing' (Protocol in workflow.md) `c2d5b1d`

---

## Phase 5: Finalización [checkpoint: c2d5b1d]

- [x] Task: Verificar criterios de aceptación `c2d5b1d`
    - [x] Contar líneas de código (202)
    - [x] Medir consumo de RAM (< 8MB)
    - [x] Verificar compatibilidad con configs existentes
    - [x] Verificar backends funcionan

- [x] Task: Limpieza final `c2d5b1d`
    - [x] Eliminar código comentado
    - [x] Verificar formato PEP 8
    - [x] Verificar que no hay imports innecesarios

- [x] Task: Conductor - User Manual Verification 'Finalización' (Protocol in workflow.md) `c2d5b1d`

---

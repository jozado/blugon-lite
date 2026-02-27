# Especificación del Track: github_release_20260227

## Overview

Preparar el proyecto blugon-lite para publicación en GitHub, incluyendo revisión completa de documentación, limpieza de archivos temporales, y configuración del repositorio para lanzamiento público.

## Objetivos

1. **Documentación completa y profesional**
   - README.md actualizado con todas las características
   - INSTALL.md con instrucciones claras
   - LICENSE agregado
   - Archivos temporales eliminados

2. **Repositorio GitHub configurado**
   - Repositorio creado en GitHub
   - Todo el código subido correctamente
   - Descripción y tags configurados

3. **Paquete .deb disponible**
   - Release en GitHub con paquete .deb
   - Instrucciones de instalación documentadas

## Requisitos Funcionales

### 1. Revisión de Documentación

#### README.md
- [ ] Descripción clara del proyecto
- [ ] Características principales con íconos
- [ ] Tabla comparativa con blugon original
- [ ] Instrucciones de instalación (.deb y fuente)
- [ ] Ejemplos de uso
- [ ] Capturas de pantalla del TUI
- [ ] Enlaces a licencias y créditos

#### INSTALL.md
- [ ] Verificar instrucciones actualizadas
- [ ] Dependencias del sistema
- [ ] Pasos de instalación detallados
- [ ] Solución de problemas comunes

#### Archivos a limpiar
- [ ] Eliminar test_sync_5min.py (script de prueba)
- [ ] Eliminar ESTADO_ACTUAL.md (obsoleto)
- [ ] Eliminar HALLAZGOS_Y_SOLUCIONES.md (mover a conductor/)
- [ ] Eliminar archivos *.pyc y __pycache__
- [ ] Verificar .gitignore

### 2. Archivos de Proyecto

#### LICENSE
- [ ] Agregar archivo LICENSE (MIT License)
- [ ] Incluir copyright y año

#### .gitignore
- [ ] Verificar que ignora archivos temporales
- [ ] Incluir __pycache__/, *.pyc, *.deb, etc.

### 3. GitHub Repository

#### Creación del repositorio
- [ ] Crear repositorio en GitHub
- [ ] Configurar descripción: "Blue Light Filter for X Window System - Lightweight version with TUI"
- [ ] Agregar topics: `blue-light-filter`, `linux`, `python`, `x11`, `debian`, `tui`

#### Release v1.0.0
- [ ] Crear tag v1.0.0
- [ ] Crear release en GitHub
- [ ] Adjuntar paquete .deb
- [ ] Notas de release detalladas

## Criterios de Aceptación

- [ ] README.md completo y profesional
- [ ] LICENSE presente (MIT)
- [ ] Archivos temporales eliminados
- [ ] Repositorio GitHub creado y público
- [ ] Release v1.0.0 creado con .deb
- [ ] Todas las funcionalidades documentadas
- [ ] Tests passing (si existen)

## Out of Scope

- Nuevas funcionalidades de código
- CI/CD pipelines automatizados
- Documentación de API (no aplica)
- Traducciones a otros idiomas

## Notas

- Este es el track FINAL de lanzamiento
- No agregar features nuevas, solo documentación
- Mantener el scope mínimo para publicación

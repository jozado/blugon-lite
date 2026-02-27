# Plan de Implementación: github_release_20260227

## Fase 1: Limpieza del Repositorio

- [ ] **Task: Identificar y eliminar archivos temporales**
    - [ ] Listar todos los archivos .py en el root
    - [ ] Identificar scripts de prueba (test_*.py)
    - [ ] Eliminar test_sync_5min.py
    - [ ] Eliminar directorios __pycache__/
    - [ ] Eliminar archivos *.pyc

- [ ] **Task: Revisar archivos de documentación**
    - [ ] Leer ESTADO_ACTUAL.md y decidir si mantener o eliminar
    - [ ] Leer HALLAZGOS_Y_SOLUCIONES.md y mover a conductor/ si es relevante
    - [ ] Verificar Propuesta_TUI/ - archivar o eliminar
    - [ ] Revisar TUI-OPTIONS.txt - incorporar o eliminar

- [ ] **Task: Verificar .gitignore**
    - [ ] Leer .gitignore actual
    - [ ] Asegurar que ignora: __pycache__/, *.pyc, *.deb, *.log
    - [ ] Agregar entradas faltantes

- [ ] Task: Conductor - User Manual Verification 'Limpieza del Repositorio' (Protocol in workflow.md)

## Fase 2: Documentación Principal

- [ ] **Task: Actualizar README.md**
    - [ ] Revisar sección de características
    - [ ] Actualizar tabla comparativa si es necesario
    - [ ] Verificar instrucciones de instalación
    - [ ] Agregar captura de pantalla del TUI (Captura.png)
    - [ ] Revisar ejemplos de uso
    - [ ] Verificar enlaces de badges

- [ ] **Task: Actualizar INSTALL.md**
    - [ ] Verificar pasos de instalación
    - [ ] Actualizar dependencias si cambió
    - [ ] Agregar solución de problemas comunes
    - [ ] Probar instalación desde cero

- [ ] **Task: Crear LICENSE**
    - [ ] Redactar LICENSE MIT
    - [ ] Incluir copyright: "Copyright (c) 2026 Jose MS"
    - [ ] Guardar como LICENSE en root

- [ ] **Task: Revisar Makefile**
    - [ ] Verificar que todos los targets funcionan
    - [ ] Probar `make clean`
    - [ ] Probar `make build`
    - [ ] Probar `make install`

- [ ] Task: Conductor - User Manual Verification 'Documentación Principal' (Protocol in workflow.md)

## Fase 3: Preparación del Release

- [ ] **Task: Crear paquete .deb limpio**
    - [ ] Ejecutar `bash build-deb.sh`
    - [ ] Verificar que no incluye archivos de debug
    - [ ] Probar instalación en sistema limpio
    - [ ] Mover .deb a carpeta temporal para release

- [ ] **Task: Preparar notas de release**
    - [ ] Listar todas las features implementadas
    - [ ] Documentar cambios importantes
    - [ ] Incluir instrucciones de instalación
    - [ ] Mencionar known issues si existen

- [ ] **Task: Crear tag git**
    - [ ] `git tag -a v1.0.0 -m "Release inicial - Blue Light Filter con TUI"`
    - [ ] Verificar tag creado: `git tag -l`

- [ ] Task: Conductor - User Manual Verification 'Preparación del Release' (Protocol in workflow.md)

## Fase 4: Publicación en GitHub

- [ ] **Task: Crear repositorio en GitHub**
    - [ ] Ir a github.com/new
    - [ ] Nombre: blugon-lite
    - [ ] Descripción: "Blue Light Filter for X Window System - Lightweight version with TUI"
    - [ ] Visibility: Público
    - [ ] NO inicializar con README (ya tenemos uno)
    - [ ] Crear repositorio

- [ ] **Task: Configurar remote y subir código**
    - [ ] `git remote add origin https://github.com/tu-usuario/blugon-lite.git`
    - [ ] `git branch -M main`
    - [ ] `git push -u origin main`
    - [ ] Verificar subida en GitHub

- [ ] **Task: Crear Release en GitHub**
    - [ ] Ir a Releases > Create a new release
    - [ ] Tag version: v1.0.0
    - [ ] Release title: v1.0.0 - Initial Release
    - [ ] Pegar notas de release
    - [ ] Adjuntar blugon-lite_1.0.0-lite-amd64.deb
    - [ ] Marcar como "Latest release"
    - [ ] Publicar release

- [ ] **Task: Configurar repositorio**
    - [ ] Agregar topics: blue-light-filter, linux, python, x11, debian, tui
    - [ ] Configurar descripción corta
    - [ ] Verificar que LICENSE se muestra correctamente
    - [ ] Revisar vista pública del repositorio

- [ ] Task: Conductor - User Manual Verification 'Publicación en GitHub' (Protocol in workflow.md)

## Fase 5: Verificación Final

- [ ] **Task: Verificar repositorio público**
    - [ ] Abrir repositorio en modo incógnito
    - [ ] Verificar que README se ve correctamente
    - [ ] Verificar que LICENSE es visible
    - [ ] Verificar que Releases está accesible
    - [ ] Verificar que .deb se puede descargar

- [ ] **Task: Probar instalación desde release**
    - [ ] Descargar .deb desde GitHub Releases
    - [ ] Instalar en sistema limpio
    - [ ] Probar `blugon-lite --version`
    - [ ] Probar `blugon-lite-tui`
    - [ ] Verificar que funciona correctamente

- [ ] **Task: Documentar enlaces finales**
    - [ ] Anotar URL del repositorio
    - [ ] Anotar URL del release
    - [ ] Actualizar tracks.md con enlace
    - [ ] Marcar track como completado

- [ ] Task: Conductor - User Manual Verification 'Verificación Final' (Protocol in workflow.md)

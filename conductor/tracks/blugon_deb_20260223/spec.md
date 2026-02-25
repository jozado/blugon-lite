# Track Specification: blugon_deb_20260223

## Descripción

Crear un paquete .deb instalable para blugon-lite que incluya una TUI (Text User Interface) con urwid para configuración interactiva, auto-configuración con fallback automático, y múltiples configuraciones predefinidas.

**Objetivo final:** El usuario puede instalar con `sudo dpkg -i blugon-lite.deb` y usar inmediatamente sin configuración manual, además de tener una TUI intuitiva tipo htop para configurar horarios.

## Alcance

### Características a Implementar

1. **Auto-Configuración del Script** (Prioridad: ALTA)
   - El script buscará configuración en este orden:
     1. `~/.config/blugon/gamma` (config del usuario)
     2. `/usr/share/blugon-lite/configs/evening/gamma` (sistema)
     3. Fallback hardcodeado en el script

2. **TUI con urwid** (Prioridad: ALTA)
   - Interfaz de texto interactiva tipo htop
   - Navegación con flechas (↑↓)
   - Ver/editar horarios configurados
   - Agregar nuevos horarios
   - Eliminar horarios existentes
   - Guardar configuración
   - Mostrar estado del daemon
   - Atajos de teclado (s=guardar, q=salir, h=ayuda)

3. **Configuraciones Predefinidas** (Prioridad: MEDIA)
   - evening/gamma (mejorado, ya existe)
   - office/gamma (trabajador 9-5)
   - student/gamma (estudiante, horarios extendidos)
   - night-owl/gamma (nocturno)
   - minimal/gamma (solo 3 puntos)

4. **Paquete Debian** (Prioridad: ALTA, pero después de testing)
   - Estructura debian/ completa
   - Scripts postinst/prerm/postrm
   - Dependencias: python3, python3-urwid, libx11-6, libxrandr2
   - Instalación automática de configs por defecto

5. **Documentación Mejorada** (Prioridad: ALTA)
   - README con instrucciones de uso del TUI
   - INSTALL.md con instalación desde fuente
   - Man page actualizada
   - Ejemplos de diferentes casos de uso

### Características NO incluidas en este track

- GUI gráfica (zenity/kdialog) - futuro
- Script blugon-lite-config wizard - futuro
- Soporte para múltiples perfiles de usuario - futuro
- Systemd service management avanzado - futuro

## Requisitos Técnicos

### Código
- **blugon-lite.py**: < 250 líneas (después de agregar fallback)
- **blugon-lite-tui.py**: ~300-400 líneas estimadas
- **Python**: 3.6+ compatible
- **Dependencias Python**: urwid (para el TUI)

### Rendimiento
- **TUI RAM**: < 15MB adicional
- **Tiempo de inicio TUI**: < 1 segundo

### Compatibilidad
- **Debian/Ubuntu**: Paquetes .deb estándar
- **Archivos gamma existentes**: Deben funcionar sin modificaciones
- **blugon original**: Mantener compatibilidad de configs

## Entregables

### Código
1. **blugon-lite.py** (modificado con auto-config fallback)
2. **blugon-lite-tui** (wrapper bash ejecutable)
3. **blugon-lite-tui.py** (código Python + urwid)
4. **configs/evening/gamma** (mejorado con comentarios)
5. **configs/office/gamma** (nuevo)
6. **configs/student/gamma** (nuevo)
7. **configs/night-owl/gamma** (nuevo)
8. **configs/minimal/gamma** (nuevo)

### Paquete Debian
9. **debian/control** (metadatos, dependencias)
10. **debian/postinst** (script post-instalación)
11. **debian/prerm** (script pre-remoción)
12. **debian/postrm** (script post-remoción)
13. **debian/conffiles** (archivos de configuración)
14. **debian/blugon-lite.docs** (documentación a instalar)
15. **debian/blugon-lite.install** (archivos a instalar)
16. **debian/blugon-lite.maintscript** (migraciones)
17. **debian/compat**
18. **debian/source/format**

### Documentación
19. **README.md** (actualizado con TUI y .deb)
20. **INSTALL.md** (nuevo, instalación desde fuente)
21. **blugon-lite.1** (actualizado)

## Criterios de Aceptación

### Funcionalidad
- [ ] blugon-lite.py funciona sin ~/.config/blugon/gamma
- [ ] Fallback a config del sistema funciona
- [ ] Fallback hardcodeado funciona
- [ ] blugon-lite-tui es intuitivo y funcional
- [ ] Navegación con flechas funciona
- [ ] Edición de horarios es correcta
- [ ] Agregar/eliminar horarios funciona
- [ ] Guardado persiste cambios
- [ ] Múltiples configs predefinidas disponibles

### Paquete .deb
- [ ] sudo dpkg -i blugon-lite.deb funciona sin errores
- [ ] Dependencias se instalan automáticamente
- [ ] postinst crea configuración por defecto
- [ ] TUI se instala y funciona
- [ ] blugon-lite se instala y funciona
- [ ] Desinstalación limpia

### Documentación
- [ ] README explica cómo usar el TUI
- [ ] README explica cómo editar configs manualmente
- [ ] INSTALL.md tiene instalación paso a paso
- [ ] Ejemplos claros para diferentes casos de uso
- [ ] Man page actualizada

### Calidad de Código
- [ ] Código Python sigue PEP 8
- [ ] No hay código comentado innecesario
- [ ] Funciones documentadas con docstrings
- [ ] No hay dependencias innecesarias
- [ ] Testing manual completado

## Notas de Implementación

### Orden de Implementación CRÍTICO
1. Primero: Auto-configuración (Fase 1)
2. Segundo: TUI (Fase 2)
3. Tercero: Configuraciones predefinidas (Fase 3)
4. Cuarto: **Testing manual del conjunto** (Fase 4) ← ¡IMPORTANTE!
5. Quinto: Documentación (Fase 5)
6. Sexto: Paquete .deb (Fase 6) ← ¡Solo después de que todo funcione!

### Sobre urwid
- No incluir en requirements.txt (es dependencia del sistema)
- El .deb lo maneja via `Depends: python3-urwid`
- Usuario no necesita instalar manualmente

### Sobre postinst
- Debe ser idempotente (puede ejecutarse múltiples veces)
- No debe sobrescribir config del usuario si ya existe
- Debe manejar actualizaciones desde versiones previas

### Sobre el TUI
- Mantener simple pero funcional
- No sobrecargar con características innecesarias
- Priorizar usabilidad sobre features
- Probar en diferentes tamaños de terminal (mínimo 80x24)

### Sobre compatibilidad
- Mantener compatibilidad con configs de blugon original
- No romper API de línea de comandos existente
- blugon-lite.py debe seguir funcionando sin el TUI

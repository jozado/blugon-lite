# Track Specification: deb_issues_20260226

## Descripción

Resolver los issues críticos restantes en el paquete .deb de blugon-lite relacionados con:
- Restauración de gamma de pantalla al detener daemon
- Restauración de gamma al desinstalar
- Limpieza completa de autoinicio al desinstalar
- Mejoras de UX en el TUI

## Problemas a Resolver

### Issue #1: Restaurar gamma al detener daemon (TUI) - CRÍTICO
**Severity:** HIGH

**Problema:**
- Al presionar 's' (Detener) en el TUI, el daemon se detiene pero la pantalla NO se restaura
- El mensaje dice "Pantalla restaurada" pero es falso
- Los colores cálidos persisten hasta el reinicio

**Causa Raíz:**
- `blugon-lite --once` falla silenciosamente en el subprocess
- El fallback a xgamma no está implementado

**Solución Requerida:**
- Implementar fallback explícito usando `xgamma -gamma 1.0`
- Si xgamma falla, intentar con redshift-cli si está disponible
- Mostrar mensaje de error detallado si todo falla

### Issue #2: Restaurar gamma al desinstalar - CRÍTICO
**Severity:** HIGH

**Problema:**
- Al hacer `apt purge blugon-lite`, la pantalla queda con colores cálidos
- El usuario debe reiniciar el sistema para ver colores normales

**Solución Requerida:**
- Agregar `export DISPLAY=:0` en postrm
- Usar `xgamma -gamma 1.0` directamente como fallback
- Logging extensivo para debug

### Issue #3: Autoinicio no se elimina al desinstalar
**Severity:** MEDIUM

**Problema:**
- El archivo `/etc/xdg/autostart/blugon-lite.desktop` persiste después de desinstalar

**Solución Requerida:**
- Eliminar en `/etc/xdg/autostart/blugon-lite.desktop`
- Eliminar en `~/.config/autostart/blugon-lite.desktop` para cada usuario
- Logging para verificar que se ejecuta rm

### Issue #4: Mejorar TUI (UX, validaciones)
**Severity:** LOW

**Mejoras Requeridas:**
1. Validar que el daemon existe antes de mostrar "Activo"
2. Agregar confirmación antes de detener daemon (opcional)
3. Mostrar mensaje de error detallado si falla la restauración
4. Mejorar diseño del footer (reducir a 1 fila si es posible)

## Requisitos Técnicos

### Dependencias
- `xorg-xgamma` - Debe estar instalado para el fallback de gamma
- `python3-xlib` - Opcional, para verificación avanzada de X11

### Scripts Debian
- `postrm`: Debe restaurar gamma ANTES de eliminar archivos
- `postinst`: Debe verificar que xgamma está disponible

### TUI
- Función `restaurar_gamma()` en `tui/utils.py`:
  - Intentar `blugon-lite --once` primero
  - Fallback a `xgamma -gamma 1.0`
  - Logging de todos los intentos
  - Retornar éxito/fracaso para mostrar mensaje apropiado

## Criterios de Aceptación

### Issue #1 - Gamma en TUI
- [ ] Al presionar 's', la pantalla se restaura a 6500K inmediatamente
- [ ] Si falla, mostrar mensaje: "Error: No se pudo restaurar gamma. Ejecute 'xgamma -gamma 1.0' manualmente"
- [ ] Logging en `/tmp/blugon-tui-debug.log` muestra intentos

### Issue #2 - Gamma en postrm
- [ ] Al hacer `apt purge`, la pantalla se restaura
- [ ] Logging en `/tmp/blugon-postrm-debug.log` confirma restauración
- [ ] Funciona incluso si blugon-lite --once falla

### Issue #3 - Autoinicio
- [ ] `ls /etc/xdg/autostart/blugon-lite.desktop` retorna "No existe" después de purge
- [ ] `ls ~/.config/autostart/blugon-lite.desktop` retorna "No existe" después de purge

### Issue #4 - TUI UX
- [ ] Mensajes de error son informativos
- [ ] Footer es compacto y legible
- [ ] Validaciones previenen acciones inválidas

## Notas de Implementación

### Orden de Prioridad
1. Issue #1 (Gamma en TUI) - Más visible para el usuario
2. Issue #2 (Gamma en postrm) - Crítico para desinstalación limpia
3. Issue #3 (Autoinicio) - Menos crítico pero importante
4. Issue #4 (UX TUI) - Mejoras cosméticas

### Comandos de Verificación
```bash
# Probar restauración de gamma
xgamma -gamma 1.0 && echo "OK" || echo "FALLÓ"

# Probar blugon-lite --once
/usr/bin/blugon-lite --once && echo "OK" || echo "FALLÓ"

# Verificar DISPLAY
echo "DISPLAY=$DISPLAY"

# Después de desinstalar
ls /etc/xdg/autostart/blugon-lite.desktop  # Debe fallar
cat /tmp/blugon-postrm-debug.log  # Ver logs
```

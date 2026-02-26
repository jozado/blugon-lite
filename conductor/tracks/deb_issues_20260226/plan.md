# Track: Solucionar issues pendientes del deb

## Descripción

Resolver los issues críticos restantes en el paquete .deb de blugon-lite relacionados con:
- Restauración de gamma de pantalla
- Limpieza completa al desinstalar
- Mejoras de UX en el TUI

**Parent Track:** `deb_funcional_20260225`  
**Priority:** HIGH  
**Estado:** Pendiente - Esperando diagnóstico del usuario

---

## Issues a Resolver

### Issue #1: Restaurar gamma al detener daemon (TUI)
**Estado:** ⏳ Pendiente de diagnóstico  
**Severity:** HIGH

**Problema:**
- Al presionar 's' (Detener) en el TUI, el daemon se detiene pero la pantalla NO se restaura
- El mensaje dice "Pantalla restaurada" pero es falso
- Los colores cálidos persisten hasta el reinicio

**Causa Probable:**
- `blugon-lite --once` falla silenciosamente en el subprocess
- Problema de permisos X11 o DISPLAY no disponible

**Diagnóstico Requerido:**
El usuario debe ejecutar en su PC real:
```bash
/usr/bin/blugon-lite --once && echo "OK" || echo "FALLÓ"
xgamma -gamma 1.0 && echo "OK" || echo "FALLÓ"
echo "DISPLAY=$DISPLAY"
```

**Solución Propuesta:**
```python
# Usar xgamma directamente si blugon-lite falla
subprocess.run(['xgamma', '-gamma', '1.0'], capture_output=True)
```

---

### Issue #2: Restaurar gamma al desinstalar
**Estado:** ⏳ Pendiente  
**Severity:** HIGH

**Problema:**
- Al hacer `apt purge blugon-lite`, la pantalla queda con colores cálidos
- El usuario debe reiniciar el sistema para ver colores normales

**Causa Probable:**
- Mismo problema que Issue #1
- postrm no tiene acceso a DISPLAY

**Solución Propuesta:**
```bash
# postrm - purge
export DISPLAY=:0
xgamma -gamma 1.0 2>/dev/null || true
```

---

### Issue #3: Autoinicio no se elimina al desinstalar
**Estado:** ⏳ Pendiente  
**Severity:** MEDIUM

**Problema:**
- El archivo `/etc/xdg/autostart/blugon-lite.desktop` persiste después de desinstalar

**Causa Probable:**
- postrm no tiene permisos o la ruta es incorrecta
- El archivo se crea en `/etc/xdg/autostart/` pero no se elimina

**Verificación Requerida:**
```bash
# Después de desinstalar
ls -la /etc/xdg/autostart/blugon-lite.desktop
cat /tmp/blugon-postrm-debug.log
```

**Solución Propuesta:**
```bash
# postrm - purge
rm -f /etc/xdg/autostart/blugon-lite.desktop
rm -f ~/.config/autostart/blugon-lite.desktop
```

---

### Issue #4: Mejorar TUI (UX, validaciones)
**Estado:** ⏳ Pendiente  
**Severity:** LOW

**Mejoras Propuestas:**
1. Validar que el daemon existe antes de mostrar "Activo"
2. Agregar confirmación antes de detener daemon
3. Mostrar mensaje de error detallado si falla la restauración
4. Agregar atajo de teclado para salir sin guardar (si aplica)
5. Mejorar diseño del footer (2 filas puede ser mucho)

---

## Plan de Implementación

### Fase 1: Diagnóstico (PENDIENTE)
- [ ] Esperar salida de comandos de diagnóstico del usuario
- [ ] Analizar logs de `/tmp/blugon-tui-debug.log`
- [ ] Identificar causa exacta del fallo de gamma

### Fase 2: Solución Issue #1 (Gamma en TUI)
- [ ] Probar `xgamma -gamma 1.0` como fallback
- [ ] Actualizar `detener_daemon()` en `tui/app.py`
- [ ] Testear en VM
- [ ] Enviar paquete al usuario

### Fase 3: Solución Issue #2 (Gamma en postrm)
- [ ] Agregar `export DISPLAY=:0` en postrm
- [ ] Usar `xgamma` directamente
- [ ] Testear desinstalación completa

### Fase 4: Solución Issue #3 (Autoinicio)
- [ ] Verificar ruta correcta del archivo .desktop
- [ ] Agregar logging en postrm
- [ ] Eliminar en ambas ubicaciones (/etc/xdg y ~/.config)

### Fase 5: Mejoras TUI (Issue #4)
- [ ] Implementar mejoras de UX priorizadas
- [ ] Testear en VM
- [ ] Documentar cambios

---

## Archivos de Contexto

| Archivo | Propósito |
|---------|-----------|
| `DEBUG_SESSION.md` | Bitácora completa de depuración (2026-02-25) |
| `HALLAZGOS_Y_PROBLEMAS.md` | Problemas originales del track padre |
| `/tmp/blugon-tui-debug.log` | Logs del TUI (generado en runtime) |
| `/tmp/blugon-postrm-debug.log` | Logs de desinstalación |

---

## Criterios de Aceptación

- [ ] Al presionar 's' en el TUI, la pantalla se restaura a 6500K
- [ ] Al desinstalar, la pantalla se restaura automáticamente
- [ ] Al desinstalar, NO queda `/etc/xdg/autostart/blugon-lite.desktop`
- [ ] Mensajes de error son informativos y útiles
- [ ] Testing completado en VM y PC real del usuario

---

## Notas de Implementación

**IMPORTANTE:** Este track depende del diagnóstico del usuario. No se puede avanzar sin:
1. La salida de los comandos de diagnóstico
2. Confirmación de que `xgamma -gamma 1.0` funciona en su sistema

**Próxima Acción:** Esperar feedback del usuario con los logs.

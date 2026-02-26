# Track: Solucionar issues pendientes del deb

## Descripción

Resolver los issues críticos restantes en el paquete .deb de blugon-lite relacionados con:
- Restauración de gamma de pantalla
- Limpieza completa al desinstalar
- Mejoras de UX en el TUI

**Parent Track:** `deb_funcional_20260225`
**Priority:** HIGH
**Estado:** ✅ IMPLEMENTADO - Pendiente de verificación

---

## Issues a Resolver

### Issue #1: Restaurar gamma al detener daemon (TUI)
**Estado:** ✅ IMPLEMENTADO - Pendiente de verificación
**Severity:** HIGH

**Problema:**
- Al presionar 's' (Detener) en el TUI, el daemon se detiene pero la pantalla NO se restaura
- El mensaje dice "Pantalla restaurada" pero es falso
- Los colores cálidos persisten hasta el reinicio

**Solución Implementada:**
- Nueva función `restaurar_gamma()` en `tui/utils.py` con 3 métodos:
  1. `blugon-lite --once` (preferido)
  2. `xgamma -gamma 1.0` (fallback directo)
  3. `xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0` (fallback alternativo)
- Logging extensivo en `/tmp/blugon-tui-debug.log`
- `detener_daemon()` actualizada para usar la nueva función y mostrar mensaje apropiado

**Verificación Requerida:**
```bash
# 1. Iniciar daemon desde TUI (tecla 'i')
# 2. Presionar 's' para detener
# 3. Verificar que la pantalla se restaura a colores normales
# 4. Revisar logs: cat /tmp/blugon-tui-debug.log | grep "restaurar_gamma"
```

---

### Issue #2: Restaurar gamma al desinstalar
**Estado:** ✅ IMPLEMENTADO - Pendiente de verificación
**Severity:** HIGH

**Problema:**
- Al hacer `apt purge blugon-lite`, la pantalla queda con colores cálidos
- El usuario debe reiniciar el sistema para ver colores normales

**Solución Implementada:**
- Función `restaurar_gamma()` en `postrm` con mismos 3 métodos
- `export DISPLAY=:0` automático si no está definido
- Logging en `/tmp/blugon-postrm-debug.log`

**Verificación Requerida:**
```bash
# 1. Instalar paquete: sudo apt install ./blugon-lite_1.0.0-lite-amd64.deb
# 2. Iniciar daemon: blugon-lite --interval 120 &
# 3. Desinstalar: sudo apt purge blugon-lite
# 4. Verificar que la pantalla se restaura
# 5. Revisar logs: cat /tmp/blugon-postrm-debug.log
```

---

### Issue #3: Autoinicio no se elimina al desinstalar
**Estado:** ✅ IMPLEMENTADO - Pendiente de verificación
**Severity:** MEDIUM

**Problema:**
- El archivo `/etc/xdg/autostart/blugon-lite.desktop` persiste después de desinstalar

**Solución Implementada:**
- `postrm` ahora elimina en `/etc/xdg/autostart/blugon-lite.desktop`
- `postrm` elimina en `~/.config/autostart/blugon-lite.desktop` para cada usuario
- Logging de cada operación de eliminación

**Verificación Requerida:**
```bash
# Después de desinstalar con purge:
ls /etc/xdg/autostart/blugon-lite.desktop  # Debe decir "No existe"
ls ~/.config/autostart/blugon-lite.desktop  # Debe decir "No existe"
cat /tmp/blugon-postrm-debug.log | grep "Eliminado"
```

---

### Issue #4: Mejorar TUI (UX, validaciones)
**Estado:** ⏳ PENDIENTE
**Severity:** LOW

**Mejoras Propuestas:**
1. ✅ Mensajes de error detallados si falla la restauración (IMPLEMENTADO)
2. [ ] Validar que el daemon existe antes de mostrar "Activo" (ya existe)
3. [ ] Agregar confirmación antes de detener daemon (opcional)
4. [ ] Mejorar diseño del footer (reducir a 1 fila si es posible)

---

## Plan de Implementación

### Fase 1: Implementación ✅ COMPLETADA
- [x] Implementar `restaurar_gamma()` en `tui/utils.py`
- [x] Actualizar `detener_daemon()` en `tui/app.py`
- [x] Mejorar `postrm` con función `restaurar_gamma()`
- [x] Agregar limpieza de autoinicio en `postrm`
- [x] Agregar logging extensivo
- [x] Commit: `b28bc5b`

### Fase 2: Verificación ⏳ PENDIENTE
- [ ] Probar Issue #1: TUI restaura gamma al detener daemon
- [ ] Probar Issue #2: postrm restaura gamma al desinstalar
- [ ] Probar Issue #3: autoinicio se elimina al desinstalar
- [ ] Revisar logs de verificación

### Fase 3: Issue #4 (Mejoras TUI) ⏳ PENDIENTE
- [ ] Implementar mejoras de UX restantes
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

## Próximos Pasos

**ACCIÓN REQUERIDA:** Ejecutar pruebas de verificación en tu PC real:

1. **Instalar el nuevo paquete:**
   ```bash
   sudo apt install ./blugon-lite_1.0.0-lite-amd64.deb
   ```

2. **Probar Issue #1 (TUI):**
   ```bash
   blugon-lite-tui
   # Presionar 'i' para iniciar daemon
   # Esperar unos segundos
   # Presionar 's' para detener
   # ¿La pantalla se restaura a colores normales?
   ```

3. **Probar Issue #2 y #3 (Desinstalación):**
   ```bash
   sudo apt purge blugon-lite
   # ¿La pantalla se restaura?
   # Verificar: ls /etc/xdg/autostart/blugon-lite.desktop
   ```

4. **Enviar logs:**
   ```bash
   cat /tmp/blugon-tui-debug.log | grep -E "restaurar_gamma|xgamma|blugon-lite --once"
   cat /tmp/blugon-postrm-debug.log
   ```

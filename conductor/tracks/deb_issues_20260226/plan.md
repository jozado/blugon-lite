# Track: Solucionar issues pendientes del deb

## Descripción

Resolver los issues críticos restantes en el paquete .deb de blugon-lite relacionados con:
- Restauración de gamma de pantalla
- Limpieza completa al desinstalar
- Mejoras de UX en el TUI

**Parent Track:** `deb_funcional_20260225`
**Priority:** HIGH
**Estado:** ✅ IMPLEMENTADO - Listo para testing final

---

## Issues a Resolver

### Issue #1: Restaurar gamma al detener daemon (TUI)
**Estado:** ✅ IMPLEMENTADO - Listo para testing
**Severity:** HIGH

**Problema:**
- Al presionar 's' (Detener) en el TUI, el daemon se detiene pero la pantalla NO se restaura
- Los colores cálidos persisten hasta el reinicio

**Causa Raíz Identificada:**
- `xgamma` necesita acceso al TTY para funcionar
- `capture_output=True` en subprocess pierde el acceso al TTY
- El código reportaba éxito pero la pantalla no se restauraba

**Solución Implementada:**
- Función `restaurar_gamma()` en `tui/utils.py` usa `with open('/dev/tty', 'w') as tty`
- Esto da acceso directo al TTY para que `xgamma` funcione
- Logging extensivo en `/tmp/blugon-tui-debug.log`

**Verificación:**
- Script de prueba confirmó: gamma cálido aplicado → pantalla restaurada correctamente
- Commit: `a1f2d9a`

---

### Issue #2: Restaurar gamma al desinstalar
**Estado:** ✅ IMPLEMENTADO - Listo para testing
**Severity:** HIGH

**Problema:**
- Al hacer `apt purge blugon-lite`, la pantalla queda con colores cálidos

**Solución Implementada:**
- Función `restaurar_gamma()` en `postrm` usa `< /dev/tty > /dev/tty`
- `export DISPLAY=:0` automático si no está definido
- Logging en `/tmp/blugon-postrm-debug.log`

---

### Issue #3: Autoinicio no se elimina al desinstalar
**Estado:** ✅ IMPLEMENTADO - Listo para testing
**Severity:** MEDIUM

**Problema:**
- El archivo `/etc/xdg/autostart/blugon-lite.desktop` persiste después de desinstalar
- Directorios `/usr/lib/blugon-lite/tui/widgets` y `modals` no se eliminan

**Solución Implementada:**
- `postrm` elimina en `/etc/xdg/autostart/blugon-lite.desktop`
- `postrm` elimina en `~/.config/autostart/blugon-lite.desktop` para cada usuario
- `postrm` limpia directorios `tui/widgets`, `tui/modals`, `tui` con `rmdir`

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
- [x] Identificar causa raíz: xgamma necesita TTY
- [x] Implementar `restaurar_gamma()` en `tui/utils.py` con `open('/dev/tty')`
- [x] Implementar `restaurar_gamma()` en `postrm` con `< /dev/tty > /dev/tty`
- [x] Agregar limpieza de autoinicio en `postrm`
- [x] Agregar limpieza de directorios en `postrm`
- [x] Agregar logging extensivo
- [x] Verificar con script de prueba
- [x] Commit: `a1f2d9a`

### Fase 2: Testing Final ⏳ PENDIENTE
- [ ] Instalar paquete: `sudo apt install ./blugon-lite_1.0.0-lite-amd64.deb`
- [ ] Probar Issue #1: TUI restaura gamma al detener daemon
- [ ] Probar Issue #2: postrm restaura gamma al desinstalar
- [ ] Probar Issue #3: autoinicio y directorios se eliminan
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
- [ ] Al desinstalar, se eliminan directorios `/usr/lib/blugon-lite/tui/*`
- [ ] Mensajes de error son informativos y útiles
- [ ] Testing completado en PC real del usuario

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
   # Verificar: ls /etc/xdg/autostart/blugon-lite.desktop  # Debe decir "No existe"
   # Verificar: ls /usr/lib/blugon-lite/tui/  # Debe estar vacío o no existir
   ```

4. **Enviar logs:**
   ```bash
   cat /tmp/blugon-tui-debug.log | grep -E "restaurar_gamma|xgamma|/dev/tty"
   cat /tmp/blugon-postrm-debug.log
   ```

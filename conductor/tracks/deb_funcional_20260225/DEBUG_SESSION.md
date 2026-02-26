# Sesión de Depuración - blugon-lite TUI Daemon Issues

**Fecha:** 2026-02-25  
**Estado:** En progreso - Esperando diagnóstico del usuario  
**Track Padre:** deb_funcional_20260225 - Crear deb funcional

---

## 🎯 Objetivo Principal

Lograr que el paquete .deb de blugon-lite:
1. ✅ Se instale correctamente
2. ✅ Se desinstale limpiamente (sin colgarse)
3. ✅ Restaure los colores de pantalla al desinstalar
4. ✅ El TUI muestre correctamente el estado del daemon
5. ✅ Los controles del daemon (Iniciar/Detener/Refrescar) funcionen correctamente

---

## 📋 Issues Detectados

### Issue #1: TUI no mostraba el estado real del daemon ✅ RESUELTO
**Problema:** El header del TUI siempre mostraba `[●] Daemon: Activo` aunque el daemon estuviera detenido.

**Causa Raíz:** `is_daemon_running()` buscaba múltiples patrones (`blugon-lite`, `blugon-lite.py`, `blugon-lite --interval`) y encontraba procesos del TUI u otros, no solo el daemon.

**Solución Aplicada:**
- Modificado `tui/utils.py` para buscar solo `blugon-lite --interval`
- Agregado logging extensivo en `/tmp/blugon-tui-debug.log`

**Estado:** ✅ RESUELTO - El header ahora muestra correctamente Activo/Inactivo

---

### Issue #2: Botón 's' (Detener) no restaura la pantalla ⏳ PENDIENTE
**Problema:** Al presionar 's' en el TUI:
- El daemon se detiene correctamente ✅
- La pantalla NO se restaura a colores normales ❌
- Mensaje muestra "Daemon detenido - Pantalla restaurada" pero es falso

**Código Actual:**
```python
# tui/app.py - detener_daemon()
subprocess.run(['/usr/bin/blugon-lite', '--once'], capture_output=True, text=True)
```

**Posibles Causas:**
1. `blugon-lite --once` falla silenciosamente (stderr capturado)
2. Problema de permisos X11
3. DISPLAY no está disponible en el contexto del subprocess
4. El backend scg falla y xgamma tampoco funciona

**Diagnóstico Pendiente:**
El usuario debe ejecutar estos comandos en su PC real:
```bash
# 1. Probar blugon-lite --once manualmente
/usr/bin/blugon-lite --once
echo "Exit code: $?"

# 2. Ver errores
/usr/bin/blugon-lite --once 2>&1

# 3. Probar xgamma directamente
xgamma -gamma 1.0 2>&1

# 4. Verificar DISPLAY
echo "DISPLAY=$DISPLAY"

# 5. Verificar permisos X11
xgamma -query 2>&1
```

**Próximos Pasos:**
1. Esperar salida de comandos de diagnóstico
2. Si `blugon-lite --once` falla, usar `xgamma -gamma 1.0` directamente
3. Agregar fallback explícito a xgamma en detener_daemon()

---

### Issue #3: Desinstalación no restaura colores ⏳ PENDIENTE
**Problema:** Al desinstalar el paquete:
- Los colores NO se restauran
- El usuario debe reiniciar el sistema para ver colores normales

**Código Actual:**
```bash
# debian/DEBIAN/postrm - purge
/usr/bin/blugon-lite --once >> "$LOGFILE" 2>&1
```

**Posible Causa:** Mismo problema que Issue #2 - `blugon-lite --once` falla en el contexto del script postrm.

**Solución Propuesta:**
```bash
# Intentar con xgamma directamente si blugon-lite falla
if ! /usr/bin/blugon-lite --once; then
    xgamma -gamma 1.0 2>/dev/null || true
fi
```

---

### Issue #4: Autoinicio no se elimina al desinstalar ⏳ PENDIENTE
**Problema:** El archivo `/etc/xdg/autostart/blugon-lite.desktop` persiste después de desinstalar.

**Código Actual:**
```bash
# debian/DEBIAN/postrm - purge
if [ -f /etc/xdg/autostart/blugon-lite.desktop ]; then
    rm -f /etc/xdg/autostart/blugon-lite.desktop
fi
```

**Posible Causa:** El archivo está en `/etc/xdg/autostart/` pero el postrm no tiene permisos o la ruta es incorrecta.

**Verificación Requerida:**
```bash
# Después de desinstalar, verificar:
ls -la /etc/xdg/autostart/blugon-lite.desktop
cat /tmp/blugon-postrm-debug.log
```

---

### Issue #5: Agregar función "Refrescar" al TUI ✅ PARCIALMENTE RESUELTO
**Problema:** El usuario necesita una forma de actualizar manualmente el estado del daemon.

**Solución Aplicada:**
- Agregado botón `[r] Refrescar` en el footer
- Función `refrescar_estado()` que llama a `is_daemon_running()` y actualiza el header

**Estado:** ✅ IMPLEMENTADO - Funciona correctamente según logs

---

## 🔧 Métodos de Depuración Utilizados

### 1. Logging Extenso en Python
```python
import logging
logging.basicConfig(filename='/tmp/blugon-tui-debug.log', level=logging.DEBUG)
logging.debug(f"variable = {value}")
```

**Ventajas:**
- Permite ver el flujo de ejecución
- Muestra valores de variables en tiempo real
- Los logs persisten después de cerrar el TUI

**Archivos de Log:**
- `/tmp/blugon-tui-debug.log` - Logs del TUI
- `/tmp/blugon-prerm-debug.log` - Logs de pre-remoción
- `/tmp/blugon-postrm-debug.log` - Logs de post-remoción
- `/tmp/blugon-lite-${USER}.log` - Logs del daemon

### 2. Logging en Scripts Bash
```bash
LOGFILE="/tmp/blugon-debug.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Mensaje" >> "$LOGFILE"
command >> "$LOGFILE" 2>&1
```

### 3. subprocess.run con capture_output
```python
result = subprocess.run(['command', 'arg'], capture_output=True, text=True)
logging.debug(f"returncode: {result.returncode}")
logging.debug(f"stdout: {result.stdout}")
logging.debug(f"stderr: {result.stderr}")
```

**Ventaja:** Captura tanto stdout como stderr para diagnóstico.

### 4. Verificación con pgrep/pkill
```bash
pgrep -f 'pattern'
echo "Exit code: $?"  # 0 = encontrado, 1 = no encontrado
```

---

## 📁 Archivos Modificados

| Archivo | Cambios | Estado |
|---------|---------|--------|
| `tui/utils.py` | `is_daemon_running()` busca solo `blugon-lite --interval` | ✅ Completado |
| `tui/app.py` | Agregadas funciones `iniciar_daemon()`, `detener_daemon()`, `refrescar_estado()` | ✅ Completado |
| `tui/app.py` | Footer con 2 filas de botones | ✅ Completado |
| `tui/app.py` | Logging extensivo en funciones del daemon | ✅ Completado |
| `debian/DEBIAN/postrm` | Restaurar gamma con logging | ⏳ Pendiente verificar |
| `debian/DEBIAN/postinst` | Copiar autostart a /etc/xdg/autostart/ | ✅ Completado |
| `blugon-lite-autostart.desktop` | Exec con ruta absoluta | ✅ Completado |
| `blugon-lite-autostart.sh` | Script de autostart con logging | ✅ Completado |
| `blugon-lite.py` | Logging del daemon | ✅ Completado |
| `blugon-lite-monitor` | Script de monitoring | ✅ Completado |

---

## 🧪 Comandos de Verificación

### Para el Usuario Ejecutar en PC Real

```bash
# === DIAGNÓSTICO DEL PROBLEMA DE GAMMA ===

# 1. ¿Funciona blugon-lite --once?
/usr/bin/blugon-lite --once
echo "Exit code: $?"

# 2. Ver errores de blugon-lite
/usr/bin/blugon-lite --once 2>&1

# 3. ¿Funciona xgamma?
xgamma -gamma 1.0 2>&1
echo "Exit code: $?"

# 4. Verificar DISPLAY
echo "DISPLAY=$DISPLAY"

# 5. Verificar permisos X11
xgamma -query 2>&1

# 6. Después de usar TUI, verificar logs
cat /tmp/blugon-tui-debug.log | grep -E "restore|Gamma|xgamma|returncode"

# 7. Verificar si el autoinicio persiste
ls -la /etc/xdg/autostart/blugon-lite.desktop

# 8. Ver logs de postrm después de desinstalar
cat /tmp/blugon-postrm-debug.log
```

---

## 📝 Próximos Pasos (Para Continuar Mañana)

### Prioridad 1: Diagnosticar Issue #2 (Gamma no se restaura)
1. [ ] Esperar salida de comandos de diagnóstico del usuario
2. [ ] Si `blugon-lite --once` falla, investigar por qué
3. [ ] Posible solución: Usar `xgamma -gamma 1.0` directamente
4. [ ] Testear en VM primero

### Prioridad 2: Verificar Issue #4 (Autoinicio persiste)
1. [ ] Verificar si postrm tiene permisos para borrar en /etc/xdg/
2. [ ] Agregar logging para ver si el rm se ejecuta
3. [ ] Testear desinstalación completa

### Prioridad 3: Reconstruir y Testear
1. [ ] Reconstruir paquete .deb
2. [ ] Testear en VM
3. [ ] Enviar a usuario para test en PC real

---

## 💡 Lecciones Aprendidas

1. **Nunca capturar stderr sin loguearlo** - Los errores silenciosos son imposibles de debuggear.

2. **El contexto de ejecución importa** - Un comando que funciona en la terminal puede fallar en:
   - subprocess de Python
   - Scripts de mantenimiento de dpkg (prerm/postrm)
   - Autoinicio de XFCE

3. **X11 requiere DISPLAY** - Los procesos que necesitan acceder a X11 deben tener la variable DISPLAY configurada.

4. **Logging > Suposiciones** - Siempre agregar logging extensivo antes de asumir qué está pasando.

5. **El usuario es el mejor tester** - Lo que funciona en la VM puede fallar en hardware real.

---

## 🔗 Referencias

- Track Plan: `conductor/tracks/deb_funcional_20260225/plan.md`
- Logs del TUI: `/tmp/blugon-tui-debug.log`
- Logs del daemon: `/tmp/blugon-lite-${USER}.log`
- Logs de desinstalación: `/tmp/blugon-prerm-debug.log`, `/tmp/blugon-postrm-debug.log`

---

**Última Actualización:** 2026-02-25 00:53  
**Próxima Acción:** Esperar diagnóstico del usuario (comandos de la sección "Issue #2")

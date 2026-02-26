# Plan: Gamma no se restaura en TUI y postrm

## Estado: 🔴 EN INVESTIGACIÓN

---

## Problema Confirmado

- **Síntoma:** `xgamma` reporta éxito pero la pantalla sigue cálida
- **Ocurre en:** TUI (al detener daemon) y postrm (al desinstalar)
- **Usuario confirmó:** "No funciona, ya lo desinstalé y sigue coloreada"

---

## Tareas Pendientes

### 1. Diagnóstico del problema de TTY
- [ ] Verificar si `open('/dev/tty', 'w')` funciona correctamente
- [ ] Probar alternativa con `os.system()` o `subprocess.Popen()`
- [ ] Verificar permisos de X11 para root (postrm)

### 2. Probar solución alternativa
- [ ] Intentar con `xgamma` sin redirección de TTY
- [ ] Probar ejecutar `xgamma` como usuario (no root) en postrm
- [ ] Considerar usar `xrandr` como alternativa

### 3. Implementar solución
- [ ] Actualizar `tui/utils.py` con solución verificada
- [ ] Actualizar `postrm` con solución verificada
- [ ] Agregar logging mejorado para diagnóstico

### 4. Verificación
- [ ] Probar en PC del usuario
- [ ] Confirmar que la pantalla se restaura VISIBILMENTE
- [ ] Revisar logs

---

## Hipótesis a Verificar

### Hipótesis 1: `open('/dev/tty', 'w')` no es suficiente
Posible solución: Usar `subprocess.Popen()` sin capturar output

### Hipótesis 2: postrm necesita ejecutar como usuario
Posible solución: Detectar usuario de sesión X11 y ejecutar `sudo -u $USER`

### Hipótesis 3: El problema es otro
Necesitamos más diagnóstico del usuario

---

## Próxima Acción

**ESPERANDO:** Que el usuario ejecute comandos de diagnóstico para entender por qué `xgamma` no funciona desde el código pero sí desde la terminal.

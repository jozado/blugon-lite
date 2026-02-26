# Plan: Gamma no se restaura en TUI y postrm

## Estado: ✅ IMPLEMENTADO - Pendiente de verificación

---

## Problema Confirmado

- **Síntoma:** `xgamma` reporta éxito pero la pantalla sigue cálida
- **Ocurre en:** TUI (al detener daemon) y postrm (al desinstalar)
- **Usuario confirmó:** "No funciona, ya lo desinstalé y sigue coloreada"

---

## Causa Raíz Identificada

### TUI
- `open('/dev/tty', 'w')` + `subprocess.run()` no heredaba correctamente el TTY
- El subprocess no tenía acceso real al TTY de la terminal padre

### postrm
- postrm se ejecuta como **root**
- La sesión X11 pertenece al **usuario**
- `xgamma` necesita ejecutarse como el usuario propietario de la sesión X11

---

## Soluciones Implementadas

### TUI - `tui/utils.py`
```python
# Usar os.system() para heredar el TTY automáticamente
result = os.system('xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0')
```

### postrm - `debian/DEBIAN/postrm`
```bash
# Detectar usuario de la sesión X11
XUSER=$(who | grep ':0' | awk '{print $1}' | head -1)

# Ejecutar xgamma como ese usuario
su "$XUSER" -c "xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0"
```

---

## Tareas

### 1. Implementar solución TUI ✅ COMPLETADA
- [x] Cambiar `subprocess.run()` a `os.system()`
- [x] Logging mantenido

### 2. Implementar solución postrm ✅ COMPLETADA
- [x] Detectar usuario de sesión X11
- [x] Ejecutar `xgamma` como ese usuario con `su`
- [x] Logging mantenido

### 3. Reconstruir paquete ✅ COMPLETADA
- [x] Ejecutar `bash build-deb.sh`
- [x] Paquete: `blugon-lite_1.0.0-lite-amd64.deb`

### 4. Testing ⏳ PENDIENTE
- [ ] Instalar paquete
- [ ] Probar TUI: iniciar daemon → detener → ¿pantalla se restaura?
- [ ] Probar postrm: `apt purge` → ¿pantalla se restaura?
- [ ] Revisar logs

---

## Próxima Acción

**TESTING REQUERIDO:** Que el usuario pruebe el paquete en su PC real:

```bash
# 1. Instalar
sudo apt install ./blugon-lite_1.0.0-lite-amd64.deb

# 2. Probar TUI
blugon-lite-tui
# 'i' = iniciar, 's' = detener
# ¿La pantalla se restaura al detener?

# 3. Probar desinstalación
sudo apt purge blugon-lite
# ¿La pantalla se restaura?
```

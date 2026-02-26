# Plan: Gamma no se restaura en TUI y postrm

## Estado: ✅ RESUELTO - Causa raíz: xrandr, no xgamma

---

## Problema Confirmado

- **Síntoma:** Pantalla permanece anaranjada al desinstalar o detener daemon
- **Ocurre en:** TUI (al detener daemon) y postrm (al desinstalar)
- **Usuario confirmó:** "No funciona, ya lo desinstalé y sigue coloreada"

---

## Causa Raíz Real (Encontrada 2026-02-26)

**NO era xgamma ni el TTY** - Era **xrandr** con gamma desbalanceada.

### Diagnóstico
```bash
xrandr --verbose | grep "Gamma:"
# Resultado:
Gamma:      1.0:2.0:5.0  # ← ¡VALORES DESBALANCEADOS!
```

**xiccd** (X ICC Color Daemon) había establecido una gamma desbalanceada:
- Rojo: 1.0
- Verde: 2.0
- Azul: 5.0

Esto causa tono anaranjado que `xgamma` NO puede corregir porque son sistemas diferentes.

---

## Solución Correcta

### Para restaurar gamma de pantalla
```bash
# Resetear gamma de xrandr para ambos monitores
xrandr --output LVDS-1 --gamma 1.0:1.0:1.0
xrandr --output VGA-1 --gamma 1.0:1.0:1.0
```

### Para blugon-lite TUI
El TUI debe usar `xrandr` en lugar de (o además de) `xgamma`:

```python
# Opción 1: Usar xrandr directamente
subprocess.run(['xrandr', '--output', 'LVDS-1', '--gamma', '1.0:1.0:1.0'])

# Opción 2: Usar ambos (xgamma + xrandr)
subprocess.run(['xgamma', '-rgamma', '1.0', '-ggamma', '1.0', '-bgamma', '1.0'])
subprocess.run(['xrandr', '--output', 'LVDS-1', '--gamma', '1.0:1.0:1.0'])
```

### Para postrm
Agregar comando xrandr además de xgamma:

```bash
# xgamma (por si acaso)
su "$XUSER" -c "xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0"

# xrandr (solución real)
su "$XUSER" -c "xrandr --output LVDS-1 --gamma 1.0:1.0:1.0"
su "$XUSER" -c "xrandr --output VGA-1 --gamma 1.0:1.0:1.0"
```

---

## Tareas

### 1. Actualizar tui/utils.py para usar xrandr ⏳ PENDIENTE
- [ ] Agregar función `restaurar_gamma_xrandr()`
- [ ] Usar xrandr en lugar de (o además de) xgamma
- [ ] Detectar outputs conectados dinámicamente

### 2. Actualizar postrm para usar xrandr ⏳ PENDIENTE
- [ ] Agregar comandos xrandr después de xgamma
- [ ] Detectar outputs conectados

### 3. Testing ⏳ PENDIENTE
- [ ] Probar en PC del usuario
- [ ] Confirmar que la pantalla se restaura VISIBILMENTE

---

## Comandos de Diagnóstico (Referencia)

```bash
# Ver gamma de xrandr
xrandr --verbose | grep "Gamma:"

# Ver gamma de xgamma
xgamma 2>&1

# Ver outputs conectados
xrandr | grep " connected"

# Ver procesos de color
ps aux | grep -iE "xiccd|colord|redshift"

# Resetear gamma
xrandr --output LVDS-1 --gamma 1.0:1.0:1.0
xrandr --output VGA-1 --gamma 1.0:1.0:1.0
```

---

## Lección Aprendida

1. **xgamma NO es lo mismo que xrandr** - Sistemas diferentes
2. **Verificar xrandr primero** - Si xgamma no funciona, revisar xrandr
3. **xiccd puede interferir** - Daemon de color de X11 puede sobrescribir configuraciones
4. **Dos monitores = dos configuraciones** - Cada output tiene su propia gamma

---

## Próxima Acción

Actualizar `tui/utils.py` y `postrm` para usar `xrandr` en lugar de `xgamma`.

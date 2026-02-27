# Plan: Gamma no se restaura en TUI y postrm

## Estado: ✅ COMPLETADO - VERIFICADO POR USUARIO

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

## Solución Implementada y Verificada

### Para restaurar gamma de pantalla
```bash
# Resetear gamma de xrandr para ambos monitores
xrandr --output LVDS-1 --gamma 1.0:1.0:1.0
xrandr --output VGA-1 --gamma 1.0:1.0:1.0
```

### Para blugon-lite TUI ✅ IMPLEMENTADO
`tui/utils.py` usa `xrandr` para restaurar gamma:
```python
# Detectar outputs conectados
outputs = subprocess.run(['xrandr', '--query'], capture_output=True, text=True)
# Para cada output conectado:
subprocess.run(['xrandr', '--output', output, '--gamma', '1.0:1.0:1.0'])
```

### Para postrm ✅ IMPLEMENTADO
`debian/DEBIAN/postrm` usa `xrandr` además de `xgamma`:
```bash
# Detectar outputs
OUTPUTS=$(xrandr --query | grep " connected" | cut -d" " -f1)
# Para cada output, restaurar gamma como usuario X11
su "$XUSER" -c "xrandr --output $output --gamma 1.0:1.0:1.0"
```

---

## Tareas

### 1. Actualizar tui/utils.py para usar xrandr ✅ COMPLETADA
- [x] Agregar detección de outputs conectados
- [x] Usar xrandr --output --gamma 1.0:1.0:1.0
- [x] Fallback a xgamma si xrandr falla

### 2. Actualizar postrm para usar xrandr ✅ COMPLETADA
- [x] Agregar comandos xrandr para cada output
- [x] Ejecutar como usuario X11 con su
- [x] Logging de cada operación

### 3. Testing ✅ COMPLETADO - VERIFICADO POR USUARIO
- [x] Probar TUI: iniciar daemon → detener → ✅ pantalla se restaura
- [x] Probar postrm: `apt purge` → ✅ pantalla se restaura
- [x] Usuario confirmó: "Ya funciona amigo! lo lograste al fin"

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
2. **SCG usa Xrandr** - Backend principal usa `XRRSetCrtcGamma()`
3. **Para restaurar, usar el mismo sistema** - Si SCG usa Xrandr, restaurar con Xrandr
4. **Verificar xrandr primero** - Si xgamma no funciona, revisar xrandr
5. **xiccd puede interferir** - Daemon de color de X11 puede sobrescribir configuraciones
6. **Dos monitores = dos configuraciones** - Cada output tiene su propia gamma

---

## Commits Relacionados

- `8dd3270` - fix(gamma): Usar xrandr en lugar de xgamma para restaurar gamma
- `4f5d3fb` - docs: Actualizar HALLAZGOS con arquitectura de backends
- `839e87a` - docs(plan): Actualizar subtrack gamma con causa raíz real - xrandr

---

## Resultado Final

✅ **TUI**: Al detener daemon, pantalla se restaura correctamente
✅ **postrm**: Al desinstalar con `apt purge`, pantalla se restaura correctamente
✅ **cleanup**: Directorios `/usr/lib/blugon-lite` se eliminan completamente

**Usuario confirmó:** "Ya funciona amigo! lo lograste al fin, ahora lo desinstale y tambien cambio los colores a como estaba al inicio!"

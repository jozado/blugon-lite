# Hallazgos y Soluciones del Proyecto blugon-lite

Este documento recopila problemas encontrados y sus soluciones para referencia futura.

---

## 2026-02-26: Gamma no se restaura - Era xrandr, no xgamma

### Problema
Al desinstalar blugon-lite o detener el daemon en el TUI, la pantalla permanecía con tono anaranjado/cálido a pesar de que:
- `xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0` se ejecutaba exitosamente
- Los logs reportaban éxito
- No había procesos de blugon-lite corriendo

### Diagnóstico
```bash
# Ver gamma actual de xrandr
xrandr --verbose | grep "Gamma:"

# Resultado:
Gamma:      1.0:2.0:5.0  # ← ¡VALORES DESBALANCEADOS!
Gamma:      1.0:1.0:1.0
```

### Causa Raíz
**xiccd** (X ICC Color Daemon) estaba corriendo en el fondo y había establecido una gamma desbalanceada en xrandr:
- Rojo: 1.0
- Verde: 2.0
- Azul: 5.0

Esto causaba un tono anaranjado/rojizo que `xgamma` NO podía corregir porque xgamma y xrandr son sistemas diferentes.

### Solución
```bash
# Resetear gamma de xrandr para ambos monitores
xrandr --output LVDS-1 --gamma 1.0:1.0:1.0
xrandr --output VGA-1 --gamma 1.0:1.0:1.0

# O alternativamente
xrandr --auto
```

### Comandos de Diagnóstico
```bash
# Verificar gamma de xrandr
xrandr --verbose | grep "Gamma:"

# Verificar gamma de xgamma
xgamma 2>&1

# Ver procesos de gestión de color
ps aux | grep -iE "xiccd|colord|redshift"

# Ver outputs conectados
xrandr | grep " connected"
```

### Lección Aprendida
1. **xgamma NO es lo mismo que xrandr** - Son sistemas diferentes de control de color
2. **Verificar xrandr primero** - Si xgamma no funciona, revisar xrandr
3. **xiccd puede interferir** - El daemon de color de X11 puede sobrescribir configuraciones
4. **Dos monitores = dos configuraciones** - Cada output tiene su propia gamma

### Referencia Rápida
```bash
# Si la pantalla está anaranjada/rojiza y xgamma no funciona:
xrandr --output LVDS-1 --gamma 1.0:1.0:1.0
xrandr --output VGA-1 --gamma 1.0:1.0:1.0

# Verificar que funcionó
xrandr --verbose | grep "Gamma:"  # Debe mostrar 1.0:1.0:1.0 en ambos
```

---

## 2026-02-26: postrm no elimina directorios con __pycache__

### Problema
Al hacer `apt purge blugon-lite`, los directorios `/usr/lib/blugon-lite/tui/widgets` y `modals` no se eliminaban.

### Causa
`rmdir` solo elimina directorios vacíos. Los directorios contenían archivos `__pycache__/` generados por Python.

### Solución
En `debian/DEBIAN/postrm`, usar `rm -rf` en lugar de `rmdir`:

```bash
# Limpiar directorio /usr/lib/blugon-lite recursivamente (purge debe eliminar TODO)
if [ -d /usr/lib/blugon-lite ]; then
    rm -rf /usr/lib/blugon-lite >> "$LOGFILE" 2>&1 && \
        echo "Eliminado /usr/lib/blugon-lite recursivamente" >> "$LOGFILE" || \
        echo "ERROR al eliminar /usr/lib/blugon-lite" >> "$LOGFILE"
fi
```

### Lección Aprendida
- `rmdir` = solo directorios vacíos
- `rm -rf` = elimina recursivamente (usar con cuidado, pero apropiado para purge)

---

## 2026-02-26: postrm necesita ejecutar xgamma como usuario, no como root

### Problema
postrm se ejecuta como root pero la sesión X11 pertenece al usuario. `xgamma` fallaba al ejecutarse como root.

### Solución
En `debian/DEBIAN/postrm`, detectar el usuario de la sesión X11 y ejecutar como ese usuario:

```bash
# Obtener usuario propietario de la sesión X11
XUSER=$(who | grep ':0' | awk '{print $1}' | head -1)

# Ejecutar xgamma como ese usuario
su "$XUSER" -c "xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0"
```

### Lección Aprendida
- Los comandos que interactúan con X11 deben ejecutarse como el usuario propietario de la sesión
- `who | grep ':0'` permite detectar el usuario de la sesión gráfica

---

## 2026-02-26: subprocess.run() con capture_output pierde el TTY

### Problema
Al usar `subprocess.run(['xgamma', ...], capture_output=True)` desde Python, xgamma reportaba éxito pero no modificaba la pantalla.

### Causa
`capture_output=True` captura stdin/stdout/stderr y pierde el acceso al TTY real que xgamma necesita.

### Solución
Usar `subprocess.run()` sin `capture_output`, heredando los file descriptors directamente:

```python
# CORRECTO: Hereda stdin/stdout/stderr del proceso padre
result = subprocess.run(
    ['xgamma', '-rgamma', '1.0', '-ggamma', '1.0', '-bgamma', '1.0'],
    timeout=5
)

# INCORRECTO: Captura y pierde el TTY
result = subprocess.run(
    ['xgamma', '-rgamma', '1.0', '-ggamma', '1.0', '-bgamma', '1.0'],
    capture_output=True,  # ← NO USAR
    text=True
)
```

### Lección Aprendida
- `xgamma` necesita acceso al TTY para funcionar
- No usar `capture_output=True` con comandos que requieren TTY
- `subprocess.run()` sin argumentos adicionales hereda stdin/stdout/stderr

---

## Comandos Útiles de Diagnóstico

### Ver gamma actual
```bash
xgamma 2>&1                    # Gamma de xgamma
xrandr --verbose | grep Gamma  # Gamma de xrandr por monitor
```

### Ver procesos relevantes
```bash
ps aux | grep -iE "blugon|xiccd|colord|redshift|gamma"
```

### Resetear gamma
```bash
# Método 1: xgamma
xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0

# Método 2: xrandr (si xgamma no funciona)
xrandr --output LVDS-1 --gamma 1.0:1.0:1.0
xrandr --output VGA-1 --gamma 1.0:1.0:1.0
```

### Ver logs de blugon-lite
```bash
cat /tmp/blugon-tui-debug.log    # Logs del TUI
cat /tmp/blugon-postrm-debug.log # Logs de desinstalación
```

---

*Última actualización: 2026-02-26*

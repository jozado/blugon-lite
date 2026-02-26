# Subtrack: Gamma no se restaura en TUI y postrm

## Descripción

Aunque `xgamma` reporta éxito en los logs, la pantalla NO se restaura a colores normales ni al detener el daemon en el TUI ni al desinstalar con `apt purge`.

**Parent Track:** `deb_issues_20260226`
**Priority:** CRITICAL
**Estado:** PENDIENTE - En investigación

---

## Evidencia de los Logs

### TUI Log (`/tmp/blugon-tui-debug.log`)
```
DEBUG:root:Restaurando gamma con restaurar_gamma()
INFO:root:Intentando método 1: xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0
DEBUG:root:xgamma RGB: returncode=0
INFO:root:✓ xgamma RGB exitoso - gamma restaurado a 6500K
DEBUG:root:restaurar_gamma resultado: exitoso=True, mensaje=Gamma restaurado a 6500K
```

**Problema:** El código reporta éxito pero el usuario confirma que la pantalla sigue cálida.

### postrm Log (`/tmp/blugon-postrm-debug.log`)
```
[2026-02-26 17:37:32] Intentando xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0 (con /dev/tty)...
[2026-02-26 17:37:32] ✓ xgamma RGB exitoso - gamma restaurado a 6500K
```

**Problema:** Mismo comportamiento - reporta éxito pero no funciona.

---

## Hipótesis

### Hipótesis 1: `open('/dev/tty', 'w')` no funciona como se espera
- El `subprocess.run()` con `stdout=tty, stderr=tty, stdin=tty` podría no estar funcionando
- Posible problema: se abre `/dev/tty` en modo escritura ('w') pero también necesitamos lectura para stdin

### Hipótesis 2: El proceso no tiene acceso al TTY correcto
- Cuando se ejecuta desde el TUI, el TTY podría ser diferente
- Cuando se ejecuta desde postrm (root), el TTY podría no estar disponible

### Hipótesis 3: xgamma necesita ser ejecutado como el usuario que posee la sesión X11
- postrm se ejecuta como root, pero la sesión X11 pertenece al usuario
- Podría necesitar `sudo -u <usuario>` o `su <usuario> -c`

---

## Plan de Diagnóstico

### Paso 1: Verificar qué TTY está disponible
```python
# En el TUI
import os
print(f"TTY: {os.ttyname(0)}")
print(f"stdin isatty: {os.isatty(0)}")
```

### Paso 2: Probar xgamma directamente desde el TUI
```bash
# Desde la misma terminal donde corre el TUI
xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0
```

### Paso 3: Probar con `os.system()` en lugar de `subprocess.run()`
```python
os.system('xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0')
```

### Paso 4: Para postrm, ejecutar como el usuario
```bash
# Obtener usuario propietario de la sesión X11
XUSER=$(who | grep ':0' | awk '{print $1}')
sudo -u $XUSER xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0
```

---

## Criterios de Aceptación

- [ ] Al presionar 's' en el TUI, la pantalla se restaura VISIBILMENTE
- [ ] Al desinstalar con `apt purge`, la pantalla se restaura VISIBILMENTE
- [ ] Los logs coinciden con el comportamiento observado
- [ ] Testing confirmado por el usuario

---

## Notas

**IMPORTANTE:** No marcar como completado hasta que el usuario confirme que la pantalla se restaura correctamente.

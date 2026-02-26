# Subtrack: postrm no elimina directorios con __pycache__

## Descripción

Al desinstalar con `apt purge`, los directorios `/usr/lib/blugon-lite/tui/widgets` y `/usr/lib/blugon-lite/tui/modals` no se eliminan porque contienen archivos `__pycache__`.

**Parent Track:** `deb_issues_20260226`
**Priority:** MEDIUM
**Estado:** PENDIENTE - En investigación

---

## Evidencia de los Logs

### postrm Log (`/tmp/blugon-postrm-debug.log`)
```
[2026-02-26 17:37:32] Limpiando directorios de /usr/lib/blugon-lite/tui...
rmdir: fallo al borrar '/usr/lib/blugon-lite/tui/widgets': El directorio no está vacío
[2026-02-26 17:37:32] No se pudo eliminar /usr/lib/blugon-lite/tui/widgets (no vacío)
rmdir: fallo al borrar '/usr/lib/blugon-lite/tui/modals': El directorio no está vacío
[2026-02-26 17:37:32] No se pudo eliminar /usr/lib/blugon-lite/tui/modals (no vacío)
```

### Estado después de desinstalar
```bash
pepe@T410PP:~$ ls /usr/lib/blugon-lite/tui/
modals  __pycache__  widgets
```

---

## Problema

El comando `rmdir` solo elimina directorios **vacíos**. Los directorios contienen:
- `__pycache__/` - Archivos .pyc generados por Python

---

## Solución Propuesta

### Opción 1: Usar `rm -rf` en lugar de `rmdir` (MÁS AGRESIVO)
```bash
rm -rf /usr/lib/blugon-lite/tui/widgets
rm -rf /usr/lib/blugon-lite/tui/modals
rm -rf /usr/lib/blugon-lite/tui
```

**Ventajas:**
- Elimina todo recursivamente
- Simple y directo

**Desventajas:**
- Potencialmente peligroso si hay archivos importantes
- No discrimina entre archivos generados y configuraciones

### Opción 2: Limpiar __pycache__ primero, luego rmdir
```bash
find /usr/lib/blugon-lite/tui -type d -name '__pycache__' -exec rm -rf {} \;
rmdir /usr/lib/blugon-lite/tui/widgets
rmdir /usr/lib/blugon-lite/tui/modals
rmdir /usr/lib/blugon-lite/tui
```

**Ventajas:**
- Más seguro
- Solo elimina archivos generados

**Desventajas:**
- Más complejo
- Podría haber otros archivos residuales

### Opción 3: Usar `rm -rf` solo en /usr/lib/blugon-lite (RECOMENDADA)
```bash
rm -rf /usr/lib/blugon-lite
```

**Ventajas:**
- Limpia TODO el directorio de la aplicación
- Simple y efectivo
- Es un purge, debería eliminar todo

**Desventajas:**
- Ninguna (es el comportamiento esperado de purge)

---

## Plan de Implementación

1. [ ] Actualizar `postrm` para usar `rm -rf /usr/lib/blugon-lite` en caso `purge`
2. [ ] Agregar logging de lo que se elimina
3. [ ] Reconstruir paquete .deb
4. [ ] Probar desinstalación completa
5. [ ] Verificar que no queden archivos

---

## Criterios de Aceptación

- [ ] Después de `apt purge`, `/usr/lib/blugon-lite` NO existe
- [ ] Después de `apt purge`, `/etc/xdg/autostart/blugon-lite.desktop` NO existe
- [ ] Después de `apt purge`, `~/.config/autostart/blugon-lite.desktop` NO existe
- [ ] Logs muestran claramente qué se eliminó
- [ ] Testing confirmado por el usuario

---

## Notas

**IMPORTANTE:** No marcar como completado hasta que el usuario confirme que no quedan archivos residuales.

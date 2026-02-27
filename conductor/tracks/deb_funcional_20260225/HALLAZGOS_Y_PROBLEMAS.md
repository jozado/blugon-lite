# Hallazgos y Problemas - Empaquetado .deb

## Fecha: 2026-02-25

---

## PROBLEMA CRÍTICO #1: Desinstalación Sucia

### Síntoma
El comando `sudo apt purge blugon-lite` se cuelga al 20% y deja el paquete en estado `rF` (removal requested, failed).

### Estado del paquete después del fallo
```
rF  blugon-lite    1.0.0-lite   amd64  Blue Light Filter for X Window System
```

### Causas Identificadas

1. **Procesos bloqueando la eliminación**
   - El daemon blugon-lite queda corriendo en segundo plano
   - El TUI (blugon-lite-tui) también puede estar activo
   - Los scripts prerm/postrm intentan matar procesos pero fallan

2. **Scripts de mantenimiento con errores**
   - `postinst` tenía `set -e` que causa aborto al primer error
   - Comandos sin `|| true` pueden fallar y bloquear todo
   - No se manejan todos los casos (failed-remove, abort-install, etc.)

3. **dpkg --configure -a falla**
   - El comando requiere privilegios de superusuario
   - A veces se ejecuta sin sudo y falla silenciosamente

### Intentos de Solución (Fallidos)

1. ✅ Scripts corregidos SIN `set -e`
2. ✅ Todos los comandos con `|| true`
3. ✅ Casos adicionales en postrm (failed-remove, abort-install, etc.)
4. ❌ PERO la desinstalación SIGUE CUELGA

### Posible Causa Raíz

**Los scripts prerm/postrm NO se están ejecutando** porque dpkg no puede leerlos del paquete .deb correctamente, O hay un proceso zombie que no puede ser eliminado con pkill normal.

---

## PROBLEMA #2: Daemon No Detecta Estado

### Síntoma
El TUI muestra `[○] Daemon: Inactivo` incluso cuando el daemon está corriendo.

### Causa Identificada

La función `is_daemon_running()` en `tui/utils.py` usa:
```python
subprocess.run(['pgrep', '-f', 'blugon-lite.py'])
```

Esto busca `blugon-lite.py` pero el daemon instalado usa la ruta `/usr/bin/blugon-lite` que es un script wrapper o el archivo Python directo.

### Solución Requerida

Actualizar `is_daemon_running()` para buscar:
- `blugon-lite` (comando instalado)
- `blugon-lite.py` (script de desarrollo)
- Verificar el proceso por el argumento `--interval`

---

## PROBLEMA #3: Servicio Systemd Fallido

### Síntoma
```
Failed to start blugon-lite.service: Unit blugon-lite.service has a bad unit file setting.
```

### Causa Identificada

El archivo del servicio tenía:
```ini
User=%i
```

Esto es para servicios template y requiere una instancia (ej: `blugon-lite@usuario.service`).

### Solución Aplicada

Remover `User=%i` del servicio para que corra como usuario por defecto del sistema.

---

## PROBLEMA #4: Lanzador del Daemon No Funciona

### Síntoma
El lanzador "blugon-lite Daemon" en el menú de aplicaciones no inicia el daemon.

### Causas Posibles

1. El archivo `.desktop` está en `/usr/share/applications/` pero debería estar en `/etc/xdg/autostart/` para autoinicio
2. El comando `Exec=blugon-lite --interval 120` no encuentra el binario en el PATH
3. Falta especificar `Terminal=false` correctamente

### Solución Requerida

1. Mover o copiar el .desktop a `/etc/xdg/autostart/`
2. Usar ruta absoluta: `Exec=/usr/bin/blugon-lite --interval 120`
3. Verificar permisos del archivo

---

## ARCHIVOS QUE NECESITAN REVISIÓN

### 1. debian/DEBIAN/prerm
- Verificar que se está incluyendo en el paquete .deb
- Agregar logging para debug: `echo "prerm: Killing processes" >> /tmp/blugon-debug.log`

### 2. debian/DEBIAN/postrm
- Agregar logging similar
- Verificar que maneja el caso `failed-remove`

### 3. debian/DEBIAN/postinst
- Ya se corrigió (sin `set -e`)
- Verificar que se ejecuta correctamente

### 4. tui/utils.py - is_daemon_running()
- Actualizar para detectar correctamente el daemon

### 5. blugon-lite.desktop
- Usar ruta absoluta para Exec
- Copiar a /etc/xdg/autostart/ en postinst

---

## PRÓXIMOS PASOS RECOMENDADOS

1. **LEER ESTE ARCHIVO** antes de cualquier otra operación
2. Agregar logging extensivo a scripts prerm/postrm
3. Reconstruir paquete con logging
4. Probar instalación Y desinstalación
5. Arreglar detección del daemon en TUI
6. Arreglar servicio systemd
7. Arreglar lanzador de autoinicio

---

## COMANDOS DE DIAGNÓSTICO

```bash
# Verificar estado del paquete
dpkg -l blugon-lite

# Ver logs de dpkg
cat /var/log/dpkg.log | grep blugon

# Ver procesos corriendo
ps aux | grep blugon-lite

# Ver servicio systemd
systemctl status blugon-lite

# Ver archivos del servicio
ls -la /usr/lib/systemd/system/blugon-lite.service
ls -la /etc/systemd/system/multi-user.target.wants/blugon-lite.service
```

---

## LECCIONES APRENDIDAS

1. **Nunca usar `set -e`** en scripts de mantenimiento de paquetes Debian
2. **Siempre usar `|| true`** en comandos que pueden fallar
3. **Manejar TODOS los casos** en prerm/postrm (remove, purge, failed-remove, abort-install, etc.)
4. **Agregar logging** para debug cuando algo falla
5. **Matar procesos ANTES** de intentar desinstalar
6. **Usar rutas absolutas** en archivos .desktop y servicios systemd
7. **Probar desinstalación** antes de considerar el paquete como "terminado"

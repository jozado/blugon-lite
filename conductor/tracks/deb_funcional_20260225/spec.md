# Track Specification: deb_funcional_20260225

## Descripción

Crear un paquete .deb completamente funcional de blugon-lite que se instale y desinstale limpiamente, con todos los componentes funcionando correctamente.

## Problemas a Resolver

### 1. Desinstalación Sucia (CRÍTICO)
- El comando `apt purge blugon-lite` se cuelga al 20%
- El paquete queda en estado `rF` (removal requested, failed)
- Requiere limpieza manual con `dpkg --purge --force-all`

### 2. Daemon No Detecta Estado
- El TUI muestra "Daemon: Inactivo" incluso cuando está corriendo
- La función `is_daemon_running()` no detecta correctamente el proceso

### 3. Servicio Systemd Fallido
- Error: "Unit blugon-lite.service has a bad unit file setting"
- Causa: `User=%i` inválido en el archivo del servicio

### 4. Lanzador del Daemon No Funciona
- El lanzador "blugon-lite Daemon" no inicia el proceso
- El autoinicio no funciona correctamente

## Alcance

### Características a Corregir

1. **Scripts de Mantenimiento (prerm/postrm)**
   - Sin `set -e` que cause abortos
   - Todos los comandos con `|| true`
   - Manejo de TODOS los casos (remove, purge, failed-remove, abort-install, etc.)
   - Logging para debug

2. **Detección del Daemon**
   - Actualizar `is_daemon_running()` en `tui/utils.py`
   - Buscar por múltiples patrones (blugon-lite, blugon-lite.py, --interval)

3. **Servicio Systemd**
   - Remover `User=%i` inválido
   - Verificar que el servicio se pueda habilitar/iniciar

4. **Lanzador de Autoinicio**
   - Usar ruta absoluta en `Exec=`
   - Copiar a `/etc/xdg/autostart/` en postinst
   - Verificar permisos

### Características NO incluidas

- Nuevas funcionalidades del TUI
- Cambios en la lógica de blugon-lite.py
- Optimizaciones de rendimiento

## Requisitos Técnicos

### Scripts Debian
- `prerm`: Máximo 20 líneas, sin comandos que puedan bloquear
- `postrm`: Manejar todos los casos, sin fallar nunca
- `postinst`: Logging, sin `set -e`

### Testing
- Desinstalación debe completar en menos de 10 segundos
- Daemon debe ser detectado correctamente por el TUI
- Servicio systemd debe poder habilitarse sin errores

## Criterios de Aceptación

### Desinstalación Limpia
- [ ] `sudo apt purge blugon-lite` completa sin colgarse
- [ ] Paquete no queda en estado `rF`
- [ ] Todos los archivos son eliminados
- [ ] No requiere intervención manual

### Detección del Daemon
- [ ] TUI muestra "Daemon: Activo" cuando está corriendo
- [ ] TUI muestra "Daemon: Inactivo" cuando está detenido
- [ ] Función `is_daemon_running()` detecta ambos modos (CLI y TUI)

### Servicio Systemd
- [ ] `sudo systemctl enable blugon-lite` funciona sin errores
- [ ] `sudo systemctl start blugon-lite` inicia el daemon
- [ ] `systemctl status blugon-lite` muestra servicio activo

### Lanzador
- [ ] Click en "blugon-lite Daemon" inicia el proceso
- [ ] Autoinicio funciona al reiniciar sesión
- [ ] Daemon persiste después de cerrar TUI

## Notas de Implementación

### Orden de Prioridad

1. **LEER HALLAZGOS_Y_PROBLEMAS.md** - Documento con todos los detalles
2. Arreglar desinstalación sucia (más crítico)
3. Arreglar detección del daemon
4. Arreglar servicio systemd
5. Arreglar lanzador de autoinicio

### Logging para Debug

Agregar a prerm/postrm:
```bash
echo "$(date): prerm $1" >> /tmp/blugon-debug.log
pkill -f blugon-lite >> /tmp/blugon-debug.log 2>&1 || true
echo "Done" >> /tmp/blugon-debug.log
```

### Comandos de Verificación

```bash
# Después de instalar
systemctl status blugon-lite
ps aux | grep blugon-lite
blugon-lite-tui  # Verificar que muestra Daemon: Activo

# Después de desinstalar
dpkg -l blugon-lite  # No debería aparecer
ls /usr/bin/blugon-lite  # No debería existir
```

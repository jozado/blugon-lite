# Plan: postrm no elimina directorios con __pycache__

## Estado: 🟡 LISTO PARA IMPLEMENTAR

---

## Problema Confirmado

```
rmdir: fallo al borrar '/usr/lib/blugon-lite/tui/widgets': El directorio no está vacío
```

Los directorios contienen archivos `__pycache__` generados por Python.

---

## Solución Seleccionada

**Opción 3:** Usar `rm -rf /usr/lib/blugon-lite` en caso `purge`

Justificación:
- Es un `purge`, debería eliminar TODO
- Simple y efectivo
- No deja archivos residuales

---

## Tareas

### 1. Implementar solución
- [ ] Actualizar `debian/DEBIAN/postrm` para usar `rm -rf /usr/lib/blugon-lite`
- [ ] Agregar logging de lo que se elimina
- [ ] Mantener logging existente para debugging

### 2. Reconstruir paquete
- [ ] Ejecutar `bash build-deb.sh`
- [ ] Verificar que el paquete se construye correctamente

### 3. Testing
- [ ] Instalar paquete
- [ ] Ejecutar `sudo apt purge blugon-lite`
- [ ] Verificar: `ls /usr/lib/blugon-lite` → debe decir "No existe"
- [ ] Revisar logs en `/tmp/blugon-postrm-debug.log`

---

## Código Propuesto para postrm

```bash
# En caso purge, después de restaurar gamma:
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Limpiando /usr/lib/blugon-lite..." >> "$LOGFILE"
if [ -d /usr/lib/blugon-lite ]; then
    rm -rf /usr/lib/blugon-lite >> "$LOGFILE" 2>&1 && \
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Eliminado /usr/lib/blugon-lite recursivamente" >> "$LOGFILE" || \
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR al eliminar /usr/lib/blugon-lite" >> "$LOGFILE"
fi
```

---

## Próxima Acción

Implementar la solución en `postrm` y reconstruir el paquete.

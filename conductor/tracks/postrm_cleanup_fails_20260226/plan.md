# Plan: postrm no elimina directorios con __pycache__

## Estado: ✅ IMPLEMENTADO - Pendiente de verificación

---

## Problema Confirmado

```
rmdir: fallo al borrar '/usr/lib/blugon-lite/tui/widgets': El directorio no está vacío
```

Los directorios contienen archivos `__pycache__` generados por Python.

---

## Solución Implementada

**Opción 3:** Usar `rm -rf /usr/lib/blugon-lite` en caso `purge`

Archivo modificado: `debian/DEBIAN/postrm`

```bash
# Limpiar directorio /usr/lib/blugon-lite recursivamente (purge debe eliminar TODO)
if [ -d /usr/lib/blugon-lite ]; then
    rm -rf /usr/lib/blugon-lite >> "$LOGFILE" 2>&1 && \
        echo "Eliminado /usr/lib/blugon-lite recursivamente" >> "$LOGFILE" || \
        echo "ERROR al eliminar /usr/lib/blugon-lite" >> "$LOGFILE"
fi
```

---

## Tareas

### 1. Implementar solución ✅ COMPLETADA
- [x] Actualizar `debian/DEBIAN/postrm` para usar `rm -rf /usr/lib/blugon-lite`
- [x] Agregar logging de lo que se elimina

### 2. Reconstruir paquete ⏳ PENDIENTE
- [ ] Ejecutar `bash build-deb.sh`
- [ ] Verificar que el paquete se construye correctamente

### 3. Testing ⏳ PENDIENTE
- [ ] Instalar paquete
- [ ] Ejecutar `sudo apt purge blugon-lite`
- [ ] Verificar: `ls /usr/lib/blugon-lite` → debe decir "No existe"
- [ ] Revisar logs en `/tmp/blugon-postrm-debug.log`

---

## Próxima Acción

Reconstruir el paquete y que el usuario pruebe la desinstalación.

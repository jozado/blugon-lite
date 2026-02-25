# blugon-lite - Requirements y Mejoras Pendientes

## Estado Actual

✅ Script blugon-lite.py funcional (202 líneas)
✅ Backends scg y xgamma implementados
✅ Documentación básica (README, man page, bash completion)
✅ Makefile para build e install
✅ Configuración de ejemplo (configs/evening/gamma)

---

## Requisitos Pendientes

### 1. Auto-Configuración del Script
**Prioridad: ALTA**

**Problema:** El usuario necesita crear manualmente `~/.config/blugon/gamma`

**Solución:**
- El script debe buscar configuración en este orden:
  1. `~/.config/blugon/gamma` (config del usuario)
  2. `/usr/share/blugon-lite/configs/evening/gamma` (config por defecto del sistema)
  3. Fallback built-in (config hardcodeada en el script)

**Implementación:**
```python
# En blugon-lite.py, función read_gamma()
def read_gamma(config_dir):
    config_file = config_dir + 'gamma'
    fallback_file = '/usr/share/blugon-lite/configs/evening/gamma'
    
    # Intentar config del usuario primero
    if os.path.exists(config_file):
        usar config_file
    # Fallback a config del sistema
    elif os.path.exists(fallback_file):
        usar fallback_file
    # Fallback built-in (hardcodeado)
    else:
        usar configuracion_por_defecto = [
            (8*60, [1.0, 1.0, 1.0]),      # 08:00 - normal
            (17*60, [1.0, 0.9, 0.8]),     # 17:00 - evening
            (21*60, [1.0, 0.8, 0.6]),     # 21:00 - warm
            (0, [1.0, 0.7, 0.5]),         # 00:00 - night
        ]
```

---

### 2. Paquete .deb con postinst
**Prioridad: ALTA**

**Problema:** Instalación manual requiere múltiples pasos

**Solución:**
- Crear estructura `debian/` para construir paquete .deb
- Script `postinst` que:
  - Crea `~/.config/blugon/` para cada usuario
  - Copia configuración por defecto
  - Ofrece activar servicio systemd (opcional)

**Archivos necesarios:**
```
debian/
├── control           # Metadatos del paquete
├── postinst          # Script post-instalación
├── prerm             # Script pre-remoción
├── conffiles         # Archivos de configuración
└── blugon-lite.docs  # Documentación a instalar
```

**Comando de build:**
```bash
dpkg-deb --build debian/ blugon-lite_1.0.0-lite_all.deb
```

---

### 3. Gestión de Configuraciones del Usuario
**Prioridad: ALTA**

**Problema:** ¿Cómo modifica el usuario los horarios fácilmente?

**Solución propuesta:**

#### 3.1 Documentación Clara
- README debe explicar CÓMO editar el archivo gamma
- Incluir ejemplos de diferentes configuraciones:
  - "Trabajador de oficina" (8am-6pm)
  - "Nocturno" (tarde-noche)
  - "Turno rotativo" (personalizable)
  - "Estudiante" (horarios extendidos)

#### 3.2 Archivo de Ejemplo Comentado
El archivo gamma por defecto debe estar BIEN COMENTADO:
```
# blugon-lite gamma configuration
# Format: HOUR MINUTE TEMPERATURE_KELVIN
#
# TEMPERATURE GUIDE:
#   6500K - Normal daylight (morning)
#   4500K - Warm white (afternoon)
#   3000K - Warm evening (evening)
#   2000K - Minimal blue light (night)
#
# Add or remove lines as needed. Times are in 24h format.
# Example: Add a noon configuration:
#   12 0 5500

8 0 6500    # 8:00 AM - Start day
17 0 4500   # 5:00 PM - Evening transition
21 0 3000   # 9:00 PM - Night mode
0 0 2000    # 12:00 AM - Deep night
6 0 2500    # 6:00 AM - Early morning
```

#### 3.3 Script de Utilidad (Opcional - Futuro)
Crear `blugon-lite-config` para generar configuraciones:
```bash
# Ejemplos de uso futuro:
blugon-lite-config --preset evening      # Config evening por defecto
blugon-lite-config --preset office       # Horario oficina 9-5
blugon-lite-config --preset night-owl    # Para nocturnos
blugon-lite-config --custom              # Wizard interactivo
```

---

### 4. Múltiples Configuraciones Predefinidas
**Prioridad: MEDIA**

**Problema:** Solo hay una configuración (evening)

**Solución:**
Incluir más configuraciones en `/usr/share/blugon-lite/configs/`:

```
configs/
├── evening/          # 17:00-08:00 (actual)
│   └── gamma
├── office/           # 9:00-18:00 trabajador oficina
│   └── gamma
├── student/          # Horarios extendidos estudiante
│   └── gamma
├── night-owl/        # Para nocturnos (despierto tarde)
│   └── gamma
├── minimal/          # Solo 3 puntos: día, tarde, noche
│   └── gamma
└── temperature/      # Basado en temperatura (ejemplo)
    └── gamma
```

**Instalación:**
```bash
# Copiar configuración predefinida
cp /usr/share/blugon-lite/configs/office/gamma ~/.config/blugon/gamma
```

---

### 5. Comando para Mostrar Configuración Actual
**Prioridad: BAJA**

**Problema:** Usuario no sabe qué configuración está activa

**Solución:**
Agregar opción `--show-config` o `--status`:
```bash
blugon-lite --status
# Output:
# Config file: /home/user/.config/blugon/gamma
# Current time: 14:30
# Current gamma: R=1.0 G=0.95 B=0.95
# Next transition: 17:00 (4500K)
```

---

## Plan de Implementación

### Fase 1 (Inmediata)
1. ✅ Hacer script auto-configurable con fallback
2. ✅ Crear estructura debian/ para paquete .deb
3. ✅ Script postinst para configuración automática
4. ✅ Mejorar comentarios en archivo gamma de ejemplo

### Fase 2 (Próxima)
5. Agregar múltiples configuraciones predefinidas
6. Documentar claramente cómo personalizar horarios
7. Agregar comando --status

### Fase 3 (Futuro)
8. Script blugon-lite-config para generación de configs
9. Soporte para múltiples perfiles de usuario
10. GUI simple para configuración (zenity/kdialog)

---

## Archivos a Modificar/Crear

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `blugon-lite.py` | Modificar | Agregar fallback automático |
| `debian/*` | Crear | Estructura del paquete .deb |
| `debian/postinst` | Crear | Script post-instalación |
| `configs/evening/gamma` | Mejorar | Agregar comentarios detallados |
| `configs/office/gamma` | Crear | Nueva config predefinida |
| `configs/student/gamma` | Crear | Nueva config predefinida |
| `README.md` | Actualizar | Documentar personalización |
| `blugon-lite.1` | Actualizar | Documentar en man page |

---

## Feedback del Usuario

Los usuarios deberían poder:
- [ ] Instalar con un solo comando (`sudo dpkg -i`)
- [ ] Usar inmediatamente sin configuración manual
- [ ] Entender cómo modificar horarios fácilmente
- [ ] Tener ejemplos claros de diferentes casos de uso
- [ ] Ver qué configuración está activa actualmente

---

## Notas

- Mantener compatibilidad con configs existentes de blugon original
- No romper la API de línea de comandos actual
- El script debe seguir siendo < 250 líneas (después de agregar fallback)

# Track Specification: blugon_lite_20260223

## Descripción

Crear una versión minimalista de blugon (blugon-lite.py) que elimine características innecesarias para reducir el consumo de RAM (< 8MB) y la complejidad del código (< 200 líneas), manteniendo la funcionalidad core de filtro de luz azul.

## Alcance

### Características a Eliminar

1. **FADE** - Todo el código de transición suave al startup
2. **SIMULATE** - Modo --simulation para simular el día completo
3. **WAIT_FOR_X** - Modo --waitforx para esperar el servidor X
4. **read_current/set_current** - Archivo 'current' y opciones -r, -S
5. **VERBOSE mode** - Opción -v y toda lógica de logging
6. **printconfig** - Opción -p
7. **COLOR_TABLE** - Tabla de colores para backend tty
8. **Backend tty completo** - backends/tty/tty.sh y lógica asociada
9. **Argumentos asociados**: --fade, --simulation, --waitforx, --readcurrent, --setcurrent, --printconfig, --verbose

### Características a Mantener

1. **Lectura de archivo gamma** - ~/.config/blugon/gamma con horarios personalizados
2. **Cálculo de interpolación** - Función calc_gamma() para interpolar entre horarios
3. **Backend scg** - Backend principal en C con Xrandr (mantener intacto)
4. **Backend xgamma** - Backend fallback usando xorg-xgamma
5. **Opciones CLI**:
   - `-o, --once` - Aplicar configuración actual y salir
   - `-i, --interval` - Intervalo entre refreshes (default: 120s)
   - `-c, --configdir, --config` - Directorio de configuración
   - `-b, --backend` - Seleccionar backend (scg o xgamma)
   - `-v, --version` - Imprimir versión y salir
6. **Función temp_to_gamma()** - Algoritmo de Tanner Helland (mantener intacto)

## Requisitos Técnicos

### Código
- **Líneas de código**: < 200 líneas (original: ~450)
- **Archivo único**: blugon-lite.py + backends separados
- **Python**: 3.6+ compatible
- **Sin dependencias adicionales**: Solo stdlib de Python

### Rendimiento
- **Consumo de RAM**: < 8MB (original: ~15MB)
- **Tiempo de inicio**: < 100ms

### Compatibilidad
- **Archivos gamma existentes**: Deben funcionar sin modificaciones
- **Formato de configuración**: Mantener formato actual (hora minuto gamma/temperatura)
- **Backends**: Mantener interfaces de llamadas existentes

## Entregables

1. **blugon-lite.py** - Script principal optimizado
2. **Makefile** - Modificado para instalar blugon-lite
3. **README.md** - Documentación con diferencias vs blugon original
4. **configs/evening/gamma** - Ejemplo de archivo gamma para horario 17:00-08:00

## Criterios de Aceptación

- [ ] El script se ejecuta con: `blugon-lite --once`
- [ ] Lee correctamente ~/.config/blugon/gamma
- [ ] Interpola entre horarios configurados
- [ ] Consumo de RAM medido < 8MB
- [ ] Código < 200 líneas
- [ ] Sin dependencias Python adicionales
- [ ] Backends scg y xgamma funcionan correctamente
- [ ] Función temp_to_gamma() sin modificaciones

## Notas de Implementación

- El código eliminado debe ser completamente removido (no comentado)
- Mantener la misma estructura de llamadas a backends
- Preservar manejo de errores básico
- El script debe ser ejecutable directamente

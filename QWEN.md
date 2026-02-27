# Configuración Global de Desarrollo

## Entorno

- **Sistema:** Debian 13 trixie
- **Escritorio:** XFCE

## Idioma

**Responder siempre en español.**

## Sudo con Askpass

**Importante:** Todos los comandos sudo deben usar `sudo -A <comando>`

## Principios de Código

**Arquitectura Modular:** El código NUNCA debe ser monolítico. Siempre priorizar:

- **Módulos pequeños y especializados:** Cada componente debe tener una única responsabilidad clara.
- **Bajo acoplamiento:** Los módulos deben ser independientes y comunicarse mediante interfaces bien definidas.
- **Alta cohesión:** La lógica relacionada debe estar agrupada en el mismo módulo.
- **Facilidad de mantenimiento:** El código debe ser fácil de entender, modificar y depurar.
- **Escalabilidad:** La arquitectura debe permitir agregar nuevas funcionalidades sin reestructurar el código existente.

**Aplicación:** Estos principios aplican a todos los proyectos dentro de este directorio.

## Depuración de Código y Sistema

**Enfoque Basado en Evidencia:** Cuando el código o sistema no funcione como se espera, NUNCA suponer soluciones. Siempre:

1. **Inyectar código/comandos de logging temporal** para observar el comportamiento en tiempo real.
2. **Identificar el problema exacto** basándose en los datos reales de ejecución.
3. **Formular una hipótesis** fundamentada en la evidencia recopilada.
4. **Implementar la solución** dirigida a la causa raíz del problema.
5. **Remover el logging temporal** una vez resuelto el problema.

**Herramientas recomendadas por contexto:**

| Contexto | Herramientas |
|----------|--------------|
| **Python** | `logging`, `loguru`, `pdb` |
| **Bash/Shell** | `set -x`, `echo`, `logger`, `bash -x` |
| **JavaScript/Node** | `console.log()`, `winston`, `debug` |
| **C/C++** | `printf()`, `gdb`, `valgrind` |
| **Sistema Debian** | `journalctl`, `dmesg`, `/var/log/*`, `strace` |
| **Red** | `curl -v`, `ping`, `tcpdump`, `ss`, `netstat` |
| **Procesos** | `ps`, `top`, `htop`, `lsof`, `pgrep` |
| **Archivos/permisos** | `ls -l`, `stat`, `getfacl`, `lsattr` |

**Principios generales:**

- Registrar valores de variables, estados, flujo de ejecución y condiciones.
- Evitar mensajes genéricos; incluir contexto suficiente (valores, timestamps, identificadores).
- Usar niveles de severidad apropiados (DEBUG, INFO, WARNING, ERROR).
- Para sistemas: revisar logs existentes antes de agregar instrumentación nueva.

**Aplicación:** Este enfoque aplica a toda depuración de código y sistema en los proyectos de este directorio y el entorno Debian 13.

---

## Revision y Documentación de Hallazgos y Soluciones

**Principio:** Cuando se encuentren problemas dificiles de resolver en el codigo revisar en el archivo `HALLAZGOS_Y_SOLUCIONES.md` para verificar si ya se han solucionado antes problemas similares en el proyecto. Cuando se encuentren soluciones a problemas que tomen tiempo resolver, o soluciones simples a problemas que puedan repetirse en el futuro, **documentar inmediatamente** en `HALLAZGOS_Y_SOLUCIONES.md`.

### Cuándo Actualizar HALLAZGOS_Y_SOLUCIONES.md

1. **Problemas que tomaron >15 minutos resolver** - Documentar causa raíz y solución
2. **Soluciones no obvias** - Workarounds, hacks, o enfoques creativos
3. **Comportamientos del sistema** - Quirks de X11, permisos, servicios, etc.
4. **Errores recurrentes** - Problemas que pueden volver a aparecer
5. **Comandos de diagnóstico útiles** - Snippets para debugging futuro
6. **Arquitectura del sistema** - Cómo interactúan los componentes

### Formato del Documento

```markdown
## FECHA: Título descriptivo del problema

### Problema
Descripción clara del síntoma observado

### Diagnóstico
Comandos usados para investigar

### Causa Raíz
Explicación técnica del porqué ocurrió

### Solución
Pasos exactos para resolver

### Lección Aprendida
Qué evitar o verificar en el futuro

### Referencia Rápida
Comandos o snippets útiles para resolver rápidamente si vuelve a ocurrir
```

### Beneficios

- **Evita repetir errores** - El equipo no cae en lo mismo dos veces
- **Debugging más rápido** - Soluciones ya documentadas para consulta rápida
- **Onboarding** - Nuevos desarrolladores aprenden de problemas pasados
- **Memoria institucional** - El conocimiento no se pierde

**Ejemplo real:** Problema "Gamma no se restaura" → Causa: xrandr vs xgamma → Solución: Usar xrandr --output --gamma

**Aplicación:** Esta práctica aplica a todo el proyecto blugon-lite y proyectos futuros.

---

## Validación de Lógica con Scripts de Prueba

**Principio:** Antes de modificar código crítico, crear script de prueba aislado para validar la lógica.

### Cuándo Usar Este Enfoque

1. **Algoritmos nuevos** - Lógica de cálculo, interpolación, sincronización
2. **Cambios críticos** - Modificaciones que afectan el core del sistema
3. **Fórmulas matemáticas** - Cálculos de tiempo, temperatura, interpolación
4. **Lógica de estado** - Máquinas de estado, transiciones, condiciones
5. **Optimizaciones** - Cambios que mejoran performance pero deben validar correctness

### Flujo Recomendado

```
1. 💡 Idea: Nueva lógica o algoritmo
2. 🧪 Prototipo: Script aislado (test_*.py)
3. ✅ Validación: Probar con casos reales
4. 🔧 Ajuste: Corregir errores en el prototipo
5. ✅ Re-validación: Confirmar que funciona
6. 🚀 Implementación: Portar al código real
7. 📊 Validación final: Teoría = Realidad
```

### Beneficios

| Ventaja | Resultado |
|---------|-----------|
| **Feedback inmediato** | Problemas detectados en segundos |
| **Debugging simple** | Sin dependencias complejas |
| **Iteración rápida** | Cambios y pruebas al toque |
| **Cero riesgo** | Si falla, no afecta el producto |
| **Confianza total** | Implementación ya validada |

### Ejemplo Real

**Problema:** Sincronizar daemon a múltiplos de 5 minutos

**Enfoque:**
```bash
# 1. Crear script de prueba
python3 test_sync_5min.py

# 2. Validar lógica (detectamos error: 23:18→23:21 en vez de 23:20)
# 3. Corregir fórmula en el script
# 4. Re-validar: ¡funciona!
# 5. Implementar en blugon-lite.py
```

**Resultado:** Error detectado y corregido en 5 minutos, sin tocar el daemon real.

**Aplicación:** Este enfoque aplica a todo desarrollo de lógica compleja en el proyecto.

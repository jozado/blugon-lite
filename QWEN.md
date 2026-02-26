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

## Documentación de Hallazgos y Soluciones

**Principio:** Cuando se encuentren soluciones a problemas que tomen tiempo resolver, o soluciones simples a problemas que puedan repetirse en el futuro, **documentar inmediatamente** en `HALLAZGOS_Y_SOLUCIONES.md`.

### Cuándo Actualizar HALLAZGOS_Y_SOLUCIONES.md

1. **Problemas que tomaron >30 minutos resolver** - Documentar causa raíz y solución
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

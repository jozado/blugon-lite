# Plan de Implementación: Sincronización del Daemon a Múltiplos de 5 Minutos

## Estado

⏳ PENDIENTE

## Tareas

### 1. Implementar función `calcular_proximo_intervalo()`
- [ ] Crear función que calcula segundos hasta próximo múltiplo de 5
- [ ] Agregar tests unitarios para validar cálculos
- [ ] Casos a probar:
  - [ ] 20:00:00 → 300s
  - [ ] 20:03:45 → 75s
  - [ ] 20:05:00 → 300s
  - [ ] 20:07:30 → 150s
  - [ ] 20:09:59 → 1s

### 2. Modificar bucle principal del daemon
- [ ] Agregar flag `primera_ejecucion`
- [ ] Calcular intervalo dinámico en primera ejecución
- [ ] Usar intervalo fijo de 300s en ejecuciones subsiguientes
- [ ] Agregar logging del intervalo calculado

### 3. Actualizar documentación
- [ ] Actualizar `blugon-lite.1` (man page)
- [ ] Comentar código nuevo
- [ ] Actualizar HALLAZGOS_Y_SOLUCIONES.md si corresponde

### 4. Testing
- [ ] Iniciar daemon a diferentes horas
- [ ] Verificar que los cambios se aplican en horas exactas
- [ ] Revisar logs para confirmar intervalos
- [ ] Probar modo `--once` (no debe verse afectado)

### 5. Commit y documentación
- [ ] Commit con mensaje descriptivo
- [ ] Actualizar tracks.md
- [ ] Marcar subtrack como COMPLETADO

## Estimación

- **Complejidad:** BAJA
- **Tiempo estimado:** 30-45 minutos
- **Riesgo:** BAJO (cambio localizado, fácil de revertir)

## Criterios de Aceptación

- [ ] Daemon verifica exactamente a las XX:00, XX:05, XX:10, etc.
- [ ] Logs muestran intervalos calculados correctamente
- [ ] 60% menos de verificaciones por hora
- [ ] Tests unitarios pasan
- [ ] Documentación actualizada

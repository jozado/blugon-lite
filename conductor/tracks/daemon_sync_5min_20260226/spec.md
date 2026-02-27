# Especificación Técnica: Sincronización del Daemon a Múltiplos de 5 Minutos

## Problema Actual

El daemon de blugon-lite verifica y aplica gamma cada **120 segundos fijos** desde su inicio:

```
20:00:00 → Inicia, verifica
20:02:00 → Verifica
20:04:00 → Verifica
20:06:00 → Verifica
...
```

**Consecuencias:**
1. Los cambios programados a las XX:05 **nunca se aplican en el momento exacto**
2. Hay un retraso de **0-2 minutos** entre la hora programada y la aplicación real
3. **30 verificaciones por hora** - más de las necesarias

## Solución Propuesta

Modificar el daemon para que:
1. **Primera verificación:** Inmediata al iniciar
2. **Cálculo del próximo intervalo:** Determinar segundos hasta el próximo múltiplo de 5
3. **Verificaciones subsiguientes:** Cada 300 segundos (5 minutos) exactos

### Ejemplo de Flujo

```
20:03:45 → Inicia, verifica inmediatamente
         → Calcula: faltan 75s para 20:05:00
         → Duerme 75 segundos
20:05:00 → Verifica (cambio programado se aplica exactamente)
         → Calcula: faltan 300s para 20:10:00
         → Duerme 300 segundos
20:10:00 → Verifica
         → Calcula: faltan 300s para 20:15:00
         → Duerme 300 segundos
```

## Beneficios

| Aspecto | Antes | Después |
|---------|-------|---------|
| Verificaciones/hora | 30 | 12 |
| Reducción de CPU | - | **60% menos** |
| Precisión | ±2 min | **Exacto** |
| Sincronización con TUI | No | **Sí (pasos de 5 min)** |

## Implementación Técnica

### Función `calcular_proximo_intervalo()`

```python
def calcular_proximo_intervalo():
    """
    Calcular segundos hasta el próximo múltiplo de 5 minutos.
    
    Retorna:
        int: Segundos a esperar hasta el próximo :00, :05, :10, etc.
    """
    now = time.localtime()
    minuto_actual = now.tm_min
    segundo_actual = now.tm_sec
    
    # Calcular minutos restantes hasta próximo múltiplo de 5
    minutos_restantes = (5 - (minuto_actual % 5)) % 5
    
    # Si estamos en múltiplo de 5 exacto (segundos = 0)
    if minutos_restantes == 0 and segundo_actual == 0:
        return 300  # Esperar 5 minutos completos
    
    # Calcular segundos totales
    segundos_espera = minutos_restantes * 60 + (60 - segundo_actual)
    
    # Si el cálculo da 0 (caso borde), usar 300
    return max(segundos_espera, 300) if segundos_espera == 0 else segundos_espera
```

### Ejemplos de Cálculo

| Hora actual | Próximo | Segundos a esperar |
|-------------|---------|-------------------|
| 20:00:00 | 20:05:00 | 300 |
| 20:03:45 | 20:05:00 | 75 |
| 20:05:00 | 20:10:00 | 300 |
| 20:07:30 | 20:10:00 | 150 |
| 20:09:59 | 20:10:00 | 1 |

### Modificación del Bucle Principal

**Código actual:**
```python
INTERVAL = 120  # Fijo

while True:
    apply_gamma()
    time.sleep(INTERVAL)
```

**Código nuevo:**
```python
primera_ejecucion = True

while True:
    apply_gamma()
    
    if primera_ejecucion:
        # Primera vez: calcular hasta próximo múltiplo de 5
        intervalo = calcular_proximo_intervalo()
        primera_ejecucion = False
    else:
        # Subsiguientes: siempre 5 minutos
        intervalo = 300
    
    logging.debug(f"Próxima verificación en {intervalo}s")
    time.sleep(intervalo)
```

## Archivos a Modificar

| Archivo | Cambios |
|---------|---------|
| `blugon-lite.py` | Agregar `calcular_proximo_intervalo()`, modificar bucle principal |
| `blugon-lite.1` | Actualizar documentación de `--interval` |

## Criterios de Aceptación

- [ ] Daemon se sincroniza a múltiplos de 5 minutos
- [ ] Cambios programados se aplican en la hora exacta
- [ ] 60% menos de verificaciones por hora
- [ ] Logs muestran próximo intervalo calculado
- [ ] Funciona con cualquier hora de inicio
- [ ] Modo `--once` no se ve afectado

## Riesgos y Mitigación

| Riesgo | Mitigación |
|--------|------------|
| Cálculo incorrecto del intervalo | Agregar tests unitarios para `calcular_proximo_intervalo()` |
| Daemon no se sincroniza | Logging extensivo para depuración |
| Usuarios con intervalos personalizados | Respetar `--interval` si es diferente de 120 |

## Notas Adicionales

- Esta mejora **no afecta** el modo `--once`
- El parámetro `--interval` podría ignorarse con esta implementación
- Alternativa: solo aplicar sincronización si `interval == 120` (default)

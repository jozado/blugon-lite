#!/usr/bin/env python3
"""Script de prueba para validar la sincronización a múltiplos de 5 minutos."""

import time
from time import localtime


def calcular_proximo_intervalo():
    """
    Calcular segundos hasta el próximo múltiplo de 5 minutos.
    
    Retorna:
        int: Segundos a esperar hasta el próximo :00, :05, :10, etc.
    """
    now = localtime()
    minuto_actual = now.tm_min
    segundo_actual = now.tm_sec
    
    # Calcular minutos restantes hasta próximo múltiplo de 5
    minutos_restantes = (5 - (minuto_actual % 5)) % 5
    
    # Si estamos en múltiplo de 5 exacto (segundos = 0)
    if minutos_restantes == 0 and segundo_actual == 0:
        return 300  # Esperar 5 minutos completos
    
    # Si estamos en múltiplo de 5 pero con segundos > 0
    # Ej: 23:05:30 → esperar hasta 23:10:00
    if minutos_restantes == 0:
        segundos_espera = 300 - segundo_actual
    else:
        # Ej: 23:18:47 → 2 min * 60 - 47 seg = 73 seg (llega a 23:20:00)
        segundos_espera = minutos_restantes * 60 - segundo_actual
    
    # Si el cálculo da 0 o negativo (caso borde), usar 300
    return max(segundos_espera, 300) if segundos_espera <= 0 else segundos_espera


def main():
    print("=" * 60)
    print("PRUEBA: Sincronización a múltiplos de 5 minutos")
    print("=" * 60)
    
    while True:
        ahora = localtime()
        hora_str = time.strftime("%H:%M:%S", ahora)
        
        # SIEMPRE calcular el próximo intervalo (no usar 300s fijos)
        intervalo = calcular_proximo_intervalo()
        
        print(f"\n[{hora_str}] ¡Despierte!")
        print(f"  Hora actual: {hora_str}")
        
        # Mostrar a qué hora será el próximo despertar
        proximo_ts = time.time() + intervalo
        proximo_str = time.strftime("%H:%M:%S", localtime(proximo_ts))
        print(f"  Calculando próximo intervalo...")
        print(f"  Próximo despertar: {proximo_str} (en {intervalo}s)")
        
        # Esperar el intervalo calculado
        print(f"  Durmiendo {intervalo} segundos...")
        print(f"  (Presiona Ctrl+C para salir)")
        
        # Countdown para ver el progreso
        for restante in range(intervalo, 0, -10):
            if restante % 60 == 0:
                print(f"    Faltan {restante // 60} minutos...")
            time.sleep(10)
        
        # Pequeña pausa final para asegurar sincronización
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INTERRUMPIDO] Saliendo...")

#!/usr/bin/env python3
"""Funciones utilitarias para el TUI."""

import math
import subprocess
from .config import DEFAULT_CONFIG, TUI_CONFIG_FILE


def temp_to_rgb(temp):
    """Convertir temperatura (Kelvin) a RGB aproximado para vista previa.
    
    Algoritmo basado en Tanner Helland.
    """
    temp = temp / 100
    
    # Calcular componente rojo
    if temp <= 66:
        r = 255
    else:
        r = temp - 60
        r = 329.698727446 * (r ** -0.1332047592)
    
    # Calcular componente verde
    if temp <= 66:
        g = temp
        g = 99.4708025861 * math.log(g) - 161.1195681661
    else:
        g = temp - 60
        g = 288.1221695283 * (g ** -0.0755148492)
    
    # Calcular componente azul
    if temp <= 10:
        b = 0
    elif temp >= 66:
        b = 255
    else:
        b = temp - 10
        b = 138.5177312231 * math.log(b) - 305.0447927307
    
    return int(max(0, min(255, r))), int(max(0, min(255, g))), int(max(0, min(255, b)))


def get_label_for_time(hour, minute):
    """Obtener etiqueta descriptiva para un horario."""
    total_minutes = hour * 60 + minute
    if 5 * 60 <= total_minutes < 12 * 60:
        return "Mañana"
    elif 12 * 60 <= total_minutes < 17 * 60:
        return "Tarde"
    elif 17 * 60 <= total_minutes < 21 * 60:
        return "Atardecer"
    elif 21 * 60 <= total_minutes < 24 * 60 or total_minutes < 5 * 60:
        return "Noche"
    else:
        return "Madrugada"


def calcular_temperatura_interpolada(schedules, current_hour, current_minute):
    """
    Calcular temperatura interpolada actual basada en los horarios configurados.
    
    Args:
        schedules: Lista de horarios con 'hour', 'minute', 'temp'
        current_hour: Hora actual (0-23)
        current_minute: Minuto actual (0-59)
    
    Retorna:
        tuple: (temperatura_interpolada, horario_anterior, horario_siguiente)
    """
    current_time = current_hour * 60 + current_minute
    
    # Convertir horarios a minutos y ordenar
    horarios = []
    for s in schedules:
        mins = s['hour'] * 60 + s['minute']
        horarios.append((mins, s['temp'], s.get('label', '')))
    horarios.sort()
    
    # Encontrar horarios adyacentes
    prev_h = None
    next_h = None
    
    for mins, temp, label in horarios:
        if mins <= current_time:
            prev_h = (mins, temp, label)
        if mins >= current_time and next_h is None:
            next_h = (mins, temp, label)
    
    # Si no hay siguiente, usar el primero del día siguiente (cruza medianoche)
    if next_h is None and prev_h is not None:
        next_h = horarios[0]
    elif prev_h is None and next_h is not None:
        prev_h = horarios[-1]
    elif prev_h is None and next_h is None:
        return 6500, None, None  # Default si no hay horarios
    
    # Calcular interpolación
    prev_mins, prev_temp, _ = prev_h
    next_mins, next_temp, _ = next_h
    
    # Ajustar si cruza medianoche
    if next_mins < prev_mins:
        next_mins += 24 * 60
    
    # Calcular factor de interpolación
    if next_mins == prev_mins:
        factor = 0
    else:
        factor = (current_time - prev_mins) / (next_mins - prev_mins)
    
    # Interpolar temperatura
    temp_actual = prev_temp + factor * (next_temp - prev_temp)
    
    return temp_actual, prev_h, next_h


def read_gamma_file(filepath):
    """Leer configuración gamma desde archivo.

    Soporta dos formatos:
    1. hora minuto temperatura [etiqueta]
    2. hora minuto temperatura (formato original)

    Returns:
        list: Lista de horarios ordenados por hora.
    """
    schedules = []
    try:
        with open(filepath, 'r') as f:
            for line in f.read().splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) >= 3:  # hora minuto temperatura [etiqueta]
                    hour = int(parts[0])
                    minute = int(parts[1])
                    temp = float(parts[2])
                    # Etiqueta opcional (cuarta columna)
                    if len(parts) >= 4:
                        label = ' '.join(parts[3:])  # Unir palabras restantes
                    else:
                        label = get_label_for_time(hour, minute)
                    schedules.append({
                        'hour': hour,
                        'minute': minute,
                        'temp': temp,
                        'time_str': f"{hour:02d}:{minute:02d}",
                        'temp_str': f"{int(temp)}K",
                        'label': label
                    })
        schedules.sort(key=lambda x: x['hour'] * 60 + x['minute'])
    except FileNotFoundError:
        pass
    return schedules


def write_gamma_file(filepath, schedules):
    """Escribir configuración gamma a archivo.
    
    Formato: hora minuto temperatura [etiqueta]
    """
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write("# =============================================================================\n")
        f.write("# blugon-lite Gamma Configuration\n")
        f.write("# Generated by blugon-lite-tui\n")
        f.write("# Format: hour minute temperature [label]\n")
        f.write("# =============================================================================\n\n")
        for sched in schedules:
            # Escribir línea de datos con etiqueta opcional
            f.write(f"{sched['hour']} {sched['minute']} {int(sched['temp'])} {sched['label']}\n")


def get_default_schedules():
    """Obtener horarios por defecto desde configuración hardcodeada."""
    schedules = []
    for line in DEFAULT_CONFIG.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = list(map(float, line.split()))
        if len(parts) == 3:
            hour, minute, temp = parts
            label = get_label_for_time(int(hour), int(minute))
            schedules.append({
                'hour': int(hour),
                'minute': int(minute),
                'temp': temp,
                'time_str': f"{int(hour):02d}:{int(minute):02d}",
                'temp_str': f"{int(temp)}K",
                'label': label
            })
    schedules.sort(key=lambda x: x['hour'] * 60 + x['minute'])
    return schedules


def save_theme(theme_id):
    """Guardar tema seleccionado a archivo de configuración."""
    import os
    os.makedirs(os.path.dirname(TUI_CONFIG_FILE), exist_ok=True)
    with open(TUI_CONFIG_FILE, 'w') as f:
        f.write(f"theme={theme_id}\n")


def load_theme():
    """Cargar tema desde archivo de configuración."""
    try:
        with open(TUI_CONFIG_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('theme='):
                    return line.split('=')[1]
    except FileNotFoundError:
        pass
    return 'dark'  # Tema por defecto


def is_daemon_running():
    """Verificar si el daemon de blugon-lite está en ejecución.

    Busca específicamente el proceso del daemon con --interval.
    NO cuenta el TUI ni otros procesos de blugon-lite.
    """
    import logging
    logging.basicConfig(filename='/tmp/blugon-tui-debug.log', level=logging.DEBUG)

    # Buscar específicamente el daemon con --interval
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'blugon-lite --interval'],
            capture_output=True,
            text=True
        )
        logging.debug(f"pgrep -f 'blugon-lite --interval': returncode={result.returncode}, stdout='{result.stdout.strip()}'")
        if result.returncode == 0 and result.stdout.strip():
            logging.info(f"Daemon detectado con patrón: 'blugon-lite --interval'")
            return True
    except Exception as e:
        logging.error(f"Error al buscar daemon: {e}")

    logging.info("No se detectó el daemon")
    return False


def toggle_daemon():
    """Alternar estado del daemon de blugon-lite."""
    import logging

    if is_daemon_running():
        logging.info("Deteniendo daemon...")
        result = subprocess.run(['pkill', '-f', 'blugon-lite'], capture_output=True, text=True)
        logging.debug(f"pkill resultado: returncode={result.returncode}")
        return False
    else:
        logging.info("Iniciando daemon...")
        # Usar ruta absoluta para el daemon
        daemon_cmd = ['/usr/bin/blugon-lite', '--interval', '120']
        # Verificar si existe /usr/bin/blugon-lite, si no usar blugon-lite.py
        import os
        if not os.path.exists('/usr/bin/blugon-lite'):
            # En desarrollo, usar el script local
            daemon_cmd = ['python3', 'blugon-lite.py', '--interval', '120']

        logging.debug(f"Ejecutando: {' '.join(daemon_cmd)}")
        subprocess.Popen(
            daemon_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        return True


def restaurar_gamma():
    """Restaurar gamma de pantalla a valores normales (6500K / RGB 1.0).

    NOTA: El backend SCG de blugon-lite usa Xrandr (XRRSetCrtcGamma).
    Para restaurar, debemos usar xrandr también, NO xgamma.

    Intenta métodos en orden:
    1. xrandr --output --gamma 1.0:1.0:1.0 (para todos los outputs conectados)
    2. xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0 (fallback)

    Returns:
        tuple: (exitoso: bool, mensaje: str)
    """
    import logging
    import subprocess
    logging.basicConfig(filename='/tmp/blugon-tui-debug.log', level=logging.DEBUG)

    logging.info("=== Iniciando restauración de gamma ===")

    # Método 1: xrandr para todos los outputs conectados (RECOMENDADO)
    logging.info("Intentando método 1: xrandr --output --gamma 1.0:1.0:1.0")
    try:
        # Obtener lista de outputs conectados
        result = subprocess.run(
            ['xrandr', '--query'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        outputs_conectados = []
        for line in result.stdout.splitlines():
            if ' connected' in line:
                output_name = line.split()[0]
                outputs_conectados.append(output_name)
        
        logging.debug(f"Outputs conectados: {outputs_conectados}")
        
        # Restaurar gamma para cada output
        exitos = 0
        for output in outputs_conectados:
            result = subprocess.run(
                ['xrandr', '--output', output, '--gamma', '1.0:1.0:1.0'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                exitos += 1
                logging.debug(f"xrandr --output {output} --gamma 1.0:1.0:1.0: exitoso")
            else:
                logging.warning(f"xrandr --output {output} falló: {result.stderr}")
        
        if exitos > 0:
            logging.info(f"✓ xrandr exitoso en {exitos}/{len(outputs_conectados)} outputs")
            return (True, f"Gamma restaurado en {exitos} monitor(es)")
        else:
            logging.warning("✗ xrandr falló en todos los outputs")
            
    except subprocess.TimeoutExpired:
        logging.error("✗ xrandr timeout")
    except Exception as e:
        logging.error(f"✗ xrandr excepción: {e}")

    # Método 2: Fallback a xgamma
    logging.info("Intentando método 2: xgamma -rgamma 1.0 -ggamma 1.0 -bgamma 1.0")
    try:
        result = subprocess.run(
            ['xgamma', '-rgamma', '1.0', '-ggamma', '1.0', '-bgamma', '1.0'],
            timeout=5
        )
        logging.debug(f"xgamma: returncode={result.returncode}")

        if result.returncode == 0:
            logging.info("✓ xgamma exitoso")
            return (True, "Gamma restaurado con xgamma")
        else:
            logging.warning(f"✗ xgamma falló con código {result.returncode}")
    except Exception as e:
        logging.error(f"✗ xgamma excepción: {e}")

    # Todos los métodos fallaron
    logging.error("✗ TODOS los métodos de restauración fallaron")
    return (False, "Error: No se pudo restaurar gamma. Ejecute 'xrandr --output --gamma 1.0:1.0:1.0' manualmente")

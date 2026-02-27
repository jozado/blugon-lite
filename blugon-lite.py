#!/usr/bin/env python3
"""blugon-lite - Blue Light Filter for X Window System (minimalist version)."""

from configparser import ConfigParser
from argparse import ArgumentParser
import time
import math
import os
from subprocess import check_call
from os import getenv, path
from sys import stdout
from io import StringIO

VERSION = '1.0.0-lite'

# Obtener directorio del script para buscar backend localmente (desarrollo)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

MAKE_INSTALL_PREFIX = '/usr'

# Default configuration
DISPLAY = getenv('DISPLAY')
ONCE = False
INTERVAL = 120
CONFIG_DIR = getenv('XDG_CONFIG_HOME') or (getenv('HOME') or '/root') + '/.config'
CONFIG_DIR += '/blugon'
BACKEND = 'scg'

MAX_MINUTE = 24 * 60
NORMAL_TEMP = 6600.0
NORMAL_RED, NORMAL_GREEN, NORMAL_BLUE = 1.0, 1.0, 1.0
BACKEND_LIST = ['xgamma', 'scg']


def calcular_proximo_intervalo():
    """
    Calcular segundos hasta el próximo múltiplo de 5 minutos.
    
    Sincroniza el daemon para que verifique exactamente a las XX:00, XX:05, XX:10, etc.
    Esto permite que los cambios programados en el TUI (que usa pasos de 5 min)
    se apliquen en el momento exacto.
    
    Retorna:
        int: Segundos a esperar hasta el próximo múltiplo de 5 minutos.
    
    Ejemplos:
        20:00:00 → 300s (próximo: 20:05:00)
        20:03:45 → 75s (próximo: 20:05:00)
        20:05:00 → 300s (próximo: 20:10:00)
        20:07:30 → 150s (próximo: 20:10:00)
        20:18:47 → 73s (próximo: 20:20:00)
    """
    now = time.localtime()
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


def temp_to_gamma(temp):
    """Transform temperature in Kelvin to Gamma values (0-1).
    Algorithm by Tanner Helland: http://www.tannerhelland.com/4435/"""
    def rgb_to_gamma(color):
        color = max(0, min(255, color))
        return color / 255

    temp = temp / 100
    if temp <= 66:
        r = 255
    else:
        r = temp - 60
        r = 329.698727446 * (r ** -0.1332047592)

    if temp <= 66:
        g = temp
        g = 99.4708025861 * math.log(g) - 161.1195681661
    else:
        g = temp - 60
        g = 288.1221695283 * (g ** -0.0755148492)

    if temp <= 10:
        b = 0
    elif temp >= 66:
        b = 255
    else:
        b = temp - 10
        b = 138.5177312231 * math.log(b) - 305.0447927307

    return map(rgb_to_gamma, (r, g, b))


def read_gamma(config_dir):
    """Read gamma configuration file. Returns (gamma_list, minutes_list).
    
    Search order:
    1. ~/.config/blugon/gamma (user config)
    2. /usr/share/blugon-lite/configs/evening/gamma (system config)
    3. Hardcoded default configuration
    """
    config_file = config_dir + 'gamma'
    system_config_file = MAKE_INSTALL_PREFIX + '/share/blugon-lite/configs/evening/gamma'
    
    # Default hardcoded configuration (evening schedule: 17:00-08:00)
    default_config = """# Default blugon-lite configuration
# Evening schedule: 17:00 - 08:00 night mode

# Daytime (08:00) - Normal white (6500K)
8 0 6500

# Evening transition starts (17:00) - Warm white (4500K)
17 0 4500

# Night mode (21:00) - Reduced blue light (3000K)
21 0 3000

# Deep night (00:00) - Minimal blue light (2000K)
0 0 2000

# Early morning (06:00) - Start transitioning back (2500K)
6 0 2500
"""

    # Try to read from user config, system config, or use hardcoded default
    file_gamma = None
    try:
        file_gamma = open(config_file, 'r')
    except:
        try:
            file_gamma = open(system_config_file, 'r')
        except:
            # Use hardcoded default configuration
            file_gamma = StringIO(default_config)

    gamma = []
    for line in file_gamma.read().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        # Soportar formato con etiqueta: hora minuto temperatura [etiqueta]
        if len(parts) >= 3:
            hour = float(parts[0])
            minute = float(parts[1])
            temp = float(parts[2])
            r, g, b = temp_to_gamma(temp)
            gamma.append([int(60 * hour + minute), r, g, b])

    file_gamma.close()
    gamma.sort(key=lambda x: x[0])  # sort by minutes
    minutes = [g[0] for g in gamma]
    gamma = [[g[1], g[2], g[3]] for g in gamma]  # [[r,g,b], ...]
    return gamma, minutes


def calc_gamma(minute, list_minutes, list_gamma):
    """Calculate interpolated RGB gamma values for current minute."""
    next_index = list_minutes.index(next((x for x in list_minutes if x >= minute), list_minutes[0]))
    next_minute = list_minutes[next_index]
    prev_minute = list_minutes[next_index - 1]
    if next_minute < prev_minute:
        next_minute += MAX_MINUTE

    def inbetween(next_val, prev_val):
        diff = next_val - prev_val
        diff_minute = (next_minute - prev_minute) % MAX_MINUTE
        add_minute = (minute - prev_minute) % MAX_MINUTE
        try:
            factor = add_minute / diff_minute
        except:
            factor = 0
        return prev_val + factor * diff

    idx = next_index
    r = inbetween(list_gamma[idx][0], list_gamma[idx - 1][0])
    g = inbetween(list_gamma[idx][1], list_gamma[idx - 1][1])
    b = inbetween(list_gamma[idx][2], list_gamma[idx - 1][2])
    return r, g, b


def call_xgamma(r, g, b):
    """Apply gamma using xorg-xgamma."""
    def bound(gamma):
        return max(0.1, min(10.0, gamma))
    r, g, b = map(bound, (r, g, b))
    check_call(['xgamma', '-quiet', '-rgamma', str(r), '-ggamma', str(g), '-bgamma', str(b)])


def call_scg(r, g, b):
    """Apply gamma using scg backend (Xrandr)."""
    # Buscar backend en directorio local (desarrollo) o en ruta de instalación
    scg_path = os.path.join(SCRIPT_DIR, 'backends', 'scg', 'scg')
    if not os.path.exists(scg_path):
        scg_path = MAKE_INSTALL_PREFIX + '/lib/blugon-lite/scg'
    check_call([scg_path, str(r), str(g), str(b)])


def call_backend(backend, r, g, b):
    """Call appropriate backend with gamma values."""
    if backend == 'xgamma':
        call_xgamma(r, g, b)
    elif backend == 'scg':
        call_scg(r, g, b)


def get_minute():
    """Return current time as minutes from midnight."""
    now = time.localtime()
    return 60 * now.tm_hour + now.tm_min + now.tm_sec / 60


def main():
    global ONCE, INTERVAL, CONFIG_DIR, BACKEND

    # Parse arguments
    argparser = ArgumentParser(prog='blugon-lite', description='Blue Light Filter for X (lite)')
    argparser.add_argument('-v', '--version', action='store_true', help='print version')
    argparser.add_argument('-o', '--once', action='store_true', help='apply once and exit')
    argparser.add_argument('-i', '--interval', nargs='?', dest='interval', type=float,
                          help='interval in seconds (default: 120)')
    argparser.add_argument('-c', '--configdir', '--config', nargs='?', dest='config_dir',
                          help='configuration directory')
    argparser.add_argument('-b', '--backend', nargs='?', dest='backend', help='backend (scg/xgamma)')
    args = argparser.parse_args()

    if args.version:
        print('blugon-lite ' + VERSION)
        return

    # Apply arguments
    if args.config_dir:
        CONFIG_DIR = args.config_dir
    if not CONFIG_DIR.endswith('/'):
        CONFIG_DIR += '/'
    if args.interval:
        INTERVAL = math.ceil(args.interval)
    if args.backend:
        BACKEND = args.backend
    if not BACKEND in BACKEND_LIST:
        raise ValueError('Invalid backend. Choose: ' + ', '.join(BACKEND_LIST))
    ONCE = args.once

    # Read gamma configuration (uses fallback if config dir doesn't exist)
    list_gamma, list_minutes = read_gamma(CONFIG_DIR)

    # Setup logging
    import logging
    import pwd
    # Usar /tmp/blugon-lite-daemon.log para el usuario actual
    try:
        user = pwd.getpwuid(os.getuid()).pw_name
        log_file = f'/tmp/blugon-lite-{user}.log'
    except:
        log_file = '/tmp/blugon-lite-daemon.log'
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,  # DEBUG para ver todos los detalles
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info(f"blugon-lite iniciado - Backend: {BACKEND}, Interval: {INTERVAL}s")
    logging.info(f"Config dir: {CONFIG_DIR}")
    logging.info(f"Horarios cargados: {len(list_gamma)}")

    def apply_gamma():
        minute = get_minute()
        r, g, b = calc_gamma(minute, list_minutes, list_gamma)
        call_backend(BACKEND, r, g, b)
        logging.debug(f"Gamma aplicado: R={r:.3f}, G={g:.3f}, B={b:.3f} (minuto={minute})")

    if ONCE:
        logging.info("Modo --once: aplicando gamma y saliendo")
        apply_gamma()
        logging.info("Gamma aplicado exitosamente")
        return

    # Main loop - Sincronizado a múltiplos de 5 minutos
    logging.info("Iniciando bucle principal (sincronizado a múltiplos de 5 min)")
    restart_count = 0
    while True:
        try:
            apply_gamma()
            
            # Calcular intervalo hasta próximo múltiplo de 5 minutos
            # Esto asegura que los cambios se apliquen exactamente a las XX:00, XX:05, etc.
            intervalo = calcular_proximo_intervalo()
            proximo_ts = time.time() + intervalo
            proximo_str = time.strftime("%H:%M:%S", time.localtime(proximo_ts))
            
            logging.info(f"Próxima verificación: {proximo_str} (en {intervalo}s)")
            time.sleep(intervalo)
        except Exception as e:
            restart_count += 1
            logging.error(f"Error en iteración {restart_count}: {e}")
            if restart_count >= 5:
                logging.critical("Demasiados errores consecutivos, saliendo")
                break
            time.sleep(5)  # Esperar antes de reintentar


if __name__ == "__main__":
    main()

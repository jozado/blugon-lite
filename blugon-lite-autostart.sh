#!/bin/bash
# blugon-lite-autostart.sh - Script de autoinicio con logging extensivo

LOG_FILE="/tmp/blugon-lite-autostart-${USER}.log"

{
    echo "=========================================="
    echo "blugon-lite Autostart Script"
    echo "Fecha: $(date)"
    echo "Usuario: ${USER}"
    echo "HOME: ${HOME}"
    echo "DISPLAY: ${DISPLAY}"
    echo "XDG_SESSION_TYPE: ${XDG_SESSION_TYPE}"
    echo "=========================================="
    
    # Verificar si ya hay un daemon corriendo
    echo ""
    echo "[$(date '+%H:%M:%S')] Verificando daemon existente..."
    if pgrep -f "blugon-lite --interval" > /dev/null; then
        PID=$(pgrep -f "blugon-lite --interval")
        echo "[$(date '+%H:%M:%S')] ✓ Daemon YA está corriendo (PID: $PID)"
        echo "[$(date '+%H:%M:%S')] Terminando script de autoinicio"
        exit 0
    else
        echo "[$(date '+%H:%M:%S')] ✗ No hay daemon corriendo"
    fi
    
    # Verificar que el comando existe
    echo ""
    echo "[$(date '+%H:%M:%S')] Verificando que blugon-lite existe..."
    if [ -x /usr/bin/blugon-lite ]; then
        echo "[$(date '+%H:%M:%S')] ✓ /usr/bin/blugon-lite existe y es ejecutable"
    else
        echo "[$(date '+%H:%M:%S')] ✗ /usr/bin/blugon-lite NO existe o no es ejecutable"
        exit 1
    fi
    
    # Verificar configuración
    echo ""
    echo "[$(date '+%H:%M:%S')] Verificando configuración..."
    if [ -f "${HOME}/.config/blugon/gamma" ]; then
        echo "[$(date '+%H:%M:%S')] ✓ ~/.config/blugon/gamma existe"
    else
        echo "[$(date '+%H:%M:%S')] ⚠ ~/.config/blugon/gamma NO existe, se usará fallback"
    fi
    
    # Esperar a que X11 esté listo
    echo ""
    echo "[$(date '+%H:%M:%S')] Esperando 5 segundos para que X11 esté listo..."
    sleep 5
    
    # Iniciar daemon
    echo ""
    echo "[$(date '+%H:%M:%S')] Iniciando daemon..."
    /usr/bin/blugon-lite --interval 120 > /tmp/blugon-lite-daemon-stdout.log 2>&1 &
    DAEMON_PID=$!
    echo "[$(date '+%H:%M:%S')] Daemon iniciado con PID: $DAEMON_PID"
    
    # Esperar y verificar
    echo ""
    echo "[$(date '+%H:%M:%S')] Esperando 3 segundos y verificando..."
    sleep 3
    
    if ps -p $DAEMON_PID > /dev/null 2>&1; then
        echo "[$(date '+%H:%M:%S')] ✓ Daemon SIGUE corriendo"
        echo "[$(date '+%H:%M:%S')] Exitoso - Daemon en PID: $DAEMON_PID"
    else
        echo "[$(date '+%H:%M:%S')] ✗ Daemon SE DETUVO"
        echo "[$(date '+%H:%M:%S')] Verificando logs del daemon..."
        if [ -f /tmp/blugon-lite-daemon-stdout.log ]; then
            echo "=== STDOUT del daemon ==="
            cat /tmp/blugon-lite-daemon-stdout.log
        fi
        if [ -f /tmp/blugon-lite-${USER}.log ]; then
            echo "=== LOG del daemon ==="
            cat /tmp/blugon-lite-${USER}.log
        fi
    fi
    
    echo ""
    echo "[$(date '+%H:%M:%S')] Script de autoinicio finalizado"
    echo "=========================================="
    
} >> "$LOG_FILE" 2>&1

exit 0

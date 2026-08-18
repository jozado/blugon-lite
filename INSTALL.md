# Guía de Instalación de blugon-lite

Esta guía te mostrará cómo instalar blugon-lite en tu sistema Debian/Ubuntu.

---

## 📋 Requisitos del sistema

### Mínimos

- **Sistema operativo**: Debian 11+ o Ubuntu 20.04+
- **Entorno gráfico**: X Window System (X11)
- **Python**: 3.8 o superior
- **RAM**: 10MB libres
- **Disco**: 5MB libres

### Dependencias

El paquete `.deb` instala automáticamente:

- `python3` - Intérprete Python
- `python3-urwid` - Librería para TUI
- `libx11-6` - Librería X11
- `libxrandr2` - Extensión Xrandr para gamma
- `x11-xserver-utils` - Utilidades X11 (xgamma)

---

## 📦 Método 1: Instalación desde paquete .deb (Recomendado)

### Paso 1: Descargar el paquete

```bash
# Desde la página de releases
wget https://github.com/tu-usuario/blugon-lite/releases/download/v1.0.0/blugon-lite_1.0.0-lite_amd64.deb
```

### Paso 2: Instalar

```bash
# Método A: Usando apt (recomendado, resuelve dependencias)
sudo apt install ./blugon-lite_1.0.0-lite_amd64.deb

# Método B: Usando dpkg
sudo dpkg -i blugon-lite_1.0.0-lite_amd64.deb
sudo apt install -f  # Si faltan dependencias
```

### Paso 3: Verificar instalación

```bash
# Verificar que los comandos están disponibles
blugon-lite --version
blugon-lite-tui --help
```

### Paso 4: Primera configuración

```bash
# Abrir el TUI para configurar horarios
blugon-lite-tui
```

---

## 🔨 Método 2: Instalación desde código fuente

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/blugon-lite.git
cd blugon-lite
```

### Paso 2: Instalar dependencias de desarrollo

```bash
sudo apt update
sudo apt install -y python3-urwid libxrandr-dev libx11-dev make gcc
```

### Paso 3: Compilar backend SCG

```bash
cd backends/scg
make build
ls -la scg  # Debería mostrar el binario compilado
cd ../..
```

### Paso 4: Instalar

```bash
# Instalación manual
sudo make install
```

### Paso 5: Verificar instalación

```bash
blugon-lite --version
which blugon-lite  # Debería mostrar /usr/bin/blugon-lite
```

---

## 🎯 Primeros pasos

### 1. Configurar horarios

```bash
# Abrir el TUI
blugon-lite-tui
```

**En el TUI:**
- `e` - Editar horario seleccionado
- `a` - Agregar nuevo horario
- `d` - Eliminar horario
- `t` - Cambiar tema
- `s` - Guardar configuración
- `q` - Salir

### 2. Probar el filtro

```bash
# Aplicar una vez para probar
blugon-lite --once

# Deberías ver un cambio en el color de la pantalla
```

### 3. Ejecutar como daemon

```bash
# Ejecutar en segundo plano (ajusta cada 120 segundos)
nohup blugon-lite --interval 120 > /tmp/blugon.log 2>&1 &

# Verificar que está corriendo
pgrep -f blugon-lite

# Ver logs
tail -f /tmp/blugon.log
```

### 4. Detener el daemon

```bash
pkill -f blugon-lite
```

---

## 🔧 Configuración avanzada

### Ubicación de archivos

| Archivo | Ubicación | Propósito |
|---------|-----------|-----------|
| Configuración | `~/.config/blugon/gamma` | Horarios personalizados |
| Tema TUI | `~/.config/blugon/tui_config` | Tema del TUI |
| Sistema | `/usr/share/blugon-lite/configs/` | Configuraciones predefinidas |
| Backend | `/usr/lib/blugon-lite/scg` | Backend SCG compilado |

### Editar configuración manualmente

```bash
# Abrir archivo de configuración
nano ~/.config/blugon/gamma
```

**Formato:**
```
# hora minuto temperatura [etiqueta]
8 0 6500 Mañana
12 0 6000 Mediodía
17 0 4500 Atardecer
21 0 3000 Noche
0 0 2000 Madrugada
```

### Usar configuración predefinida

```bash
# Copiar configuración de ejemplo
cp /usr/share/blugon-lite/configs/evening/gamma ~/.config/blugon/gamma
```

---

## ❌ Desinstalación

### Desde paquete .deb

```bash
sudo apt remove blugon-lite

# O para remover completamente incluyendo configuración
sudo apt purge blugon-lite
```

### Desde código fuente

```bash
cd /path/to/blugon-lite
sudo make uninstall
```

### Limpieza manual

```bash
# Remover configuración del usuario
rm -rf ~/.config/blugon

# Remover logs
rm -f /tmp/blugon.log
```

---

## 🐛 Solución de problemas

### Problema: "command not found"

**Solución:**
```bash
# Verificar que está instalado
which blugon-lite

# Si no está, agregar PATH
export PATH=$PATH:/usr/bin
```

### Problema: "python3-urwid not found"

**Solución:**
```bash
sudo apt install python3-urwid
```

### Problema: El filtro no aplica cambios

**Solución:**
1. Verificar backend:
   ```bash
   blugon-lite --once --backend xgamma
   ```

2. Verificar permisos X11:
   ```bash
   xgamma -query
   ```

### Problema: TUI no inicia

**Solución:**
```bash
# Verificar dependencias
python3 -c "import urwid"

# Si falla, reinstalar
sudo apt install --reinstall python3-urwid
```

### Problema: Cambios no persisten

**Solución:**
```bash
# Verificar permisos
ls -la ~/.config/blugon/gamma

# Si es necesario, corregir permisos
chmod 644 ~/.config/blugon/gamma
```

---

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs: `tail -f /tmp/blugon.log`
2. Verifica la versión: `blugon-lite --version`
3. Reporta el issue en GitHub

---

## ✅ Verificación post-instalación

Ejecuta estos comandos para verificar que todo está correcto:

```bash
# 1. Versión correcta
blugon-lite --version

# 2. Backend disponible
ls -la /usr/lib/blugon-lite/scg

# 3. TUI inicia
blugon-lite-tui --help

# 4. Configuración existe
ls -la ~/.config/blugon/gamma

# 5. Filtro aplica
blugon-lite --once && echo "Filtro aplicado correctamente"
```

Si todos los comandos funcionan, ¡la instalación fue exitosa! 🎉

# blugon-lite

Blue Light Filter for X Window System - **Minimalist Version**

A lightweight fork of [blugon](https://github.com/jumper149/blugon) that reduces RAM consumption and code complexity while maintaining core functionality.

## Features

- ✅ Automatic blue light filtering based on time of day
- ✅ Customizable gamma/temperature schedules
- ✅ Two backends: scg (Xrandr) and xgamma
- ✅ Daemon mode or one-time application
- ✅ **< 8MB RAM** consumption (vs ~15MB original)
- ✅ **202 lines of code** (vs ~450 original)

## Differences from blugon

### Removed Features

| Feature | Reason |
|---------|--------|
| `--fade` | Smooth startup transition (unnecessary) |
| `--simulation` | Day simulation mode (debug only) |
| `--waitforx` | Wait for X server (edge case) |
| `--readcurrent` / `--setcurrent` | Current temperature file (complexity) |
| `--verbose` | Verbose logging (debug only) |
| `--printconfig` | Print default config (unnecessary) |
| TTY backend | Virtual console support (not needed for X) |

### Maintained Features

- All core gamma filtering functionality
- Time-based interpolation
- Custom configuration files
- Backend selection (scg/xgamma)
- Daemon mode with configurable interval

## Installation

### Dependencies

- **Python 3.6+**
- **libx11** and **libxrandr** development files
- **gcc** (for building scg backend)
- **xorg-xgamma** (optional, for xgamma backend)

### From Source

```bash
# Build
make

# Install (as root)
sudo make install
```

### Arch Linux

Available via AUR (coming soon).

## Usage

### Basic Usage

```bash
# Run as daemon (updates every 120 seconds)
blugon-lite

# Run once and exit
blugon-lite --once

# Run in background
(blugon-lite &)

# Stop
killall blugon-lite
```

### Options

```
-v, --version           Print version and exit
-o, --once              Apply configuration once and exit
-i, --interval [secs]   Set refresh interval (default: 120)
-c, --configdir [path]  Set configuration directory
-b, --backend [name]    Set backend: scg or xgamma (default: scg)
```

### Examples

```bash
# Use xgamma backend instead of scg
blugon-lite --backend xgamma

# Refresh every 60 seconds
blugon-lite --interval 60

# Use custom configuration directory
blugon-lite --configdir ~/.config/blugon-custom

# Apply current settings once (useful for testing)
blugon-lite --once
```

## Configuration

### Setup

```bash
# Create configuration directory
mkdir -p ~/.config/blugon

# Copy evening schedule (included)
cp /usr/share/blugon-lite/configs/evening/gamma ~/.config/blugon/gamma
```

### Gamma File Format

Location: `~/.config/blugon/gamma`

Two formats supported:

**Format 1: Temperature (Kelvin)**
```
# hour minute temperature
8 0 6500
17 0 4500
21 0 3000
0 0 2000
```

**Format 2: RGB Gamma values (0.0 - 1.0)**
```
# hour minute red green blue
8 0 1.0 1.0 1.0
17 0 1.0 0.9 0.8
21 0 1.0 0.8 0.6
```

### Example Schedule (Evening)

The included `evening/gamma` provides:

| Time | Temperature | Description |
|------|-------------|-------------|
| 08:00 | 6500K | Daylight (normal) |
| 17:00 | 4500K | Evening transition |
| 21:00 | 3000K | Warm evening |
| 00:00 | 2000K | Night mode (minimal blue) |
| 06:00 | 2500K | Early morning |

## Systemd Service

Create `~/.config/systemd/user/blugon-lite.service`:

```ini
[Unit]
Description=Blue Light Filter (lite)
After=graphical-session.target

[Service]
Type=simple
ExecStart=%h/.local/bin/blugon-lite
Restart=always

[Install]
WantedBy=default.target
```

Enable with:
```bash
systemctl --user enable blugon-lite.service
systemctl --user start blugon-lite.service
```

## Performance

| Metric | blugon | blugon-lite |
|--------|--------|-------------|
| Lines of code | ~450 | 202 |
| RAM usage | ~15MB | < 8MB |
| Features | Full | Core only |
| Backends | 3 (scg, xgamma, tty) | 2 (scg, xgamma) |

## Troubleshooting

### "Config directory not found"

Create the directory and copy a gamma file:
```bash
mkdir -p ~/.config/blugon
cp /usr/share/blugon-lite/configs/evening/gamma ~/.config/blugon/gamma
```

### "Cannot open display"

Ensure DISPLAY is set:
```bash
export DISPLAY=:0
blugon-lite --once
```

### Backend fails

Try the alternative backend:
```bash
blugon-lite --backend xgamma --once
```

## License

Apache-2.0 (same as original blugon)

## Acknowledgments

- Original [blugon](https://github.com/jumper149/blugon) by jumper149
- Temperature to RGB algorithm by [Tanner Helland](http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/)

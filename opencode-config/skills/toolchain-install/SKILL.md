---
name: toolchain-install
description: Install cross-compilation toolchains for m68k, ARM (STM32), and AVR using tcman
---
# Toolchain Installation Skill

## Description
Provides instructions for installing cross-compilation development toolchains using the **tcman** toolchain manager. Supports multiple embedded targets:

- **m68k-elf** — Motorola 68000 / CPU32 / ColdFire (e.g. MC68331)
- **arm-none-eabi** — ARM Cortex-M (e.g. STM32)
- **avr** — Atmel AVR (e.g. Arduino)

## tcman Toolchain Manager

`tcman` manages cross-compilation toolchains from `github.com/haarer/toolchain68k`. It handles downloading, installing, and removing toolchains in `/opt`.

### Installation

Download `tcman` from GitHub and install it to your PATH:

```bash
curl -sL https://raw.githubusercontent.com/haarer/tcman/main/tcman.sh -o tcman.sh
sudo cp tcman.sh /usr/local/bin/tcman
sudo chmod +x /usr/local/bin/tcman
```

### Commands

```bash
# List installed toolchains
tcman list

# List available toolchains from GitHub releases
tcman available

# Install a toolchain (requires root)
sudo tcman install m68k-elf
sudo tcman install arm-none-eabi
sudo tcman install avr

# Remove a toolchain (requires root)
sudo tcman remove m68k-elf

# Interactive menu
tcman
```

### Supported Targets

| Target | Description |
|--------|-------------|
| `m68k-elf` | Motorola 68000 / CPU32 / ColdFire |
| `arm-none-eabi` | ARM Cortex-M (STM32, etc.) |
| `avr` | Atmel AVR (Arduino, etc.) |

Toolchains include: GCC, Binutils, GDB, and Newlib.

### Directory Structure

Toolchains are installed as subdirectories in `/opt`:

```
/opt/
├── toolchain-m68k-elf-current/
│   ├── bin/
│   ├── include/
│   ├── lib/
│   ├── m68k-elf/
│   ├── share/
│   └── package.json
├── toolchain-arm-none-eabi-current/
└── toolchain-avr-current/
```

Only one version per target can be installed at a time. Installing a newer version replaces the existing one.

### Platform Support

`tcman` auto-detects the platform (glibc-based Linux or Alpine/musl) and fetches the matching binary from GitHub releases. No manual platform checks needed.

### Using Installed Toolchains

Add the `bin` directory to your PATH:

```bash
export PATH=$PATH:/opt/toolchain-m68k-elf-current/bin       # m68k
export PATH=$PATH:/opt/toolchain-arm-none-eabi-current/bin   # ARM Cortex-M
export PATH=$PATH:/opt/toolchain-avr-current/bin             # AVR
```

Or use directly:

```bash
/opt/toolchain-m68k-elf-current/bin/m68k-elf-gcc -o firmware.elf main.c
/opt/toolchain-arm-none-eabi-current/bin/arm-none-eabi-gcc -c main.c
/opt/toolchain-avr-current/bin/avr-gcc -mmcu=atmega328p main.c -o firmware.elf
```

## Workflow

1. **Install tcman** (if not already in PATH)
2. **Check available toolchains**: `tcman available`
3. **Install desired toolchain**: `sudo tcman install m68k-elf`
4. **Verify installation**: `tcman list`
5. **Add to PATH** or use full paths to tools

## Requirements

- bash
- curl or wget
- tar
- gzip
- root (for install/remove to /opt)

## Runtime Library Dependencies

The prebuilt toolchain binaries (gcc, cc1, etc.) are dynamically linked and require shared libraries on the host system. On Alpine Linux (musl), install these before using the toolchain:

```bash
apk add gmp mpfr4 mpc1 isl25
```

On glibc-based distributions (Debian/Ubuntu), install:

```bash
apt install libgmp10 libmpfr6 libmpc3 libisl23
```

Missing these libraries will cause errors like `libisl.so.23: No such file or directory` or symbol-not-found errors when invoking `m68k-elf-gcc`.

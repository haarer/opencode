---
name: m68k-analysis
description: Analyze MC68331 CPU32 binaries
---
# M68K Binary Analysis Skill

## Description
Provides specialized instructions for analyzing MC68331 (CPU32) and other m68k binaries. Integrates with the cross-compilation toolchain at `/opt/toolchain/` for disassembly and analysis.

## Commands

### Disassemble a binary
```bash
disasm.py <binary> -d [-b <base_addr>] [-s intel|att]
```
Disassemble binary code starting at optional base address.

### Full binary analysis
```bash
disasm.py <binary> -a [-j]
```
Shows file info, sections, symbols, strings, and relocations. Use `-j` for JSON output.

### Find function boundaries
```bash
disasm.py <binary> -f [-b <base_addr>]
```
Identifies function start/end using objdump control flow analysis.

### Direct toolchain commands
```bash
export PATH=/opt/toolchain/bin:$PATH
m68k-elf-objdump -d -m m68k:68000 <binary>
m68k-elf-nm -n <binary>
m68k-elf-readelf -r <binary>
```

## Workflow

1. **Identify binary type**: Run `file <binary>` or analysis `-a`
2. **Find entry point**: Check for `_start`, `main`, or reset vector at 0x0
3. **Map sections**: Identify .text (code), .data, .rodata, .bss
4. **Analyze functions**: Use `-f` to find functions, then `-d` to disassemble specific ranges
5. **Extract strings**: Look for embedded strings, error messages, symbols
6. **Check relocations**: Identify external references that need fixing

## CPU32/MC68331 Specifics

- 32-bit processor with 68000 instruction set (no 020+ instructions)
- Memory map typically starts at 0x0 with RAM/ROM
- Peripherals at high addresses (e.g., 0xFFFFF400 for GPT)
- Reset vector at 0x0 (startup code location)
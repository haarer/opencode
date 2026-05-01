#!/usr/bin/env python3
"""
M68K Binary Disassembler and Analyzer
Integrates with opencode for AI-powered binary analysis
"""

import argparse
import subprocess
import sys
import os
import re
from pathlib import Path

TOOLCHAIN_PATH = "/opt/toolchain/bin"
PREFIX = "m68k-elf-"

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr

def disassemble(binary_path, base_addr=0x0, syntax="att"):
    """Disassemble a binary file using objdump"""
    if not os.path.exists(binary_path):
        return None, f"File not found: {binary_path}"
    
    cmd = [
        f"{TOOLCHAIN_PATH}/{PREFIX}objdump",
        "-D", "-b", "binary", "-m", "m68k:68000",
        "-M", "reg-names裸, aliases",
        f"--start-address={base_addr}",
        "-m", "m68k:68000"
    ]
    if syntax == "intel":
        cmd.append("-M")
        cmd.append("intel")
    
    cmd.extend(["-D", binary_path])
    
    stdout, stderr = run_cmd(cmd)
    return stdout, stderr

def analyze_binary(binary_path):
    """Perform comprehensive binary analysis"""
    results = {
        "file_info": {},
        "sections": [],
        "symbols": [],
        "strings": [],
        "relocations": [],
        "header": {}
    }
    
    cmd_prefix = f"{TOOLCHAIN_PATH}/{PREFIX}"
    
    file_info_cmd = ["file", binary_path]
    stdout, _ = run_cmd(file_info_cmd)
    results["file_info"]["type"] = stdout.strip()
    
    try:
        size = os.path.getsize(binary_path)
        results["file_info"]["size"] = size
    except:
        pass
    
    objdump_cmd = [f"{cmd_prefix}objdump", "-h", binary_path]
    stdout, _ = run_cmd(objdump_cmd)
    if stdout:
        results["sections"] = parse_sections(stdout)
    
    nm_cmd = [f"{cmd_prefix}nm", "-n", binary_path]
    stdout, _ = run_cmd(nm_cmd)
    if stdout:
        results["symbols"] = parse_symbols(stdout)
    
    strings_cmd = ["strings", "-t", "x", binary_path]
    stdout, _ = run_cmd(strings_cmd)
    if stdout:
        results["strings"] = parse_strings(stdout)
    
    readelf_cmd = [f"{cmd_prefix}readelf", "-r", binary_path]
    stdout, _ = run_cmd(readelf_cmd)
    if stdout:
        results["relocations"] = parse_relocations(stdout)
    
    objdump_elf_cmd = [f"{cmd_prefix}objdump", "-f", binary_path]
    stdout, _ = run_cmd(objdump_elf_cmd)
    if stdout:
        results["header"] = parse_header(stdout)
    
    return results

def parse_sections(output):
    sections = []
    for line in output.split('\n'):
        if line.strip() and not line.startswith('Sections:'):
            parts = line.split()
            if len(parts) >= 6:
                sections.append({
                    "idx": parts[0] if parts[0].isdigit() else "0",
                    "name": parts[1],
                    "type": parts[2] if len(parts) > 2 else "UNKNOWN",
                    "addr": parts[3] if len(parts) > 3 else "0",
                    "off": parts[4] if len(parts) > 4 else "0",
                    "size": parts[5] if len(parts) > 5 else "0"
                })
    return sections

def parse_symbols(output):
    symbols = []
    for line in output.split('\n'):
        parts = line.split()
        if len(parts) >= 3:
            addr = parts[0] if re.match(r'^[0-9a-fA-F]+$', parts[0]) else "0"
            sym_type = parts[1] if len(parts) > 1 else "?"
            name = ' '.join(parts[2:])
            symbols.append({
                "addr": addr,
                "type": sym_type,
                "name": name
            })
    return symbols

def parse_strings(output):
    strings = []
    for line in output.split('\n'):
        parts = line.split(None, 1)
        if len(parts) >= 2:
            addr = parts[0]
            text = parts[1]
            strings.append({
                "addr": addr,
                "text": text
            })
    return strings

def parse_relocations(output):
    relocs = []
    in_rela = False
    for line in output.split('\n'):
        if 'Relocation section' in line:
            in_rela = True
            continue
        if in_rela and line.strip() and not line.startswith('Offset'):
            parts = line.split()
            if len(parts) >= 4:
                relocs.append({
                    "offset": parts[0],
                    "info": parts[1],
                    "type": parts[2] if len(parts) > 2 else "?",
                    "sym": ' '.join(parts[3:]) if len(parts) > 3 else ""
                })
    return relocs

def parse_header(output):
    header = {}
    for line in output.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            header[key.strip()] = val.strip()
    return header

def find_functions(binary_path, base_addr=0x0):
    """Identify function boundaries using objdump"""
    cmd = [
        f"{TOOLCHAIN_PATH}/{PREFIX}objdump",
        "-d", "-b", "binary", "-m", "m68k:68000",
        f"--start-address={base_addr}",
        binary_path
    ]
    stdout, _ = run_cmd(cmd)
    
    functions = []
    current_func = None
    
    for line in stdout.split('\n'):
        addr_match = re.match(r'\s*([0-9a-f]+) <(\S+)>:', line)
        if addr_match:
            if current_func:
                current_func["end"] = addr_match.group(1)
            addr = int(addr_match.group(1), 16)
            current_func = {
                "addr": f"0x{addr:08x}",
                "name": addr_match.group(2),
                "instructions": []
            }
            functions.append(current_func)
        
        elif current_func and line.strip():
            parts = line.strip().split(':', 1)
            if len(parts) == 2:
                inst = parts[1].strip()
                if inst:
                    current_func["instructions"].append(inst)
                    if inst.startswith('rts') or inst.startswith('rtd'):
                        current_func["end"] = parts[0]
    
    if current_func:
        current_func["end"] = current_func.get("addr", "unknown")
    
    return functions

def main():
    parser = argparse.ArgumentParser(
        description="M68K Binary Disassembler and Analyzer for CPU32/MC68331"
    )
    parser.add_argument("binary", help="Binary file to analyze")
    parser.add_argument("-d", "--disasm", action="store_true", help="Disassemble code")
    parser.add_argument("-a", "--analyze", action="store_true", help="Full analysis")
    parser.add_argument("-f", "--functions", action="store_true", help="Find functions")
    parser.add_argument("-b", "--base", type=lambda x: int(x, 0), default=0x0,
                        help="Base address (hex)")
    parser.add_argument("-s", "--syntax", choices=["att", "intel"], default="att",
                        help="Assembly syntax")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-j", "--json", action="store_true", help="JSON output")
    
    args = parser.parse_args()
    
    if args.analyze:
        import json
        results = analyze_binary(args.binary)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"=== Binary Analysis: {args.binary} ===")
            print(f"\nFile Info:")
            for k, v in results["file_info"].items():
                print(f"  {k}: {v}")
            
            print(f"\nSections:")
            for sec in results["sections"]:
                print(f"  {sec['name']}: addr={sec['addr']} size={sec['size']}")
            
            print(f"\nSymbols ({len(results['symbols'])}):")
            for sym in results['symbols'][:20]:
                print(f"  {sym['addr']} {sym['type']} {sym['name']}")
            if len(results['symbols']) > 20:
                print(f"  ... and {len(results['symbols']) - 20} more")
            
            print(f"\nStrings ({len(results['strings'])}):")
            for s in results['strings'][:20]:
                print(f"  {s['addr']}: {s['text']}")
            if len(results['strings']) > 20:
                print(f"  ... and {len(results['strings']) - 20} more")
    
    elif args.disasm:
        output, error = disassemble(args.binary, args.base, args.syntax)
        if error:
            print(f"Error: {error}", file=sys.stderr)
        if output:
            print(output)
    
    elif args.functions:
        funcs = find_functions(args.binary, args.base)
        print(f"=== Functions found: {len(funcs)} ===")
        for f in funcs:
            print(f"  {f['addr']} {f['name']} ({len(f['instructions'])} instructions)")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
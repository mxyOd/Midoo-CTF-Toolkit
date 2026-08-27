#!/usr/bin/env python3

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


BANNER = r"""
=============================================
            Midoo Pwn Toolkit v1.0
=============================================
"""


def command_exists(command):
    return shutil.which(command) is not None


def run_command(command, timeout=20):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return 127, "", f"{command[0]}: command not found"
    except subprocess.TimeoutExpired:
        return 124, "", "Command timed out"


def checksec(binary):
    print("\n[+] Security Protections")

    if command_exists("checksec"):
        rc, out, err = run_command(["checksec", "--file=" + str(binary)])
        if out:
            print(out.strip())
        else:
            print(err.strip())
        return

    # Fallback using readelf when checksec is unavailable.
    if not command_exists("readelf"):
        print("[-] checksec dan readelf tidak ditemukan.")
        return

    rc, program_headers, _ = run_command(
        ["readelf", "-W", "-l", str(binary)]
    )
    rc2, sections, _ = run_command(
        ["readelf", "-W", "-S", str(binary)]
    )

    relro = "No RELRO"
    if "GNU_RELRO" in program_headers:
        relro = "Partial RELRO"
        if "BIND_NOW" in program_headers or "NOW" in sections:
            relro = "Full RELRO"

    nx = "NX: Enabled"
    if "GNU_STACK" in program_headers:
        stack_lines = [
            line for line in program_headers.splitlines()
            if "GNU_STACK" in line
        ]
        if stack_lines and "RWE" in stack_lines[0]:
            nx = "NX: Disabled"

    pie = "PIE: Unknown"
    if command_exists("readelf"):
        rc3, header, _ = run_command(
            ["readelf", "-h", str(binary)]
        )
        if "DYN (Shared object file)" in header:
            pie = "PIE: Enabled"
        elif "EXEC (Executable file)" in header:
            pie = "PIE: Disabled"

    canary = "Canary: Unknown"
    rc4, symbols, _ = run_command(
        ["readelf", "-Ws", str(binary)]
    )
    if "__stack_chk_fail" in symbols:
        canary = "Canary: Found"
    else:
        canary = "Canary: Not found"

    print(f"  {relro}")
    print(f"  {nx}")
    print(f"  {pie}")
    print(f"  {canary}")


def elf_info(binary):
    print("\n[+] ELF Information")

    if not command_exists("readelf"):
        print("[-] readelf tidak ditemukan.")
        return

    rc, out, err = run_command(
        ["readelf", "-h", str(binary)]
    )

    if rc != 0:
        print(err.strip())
        return

    wanted = {
        "Class:",
        "Data:",
        "Type:",
        "Machine:",
        "Entry point address:",
    }

    for line in out.splitlines():
        stripped = line.strip()

        if any(stripped.startswith(item) for item in wanted):
            print("  " + stripped)


def sections(binary):
    print("\n[+] ELF Sections")

    if not command_exists("readelf"):
        print("[-] readelf tidak ditemukan.")
        return

    rc, out, err = run_command(
        ["readelf", "-W", "-S", str(binary)]
    )

    if rc != 0:
        print(err.strip())
        return

    for line in out.splitlines():
        if re.search(r"\[\s*\d+\]\s+\S+", line):
            print("  " + line.strip())


def symbols(binary):
    print("\n[+] Symbols")

    if not command_exists("readelf"):
        print("[-] readelf tidak ditemukan.")
        return

    rc, out, err = run_command(
        ["readelf", "-Ws", str(binary)]
    )

    if rc != 0:
        print(err.strip())
        return

    count = 0

    for line in out.splitlines():
        if re.search(
            r"\bFUNC\b|\bOBJECT\b|\bNOTYPE\b",
            line
        ):
            print("  " + line.strip())
            count += 1

            if count >= 100:
                print("  ... output dibatasi 100 baris.")
                break


def plt_got(binary):
    print("\n[+] PLT / GOT")

    if not command_exists("objdump"):
        print("[-] objdump tidak ditemukan.")
        return

    rc, out, err = run_command(
        ["objdump", "-d", "-j", ".plt", str(binary)]
    )

    if rc == 0 and out.strip():
        print("\n--- PLT ---")
        print(out.strip())

    if command_exists("readelf"):
        rc, out, err = run_command(
            ["readelf", "-r", str(binary)]
        )

        if rc == 0 and out.strip():
            print("\n--- Relocations / GOT ---")
            print(out.strip())


def strings_scan(binary, minimum=6):
    print("\n[+] Strings")

    if command_exists("strings"):
        rc, out, err = run_command(
            ["strings", "-n", str(minimum), str(binary)]
        )

        if rc == 0:
            lines = out.splitlines()

            for line in lines[:200]:
                print("  " + line)

            if len(lines) > 200:
                print("  ... output dibatasi 200 baris.")

            return

    print("[-] strings tidak ditemukan.")


def rop_gadgets(binary):
    print("\n[+] ROP Gadgets")

    if command_exists("ROPgadget"):
        rc, out, err = run_command(
            ["ROPgadget", "--binary", str(binary)],
            timeout=60,
        )

        if rc == 0:
            lines = out.splitlines()

            for line in lines[:200]:
                print("  " + line)

            if len(lines) > 200:
                print("  ... output dibatasi 200 baris.")

            return

        print(err.strip())
        return

    if command_exists("ropper"):
        rc, out, err = run_command(
            ["ropper", "--file", str(binary), "--nocolor"],
            timeout=60,
        )

        if rc == 0:
            lines = out.splitlines()

            for line in lines[:200]:
                print("  " + line)

            if len(lines) > 200:
                print("  ... output dibatasi 200 baris.")

            return

        print(err.strip())
        return

    print(
        "[-] ROPgadget/ropper tidak ditemukan."
        "\n    Install salah satu tool tersebut untuk fitur ROP."
    )


def search_hex(binary, pattern):
    print("\n[+] Hex Pattern Search")

    try:
        raw = bytes.fromhex(pattern.replace(" ", ""))
    except ValueError:
        print("[-] Pattern bukan hexadecimal yang valid.")
        return

    data = Path(binary).read_bytes()

    offsets = []
    start = 0

    while True:
        position = data.find(raw, start)

        if position == -1:
            break

        offsets.append(position)
        start = position + 1

    if not offsets:
        print("[-] Pattern tidak ditemukan.")
        return

    print(f"[✓] Ditemukan {len(offsets)} kecocokan.")

    for offset in offsets[:100]:
        print(f"  0x{offset:x}")

    if len(offsets) > 100:
        print("  ... output dibatasi 100 offset.")


def analyze(binary, args):
    print(BANNER)

    print(f"File : {binary}")
    print(f"Size : {binary.stat().st_size} bytes")

    if args.info:
        elf_info(binary)

    if args.checksec:
        checksec(binary)

    if args.sections:
        sections(binary)

    if args.symbols:
        symbols(binary)

    if args.pltgot:
        plt_got(binary)

    if args.strings:
        strings_scan(binary, args.min_string)

    if args.rop:
        rop_gadgets(binary)

    if args.hex:
        search_hex(binary, args.hex)

    if not any([
        args.info,
        args.checksec,
        args.sections,
        args.symbols,
        args.pltgot,
        args.strings,
        args.rop,
        args.hex,
    ]):
        elf_info(binary)
        checksec(binary)
        sections(binary)
        symbols(binary)
        plt_got(binary)


def main():
    parser = argparse.ArgumentParser(
        prog="pwn_tool.py",
        description=(
            "Midoo Pwn Toolkit - ELF dan binary analysis "
            "untuk CTF/lab"
        ),
        epilog=(
            "Contoh:\n"
            "  python pwn_tool.py -f ./chall\n"
            "  python pwn_tool.py -f ./chall --checksec\n"
            "  python pwn_tool.py -f ./chall --symbols --pltgot\n"
            "  python pwn_tool.py -f ./chall --rop\n"
            "  python pwn_tool.py -f ./chall --strings\n"
            "  python pwn_tool.py -f ./chall --hex '90 90'\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path ke ELF/binary target",
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Tampilkan informasi ELF",
    )

    parser.add_argument(
        "--checksec",
        action="store_true",
        help="Periksa security protections",
    )

    parser.add_argument(
        "--sections",
        action="store_true",
        help="Tampilkan section ELF",
    )

    parser.add_argument(
        "--symbols",
        action="store_true",
        help="Tampilkan symbol table",
    )

    parser.add_argument(
        "--pltgot",
        action="store_true",
        help="Tampilkan PLT dan relocation/GOT",
    )

    parser.add_argument(
        "--strings",
        action="store_true",
        help="Tampilkan printable strings",
    )

    parser.add_argument(
        "--min-string",
        type=int,
        default=6,
        help="Minimum panjang strings (default: 6)",
    )

    parser.add_argument(
        "--rop",
        action="store_true",
        help="Cari ROP gadgets menggunakan ROPgadget/ropper",
    )

    parser.add_argument(
        "--hex",
        help="Cari byte pattern hexadecimal, contoh: '48 89 e5'",
    )

    args = parser.parse_args()

    binary = Path(args.file)

    if not binary.is_file():
        print(f"[!] File tidak ditemukan: {binary}")
        return 1

    if not os.access(binary, os.R_OK):
        print(f"[!] File tidak dapat dibaca: {binary}")
        return 1

    analyze(binary, args)

    print("\n=============================================")
    print("              ANALYSIS DONE")
    print("=============================================")

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3

import argparse
import hashlib
import math
import os
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path


BANNER = r"""
=============================================
    Midoo Reverse Engineering Toolkit
                    v1.0
=============================================
"""


def tool_exists(name):
    return shutil.which(name) is not None


def run_command(command, timeout=30):
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


def sha256_file(path):
    digest = hashlib.sha256()

    with open(path, "rb") as file:
        while chunk := file.read(1024 * 1024):
            digest.update(chunk)

    return digest.hexdigest()


def entropy(data):
    if not data:
        return 0.0

    counts = [0] * 256

    for byte in data:
        counts[byte] += 1

    length = len(data)
    value = 0.0

    for count in counts:
        if count:
            probability = count / length
            value -= probability * math.log2(probability)

    return value


def detect_format(path):
    with open(path, "rb") as file:
        header = file.read(64)

    if header.startswith(b"\x7fELF"):
        return "ELF"

    if header.startswith(b"MZ"):
        return "PE/DOS"

    if header.startswith(b"\xCA\xFE\xBA\xBE"):
        return "Mach-O / Fat Binary"

    if header.startswith(b"\xCE\xFA\xED\xFE"):
        return "Mach-O 32-bit"

    if header.startswith(b"\xCF\xFA\xED\xFE"):
        return "Mach-O 64-bit"

    return "Unknown"


def basic_info(path):
    print("\n[+] File Information")

    print(f"  Name       : {path.name}")
    print(f"  Size       : {path.stat().st_size} bytes")
    print(f"  Format     : {detect_format(path)}")
    print(f"  SHA256     : {sha256_file(path)}")

    with open(path, "rb") as file:
        sample = file.read(1024 * 1024)

    print(f"  Entropy    : {entropy(sample):.4f}")


def elf_info(path):
    print("\n[+] ELF Information")

    if not tool_exists("readelf"):
        print("[-] readelf tidak ditemukan.")
        return

    rc, output, error = run_command(
        ["readelf", "-h", str(path)]
    )

    if rc != 0:
        print(error.strip())
        return

    fields = [
        "Class:",
        "Data:",
        "Type:",
        "Machine:",
        "Entry point address:",
        "Start of program headers:",
        "Start of section headers:",
    ]

    for line in output.splitlines():
        line = line.strip()

        if any(line.startswith(field) for field in fields):
            print("  " + line)


def pe_info(path):
    print("\n[+] PE Information")

    try:
        with open(path, "rb") as file:
            data = file.read()

        if data[:2] != b"MZ":
            print("[-] Bukan file PE/MZ.")
            return

        pe_offset = struct.unpack_from("<I", data, 0x3C)[0]

        if data[pe_offset:pe_offset + 4] != b"PE\x00\x00":
            print("[-] PE signature tidak ditemukan.")
            return

        machine = struct.unpack_from(
            "<H",
            data,
            pe_offset + 4
        )[0]

        sections = struct.unpack_from(
            "<H",
            data,
            pe_offset + 6
        )[0]

        timestamp = struct.unpack_from(
            "<I",
            data,
            pe_offset + 8
        )[0]

        optional_size = struct.unpack_from(
            "<H",
            data,
            pe_offset + 20
        )[0]

        optional_offset = pe_offset + 24

        magic = struct.unpack_from(
            "<H",
            data,
            optional_offset
        )[0]

        subsystem = None

        if optional_size >= 70:
            subsystem = struct.unpack_from(
                "<H",
                data,
                optional_offset + 68
            )[0]

        machine_names = {
            0x014C: "x86",
            0x8664: "x64",
            0x01C0: "ARM",
            0xAA64: "ARM64",
        }

        print(f"  Machine    : {machine_names.get(machine, hex(machine))}")
        print(f"  Sections   : {sections}")
        print(f"  Timestamp  : {timestamp}")
        print(f"  PE Magic   : 0x{magic:04x}")

        if subsystem is not None:
            print(f"  Subsystem  : {subsystem}")

    except (OSError, struct.error) as error:
        print(f"[-] Gagal membaca PE: {error}")


def sections(path):
    print("\n[+] Sections")

    if detect_format(path) == "ELF" and tool_exists("readelf"):
        rc, output, error = run_command(
            ["readelf", "-W", "-S", str(path)]
        )

        if rc == 0:
            print(output.strip())
        else:
            print(error.strip())

        return

    if detect_format(path) in ("PE/DOS",) and tool_exists("objdump"):
        rc, output, error = run_command(
            ["objdump", "-h", str(path)]
        )

        if rc == 0:
            print(output.strip())
        else:
            print(error.strip())

        return

    print("[-] Tidak ada parser section yang sesuai.")


def strings_scan(path, minimum=6):
    print("\n[+] Printable Strings")

    if not tool_exists("strings"):
        print("[-] strings tidak ditemukan.")
        return

    rc, output, error = run_command(
        ["strings", "-n", str(minimum), str(path)],
        timeout=60,
    )

    if rc != 0:
        print(error.strip())
        return

    lines = output.splitlines()

    for line in lines[:300]:
        print("  " + line)

    if len(lines) > 300:
        print("  ... output dibatasi 300 baris.")


def imports_exports(path):
    print("\n[+] Imports / Exports")

    fmt = detect_format(path)

    if fmt == "ELF" and tool_exists("readelf"):
        rc, output, error = run_command(
            ["readelf", "-Ws", str(path)]
        )

        if rc == 0:
            for line in output.splitlines():
                if " UND " in line or "FUNC" in line:
                    print("  " + line.strip())
        else:
            print(error.strip())

    elif fmt == "PE/DOS" and tool_exists("objdump"):
        rc, output, error = run_command(
            ["objdump", "-p", str(path)]
        )

        if rc == 0:
            lines = output.splitlines()
            show = False

            for line in lines:
                if "DLL Name" in line or "Export Table" in line:
                    show = True

                if show:
                    print("  " + line)

            if not show:
                print("[-] Import/export information tidak ditemukan.")

        else:
            print(error.strip())

    else:
        print("[-] Format belum didukung untuk fitur ini.")


def disassemble(path):
    print("\n[+] Disassembly")

    if not tool_exists("objdump"):
        print("[-] objdump tidak ditemukan.")
        return

    rc, output, error = run_command(
        [
            "objdump",
            "-d",
            "-M",
            "intel",
            str(path),
        ],
        timeout=60,
    )

    if rc != 0:
        print(error.strip())
        return

    lines = output.splitlines()

    for line in lines[:500]:
        print(line)

    if len(lines) > 500:
        print("\n... output dibatasi 500 baris.")


def find_patterns(path, pattern):
    print("\n[+] Pattern Search")

    data = path.read_bytes()

    try:
        regex = re.compile(pattern.encode())
    except re.error as error:
        print(f"[-] Regex tidak valid: {error}")
        return

    matches = list(regex.finditer(data))

    if not matches:
        print("[-] Pattern tidak ditemukan.")
        return

    print(f"[✓] Ditemukan {len(matches)} kecocokan.")

    for match in matches[:100]:
        print(f"  Offset: 0x{match.start():x}")

    if len(matches) > 100:
        print("  ... output dibatasi 100 hasil.")


def scan_embedded_strings(path):
    print("\n[+] Interesting Embedded Content")

    data = path.read_bytes()

    signatures = {
        b"PK\x03\x04": "ZIP",
        b"\x89PNG\r\n\x1a\n": "PNG",
        b"\xff\xd8\xff": "JPEG",
        b"%PDF": "PDF",
        b"7z\xbc\xaf\x27\x1c": "7-Zip",
        b"Rar!\x1a\x07": "RAR",
    }

    found = []

    for signature, name in signatures.items():
        offset = data.find(signature)

        if offset != -1:
            found.append((name, offset))

    if not found:
        print("[-] Signature embedded yang dikenal tidak ditemukan.")
        return

    for name, offset in found:
        print(f"  [+] {name} pada offset 0x{offset:x}")


def analyze(path, args):
    print(BANNER)

    basic_info(path)

    if args.info:
        fmt = detect_format(path)

        if fmt == "ELF":
            elf_info(path)
        elif fmt == "PE/DOS":
            pe_info(path)
        else:
            print("\n[!] Format binary tidak dikenali sebagai ELF/PE.")

    if args.sections:
        sections(path)

    if args.strings:
        strings_scan(path, args.min_string)

    if args.imports:
        imports_exports(path)

    if args.disasm:
        disassemble(path)

    if args.pattern:
        find_patterns(path, args.pattern)

    if args.embedded:
        scan_embedded_strings(path)

    if not any([
        args.info,
        args.sections,
        args.strings,
        args.imports,
        args.disasm,
        args.pattern,
        args.embedded,
    ]):
        print("\n[i] Mode default: informasi dasar + format binary.")

        fmt = detect_format(path)

        if fmt == "ELF":
            elf_info(path)
        elif fmt == "PE/DOS":
            pe_info(path)


def main():
    parser = argparse.ArgumentParser(
        prog="re_tool.py",
        description=(
            "Midoo Reverse Engineering Toolkit - "
            "static binary analysis untuk CTF/lab"
        ),
        epilog="""
Contoh:
  python re_tool.py -f ./chall
  python re_tool.py -f ./chall --info
  python re_tool.py -f ./chall --sections
  python re_tool.py -f ./chall --strings
  python re_tool.py -f ./chall --imports
  python re_tool.py -f ./chall --disasm
  python re_tool.py -f ./chall --embedded
  python re_tool.py -f ./chall --pattern "flag"
  python re_tool.py -f ./program.exe --info
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path ke binary/ELF/PE",
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Tampilkan informasi format dan metadata binary",
    )

    parser.add_argument(
        "--sections",
        action="store_true",
        help="Tampilkan section binary",
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
        help="Minimum panjang string (default: 6)",
    )

    parser.add_argument(
        "--imports",
        action="store_true",
        help="Analisis imports/symbols dan exports",
    )

    parser.add_argument(
        "--disasm",
        action="store_true",
        help="Tampilkan disassembly menggunakan objdump",
    )

    parser.add_argument(
        "--pattern",
        help="Cari regex ASCII dalam binary",
    )

    parser.add_argument(
        "--embedded",
        action="store_true",
        help="Cari signature file yang tertanam",
    )

    args = parser.parse_args()

    path = Path(args.file)

    if not path.is_file():
        print(f"[!] File tidak ditemukan: {path}")
        return 1

    if not os.access(path, os.R_OK):
        print(f"[!] File tidak dapat dibaca: {path}")
        return 1

    try:
        analyze(path, args)
    except KeyboardInterrupt:
        print("\n[!] Analisis dihentikan.")
        return 130
    except Exception as error:
        print(f"\n[!] Error: {error}")
        return 1

    print("\n=============================================")
    print("              ANALYSIS DONE")
    print("=============================================")

    return 0


if __name__ == "__main__":
    sys.exit(main())

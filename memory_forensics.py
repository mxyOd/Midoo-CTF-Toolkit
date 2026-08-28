#!/usr/bin/env python3

import argparse
import hashlib
import math
import os
import re
import shutil
import subprocess
from collections import Counter


def calculate_entropy(data):
    if not data:
        return 0.0

    counter = Counter(data)
    length = len(data)

    entropy = 0.0

    for count in counter.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy


def calculate_hash(path, algorithm):
    hasher = hashlib.new(algorithm)

    with open(path, "rb") as file:
        while True:
            chunk = file.read(1024 * 1024)

            if not chunk:
                break

            hasher.update(chunk)

    return hasher.hexdigest()


def extract_strings(data, minimum=4):
    pattern = rb"[\x20-\x7e]{%d,}" % minimum

    return [
        item.decode("utf-8", errors="replace")
        for item in re.findall(pattern, data)
    ]


def find_ips(data):
    pattern = rb"\b(?:\d{1,3}\.){3}\d{1,3}\b"

    results = set()

    for match in re.findall(pattern, data):
        try:
            ip = match.decode("ascii")

            parts = ip.split(".")

            if all(0 <= int(part) <= 255 for part in parts):
                results.add(ip)

        except (ValueError, UnicodeDecodeError):
            continue

    return sorted(results)


def find_urls(data):
    pattern = rb"https?://[^\s\"'<>]+"

    results = set()

    for match in re.findall(pattern, data, re.IGNORECASE):
        results.add(
            match.decode(
                "utf-8",
                errors="replace"
            )
        )

    return sorted(results)


def find_paths(data):
    patterns = [
        rb"[A-Za-z]:\\(?:[^\\\x00-\x1f]+\\?)+",
        rb"/(?:home|root|tmp|var|etc|opt|usr)/[^\x00\s]+",
    ]

    results = set()

    for pattern in patterns:
        for match in re.findall(pattern, data):
            results.add(
                match.decode(
                    "utf-8",
                    errors="replace"
                )
            )

    return sorted(results)


def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )

        return result.returncode, result.stdout, result.stderr

    except FileNotFoundError:
        return None, "", ""


def show_volatility():
    print("\n[+] Volatility")

    volatility = None

    for command in ["vol", "vol.py", "volatility3"]:
        path = shutil.which(command)

        if path:
            volatility = path
            break

    if not volatility:
        print("  [-] Volatility tidak ditemukan.")
        print("  [i] Install Volatility 3 jika diperlukan.")
        return

    print(f"  [✓] Volatility ditemukan: {volatility}")

    code, output, error = run_command(
        [volatility, "-h"]
    )

    if code == 0:
        print("  [✓] Volatility dapat dijalankan.")
    else:
        print("  [-] Volatility terdeteksi tetapi gagal dijalankan.")


def show_info(path, data):
    print("[+] Memory Dump Information")

    print(f"  Name       : {os.path.basename(path)}")
    print(f"  Path       : {os.path.abspath(path)}")
    print(f"  Size       : {len(data)} bytes")
    print(f"  Size       : {len(data) / (1024 * 1024):.2f} MB")
    print(f"  MD5        : {calculate_hash(path, 'md5')}")
    print(f"  SHA1       : {calculate_hash(path, 'sha1')}")
    print(f"  SHA256     : {calculate_hash(path, 'sha256')}")
    print(f"  Entropy    : {calculate_entropy(data):.4f}")


def show_strings(data):
    print("\n[+] Printable Strings")

    strings = extract_strings(data)

    if not strings:
        print("  Tidak ditemukan strings.")
        return

    for string in strings[:200]:
        print(f"  {string}")

    if len(strings) > 200:
        print(
            f"\n  ... {len(strings) - 200} strings lainnya"
        )


def show_ips(data):
    print("\n[+] IP Addresses")

    ips = find_ips(data)

    if not ips:
        print("  Tidak ditemukan IP address.")
        return

    for ip in ips:
        print(f"  {ip}")


def show_urls(data):
    print("\n[+] URLs")

    urls = find_urls(data)

    if not urls:
        print("  Tidak ditemukan URL.")
        return

    for url in urls:
        print(f"  {url}")


def show_paths(data):
    print("\n[+] File Paths")

    paths = find_paths(data)

    if not paths:
        print("  Tidak ditemukan path yang dikenali.")
        return

    for path in paths[:200]:
        print(f"  {path}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Midoo Memory Forensics - "
            "Static Memory Dump Analysis"
        )
    )

    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Memory dump yang akan dianalisis"
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Tampilkan informasi memory dump"
    )

    parser.add_argument(
        "--strings",
        action="store_true",
        help="Tampilkan printable strings"
    )

    parser.add_argument(
        "--ips",
        action="store_true",
        help="Cari IP addresses"
    )

    parser.add_argument(
        "--urls",
        action="store_true",
        help="Cari URLs"
    )

    parser.add_argument(
        "--paths",
        action="store_true",
        help="Cari file paths"
    )

    parser.add_argument(
        "--volatility",
        action="store_true",
        help="Periksa ketersediaan Volatility"
    )

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(
            f"[!] File tidak ditemukan: {args.file}"
        )
        return 1

    try:
        with open(args.file, "rb") as file:
            data = file.read()

    except PermissionError:
        print("[!] Tidak memiliki izin membaca file.")
        return 1

    print("=============================================")
    print("         Midoo Memory Forensics")
    print("                  v1.0")
    print("=============================================\n")

    show_info(args.file, data)

    no_option = not any(
        [
            args.info,
            args.strings,
            args.ips,
            args.urls,
            args.paths,
            args.volatility,
        ]
    )

    if no_option:
        print(
            "\n[i] Mode default: "
            "informasi dasar memory dump."
        )

    if args.strings:
        show_strings(data)

    if args.ips:
        show_ips(data)

    if args.urls:
        show_urls(data)

    if args.paths:
        show_paths(data)

    if args.volatility:
        show_volatility()

    print("\n=============================================")
    print("              ANALYSIS DONE")
    print("=============================================")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
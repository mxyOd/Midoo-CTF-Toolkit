#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
from pathlib import Path


SECTOR_SIZE = 512


def human_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"
        value /= 1024


def sha256_file(path):
    digest = hashlib.sha256()

    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            digest.update(chunk)

    return digest.hexdigest()


def read_mbr(path):
    with open(path, "rb") as f:
        mbr = f.read(SECTOR_SIZE)

    if len(mbr) < SECTOR_SIZE:
        raise ValueError("File terlalu kecil untuk menjadi disk image.")

    signature = mbr[510:512]

    partitions = []

    for index in range(4):
        offset = 446 + (index * 16)
        entry = mbr[offset:offset + 16]

        status = entry[0]
        partition_type = entry[4]
        start_lba = struct.unpack_from("<I", entry, 8)[0]
        sectors = struct.unpack_from("<I", entry, 12)[0]

        if partition_type != 0 and sectors != 0:
            partitions.append({
                "index": index + 1,
                "bootable": status == 0x80,
                "type_hex": f"0x{partition_type:02x}",
                "start_lba": start_lba,
                "sectors": sectors,
                "offset": start_lba * SECTOR_SIZE,
                "size": sectors * SECTOR_SIZE,
            })

    return {
        "signature": signature.hex(),
        "valid_mbr_signature": signature == b"\x55\xaa",
        "partitions": partitions,
    }


def detect_filesystem(path, offset=0):
    with open(path, "rb") as f:
        f.seek(offset)
        data = f.read(4096)

    checks = []

    if data[54:62] in (b"FAT12   ", b"FAT16   "):
        checks.append("FAT12/FAT16")

    if data[82:90] == b"FAT32   ":
        checks.append("FAT32")

    # NTFS signature is at offset 3 within the filesystem boot sector.
    if data[3:8] == b"NTFS ":
        checks.append("NTFS")

    # ext2/3/4 superblock magic: 0xEF53 at offset 0x438.
    if len(data) >= 0x43A:
        if data[0x438:0x43A] == b"\x53\xef":
            checks.append("ext2/ext3/ext4")

    if data[0:4] == b"XFSB":
        checks.append("XFS")

    if data[0:8] == b"_BHRfS_M":
        checks.append("Btrfs")

    return checks


def printable_strings(path, min_length=6, max_results=100):
    results = []
    pattern = re.compile(rb"[\x20-\x7e]{%d,}" % min_length)

    with open(path, "rb") as f:
        data = f.read()

    for match in pattern.finditer(data):
        value = match.group().decode("ascii", errors="replace")
        results.append({
            "offset": match.start(),
            "text": value,
        })

        if len(results) >= max_results:
            break

    return results


def run_sleuthkit(path, partitions):
    """
    Uses Sleuth Kit if installed:
      mmls -> partition information
      fls  -> recursive directory listing
    """
    mmls = shutil_which("mmls")
    fls = shutil_which("fls")

    result = {
        "available": bool(mmls and fls),
        "mmls": None,
        "fls": [],
    }

    if not mmls:
        return result

    try:
        completed = subprocess.run(
            [mmls, "-b", str(SECTOR_SIZE), str(path)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        result["mmls"] = completed.stdout
    except Exception as exc:
        result["mmls"] = f"Error: {exc}"

    if not fls:
        return result

    for part in partitions:
        try:
            # -o expects sector offset.
            completed = subprocess.run(
                [
                    fls,
                    "-r",
                    "-p",
                    "-o",
                    str(part["start_lba"]),
                    str(path),
                ],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )

            result["fls"].append({
                "partition": part["index"],
                "output": completed.stdout,
                "stderr": completed.stderr,
                "returncode": completed.returncode,
            })
        except Exception as exc:
            result["fls"].append({
                "partition": part["index"],
                "error": str(exc),
            })

    return result


def shutil_which(command):
    paths = os.environ.get("PATH", "").split(os.pathsep)

    extensions = [""]
    if os.name == "nt":
        extensions = os.environ.get("PATHEXT", ".EXE").split(os.pathsep)

    for directory in paths:
        for extension in extensions:
            candidate = Path(directory) / (command + extension)
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return str(candidate)

    return None


def print_tree_from_fls(fls_results):
    print("\n========================================")
    print("             FILESYSTEM TREE")
    print("========================================")

    printed = False

    for item in fls_results:
        output = item.get("output", "").strip()

        if not output:
            continue

        printed = True

        for line in output.splitlines():
            print(line)

    if not printed:
        print("[-] Directory tree belum tersedia.")
        print("[i] Install Sleuth Kit untuk analisis filesystem.")


def scan(args):
    image = Path(args.file)

    if not image.is_file():
        print(f"[!] File tidak ditemukan: {image}")
        return 1

    print("========================================")
    print("          Midoo Disk Forensics")
    print("========================================")

    print(f"\nFile   : {image}")
    print(f"Size   : {human_size(image.stat().st_size)}")
    print(f"SHA256 : {sha256_file(image)}")

    print("\n[•] Membaca MBR...")

    try:
        mbr = read_mbr(image)
    except Exception as exc:
        print(f"[!] Gagal membaca MBR: {exc}")
        return 1

    if mbr["valid_mbr_signature"]:
        print("[✓] MBR signature: 55 aa")
    else:
        print("[!] MBR signature tidak ditemukan.")

    partitions = mbr["partitions"]

    print(f"[✓] Partition ditemukan: {len(partitions)}")

    for part in partitions:
        print(
            f"\n  Partition {part['index']}"
            f"\n    Type       : {part['type_hex']}"
            f"\n    Bootable   : {part['bootable']}"
            f"\n    Start LBA  : {part['start_lba']}"
            f"\n    Size       : {human_size(part['size'])}"
        )

        filesystems = detect_filesystem(
            image,
            part["offset"],
        )

        part["filesystem"] = filesystems

        if filesystems:
            print(
                f"    Filesystem : {', '.join(filesystems)}"
            )
        else:
            print("    Filesystem : tidak terdeteksi")

    print("\n[•] Mencari printable strings...")

    strings = printable_strings(
        image,
        min_length=args.min_string,
        max_results=args.max_strings,
    )

    print(f"[✓] Strings ditemukan: {len(strings)}")

    interesting = []

    flag_pattern = re.compile(
        rb"(?:FLAG|CTF)\{[^}\r\n]{1,200}\}",
        re.IGNORECASE,
    )

    with open(image, "rb") as f:
        raw = f.read()

    for match in flag_pattern.finditer(raw):
        try:
            value = match.group().decode(
                "utf-8",
                errors="replace",
            )
        except Exception:
            continue

        interesting.append({
            "offset": match.start(),
            "value": value,
        })

    if interesting:
        print("\n[!] Potential flag ditemukan:")
        for item in interesting:
            print(
                f"    Offset {item['offset']}: "
                f"{item['value']}"
            )
    else:
        print("[-] Tidak ditemukan pola flag sederhana.")

    print("\n[•] Memeriksa Sleuth Kit...")

    sleuth = run_sleuthkit(
        image,
        partitions,
    )

    if sleuth["available"]:
        print("[✓] Sleuth Kit tersedia.")
        print_tree_from_fls(sleuth["fls"])
    else:
        print(
            "[i] Sleuth Kit tidak ditemukan. "
            "Analisis filesystem rekursif dilewati."
        )

    result = {
        "tool": "Midoo Disk Forensics",
        "version": "1.0",
        "file": str(image),
        "size": image.stat().st_size,
        "sha256": sha256_file(image),
        "mbr": mbr,
        "strings": strings,
        "potential_flags": interesting,
        "sleuth_kit": sleuth,
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(
                result,
                f,
                indent=4,
                ensure_ascii=False,
            )

        print(
            f"\n[✓] Report disimpan: {args.output}"
        )

    print("\n========================================")
    print("              ANALYSIS DONE")
    print("========================================")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Midoo Disk Forensics - "
            "Analisis disk image untuk CTF/lab"
        )
    )

    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path ke disk image",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Simpan report ke JSON",
    )

    parser.add_argument(
        "--min-string",
        type=int,
        default=6,
        help="Minimum panjang printable string",
    )

    parser.add_argument(
        "--max-strings",
        type=int,
        default=100,
        help="Jumlah maksimum strings yang ditampilkan",
    )

    args = parser.parse_args()

    try:
        raise SystemExit(scan(args))
    except KeyboardInterrupt:
        print("\n[!] Analisis dihentikan.")


if __name__ == "__main__":
    main()

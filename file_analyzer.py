import hashlib
import math
import os
import re

MAGIC_SIGNATURES = {
    b"\x89PNG\r\n\x1a\n": "PNG Image",
    b"\xff\xd8\xff": "JPEG Image",
    b"GIF87a": "GIF Image",
    b"GIF89a": "GIF Image",
    b"%PDF": "PDF Document",
    b"PK\x03\x04": "ZIP / Office Archive",
    b"Rar!\x1a\x07\x00": "RAR Archive",
    b"7z\xbc\xaf\x27\x1c": "7-Zip Archive",
    b"\x7fELF": "ELF Executable",
    b"MZ": "Windows PE Executable",
    b"SQLite format 3\x00": "SQLite Database",
}


def read_file(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception as e:
        print(f"[!] Error: {e}")
        return None


def detect_magic(data):
    for signature, name in MAGIC_SIGNATURES.items():
        if data.startswith(signature):
            return name, signature.hex(" ")
    return "Unknown", data[:16].hex(" ")


def calculate_hash(data):
    return {
        "MD5": hashlib.md5(data).hexdigest(),
        "SHA1": hashlib.sha1(data).hexdigest(),
        "SHA256": hashlib.sha256(data).hexdigest(),
    }


def calculate_entropy(data):
    if not data:
        return 0.0

    frequency = [0] * 256

    for byte in data:
        frequency[byte] += 1

    entropy = 0

    for count in frequency:
        if count == 0:
            continue

        probability = count / len(data)
        entropy -= probability * math.log2(probability)

    return entropy


def extract_strings(data, minimum=4):
    pattern = rb"[\x20-\x7e]{%d,}" % minimum
    matches = re.findall(pattern, data)

    return [x.decode("ascii", errors="ignore") for x in matches]


def hex_preview(data, length=64):
    preview = data[:length]

    print("\nHex Preview:")
    print(preview.hex(" "))

    print("\nASCII:")
    print("".join(chr(x) if 32 <= x <= 126 else "." for x in preview))


def analyze_file():
    path = input("\nMasukkan path file: ").strip()

    if not os.path.isfile(path):
        print("[!] File tidak ditemukan.")
        return

    data = read_file(path)

    if data is None:
        return

    filename = os.path.basename(path)
    size = os.path.getsize(path)

    file_type, magic = detect_magic(data)
    hashes = calculate_hash(data)
    entropy = calculate_entropy(data)

    print("\n========================================")
    print("          FILE INFORMATION")
    print("========================================")
    print(f"Filename : {filename}")
    print(f"Size     : {size} bytes")
    print(f"Type     : {file_type}")
    print(f"Magic    : {magic}")
    print(f"Entropy  : {entropy:.4f}")

    print("\n========================================")
    print("               HASH")
    print("========================================")
    print(f"MD5      : {hashes['MD5']}")
    print(f"SHA1     : {hashes['SHA1']}")
    print(f"SHA256   : {hashes['SHA256']}")

    hex_preview(data)

    print("\n========================================")
    print("              STRINGS")
    print("========================================")

    strings = extract_strings(data)

    if strings:
        for string in strings[:50]:
            print(string)

        if len(strings) > 50:
            print(f"\n[+] {len(strings) - 50} strings lainnya tidak ditampilkan.")
    else:
        print("[!] Tidak menemukan printable strings.")


def main():
    while True:
        print("""
========================================
        Midoo File Analyzer
========================================
1. Analyze File
2. Exit
========================================
""")

        pilihan = input("Pilih: ")

        if pilihan == "1":
            analyze_file()

        elif pilihan == "2":
            print("Keluar...")
            break

        else:
            print("[!] Pilihan tidak valid.")


if __name__ == "__main__":
    main()

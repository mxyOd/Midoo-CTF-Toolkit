import hashlib
import os
import re


def hash_text(algorithm):
    text = input("\nMasukkan text: ")

    try:
        hasher = hashlib.new(algorithm)
        hasher.update(text.encode("utf-8"))

        print(f"\n{algorithm.upper()}:")
        print(hasher.hexdigest())

    except ValueError:
        print("[!] Algoritma tidak tersedia.")


def hash_file():
    path = input("\nMasukkan path file: ").strip()

    if not os.path.isfile(path):
        print("[!] File tidak ditemukan.")
        return

    algorithms = ["md5", "sha1", "sha256", "sha512"]

    print("\n========================================")
    print("               FILE HASH")
    print("========================================")

    hashers = {
        algorithm: hashlib.new(algorithm)
        for algorithm in algorithms
    }

    try:
        with open(path, "rb") as file:

            while True:
                chunk = file.read(1024 * 1024)

                if not chunk:
                    break

                for hasher in hashers.values():
                    hasher.update(chunk)

        for algorithm, hasher in hashers.items():
            print(f"{algorithm.upper():8}: {hasher.hexdigest()}")

    except Exception as error:
        print(f"[!] Error: {error}")


def compare_hash():
    path = input("\nMasukkan path file: ").strip()

    if not os.path.isfile(path):
        print("[!] File tidak ditemukan.")
        return

    expected = input("Masukkan expected hash: ").strip().lower()

    if not re.fullmatch(r"[0-9a-f]+", expected):
        print("[!] Format hash tidak valid.")
        return

    if len(expected) == 32:
        algorithm = "md5"

    elif len(expected) == 40:
        algorithm = "sha1"

    elif len(expected) == 64:
        algorithm = "sha256"

    elif len(expected) == 128:
        algorithm = "sha512"

    else:
        print("[!] Panjang hash tidak dikenali.")
        return

    hasher = hashlib.new(algorithm)

    try:
        with open(path, "rb") as file:

            while True:
                chunk = file.read(1024 * 1024)

                if not chunk:
                    break

                hasher.update(chunk)

        actual = hasher.hexdigest()

        print(f"\nAlgorithm : {algorithm.upper()}")
        print(f"Expected  : {expected}")
        print(f"Actual    : {actual}")

        if actual == expected:
            print("\n[+] HASH MATCH")
        else:
            print("\n[-] HASH TIDAK COCOK")

    except Exception as error:
        print(f"[!] Error: {error}")


def identify_hash():
    value = input("\nMasukkan hash: ").strip()

    if not re.fullmatch(r"[0-9a-fA-F]+", value):
        print("[!] Bukan hexadecimal hash.")
        return

    length = len(value)

    print("\n========================================")
    print("             HASH IDENTIFIER")
    print("========================================")

    if length == 32:
        print("[+] Kemungkinan:")
        print("    MD5")
        print("    NTLM")

    elif length == 40:
        print("[+] Kemungkinan:")
        print("    SHA1")

    elif length == 64:
        print("[+] Kemungkinan:")
        print("    SHA256")

    elif length == 96:
        print("[+] Kemungkinan:")
        print("    SHA384")

    elif length == 128:
        print("[+] Kemungkinan:")
        print("    SHA512")

    else:
        print("[-] Tidak ada format umum yang cocok.")

    print(f"\nLength: {length} hexadecimal characters")
    print(f"Bytes : {length // 2}")


def main():

    while True:

        print("""
========================================
          Midoo Hash Analyzer
========================================
1. Generate MD5
2. Generate SHA1
3. Generate SHA256
4. Generate SHA512
5. Hash File
6. Compare Hash
7. Identify Hash
8. Exit
========================================
""")

        pilihan = input("Pilih: ")

        if pilihan == "1":
            hash_text("md5")

        elif pilihan == "2":
            hash_text("sha1")

        elif pilihan == "3":
            hash_text("sha256")

        elif pilihan == "4":
            hash_text("sha512")

        elif pilihan == "5":
            hash_file()

        elif pilihan == "6":
            compare_hash()

        elif pilihan == "7":
            identify_hash()

        elif pilihan == "8":
            print("Keluar...")
            break

        else:
            print("[!] Pilihan tidak valid.")


if __name__ == "__main__":
    main()
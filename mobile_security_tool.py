#!/usr/bin/env python3

import hashlib
import os
import re
import shutil
import subprocess
import zipfile


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def wait_enter():
    input("\nTekan Enter untuk kembali...")


def command_exists(command):
    return shutil.which(command) is not None


def check_apk(path):
    if not path:
        print("\n[!] File APK tidak boleh kosong.")
        return False

    if not os.path.isfile(path):
        print(f"\n[!] File tidak ditemukan: {path}")
        return False

    if not path.lower().endswith(".apk"):
        print("\n[!] File harus berekstensi .apk.")
        return False

    return True


def get_apk():
    path = input(
        "\nMasukkan path APK: "
    ).strip()

    if not check_apk(path):
        wait_enter()
        return None

    return path


def apk_information():
    clear_screen()

    print("""
=============================================
          Midoo APK Information
=============================================
""")

    apk = get_apk()

    if not apk:
        return

    size = os.path.getsize(apk)

    print(f"\nName       : {os.path.basename(apk)}")
    print(f"Path       : {os.path.abspath(apk)}")
    print(f"Size       : {size} bytes")

    try:
        with zipfile.ZipFile(apk, "r") as z:
            files = z.namelist()

            print(f"ZIP Files  : {len(files)}")

            if "AndroidManifest.xml" in files:
                print("Manifest   : Found")
            else:
                print("Manifest   : Not found")

            dex_files = [
                name for name in files
                if name.endswith(".dex")
            ]

            print(
                f"DEX Files  : {len(dex_files)}"
            )

            for dex in dex_files:
                print(f"             {dex}")

    except zipfile.BadZipFile:
        print("\n[!] APK bukan ZIP/APK yang valid.")

    except Exception as error:
        print(f"\n[!] Error: {error}")

    wait_enter()


def apk_strings():
    clear_screen()

    print("""
=============================================
             Midoo APK Strings
=============================================
""")

    apk = get_apk()

    if not apk:
        return

    try:
        with zipfile.ZipFile(apk, "r") as z:

            print("\n[+] Printable strings:\n")

            pattern = re.compile(
                rb"[ -~]{5,}"
            )

            total = 0

            for name in z.namelist():

                try:
                    data = z.read(name)
                except Exception:
                    continue

                for match in pattern.findall(data):

                    text = match.decode(
                        "utf-8",
                        errors="replace"
                    )

                    print(
                        f"{name}: {text}"
                    )

                    total += 1

                    if total >= 300:
                        print(
                            "\n[i] Output dibatasi "
                            "hingga 300 string."
                        )
                        wait_enter()
                        return

    except Exception as error:
        print(f"\n[!] Error: {error}")

    wait_enter()


def apk_manifest():
    clear_screen()

    print("""
=============================================
            Midoo APK Manifest
=============================================
""")

    apk = get_apk()

    if not apk:
        return

    if command_exists("apkanalyzer"):

        subprocess.run(
            [
                "apkanalyzer",
                "manifest",
                "print",
                apk
            ],
            check=False
        )

    elif command_exists("aapt"):

        subprocess.run(
            [
                "aapt",
                "dump",
                "badging",
                apk
            ],
            check=False
        )

    else:

        print(
            "[!] apkanalyzer/aapt tidak ditemukan."
        )

        print(
            "\n[*] Install Android build-tools "
            "untuk analisis manifest."
        )

    wait_enter()


def apk_permissions():
    clear_screen()

    print("""
=============================================
           Midoo APK Permissions
=============================================
""")

    apk = get_apk()

    if not apk:
        return

    if command_exists("aapt"):

        subprocess.run(
            [
                "aapt",
                "dump",
                "permissions",
                apk
            ],
            check=False
        )

    elif command_exists("apkanalyzer"):

        subprocess.run(
            [
                "apkanalyzer",
                "manifest",
                "permissions",
                apk
            ],
            check=False
        )

    else:

        print(
            "[!] Android build-tools tidak ditemukan."
        )

    wait_enter()


def apk_certificate():
    clear_screen()

    print("""
=============================================
           Midoo APK Certificate
=============================================
""")

    apk = get_apk()

    if not apk:
        return

    if command_exists("apksigner"):

        subprocess.run(
            [
                "apksigner",
                "verify",
                "--print-certs",
                apk
            ],
            check=False
        )

    else:

        print(
            "[!] apksigner tidak ditemukan."
        )

        print(
            "\n[*] Gunakan Android build-tools "
            "untuk memeriksa certificate."
        )

    wait_enter()


def apk_hash():
    clear_screen()

    print("""
=============================================
              Midoo APK Hash
=============================================
""")

    apk = get_apk()

    if not apk:
        return

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    try:
        with open(
            apk,
            "rb"
        ) as file:

            while True:

                data = file.read(1024 * 1024)

                if not data:
                    break

                md5.update(data)
                sha1.update(data)
                sha256.update(data)

        print(
            f"\nMD5    : {md5.hexdigest()}"
        )

        print(
            f"SHA1   : {sha1.hexdigest()}"
        )

        print(
            f"SHA256 : {sha256.hexdigest()}"
        )

    except Exception as error:
        print(
            f"\n[!] Error: {error}"
        )

    wait_enter()


def dex_information():
    clear_screen()

    print("""
=============================================
             Midoo DEX Information
=============================================
""")

    apk = get_apk()

    if not apk:
        return

    try:
        with zipfile.ZipFile(apk, "r") as z:

            dex_files = [
                name for name in z.namelist()
                if name.endswith(".dex")
            ]

            if not dex_files:
                print(
                    "\n[-] Tidak ditemukan file DEX."
                )

            for dex in dex_files:

                info = z.getinfo(dex)

                print(
                    f"\nFile : {dex}"
                )

                print(
                    f"Size : {info.file_size} bytes"
                )

                print(
                    f"CRC  : {hex(info.CRC)}"
                )

    except Exception as error:
        print(
            f"\n[!] Error: {error}"
        )

    wait_enter()


def jadx_analysis():
    clear_screen()

    print("""
=============================================
              Midoo JADX Analysis
=============================================
""")

    apk = get_apk()

    if not apk:
        return

    if not command_exists("jadx"):

        print(
            "[!] JADX tidak ditemukan."
        )

        print(
            "\n[*] Install JADX terlebih dahulu "
            "jika ingin melakukan decompile."
        )

        wait_enter()
        return

    output = input(
        "\nFolder output [jadx_output]: "
    ).strip()

    if not output:
        output = "jadx_output"

    print(
        "\n[*] Menjalankan JADX...\n"
    )

    subprocess.run(
        [
            "jadx",
            "-d",
            output,
            apk
        ],
        check=False
    )

    print(
        f"\n[✓] Output: {output}"
    )

    wait_enter()


def apktool_analysis():
    clear_screen()

    print("""
=============================================
             Midoo APKTool Analysis
=============================================
""")

    apk = get_apk()

    if not apk:
        return

    if not command_exists("apktool"):

        print(
            "[!] apktool tidak ditemukan."
        )

        wait_enter()
        return

    output = input(
        "\nFolder output [apktool_output]: "
    ).strip()

    if not output:
        output = "apktool_output"

    print(
        "\n[*] Menjalankan APKTool...\n"
    )

    subprocess.run(
        [
            "apktool",
            "d",
            apk,
            "-o",
            output,
            "-f"
        ],
        check=False
    )

    print(
        f"\n[✓] Output: {output}"
    )

    wait_enter()


def search_sensitive_strings():
    clear_screen()

    print("""
=============================================
       Midoo Sensitive String Search
=============================================
""")

    apk = get_apk()

    if not apk:
        return

    patterns = {
        "API Key": r"(?i)(api[_-]?key|apikey)",
        "Secret": r"(?i)(secret|client[_-]?secret)",
        "Password": r"(?i)(password|passwd|pwd)",
        "Token": r"(?i)(token|access[_-]?token)",
        "Firebase": r"(?i)firebase",
        "AWS": r"(?i)(aws_access_key|aws_secret)",
        "Private Key": r"-----BEGIN .*PRIVATE KEY-----",
    }

    try:
        with zipfile.ZipFile(apk, "r") as z:

            found = False

            for name in z.namelist():

                try:
                    data = z.read(name).decode(
                        "utf-8",
                        errors="ignore"
                    )
                except Exception:
                    continue

                for label, pattern in patterns.items():

                    if re.search(pattern, data):

                        print(
                            f"[!] {label} "
                            f"potential match: {name}"
                        )

                        found = True

            if not found:

                print(
                    "[✓] Tidak ditemukan "
                    "pattern sensitif dasar."
                )

    except Exception as error:
        print(
            f"\n[!] Error: {error}"
        )

    wait_enter()


def search_urls():
    clear_screen()

    print("""
=============================================
              Midoo URL Search
=============================================
""")

    apk = get_apk()

    if not apk:
        return

    url_pattern = re.compile(
        r"https?://[^\s\"'<>]+"
    )

    try:
        with zipfile.ZipFile(apk, "r") as z:

            found = set()

            for name in z.namelist():

                try:
                    data = z.read(name).decode(
                        "utf-8",
                        errors="ignore"
                    )
                except Exception:
                    continue

                for url in url_pattern.findall(data):
                    found.add(url)

            if found:

                for url in sorted(found):
                    print(url)

            else:

                print(
                    "[-] Tidak ditemukan URL."
                )

    except Exception as error:
        print(
            f"\n[!] Error: {error}"
        )

    wait_enter()


def show_menu():

    print("""
=============================================
          Midoo Mobile Security
                     v1.0
=============================================

    [1]  APK Information
    [2]  APK Strings
    [3]  APK Manifest
    [4]  APK Permissions
    [5]  APK Certificate
    [6]  APK Hash
    [7]  DEX Information
    [8]  JADX Analysis
    [9]  APKTool Analysis
    [10] Search Sensitive Strings
    [11] Search URLs

    [0]  Kembali

=============================================
""")


def main():

    while True:

        clear_screen()
        show_menu()

        pilihan = input(
            "Midoo Mobile > "
        ).strip()

        if pilihan == "0":
            break

        elif pilihan == "1":
            apk_information()

        elif pilihan == "2":
            apk_strings()

        elif pilihan == "3":
            apk_manifest()

        elif pilihan == "4":
            apk_permissions()

        elif pilihan == "5":
            apk_certificate()

        elif pilihan == "6":
            apk_hash()

        elif pilihan == "7":
            dex_information()

        elif pilihan == "8":
            jadx_analysis()

        elif pilihan == "9":
            apktool_analysis()

        elif pilihan == "10":
            search_sensitive_strings()

        elif pilihan == "11":
            search_urls()

        else:

            print(
                "\n[!] Pilihan tidak valid."
            )

            wait_enter()


if __name__ == "__main__":
    main()
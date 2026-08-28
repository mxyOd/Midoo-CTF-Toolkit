#!/usr/bin/env python3

import json
import os
import shutil
import socket
import subprocess
import urllib.parse


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def wait_enter():
    input("\nTekan Enter untuk kembali...")


def command_exists(command):
    return shutil.which(command) is not None


def run_command(command, args=None):
    if args is None:
        args = []

    try:
        subprocess.run(
            [command] + args,
            check=False
        )
    except KeyboardInterrupt:
        print("\n[!] Tool dihentikan.")
    except Exception as error:
        print(f"\n[!] Error: {error}")

    wait_enter()


def aws_analyzer():
    clear_screen()

    print("""
=============================================
          Midoo AWS Analyzer
=============================================
""")

    if not command_exists("aws"):
        print("[!] AWS CLI tidak ditemukan.")
        print("\n[*] Install AWS CLI terlebih dahulu jika diperlukan.")
        wait_enter()
        return

    print("[+] AWS CLI ditemukan.")
    print()

    run_command("aws", ["--version"])


def s3_analyzer():
    clear_screen()

    print("""
=============================================
           Midoo S3 Analyzer
=============================================
""")

    bucket = input("Masukkan nama bucket milikmu: ").strip()

    if not bucket:
        print("\n[!] Bucket tidak boleh kosong.")
        wait_enter()
        return

    print("\n[*] Memeriksa format bucket...")
    
    if bucket.startswith("s3://"):
        bucket = bucket[5:]

    print(f"[+] Bucket: {bucket}")

    print("\n[*] Untuk pemeriksaan akses, gunakan AWS CLI")
    print("    dengan credential yang memang kamu miliki.")

    if command_exists("aws"):
        print("\n[*] Menjalankan pemeriksaan konfigurasi lokal...")
        run_command(
            "aws",
            [
                "s3api",
                "get-bucket-location",
                "--bucket",
                bucket
            ]
        )
    else:
        print("\n[!] AWS CLI tidak ditemukan.")
        wait_enter()


def iam_analyzer():
    clear_screen()

    print("""
=============================================
            Midoo IAM Analyzer
=============================================
""")

    if not command_exists("aws"):
        print("[!] AWS CLI tidak ditemukan.")
        wait_enter()
        return

    print("""
[*] Pemeriksaan IAM hanya menggunakan
    credential AWS yang sedang dikonfigurasi.

[*] Tidak melakukan credential discovery.
""")

    run_command(
        "aws",
        [
            "iam",
            "get-account-summary"
        ]
    )


def azure_analyzer():
    clear_screen()

    print("""
=============================================
           Midoo Azure Analyzer
=============================================
""")

    if not command_exists("az"):
        print("[!] Azure CLI tidak ditemukan.")
        print("\n[*] Install Azure CLI jika diperlukan.")
        wait_enter()
        return

    print("[+] Azure CLI ditemukan.")
    print()

    run_command(
        "az",
        [
            "account",
            "show"
        ]
    )


def gcp_analyzer():
    clear_screen()

    print("""
=============================================
            Midoo GCP Analyzer
=============================================
""")

    if not command_exists("gcloud"):
        print("[!] Google Cloud CLI tidak ditemukan.")
        print("\n[*] Install gcloud CLI jika diperlukan.")
        wait_enter()
        return

    print("[+] Google Cloud CLI ditemukan.")
    print()

    run_command(
        "gcloud",
        [
            "config",
            "list"
        ]
    )


def cloud_metadata():
    clear_screen()

    print("""
=============================================
          Midoo Cloud Metadata
=============================================
""")

    print("""
Cloud metadata digunakan untuk memahami
konfigurasi instance cloud milik sendiri.

Tool ini tidak melakukan scanning eksternal.
Gunakan pada VM/lab yang kamu kontrol.
""")

    print("[1] Show local hostname")
    print("[2] Show local IP")
    print("[0] Kembali")

    pilihan = input("\nMidoo Cloud > ").strip()

    if pilihan == "1":
        print(
            f"\nHostname: {socket.gethostname()}"
        )
        wait_enter()

    elif pilihan == "2":
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)

            print(f"\nLocal IP: {ip}")

        except Exception as error:
            print(f"\n[!] Error: {error}")

        wait_enter()


def config_checker():
    clear_screen()

    print("""
=============================================
        Midoo Cloud Configuration Checker
=============================================
""")

    print("""
Pemeriksaan dasar environment lokal.
Tidak melakukan eksploitasi atau scanning
terhadap resource eksternal.
""")

    checks = {
        "AWS CLI": "aws",
        "Azure CLI": "az",
        "GCloud CLI": "gcloud",
        "Docker": "docker"
    }

    print()

    for name, command in checks.items():
        if command_exists(command):
            print(f"[✓] {name:<15} tersedia")
        else:
            print(f"[-] {name:<15} tidak ditemukan")

    wait_enter()


def cloud_url_analyzer():
    clear_screen()

    print("""
=============================================
          Midoo Cloud URL Analyzer
=============================================
""")

    url = input("Masukkan URL: ").strip()

    if not url:
        print("\n[!] URL tidak boleh kosong.")
        wait_enter()
        return

    try:
        parsed = urllib.parse.urlparse(url)

        print("\n[+] Scheme     :", parsed.scheme)
        print("[+] Host       :", parsed.hostname)
        print("[+] Port       :", parsed.port)
        print("[+] Path       :", parsed.path)
        print("[+] Query      :", parsed.query)

    except Exception as error:
        print(f"\n[!] Error: {error}")

    wait_enter()


def tool_status():
    clear_screen()

    print("""
=============================================
          Midoo Cloud Tool Status
=============================================
""")

    tools = {
        "AWS CLI": "aws",
        "Azure CLI": "az",
        "GCloud CLI": "gcloud",
        "Docker": "docker"
    }

    for name, command in tools.items():

        if command_exists(command):
            print(f"[✓] {name:<15} Installed")
        else:
            print(f"[-] {name:<15} Not Found")

    wait_enter()


def show_menu():
    print("""
=============================================
       Midoo Cloud Security Toolkit
                    v1.0
=============================================

    [1] AWS Analyzer
    [2] S3 Analyzer
    [3] IAM Analyzer
    [4] Azure Analyzer
    [5] GCP Analyzer
    [6] Cloud Metadata
    [7] Configuration Checker
    [8] Cloud URL Analyzer
    [9] Tool Status

    [0] Kembali

=============================================
""")


def main():

    while True:

        clear_screen()
        show_menu()

        pilihan = input(
            "Midoo Cloud > "
        ).strip()

        if pilihan == "0":
            break

        elif pilihan == "1":
            aws_analyzer()

        elif pilihan == "2":
            s3_analyzer()

        elif pilihan == "3":
            iam_analyzer()

        elif pilihan == "4":
            azure_analyzer()

        elif pilihan == "5":
            gcp_analyzer()

        elif pilihan == "6":
            cloud_metadata()

        elif pilihan == "7":
            config_checker()

        elif pilihan == "8":
            cloud_url_analyzer()

        elif pilihan == "9":
            tool_status()

        else:
            print("\n[!] Pilihan tidak valid.")
            wait_enter()


if __name__ == "__main__":
    main()
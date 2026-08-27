import os
import subprocess
import sys


TOOLS = {
    "1": ("Crypto Tool", "crypto_tool.py"),
    "2": ("File Analyzer", "file_analyzer.py"),
    "3": ("Network Analyzer", "network_analyzer.py"),
    "4": ("PCAP Analyzer", "pcap_analyzer.py"),
    "5": ("Hash Analyzer", "hash_analyzer.py"),
    "6": ("JWT Analyzer", "jwt_analyzer.py"),
    "7": ("Web Recon", "web_recon.py"),
    "8": ("Stego Analyzer", "stego_analyzer.py"),
    "9": ("URL Analyzer", "url_analyzer.py"),
    "10": ("HTTP Analyzer", "http_analyzer.py"),
    "11": ("VulnScope", "vulnscope.py"),
    "12": ("API Tester", "api_tester.py"),
    "13": ("Disk Forensics", "disk_forensics.py"),
}


CLI_TOOLS = {
    "1": ("VulnScope", "vulnscope.py"),
    "2": ("API Tester", "api_tester.py"),
    "3": ("Disk Forensics", "disk_forensics.py"),
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def wait_enter():
    input("\nTekan Enter untuk kembali...")


def check_file(filename):
    if not os.path.exists(filename):
        print(f"\n[!] File tidak ditemukan: {filename}")
        wait_enter()
        return False

    return True


def run_tool(name, filename):
    if not check_file(filename):
        return

    clear_screen()

    print("=============================================")
    print(f"             Midoo {name}")
    print("=============================================\n")

    try:
        subprocess.run(
            [sys.executable, filename],
            check=False
        )

    except KeyboardInterrupt:
        print("\n[!] Tool dihentikan.")

    except Exception as error:
        print(f"\n[!] Error: {error}")

    wait_enter()


def run_vulnscope():
    filename = TOOLS["11"][1]

    if not check_file(filename):
        return

    clear_screen()

    print("=============================================")
    print("             Midoo VulnScope")
    print("=============================================")

    target = input("\nMasukkan target: ").strip()

    if not target:
        print("\n[!] Target tidak boleh kosong.")
        wait_enter()
        return

    output = input(
        "Nama output JSON [hasil.json]: "
    ).strip()

    if not output:
        output = "hasil.json"

    print("\n[*] Menjalankan VulnScope...\n")

    try:
        subprocess.run(
            [
                sys.executable,
                filename,
                "-d",
                target,
                "-o",
                output
            ],
            check=False
        )

    except KeyboardInterrupt:
        print("\n[!] VulnScope dihentikan.")

    except Exception as error:
        print(f"\n[!] Error: {error}")

    wait_enter()


def run_disk_forensics():
    filename = TOOLS["13"][1]

    if not check_file(filename):
        return

    clear_screen()

    print("=============================================")
    print("          Midoo Disk Forensics")
    print("=============================================")

    image = input("\nMasukkan file image: ").strip()

    if not image:
        print("\n[!] File image tidak boleh kosong.")
        wait_enter()
        return

    if not os.path.exists(image):
        print(f"\n[!] File tidak ditemukan: {image}")
        wait_enter()
        return

    output = input(
        "Nama report JSON [hasil.json]: "
    ).strip()

    if not output:
        output = "hasil.json"

    print("\n[*] Menjalankan Disk Forensics...\n")

    try:
        subprocess.run(
            [
                sys.executable,
                filename,
                "-f",
                image,
                "-o",
                output
            ],
            check=False
        )

    except KeyboardInterrupt:
        print("\n[!] Disk Forensics dihentikan.")

    except Exception as error:
        print(f"\n[!] Error: {error}")

    wait_enter()


def show_cli_help():
    while True:
        clear_screen()

        print("""
=============================================
             Midoo Tool Help
=============================================

    [1] VulnScope
    [2] API Tester
    [3] Disk Forensics

    [4] Kembali

=============================================
""")

        pilihan = input("Midoo Help > ").strip()

        if pilihan == "4":
            break

        if pilihan not in CLI_TOOLS:
            print("\n[!] Pilihan tidak valid.")
            wait_enter()
            continue

        name, filename = CLI_TOOLS[pilihan]

        if not check_file(filename):
            continue

        clear_screen()

        print("=============================================")
        print(f"             {name} Help")
        print("=============================================\n")

        try:
            subprocess.run(
                [
                    sys.executable,
                    filename,
                    "-h"
                ],
                check=False
            )

        except KeyboardInterrupt:
            print("\n[!] Help dihentikan.")

        except Exception as error:
            print(f"\n[!] Error: {error}")

        wait_enter()


def show_menu():
    print("""
=============================================
            Midoo CTF Toolkit
=============================================

    [1]  Crypto Tool
    [2]  File Analyzer
    [3]  Network Analyzer
    [4]  PCAP Analyzer
    [5]  Hash Analyzer
    [6]  JWT Analyzer
    [7]  Web Recon
    [8]  Stego Analyzer
    [9]  URL Analyzer
    [10] HTTP Analyzer
    [11] VulnScope
    [12] API Tester
    [13] Disk Forensics

    [14] Tool Help
    [15] Exit

=============================================
""")


def main():

    while True:

        clear_screen()
        show_menu()

        pilihan = input("Midoo > ").strip()

        # VulnScope
        if pilihan == "11":
            run_vulnscope()
            continue

        # Disk Forensics
        if pilihan == "13":
            run_disk_forensics()
            continue

        # Tool Help
        if pilihan == "14":
            show_cli_help()
            continue

        # Exit
        if pilihan == "15":
            clear_screen()
            print("Midoo CTF Toolkit terminated.")
            break

        # Tool biasa
        if pilihan in TOOLS:

            name, filename = TOOLS[pilihan]

            run_tool(name, filename)

            continue

        print("\n[!] Pilihan tidak valid.")
        wait_enter()


if __name__ == "__main__":
    main()
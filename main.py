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
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def wait_enter():
    input("\nTekan Enter untuk kembali...")


def run_tool(name, filename):
    """Menjalankan tool biasa tanpa argument CLI."""

    if not os.path.exists(filename):
        print(f"\n[!] File tidak ditemukan: {filename}")
        wait_enter()
        return

    clear_screen()

    print("=============================================")
    print(f"          Midoo {name}")
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
    """Menjalankan VulnScope dengan argument -d dan -o."""

    filename = TOOLS["11"][1]

    if not os.path.exists(filename):
        print(f"\n[!] File tidak ditemukan: {filename}")
        wait_enter()
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

    [12] Exit

=============================================
""")


def main():

    while True:

        clear_screen()

        show_menu()

        pilihan = input("Midoo > ").strip()

        # Exit
        if pilihan == "12":
            clear_screen()
            print("Midoo CTF Toolkit terminated.")
            break

        # VulnScope
        if pilihan == "11":
            run_vulnscope()
            continue

        # Tool lainnya
        if pilihan in TOOLS:

            name, filename = TOOLS[pilihan]

            run_tool(name, filename)

        else:

            print("\n[!] Pilihan tidak valid.")
            wait_enter()


if __name__ == "__main__":
    main()
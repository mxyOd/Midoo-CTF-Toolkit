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
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def run_tool(name, filename):

    if not os.path.exists(filename):
        print(f"\n[!] File tidak ditemukan: {filename}")
        input("\nTekan Enter untuk kembali...")
        return

    clear_screen()

    print(f"[*] Membuka {name}...\n")

    try:
        subprocess.run([sys.executable, filename], check=False)

    except KeyboardInterrupt:
        print("\n[!] Tool dihentikan.")

    except Exception as error:
        print(f"\n[!] Error: {error}")

    input("\nTekan Enter untuk kembali ke Midoo CTF Toolkit...")


def main():

    while True:

        clear_screen()

        print("""
=============================================
              Midoo CTF Toolkit
=============================================
       Cyber Security & CTF Toolkit
=============================================

    [1] Crypto Tool
    [2] File Analyzer
    [3] Network Analyzer
    [4] PCAP Analyzer
    [5] Hash Analyzer
    [6] JWT Analyzer
    [7] Web Recon
    [8] Stego Analyzer

    [9] Exit

=============================================
""")

        pilihan = input("Midoo > ").strip()

        if pilihan == "9":
            clear_screen()
            print("Midoo CTF Toolkit terminated.")
            break

        if pilihan in TOOLS:

            name, filename = TOOLS[pilihan]

            run_tool(name, filename)

        else:

            print("\n[!] Pilihan tidak valid.")
            input("Tekan Enter...")


if __name__ == "__main__":
    main()

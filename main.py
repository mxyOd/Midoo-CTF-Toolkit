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
    "14": ("Pwn Toolkit", "pwn_tool.py"),
    "15": ("Reverse Engineering", "re_tool.py"),
    "16": ("Malware Analyzer", "malware_analyzer.py"),
    "17": ("Memory Forensics", "memory_forensics.py"),
    "18": ("Log Analyzer", "log_analyzer.py"),
    "19": ("Wordlist Toolkit", "wordlist_tool.py"),
    "20": ("OSINT Toolkit", "osint_tool.py"),
    "21": ("Cloud Security Toolkit", "cloud_security_tool.py"),
    "22": ("Container Security Toolkit", "container_security_tool.py"),
    "23": ("Mobile Security Toolkit", "mobile_security_tool.py"),
    "24": ("Database Forensics Toolkit", "database_forensics_tool.py"),
    "25": ("Rentora Analyzer", "rentora_analyzer_v2.py"),
}


CLI_TOOLS = {
    "1": ("VulnScope", "vulnscope.py"),
    "2": ("API Tester", "api_tester.py"),
    "3": ("Disk Forensics", "disk_forensics.py"),
    "4": ("Pwn Toolkit", "pwn_tool.py"),
    "5": ("Reverse Engineering", "re_tool.py"),
    "6": ("Malware Analyzer", "malware_analyzer.py"),
    "7": ("Memory Forensics", "memory_forensics.py"),
    "8": ("Log Analyzer", "log_analyzer.py"),
    "9": ("Wordlist Toolkit", "wordlist_tool.py"),
    "10": ("OSINT Toolkit", "osint_tool.py"),
    "11": ("Cloud Security Toolkit", "cloud_security_tool.py"),
    "12": ("Container Security Toolkit", "container_security_tool.py"),
    "13": ("Mobile Security Toolkit", "mobile_security_tool.py"),
    "14": ("Database Forensics Toolkit", "database_forensics_tool.py"),
    "15": ("Rentora Analyzer", "rentora_analyzer_v2.py"),
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
    print(f"              Midoo {name}")
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


def run_file_tool(number, title, argument):
    filename = TOOLS[number][1]

    if not check_file(filename):
        return

    clear_screen()

    print("=============================================")
    print(f"              Midoo {title}")
    print("=============================================")

    target = input(
        f"\nMasukkan {argument}: "
    ).strip()

    if not target:
        print(
            f"\n[!] {argument.capitalize()} "
            "tidak boleh kosong."
        )

        wait_enter()
        return

    if not os.path.exists(target):
        print(
            f"\n[!] File tidak ditemukan: {target}"
        )

        wait_enter()
        return

    print(
        f"\n[*] Menjalankan {title}...\n"
    )

    try:
        subprocess.run(
            [
                sys.executable,
                filename,
                "-f",
                target
            ],
            check=False
        )

    except KeyboardInterrupt:
        print(
            f"\n[!] {title} dihentikan."
        )

    except Exception as error:
        print(
            f"\n[!] Error: {error}"
        )

    wait_enter()


def run_vulnscope():
    filename = TOOLS["11"][1]

    if not check_file(filename):
        return

    clear_screen()

    print("=============================================")
    print("              Midoo VulnScope")
    print("=============================================")

    target = input(
        "\nMasukkan target: "
    ).strip()

    if not target:
        print(
            "\n[!] Target tidak boleh kosong."
        )

        wait_enter()
        return

    output = input(
        "Nama output JSON [hasil.json]: "
    ).strip()

    if not output:
        output = "hasil.json"

    print(
        "\n[*] Menjalankan VulnScope...\n"
    )

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
        print(
            "\n[!] VulnScope dihentikan."
        )

    except Exception as error:
        print(
            f"\n[!] Error: {error}"
        )

    wait_enter()


def run_rentora():
    filename = TOOLS["25"][1]

    if not check_file(filename):
        return

    clear_screen()

    print("=============================================")
    print("              Midoo Rentora Analyzer")
    print("=============================================")

    target = input("\nMasukkan target URL: ").strip()

    if not target:
        print("\n[!] URL tidak boleh kosong.")
        wait_enter()
        return

    print("""
---------------------------------------------
Mode:
  [1] Scan halaman saja
  [2] Scan + interactive booking form
---------------------------------------------
""")

    mode = input("Pilih mode [1/2]: ").strip()

    if mode not in ("1", "2"):
        print("\n[!] Pilihan tidak valid.")
        wait_enter()
        return

    command = [
        sys.executable,
        filename,
        "-u",
        target
    ]

    if mode == "2":
        command.append("-i")

    print("\n[*] Menjalankan Rentora Analyzer...\n")

    try:
        subprocess.run(
            command,
            check=False
        )
    except KeyboardInterrupt:
        print("\n[!] Rentora Analyzer dihentikan.")
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

    [1]  VulnScope
    [2]  API Tester
    [3]  Disk Forensics
    [4]  Pwn Toolkit
    [5]  Reverse Engineering
    [6]  Malware Analyzer
    [7]  Memory Forensics
    [8]  Log Analyzer
    [9]  Wordlist Toolkit
    [10] OSINT Toolkit
    [11] Cloud Security Toolkit
    [12] Container Security Toolkit
    [13] Mobile Security Toolkit
    [14] Database Forensics Toolkit

    [0]  Kembali

=============================================
""")

        pilihan = input(
            "Midoo Help > "
        ).strip()

        if pilihan == "0":
            break

        if pilihan not in CLI_TOOLS:
            print(
                "\n[!] Pilihan tidak valid."
            )

            wait_enter()
            continue

        name, filename = CLI_TOOLS[pilihan]

        if not check_file(filename):
            continue

        clear_screen()

        print("=============================================")
        print(f"              {name} Help")
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
            print(
                "\n[!] Help dihentikan."
            )

        except Exception as error:
            print(
                f"\n[!] Error: {error}"
            )

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
    [14] Pwn Toolkit
    [15] Reverse Engineering
    [16] Malware Analyzer
    [17] Memory Forensics
    [18] Log Analyzer
    [19] Wordlist Toolkit
    [20] OSINT Toolkit
    [21] Cloud Security Toolkit
    [22] Container Security Toolkit
    [23] Mobile Security Toolkit
    [24] Database Forensics Toolkit
    [25] Rentora Analyzer

    [26] Tool Help
    [0]  Exit

=============================================
""")


def main():

    while True:

        clear_screen()
        show_menu()

        pilihan = input(
            "Midoo > "
        ).strip()

        # Exit
        if pilihan == "0":
            clear_screen()

            print(
                "Midoo CTF Toolkit terminated."
            )

            break

        # VulnScope
        if pilihan == "11":
            run_vulnscope()
            continue

        # Disk Forensics
        if pilihan == "13":
            run_file_tool(
                "13",
                "Disk Forensics",
                "file image"
            )
            continue

        # Pwn Toolkit
        if pilihan == "14":
            run_file_tool(
                "14",
                "Pwn Toolkit",
                "binary"
            )
            continue

        # Reverse Engineering
        if pilihan == "15":
            run_file_tool(
                "15",
                "Reverse Engineering",
                "binary"
            )
            continue

        # Malware Analyzer
        if pilihan == "16":
            run_file_tool(
                "16",
                "Malware Analyzer",
                "file"
            )
            continue

        # Memory Forensics
        if pilihan == "17":
            run_file_tool(
                "17",
                "Memory Forensics",
                "memory dump"
            )
            continue

        # Log Analyzer
        if pilihan == "18":
            run_file_tool(
                "18",
                "Log Analyzer",
                "log file"
            )
            continue

        # Wordlist Toolkit
        if pilihan == "19":
            run_tool(
                "Wordlist Toolkit",
                TOOLS["19"][1]
            )
            continue

        # OSINT Toolkit
        if pilihan == "20":
            run_tool(
                "OSINT Toolkit",
                TOOLS["20"][1]
            )
            continue

        # Cloud Security Toolkit
        if pilihan == "21":
            run_tool(
                "Cloud Security Toolkit",
                TOOLS["21"][1]
            )
            continue

        # Container Security Toolkit
        if pilihan == "22":
            run_tool(
                "Container Security Toolkit",
                TOOLS["22"][1]
            )
            continue

        # Mobile Security Toolkit
        if pilihan == "23":
            run_tool(
                "Mobile Security Toolkit",
                TOOLS["23"][1]
            )
            continue

        # Database Forensics Toolkit
        if pilihan == "24":
            run_tool(
                "Database Forensics Toolkit",
                TOOLS["24"][1]
            )
            continue

        # Rentora Analyzer
        if pilihan == "25":
            run_rentora()
            continue

        # Tool Help
        if pilihan == "26":
            show_cli_help()
            continue

        # Tool biasa
        if pilihan in TOOLS:

            name, filename = TOOLS[pilihan]

            run_tool(
                name,
                filename
            )

            continue

        print(
            "\n[!] Pilihan tidak valid."
        )

        wait_enter()


if __name__ == "__main__":
    main()
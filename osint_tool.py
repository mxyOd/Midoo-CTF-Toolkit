#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import webbrowser


TOOLS = {
    "1": {
        "name": "Sherlock",
        "command": "sherlock",
        "description": "Username OSINT"
    },
    "2": {
        "name": "theHarvester",
        "command": "theHarvester",
        "description": "Domain / email / host OSINT"
    },
    "3": {
        "name": "Shodan CLI",
        "command": "shodan",
        "description": "Internet-connected device search"
    },
    "4": {
        "name": "Censys CLI",
        "command": "censys",
        "description": "Internet host and certificate search"
    },
    "5": {
        "name": "Recon-ng",
        "command": "recon-ng",
        "description": "OSINT reconnaissance framework"
    },
    "6": {
        "name": "SpiderFoot",
        "command": "sf.py",
        "description": "Automated OSINT reconnaissance"
    },
}


WEB_TOOLS = {
    "7": (
        "OSINT HackUnderway",
        "https://" + "osint.hackunderway.io/"
    ),
    "8": (
        "Maltego",
        "https://" + "www.maltego.com/"
    ),
    "9": (
        "Google Dorking",
        "https://www.google.com/search?q="
    ),
    "10": (
        "IntelX",
        "https://" + "intelx.io/"
    ),
    "11": (
        "IntelBase",
        "https://" + "intelbase.is/"
    ),
    "12": (
        "ShadowDragon",
        "https://" + "shadowdragon.io/"
    ),
    "13": (
        "PhoneHunter",
        "https://" + "phonehunter.io/"
    ),
}


def clear_screen():
    os.system(
        "cls" if os.name == "nt" else "clear"
    )


def wait_enter():
    input("\nTekan Enter untuk kembali...")


def command_exists(command):
    return shutil.which(command) is not None


def check_tool(command):
    if not command_exists(command):
        print(
            f"\n[!] Tool tidak ditemukan: {command}"
        )

        print(
            "\n[*] Install tool tersebut terlebih dahulu "
            "atau pastikan sudah ada di PATH."
        )

        wait_enter()
        return False

    return True


def run_command(command, arguments=None):
    if arguments is None:
        arguments = []

    try:
        subprocess.run(
            [command] + arguments,
            check=False
        )

    except KeyboardInterrupt:
        print(
            "\n\n[!] Tool dihentikan."
        )

    except Exception as error:
        print(
            f"\n[!] Error: {error}"
        )

    wait_enter()


def run_sherlock():
    command = TOOLS["1"]["command"]

    if not check_tool(command):
        return

    clear_screen()

    print("""
=============================================
              Midoo Sherlock
=============================================
""")

    username = input(
        "Masukkan username: "
    ).strip()

    if not username:
        print(
            "\n[!] Username tidak boleh kosong."
        )
        wait_enter()
        return

    print(
        f"\n[*] Mencari username: {username}\n"
    )

    run_command(
        command,
        [username]
    )


def run_theharvester():
    command = TOOLS["2"]["command"]

    if not check_tool(command):
        return

    clear_screen()

    print("""
=============================================
             Midoo theHarvester
=============================================
""")

    domain = input(
        "Masukkan domain: "
    ).strip()

    if not domain:
        print(
            "\n[!] Domain tidak boleh kosong."
        )
        wait_enter()
        return

    print("""
Contoh source pasif:
    crtsh
    certspotter

Gunakan source yang diperlukan saja.
""")

    source = input(
        "Source [crtsh,certspotter]: "
    ).strip()

    if not source:
        source = "crtsh,certspotter"

    print(
        "\n[*] Menjalankan theHarvester...\n"
    )

    run_command(
        command,
        [
            "-d",
            domain,
            "-b",
            source
        ]
    )


def run_shodan():
    command = TOOLS["3"]["command"]

    if not check_tool(command):
        return

    clear_screen()

    print("""
=============================================
              Midoo Shodan
=============================================
""")

    print(
        "Masukkan command Shodan setelah menu ini."
    )

    print(
        "\nContoh:"
    )

    print(
        "  shodan -h"
    )

    print(
        "  shodan info"
    )

    print(
        "  shodan host <IP>"
    )

    print()

    run_command(
        command,
        []
    )


def run_censys():
    command = TOOLS["4"]["command"]

    if not check_tool(command):
        return

    clear_screen()

    print("""
=============================================
              Midoo Censys
=============================================
""")

    print(
        "[*] Membuka Censys CLI..."
    )

    print(
        "[*] Gunakan -h untuk melihat command."
    )

    print()

    run_command(
        command,
        []
    )


def run_recon_ng():
    command = TOOLS["5"]["command"]

    if not check_tool(command):
        return

    clear_screen()

    print("""
=============================================
              Midoo Recon-ng
=============================================
""")

    print(
        "[*] Menjalankan Recon-ng...\n"
    )

    run_command(
        command,
        []
    )


def run_spiderfoot():
    command = TOOLS["6"]["command"]

    if not check_tool(command):
        return

    clear_screen()

    print("""
=============================================
             Midoo SpiderFoot
=============================================
""")

    print(
        "[*] Menjalankan SpiderFoot..."
    )

    print(
        "[*] SpiderFoot biasanya menyediakan "
        "web interface lokal."
    )

    print()

    run_command(
        command,
        [
            "-l",
            "127.0.0.1:5001"
        ]
    )


def open_web_tool(name, url):
    clear_screen()

    print("=============================================")
    print(f"              {name}")
    print("=============================================\n")

    print(
        f"[*] Membuka {name} di browser..."
    )

    try:
        webbrowser.open(url)

    except Exception as error:
        print(
            f"\n[!] Gagal membuka browser: {error}"
        )

    wait_enter()


def google_dorking():
    clear_screen()

    print("""
=============================================
             Midoo Google Dorking
=============================================
""")

    print("""
Contoh query:

    site:example.com
    site:example.com filetype:pdf
    site:example.com inurl:login
    site:example.com intitle:index.of

Gunakan hanya pada domain yang memang
berada dalam scope pengujian.
""")

    query = input(
        "Masukkan dork: "
    ).strip()

    if not query:
        print(
            "\n[!] Query tidak boleh kosong."
        )
        wait_enter()
        return

    url = (
        "https://www.google.com/search?q="
        + query.replace(" ", "+")
    )

    open_web_tool(
        "Google Dorking",
        url
    )


def show_tool_status():
    clear_screen()

    print("""
=============================================
            Midoo OSINT Tool Status
=============================================
""")

    for number, data in TOOLS.items():
        command = data["command"]

        if command_exists(command):
            status = "[✓] Installed"
        else:
            status = "[-] Not Found"

        print(
            f"  [{number}] "
            f"{data['name']:<20} "
            f"{status}"
        )

    print(
        "\n============================================="
    )

    wait_enter()


def show_menu():
    print("""
=============================================
            Midoo OSINT Toolkit
                    v2.0
=============================================

  LOCAL / CLI TOOLS

    [1]  Sherlock
    [2]  theHarvester
    [3]  Shodan CLI
    [4]  Censys CLI
    [5]  Recon-ng
    [6]  SpiderFoot

  WEB OSINT

    [7]  OSINT HackUnderway
    [8]  Maltego
    [9]  Google Dorking
    [10] IntelX
    [11] IntelBase
    [12] ShadowDragon
    [13] PhoneHunter

  UTILITY

    [14] Tool Status
    [0]  Exit

=============================================
""")


def main():
    while True:
        clear_screen()
        show_menu()

        pilihan = input(
            "Midoo OSINT > "
        ).strip()

        if pilihan == "0":
            clear_screen()

            print(
                "Midoo OSINT Toolkit terminated."
            )

            break

        if pilihan == "1":
            run_sherlock()
            continue

        if pilihan == "2":
            run_theharvester()
            continue

        if pilihan == "3":
            run_shodan()
            continue

        if pilihan == "4":
            run_censys()
            continue

        if pilihan == "5":
            run_recon_ng()
            continue

        if pilihan == "6":
            run_spiderfoot()
            continue

        if pilihan == "7":
            open_web_tool(
                WEB_TOOLS["7"][0],
                WEB_TOOLS["7"][1]
            )
            continue

        if pilihan == "8":
            open_web_tool(
                WEB_TOOLS["8"][0],
                WEB_TOOLS["8"][1]
            )
            continue

        if pilihan == "9":
            google_dorking()
            continue

        if pilihan == "10":
            open_web_tool(
                WEB_TOOLS["10"][0],
                WEB_TOOLS["10"][1]
            )
            continue

        if pilihan == "11":
            open_web_tool(
                WEB_TOOLS["11"][0],
                WEB_TOOLS["11"][1]
            )
            continue

        if pilihan == "12":
            open_web_tool(
                WEB_TOOLS["12"][0],
                WEB_TOOLS["12"][1]
            )
            continue

        if pilihan == "13":
            open_web_tool(
                WEB_TOOLS["13"][0],
                WEB_TOOLS["13"][1]
            )
            continue

        if pilihan == "14":
            show_tool_status()
            continue

        print(
            "\n[!] Pilihan tidak valid."
        )

        wait_enter()


if __name__ == "__main__":
    main()
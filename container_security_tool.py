#!/usr/bin/env python3

import json
import os
import shutil
import subprocess


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def wait_enter():
    input("\nTekan Enter untuk kembali...")


def docker_available():
    return shutil.which("docker") is not None


def run_docker(args):
    try:
        result = subprocess.run(
            ["docker"] + args,
            capture_output=True,
            text=True,
            check=False
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        return result.returncode

    except KeyboardInterrupt:
        print("\n[!] Proses dihentikan.")
        return 1

    except Exception as error:
        print(f"\n[!] Error: {error}")
        return 1


def docker_analyzer():
    clear_screen()

    print("""
=============================================
          Midoo Docker Analyzer
=============================================
""")

    if not docker_available():
        print("[!] Docker tidak ditemukan.")
        wait_enter()
        return

    print("[+] Docker tersedia.\n")

    run_docker(["version", "--format", "{{.Server.Version}}"])

    print("\n[+] Docker Information\n")

    run_docker(["info"])

    wait_enter()


def image_analyzer():
    clear_screen()

    print("""
=============================================
           Midoo Image Analyzer
=============================================
""")

    if not docker_available():
        print("[!] Docker tidak ditemukan.")
        wait_enter()
        return

    image = input(
        "\nMasukkan nama image: "
    ).strip()

    if not image:
        print("\n[!] Image tidak boleh kosong.")
        wait_enter()
        return

    print(
        f"\n[*] Menganalisis image: {image}\n"
    )

    run_docker([
        "image",
        "inspect",
        image
    ])

    wait_enter()


def dockerfile_analyzer():
    clear_screen()

    print("""
=============================================
         Midoo Dockerfile Analyzer
=============================================
""")

    path = input(
        "\nMasukkan path Dockerfile: "
    ).strip()

    if not path:
        print("\n[!] Path tidak boleh kosong.")
        wait_enter()
        return

    if not os.path.isfile(path):
        print(
            f"\n[!] File tidak ditemukan: {path}"
        )
        wait_enter()
        return

    print("\n[+] Dockerfile Analysis\n")

    dangerous_patterns = {
        "latest tag": ":latest",
        "privileged": "privileged",
        "host network": "network=host",
        "ADD remote URL": "ADD http",
        "curl pipe shell": "| sh",
        "wget pipe shell": "| bash",
    }

    try:
        with open(
            path,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as file:
            content = file.read()

        lines = content.splitlines()

        print(
            f"[*] Total lines : {len(lines)}"
        )

        print("\n[*] Instructions:")

        for line in lines:
            stripped = line.strip()

            if stripped and not stripped.startswith("#"):
                print(f"    {stripped}")

        print("\n[*] Basic Checks:")

        found = False

        lower_content = content.lower()

        for name, pattern in dangerous_patterns.items():

            if pattern.lower() in lower_content:
                print(
                    f"  [!] Potential issue: {name}"
                )
                found = True

        if not found:
            print(
                "  [✓] Tidak ditemukan pattern "
                "dasar yang diperiksa."
            )

    except Exception as error:
        print(
            f"\n[!] Error: {error}"
        )

    wait_enter()


def container_configuration():
    clear_screen()

    print("""
=============================================
       Midoo Container Configuration
=============================================
""")

    if not docker_available():
        print("[!] Docker tidak ditemukan.")
        wait_enter()
        return

    container = input(
        "\nMasukkan container name/ID: "
    ).strip()

    if not container:
        print("\n[!] Container tidak boleh kosong.")
        wait_enter()
        return

    print("\n[+] Container Configuration\n")

    run_docker([
        "inspect",
        container
    ])

    wait_enter()


def port_network_analysis():
    clear_screen()

    print("""
=============================================
        Midoo Port & Network Analysis
=============================================
""")

    if not docker_available():
        print("[!] Docker tidak ditemukan.")
        wait_enter()
        return

    container = input(
        "\nMasukkan container name/ID: "
    ).strip()

    if not container:
        print("\n[!] Container tidak boleh kosong.")
        wait_enter()
        return

    print("\n[+] Port Mapping\n")

    run_docker([
        "port",
        container
    ])

    print("\n[+] Network Information\n")

    run_docker([
        "inspect",
        "--format",
        "{{json .NetworkSettings.Networks}}",
        container
    ])

    wait_enter()


def environment_analysis():
    clear_screen()

    print("""
=============================================
         Midoo Environment Analysis
=============================================
""")

    if not docker_available():
        print("[!] Docker tidak ditemukan.")
        wait_enter()
        return

    container = input(
        "\nMasukkan container name/ID: "
    ).strip()

    if not container:
        print("\n[!] Container tidak boleh kosong.")
        wait_enter()
        return

    print("""
[!] Perhatian:
    Environment variable dapat berisi
    credential atau secret.

    Jangan membagikan output ke repository
    publik atau orang lain.
""")

    confirm = input(
        "Tampilkan environment? [y/N]: "
    ).strip().lower()

    if confirm != "y":
        print("\n[*] Dibatalkan.")
        wait_enter()
        return

    print("\n[+] Environment Variables\n")

    run_docker([
        "inspect",
        "--format",
        "{{range .Config.Env}}{{println .}}{{end}}",
        container
    ])

    wait_enter()


def filesystem_analysis():
    clear_screen()

    print("""
=============================================
         Midoo Container Filesystem
=============================================
""")

    if not docker_available():
        print("[!] Docker tidak ditemukan.")
        wait_enter()
        return

    container = input(
        "\nMasukkan container name/ID: "
    ).strip()

    if not container:
        print("\n[!] Container tidak boleh kosong.")
        wait_enter()
        return

    print("\n[+] Container Mounts\n")

    run_docker([
        "inspect",
        "--format",
        "{{json .Mounts}}",
        container
    ])

    print("\n[+] Container Root Filesystem\n")

    run_docker([
        "exec",
        container,
        "sh",
        "-c",
        "ls -la /"
    ])

    wait_enter()


def security_checker():
    clear_screen()

    print("""
=============================================
          Midoo Container Security
=============================================
""")

    if not docker_available():
        print("[!] Docker tidak ditemukan.")
        wait_enter()
        return

    container = input(
        "\nMasukkan container name/ID: "
    ).strip()

    if not container:
        print("\n[!] Container tidak boleh kosong.")
        wait_enter()
        return

    try:
        result = subprocess.run(
            [
                "docker",
                "inspect",
                container
            ],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            print(
                "\n[!] Container tidak ditemukan."
            )
            wait_enter()
            return

        data = json.loads(result.stdout)[0]

        host_config = data.get(
            "HostConfig",
            {}
        )

        config = data.get(
            "Config",
            {}
        )

        print("\n[+] Basic Security Checks\n")

        privileged = host_config.get(
            "Privileged",
            False
        )

        if privileged:
            print(
                "[!] Privileged mode : ENABLED"
            )
        else:
            print(
                "[✓] Privileged mode : disabled"
            )

        network_mode = host_config.get(
            "NetworkMode"
        )

        print(
            f"[*] Network mode     : {network_mode}"
        )

        user = config.get("User")

        if user:
            print(
                f"[✓] Container user   : {user}"
            )
        else:
            print(
                "[!] Container user   : default/root"
            )

        readonly = host_config.get(
            "ReadonlyRootfs",
            False
        )

        if readonly:
            print(
                "[✓] Read-only rootfs : enabled"
            )
        else:
            print(
                "[!] Read-only rootfs : disabled"
            )

    except json.JSONDecodeError:
        print(
            "\n[!] Gagal membaca Docker JSON."
        )

    except Exception as error:
        print(
            f"\n[!] Error: {error}"
        )

    wait_enter()


def tool_status():
    clear_screen()

    print("""
=============================================
        Midoo Container Tool Status
=============================================
""")

    if docker_available():
        print("[✓] Docker CLI        Installed")

        run_docker([
            "--version"
        ])

    else:
        print("[-] Docker CLI        Not Found")

    wait_enter()


def show_menu():
    print("""
=============================================
       Midoo Container Security Toolkit
                    v1.0
=============================================

    [1] Docker Analyzer
    [2] Image Analyzer
    [3] Dockerfile Analyzer
    [4] Container Configuration
    [5] Port & Network Analysis
    [6] Environment Analysis
    [7] Container Filesystem
    [8] Security Checker
    [9] Tool Status

    [0] Kembali

=============================================
""")


def main():

    while True:

        clear_screen()
        show_menu()

        pilihan = input(
            "Midoo Container > "
        ).strip()

        if pilihan == "0":
            break

        elif pilihan == "1":
            docker_analyzer()

        elif pilihan == "2":
            image_analyzer()

        elif pilihan == "3":
            dockerfile_analyzer()

        elif pilihan == "4":
            container_configuration()

        elif pilihan == "5":
            port_network_analysis()

        elif pilihan == "6":
            environment_analysis()

        elif pilihan == "7":
            filesystem_analysis()

        elif pilihan == "8":
            security_checker()

        elif pilihan == "9":
            tool_status()

        else:
            print(
                "\n[!] Pilihan tidak valid."
            )
            wait_enter()


if __name__ == "__main__":
    main()
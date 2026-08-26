import os
import re
import subprocess


def check_tshark():
    try:
        subprocess.run(
            ["tshark", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except Exception:
        return False


def run_tshark(args):
    try:
        result = subprocess.run(
            ["tshark"] + args,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print("[!] TShark error:")
            print(result.stderr.strip())
            return None

        return result.stdout

    except subprocess.TimeoutExpired:
        print("[!] Analisis timeout.")
        return None


def get_file():
    path = input("\nMasukkan path PCAP/PCAPNG: ").strip()

    if not os.path.isfile(path):
        print("[!] File tidak ditemukan.")
        return None

    return path


def pcap_information():
    path = get_file()

    if not path:
        return

    output = run_tshark(["-r", path, "-q", "-z", "io,phs"])

    print("\n========================================")
    print("             PCAP INFORMATION")
    print("========================================")

    if output:
        print(output)


def packet_summary():
    path = get_file()

    if not path:
        return

    output = run_tshark([
        "-r",
        path,
        "-c",
        "30"
    ])

    print("\n========================================")
    print("              PACKETS")
    print("========================================")

    if output:
        print(output)


def protocol_statistics():
    path = get_file()

    if not path:
        return

    output = run_tshark([
        "-r",
        path,
        "-q",
        "-z",
        "io,phs"
    ])

    print("\n========================================")
    print("          PROTOCOL STATISTICS")
    print("========================================")

    if output:
        print(output)


def ip_statistics():
    path = get_file()

    if not path:
        return

    output = run_tshark([
        "-r",
        path,
        "-T",
        "fields",
        "-e",
        "ip.src",
        "-e",
        "ip.dst"
    ])

    print("\n========================================")
    print("              IP STATISTICS")
    print("========================================")

    if not output:
        return

    pairs = {}

    for line in output.splitlines():
        parts = line.split("\t")

        if len(parts) < 2:
            continue

        src = parts[0]
        dst = parts[1]

        if not src or not dst:
            continue

        key = (src, dst)
        pairs[key] = pairs.get(key, 0) + 1

    for (src, dst), count in sorted(
        pairs.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"{src:20} -> {dst:20} {count} packets")


def port_statistics():
    path = get_file()

    if not path:
        return

    output = run_tshark([
        "-r",
        path,
        "-T",
        "fields",
        "-e",
        "tcp.dstport",
        "-e",
        "udp.dstport"
    ])

    print("\n========================================")
    print("             PORT STATISTICS")
    print("========================================")

    if not output:
        return

    ports = {}

    for line in output.splitlines():
        for port in line.split("\t"):
            if port.isdigit():
                ports[port] = ports.get(port, 0) + 1

    for port, count in sorted(
        ports.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"Port {port:5} : {count} packets")


def dns_queries():
    path = get_file()

    if not path:
        return

    output = run_tshark([
        "-r",
        path,
        "-Y",
        "dns.qry.name",
        "-T",
        "fields",
        "-e",
        "frame.number",
        "-e",
        "ip.src",
        "-e",
        "dns.qry.name"
    ])

    print("\n========================================")
    print("               DNS QUERIES")
    print("========================================")

    if output:
        print(output)
    else:
        print("[!] Tidak ditemukan DNS query.")


def http_requests():
    path = get_file()

    if not path:
        return

    output = run_tshark([
        "-r",
        path,
        "-Y",
        "http.request",
        "-T",
        "fields",
        "-e",
        "frame.number",
        "-e",
        "ip.src",
        "-e",
        "http.host",
        "-e",
        "http.request.method",
        "-e",
        "http.request.uri"
    ])

    print("\n========================================")
    print("             HTTP REQUESTS")
    print("========================================")

    if output:
        print(output)
    else:
        print("[!] Tidak ditemukan HTTP request.")


def search_flag():
    path = get_file()

    if not path:
        return

    print("\nMasukkan keyword yang dicari.")
    keyword = input("Keyword [default: Midoo{]: ").strip()

    if not keyword:
        keyword = "Midoo{"

    output = run_tshark([
        "-r",
        path,
        "-x"
    ])

    print("\n========================================")
    print("              FLAG SEARCH")
    print("========================================")

    if not output:
        print("[!] Tidak ada data.")
        return

    matches = re.findall(
        rf".{{0,100}}{re.escape(keyword)}.{{0,150}}",
        output,
        re.IGNORECASE
    )

    if matches:
        for match in matches:
            print(match)
    else:
        print(f"[-] Keyword '{keyword}' tidak ditemukan.")


def extract_strings():
    path = get_file()

    if not path:
        return

    try:
        with open(path, "rb") as f:
            data = f.read()

        strings = re.findall(rb"[\x20-\x7e]{4,}", data)

        print("\n========================================")
        print("            PRINTABLE STRINGS")
        print("========================================")

        count = 0

        for item in strings:
            print(item.decode("ascii", errors="ignore"))
            count += 1

            if count >= 100:
                print("\n[!] Hanya 100 string pertama.")
                break

        print(f"\n[+] Total printable strings: {len(strings)}")

    except Exception as e:
        print(f"[!] Error: {e}")


def main():

    if not check_tshark():
        print("[!] TShark belum terinstall.")
        print("Install dengan:")
        print("sudo apt install tshark")
        return

    while True:

        print("""
========================================
        Midoo PCAP Analyzer
========================================
1. PCAP Information
2. Packet Summary
3. Protocol Statistics
4. IP Statistics
5. Port Statistics
6. DNS Queries
7. HTTP Requests
8. Search Flag
9. Extract Strings
10. Exit
========================================
""")

        pilihan = input("Pilih: ")

        if pilihan == "1":
            pcap_information()

        elif pilihan == "2":
            packet_summary()

        elif pilihan == "3":
            protocol_statistics()

        elif pilihan == "4":
            ip_statistics()

        elif pilihan == "5":
            port_statistics()

        elif pilihan == "6":
            dns_queries()

        elif pilihan == "7":
            http_requests()

        elif pilihan == "8":
            search_flag()

        elif pilihan == "9":
            extract_strings()

        elif pilihan == "10":
            print("Keluar...")
            break

        else:
            print("[!] Pilihan tidak valid.")


if __name__ == "__main__":
    main()
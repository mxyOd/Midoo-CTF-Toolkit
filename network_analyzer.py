import ipaddress
import socket
import subprocess


def ip_information():
    value = input("\nMasukkan IP/CIDR: ").strip()

    try:
        if "/" in value:
            network = ipaddress.ip_network(value, strict=False)
        else:
            address = ipaddress.ip_address(value)
            network = ipaddress.ip_network(
                f"{address}/{32 if address.version == 4 else 128}",
                strict=False
            )

        print("\n========================================")
        print("             IP INFORMATION")
        print("========================================")
        print(f"IP Version    : IPv{network.version}")
        print(f"Network       : {network.network_address}")
        print(f"Netmask       : {network.netmask}")
        print(f"Broadcast     : {network.broadcast_address}")
        print(f"Prefix        : /{network.prefixlen}")
        print(f"Total Address : {network.num_addresses}")

        if network.version == 4:
            usable = max(network.num_addresses - 2, 0)
            print(f"Usable Hosts  : {usable}")

            hosts = list(network.hosts())

            if hosts:
                print(f"First Host    : {hosts[0]}")
                print(f"Last Host     : {hosts[-1]}")

    except ValueError:
        print("[!] IP/CIDR tidak valid.")


def cidr_calculator():
    cidr = input("\nMasukkan CIDR: ").strip()

    try:
        network = ipaddress.ip_network(cidr, strict=False)

        print("\n========================================")
        print("             CIDR CALCULATOR")
        print("========================================")
        print(f"Network       : {network.network_address}")
        print(f"Netmask       : {network.netmask}")
        print(f"Prefix        : /{network.prefixlen}")
        print(f"Broadcast     : {network.broadcast_address}")
        print(f"Total Address : {network.num_addresses}")

        if network.version == 4:
            print(f"Usable Hosts  : {max(network.num_addresses - 2, 0)}")

        print(f"First Address : {network.network_address}")
        print(f"Last Address  : {network.broadcast_address}")

    except ValueError:
        print("[!] CIDR tidak valid.")


def dns_lookup():
    domain = input("\nMasukkan domain: ").strip()

    print("\n========================================")
    print("               DNS LOOKUP")
    print("========================================")

    try:
        results = socket.getaddrinfo(domain, None)

        ipv4 = set()
        ipv6 = set()

        for result in results:
            address = result[4][0]

            if ":" in address:
                ipv6.add(address)
            else:
                ipv4.add(address)

        print("\nA Records:")
        if ipv4:
            for ip in sorted(ipv4):
                print(f"  {ip}")
        else:
            print("  Tidak ditemukan.")

        print("\nAAAA Records:")
        if ipv6:
            for ip in sorted(ipv6):
                print(f"  {ip}")
        else:
            print("  Tidak ditemukan.")

    except socket.gaierror:
        print("[!] Domain tidak dapat di-resolve.")


def dns_record_lookup():
    domain = input("\nMasukkan domain: ").strip()

    print("""
========================================
             DNS RECORDS
========================================
1. A
2. AAAA
3. MX
4. NS
5. TXT
6. Semua
========================================
""")

    record = input("Pilih: ").strip()

    record_types = {
        "1": "A",
        "2": "AAAA",
        "3": "MX",
        "4": "NS",
        "5": "TXT",
    }

    if record == "6":
        records = ["A", "AAAA", "MX", "NS", "TXT"]
    elif record in record_types:
        records = [record_types[record]]
    else:
        print("[!] Pilihan tidak valid.")
        return

    for record_type in records:
        print(f"\n--- {record_type} ---")

        try:
            result = subprocess.run(
                ["dig", "+short", record_type, domain],
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout.strip()

            if output:
                print(output)
            else:
                print("Tidak ditemukan.")

        except FileNotFoundError:
            print("[!] Command 'dig' belum tersedia.")
            print("Install dengan:")
            print("sudo apt install dnsutils")
            return

        except subprocess.TimeoutExpired:
            print("[!] DNS query timeout.")


def reverse_dns():
    ip = input("\nMasukkan IP: ").strip()

    try:
        ipaddress.ip_address(ip)

        hostname, aliases, addresses = socket.gethostbyaddr(ip)

        print("\n========================================")
        print("             REVERSE DNS")
        print("========================================")
        print(f"IP       : {ip}")
        print(f"Hostname : {hostname}")

        if aliases:
            print(f"Aliases  : {', '.join(aliases)}")

    except ValueError:
        print("[!] IP tidak valid.")

    except socket.herror:
        print("[!] Reverse DNS tidak ditemukan.")


def connectivity():
    host = input("\nMasukkan IP/domain: ").strip()

    print("\nChecking connectivity...")

    try:
        result = subprocess.run(
            ["ping", "-c", "4", host],
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.returncode == 0:
            print("[+] Host reachable.")
        else:
            print("[-] Host tidak merespons.")

    except FileNotFoundError:
        print("[!] Command ping tidak ditemukan.")


def port_check():
    host = input("\nMasukkan IP/domain: ").strip()

    try:
        port = int(input("Masukkan port: "))

        if not 1 <= port <= 65535:
            print("[!] Port harus 1-65535.")
            return

        print(f"\nChecking {host}:{port}...")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            print(f"[+] Port {port} OPEN")
        else:
            print(f"[-] Port {port} CLOSED/FILTERED")

    except ValueError:
        print("[!] Port harus berupa angka.")

    except socket.gaierror:
        print("[!] Host tidak dapat ditemukan.")


def main():
    while True:
        print("""
========================================
        Midoo Network Analyzer v2
========================================
1. IP Information
2. CIDR Calculator
3. DNS Lookup
4. DNS Records
5. Reverse DNS
6. Check Connectivity
7. Port Check
8. Exit
========================================
""")

        pilihan = input("Pilih: ")

        if pilihan == "1":
            ip_information()

        elif pilihan == "2":
            cidr_calculator()

        elif pilihan == "3":
            dns_lookup()

        elif pilihan == "4":
            dns_record_lookup()

        elif pilihan == "5":
            reverse_dns()

        elif pilihan == "6":
            connectivity()

        elif pilihan == "7":
            port_check()

        elif pilihan == "8":
            print("Keluar...")
            break

        else:
            print("[!] Pilihan tidak valid.")


if __name__ == "__main__":
    main()
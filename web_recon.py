import re
import socket
import ssl
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlparse


USER_AGENT = "Midoo-Web-Recon/1.0"


def normalize_url(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    return url.rstrip("/")


def request(url, timeout=10):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )

    try:
        return urllib.request.urlopen(req, timeout=timeout)

    except urllib.error.HTTPError as e:
        return e

    except urllib.error.URLError as e:
        print(f"[!] Connection error: {e.reason}")
        return None

    except Exception as e:
        print(f"[!] Error: {e}")
        return None


def get_target():
    url = input("\nMasukkan URL target: ")
    return normalize_url(url)


def http_headers():
    url = get_target()
    response = request(url)

    if not response:
        return

    print("\n========================================")
    print("              HTTP HEADERS")
    print("========================================")

    print(f"URL    : {response.geturl()}")
    print(f"Status : {response.status}")

    for key, value in response.headers.items():
        print(f"{key}: {value}")


def status_code():
    url = get_target()
    response = request(url)

    if not response:
        return

    print("\n========================================")
    print("              STATUS CODE")
    print("========================================")

    print(f"URL    : {response.geturl()}")
    print(f"Status : {response.status}")
    print(f"Reason : {response.reason}")


def dns_information():
    url = get_target()
    hostname = urlparse(url).hostname

    if not hostname:
        print("[!] Hostname tidak valid.")
        return

    print("\n========================================")
    print("             DNS INFORMATION")
    print("========================================")

    print(f"Hostname: {hostname}")

    try:
        addresses = socket.getaddrinfo(hostname, None)

        ipv4 = set()
        ipv6 = set()

        for result in addresses:
            address = result[4][0]

            if ":" in address:
                ipv6.add(address)
            else:
                ipv4.add(address)

        print("\nIPv4:")

        for ip in sorted(ipv4):
            print(f"  {ip}")

        print("\nIPv6:")

        for ip in sorted(ipv6):
            print(f"  {ip}")

    except socket.gaierror:
        print("[!] DNS resolution gagal.")


def robots_txt():
    url = get_target()
    target = urljoin(url + "/", "robots.txt")

    response = request(target)

    print("\n========================================")
    print("              ROBOTS.TXT")
    print("========================================")

    if not response:
        return

    if response.status != 200:
        print(f"[!] Status: {response.status}")
        return

    try:
        content = response.read().decode(
            "utf-8",
            errors="ignore"
        )

        print(content)

    except Exception as e:
        print(f"[!] Error membaca robots.txt: {e}")


def sitemap_xml():
    url = get_target()
    target = urljoin(url + "/", "sitemap.xml")

    response = request(target)

    print("\n========================================")
    print("             SITEMAP.XML")
    print("========================================")

    if not response:
        return

    if response.status != 200:
        print(f"[!] Status: {response.status}")
        return

    try:
        content = response.read().decode(
            "utf-8",
            errors="ignore"
        )

        print(content)

    except Exception as e:
        print(f"[!] Error membaca sitemap.xml: {e}")


def tls_information():
    url = get_target()
    parsed = urlparse(url)

    hostname = parsed.hostname

    if not hostname:
        print("[!] Hostname tidak valid.")
        return

    port = parsed.port or 443

    print("\n========================================")
    print("              TLS INFORMATION")
    print("========================================")

    print(f"Host : {hostname}")
    print(f"Port : {port}")

    context = ssl.create_default_context()

    try:
        with socket.create_connection(
            (hostname, port),
            timeout=10
        ) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=hostname
            ) as secure_sock:

                certificate = secure_sock.getpeercert()

                print(f"TLS Version : {secure_sock.version()}")
                print(f"Cipher      : {secure_sock.cipher()[0]}")

                subject = certificate.get("subject", [])

                print("\nCertificate Subject:")

                for item in subject:
                    for key, value in item:
                        print(f"  {key}: {value}")

    except Exception as e:
        print(f"[!] TLS connection gagal: {e}")


def page_title():
    url = get_target()
    response = request(url)

    if not response:
        return

    print("\n========================================")
    print("               PAGE TITLE")
    print("========================================")

    try:
        content = response.read().decode(
            "utf-8",
            errors="ignore"
        )

        match = re.search(
            r"<title[^>]*>(.*?)</title>",
            content,
            re.IGNORECASE | re.DOTALL
        )

        if match:
            title = re.sub(
                r"\s+",
                " ",
                match.group(1)
            ).strip()

            print(f"Title: {title}")

        else:
            print("[!] Title tidak ditemukan.")

    except Exception as e:
        print(f"[!] Error: {e}")


def technology_hints():
    url = get_target()
    response = request(url)

    if not response:
        return

    print("\n========================================")
    print("           TECHNOLOGY HINTS")
    print("========================================")

    headers = response.headers

    detected = set()

    server = headers.get("Server")

    if server:
        print(f"[+] Server: {server}")
        detected.add(server)

    powered = headers.get("X-Powered-By")

    if powered:
        print(f"[+] X-Powered-By: {powered}")
        detected.add(powered)

    try:
        content = response.read().decode(
            "utf-8",
            errors="ignore"
        )

        signatures = {
            "WordPress": [
                "wp-content",
                "wp-includes"
            ],
            "React": [
                "__NEXT_DATA__",
                "react"
            ],
            "Vue": [
                "vue"
            ],
            "Laravel": [
                "laravel"
            ],
            "Django": [
                "csrfmiddlewaretoken"
            ]
        }

        for technology, patterns in signatures.items():

            for pattern in patterns:

                if pattern.lower() in content.lower():

                    print(f"[+] Possible: {technology}")
                    detected.add(technology)
                    break

    except Exception:
        pass

    if not detected:
        print("[-] Tidak ada technology signature yang jelas.")


def main():

    while True:

        print("""
========================================
           Midoo Web Recon
========================================
1. HTTP Headers
2. Status Code
3. DNS Information
4. Robots.txt
5. Sitemap.xml
6. TLS Information
7. Page Title
8. Technology Hints
9. Exit
========================================
""")

        pilihan = input("Pilih: ")

        if pilihan == "1":
            http_headers()

        elif pilihan == "2":
            status_code()

        elif pilihan == "3":
            dns_information()

        elif pilihan == "4":
            robots_txt()

        elif pilihan == "5":
            sitemap_xml()

        elif pilihan == "6":
            tls_information()

        elif pilihan == "7":
            page_title()

        elif pilihan == "8":
            technology_hints()

        elif pilihan == "9":
            print("Keluar...")
            break

        else:
            print("[!] Pilihan tidak valid.")


if __name__ == "__main__":
    main()
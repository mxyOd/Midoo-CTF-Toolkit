#!/usr/bin/env python3

import argparse
import ipaddress
import json
import re
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime


USER_AGENT = "Midoo-CTF-Toolkit/1.0"


def http_request(url, timeout=10):
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": USER_AGENT}
        )

        context = ssl.create_default_context()

        with urllib.request.urlopen(
            request,
            timeout=timeout,
            context=context
        ) as response:

            body = response.read(200000)

            return {
                "status": response.status,
                "url": response.geturl(),
                "headers": dict(response.headers),
                "body": body.decode(
                    "utf-8",
                    errors="replace"
                )
            }

    except urllib.error.HTTPError as error:
        return {
            "status": error.code,
            "url": error.geturl(),
            "headers": dict(error.headers),
            "body": ""
        }

    except Exception as error:
        return {
            "error": str(error)
        }


def normalize_url(value):
    if not value.startswith(
        ("http://", "https://")
    ):
        return "https://" + value

    return value


def dns_lookup(domain):
    results = set()

    try:
        addresses = socket.getaddrinfo(
            domain,
            None
        )

        for item in addresses:
            address = item[4][0]
            results.add(address)

    except socket.gaierror:
        pass

    return sorted(results)


def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]

    except (socket.herror, socket.gaierror):
        return None


def validate_ip(value):
    try:
        return ipaddress.ip_address(value)

    except ValueError:
        return None


def whois_lookup(domain):
    try:
        import shutil
        import subprocess

        if not shutil.which("whois"):
            return None

        result = subprocess.run(
            ["whois", domain],
            capture_output=True,
            text=True,
            timeout=15,
            check=False
        )

        if result.returncode == 0:
            return result.stdout

    except Exception:
        pass

    return None


def extract_technologies(headers, body):
    technologies = set()

    server = headers.get(
        "Server",
        ""
    )

    powered = headers.get(
        "X-Powered-By",
        ""
    )

    combined = (
        server + " " +
        powered + " " +
        body[:100000]
    ).lower()

    signatures = {
        "Nginx": [
            "nginx"
        ],
        "Apache": [
            "apache"
        ],
        "PHP": [
            "php",
            "x-powered-by: php"
        ],
        "WordPress": [
            "wp-content",
            "wp-includes"
        ],
        "React": [
            "react"
        ],
        "Vue.js": [
            "vue"
        ],
        "jQuery": [
            "jquery"
        ],
        "Bootstrap": [
            "bootstrap"
        ],
        "Cloudflare": [
            "cloudflare"
        ],
    }

    for name, patterns in signatures.items():
        for pattern in patterns:
            if pattern in combined:
                technologies.add(name)
                break

    return sorted(technologies)


def show_dns(domain):
    print("\n[+] DNS Information")

    addresses = dns_lookup(domain)

    if not addresses:
        print("  Tidak ditemukan address.")
        return

    for address in addresses:
        print(f"  {address}")


def show_ip_info(value):
    ip = validate_ip(value)

    if not ip:
        print(
            f"\n[!] IP tidak valid: {value}"
        )
        return

    print("\n[+] IP Information")

    print(f"  Address : {ip}")
    print(f"  Version : IPv{ip.version}")
    print(f"  Private : {ip.is_private}")
    print(f"  Global  : {ip.is_global}")
    print(f"  Loopback: {ip.is_loopback}")

    hostname = reverse_dns(value)

    if hostname:
        print(f"  Reverse : {hostname}")
    else:
        print("  Reverse : Tidak ditemukan")


def show_headers(result):
    print("\n[+] HTTP Information")

    if "error" in result:
        print(f"  Error: {result['error']}")
        return

    print(
        f"  Status : {result.get('status', '-')}"
    )

    print(
        f"  Final URL : {result.get('url', '-')}"
    )

    print("\n  Headers:")

    for key, value in result.get(
        "headers",
        {}
    ).items():
        print(
            f"    {key}: {value}"
        )


def show_security_headers(headers):
    print("\n[+] Security Headers")

    security_headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Permissions-Policy",
    ]

    for header in security_headers:
        value = headers.get(header)

        if value:
            print(
                f"  [✓] {header}: {value}"
            )
        else:
            print(
                f"  [-] {header}: tidak ditemukan"
            )


def show_url_info(url):
    parsed = urllib.parse.urlparse(url)

    print("\n[+] URL Information")

    print(f"  Scheme   : {parsed.scheme}")
    print(f"  Host     : {parsed.hostname}")
    print(f"  Port     : {parsed.port or '-'}")
    print(f"  Path     : {parsed.path or '/'}")
    print(f"  Query    : {parsed.query or '-'}")

    if parsed.query:
        parameters = urllib.parse.parse_qs(
            parsed.query
        )

        print("\n  Parameters:")

        for key in parameters:
            print(f"    {key}")


def show_username(username):
    print("\n[+] Public Username Check")

    platforms = {
        "GitHub": (
            "https://github.com/"
            + urllib.parse.quote(username)
        ),
        "GitLab": (
            "https://gitlab.com/"
            + urllib.parse.quote(username)
        ),
    }

    for platform, url in platforms.items():
        result = http_request(url)

        status = result.get("status")

        if status == 200:
            print(
                f"  [✓] {platform}: kemungkinan tersedia"
            )

        elif status == 404:
            print(
                f"  [-] {platform}: tidak ditemukan"
            )

        else:
            print(
                f"  [?] {platform}: HTTP {status}"
            )


def show_whois(domain):
    print("\n[+] WHOIS")

    result = whois_lookup(domain)

    if not result:
        print(
            "  WHOIS command tidak tersedia "
            "atau lookup gagal."
        )
        return

    lines = result.splitlines()

    for line in lines[:100]:
        print(f"  {line}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Midoo OSINT Toolkit - "
            "Passive Information Gathering"
        )
    )

    parser.add_argument(
        "-d",
        "--domain",
        help="Analisis domain"
    )

    parser.add_argument(
        "-i",
        "--ip",
        help="Analisis IP address"
    )

    parser.add_argument(
        "-u",
        "--url",
        help="Analisis URL"
    )

    parser.add_argument(
        "--username",
        help="Check username pada platform publik"
    )

    parser.add_argument(
        "--dns",
        action="store_true",
        help="Lakukan DNS lookup"
    )

    parser.add_argument(
        "--whois",
        action="store_true",
        help="Lakukan WHOIS lookup"
    )

    parser.add_argument(
        "--headers",
        action="store_true",
        help="Tampilkan HTTP headers"
    )

    parser.add_argument(
        "--security-headers",
        action="store_true",
        help="Analisis security headers"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Simpan hasil JSON"
    )

    args = parser.parse_args()

    if not any(
        [
            args.domain,
            args.ip,
            args.url,
            args.username,
        ]
    ):
        parser.print_help()
        return 1

    print("=============================================")
    print("             Midoo OSINT Toolkit")
    print("                  v1.0")
    print("=============================================\n")

    report = {
        "tool": "Midoo OSINT Toolkit",
        "version": "1.0",
        "timestamp": datetime.now().isoformat(),
    }

    if args.domain:
        domain = args.domain.strip()

        print("[+] Target Domain")
        print(f"  {domain}")

        report["domain"] = domain

        if args.dns or not (
            args.ip or
            args.url or
            args.username
        ):
            addresses = dns_lookup(domain)

            report["dns"] = addresses

            show_dns(domain)

        if args.whois:
            whois = whois_lookup(domain)

            if whois:
                report["whois"] = whois

            show_whois(domain)

    if args.ip:
        ip = args.ip.strip()

        show_ip_info(ip)

        report["ip"] = ip

    if args.url:
        url = normalize_url(
            args.url.strip()
        )

        show_url_info(url)

        result = http_request(url)

        report["url"] = url
        report["http"] = {
            "status": result.get("status"),
            "final_url": result.get("url"),
        }

        if args.headers:
            show_headers(result)

        if args.security_headers:
            show_security_headers(
                result.get("headers", {})
            )

        technologies = extract_technologies(
            result.get("headers", {}),
            result.get("body", "")
        )

        if technologies:
            print("\n[+] Technology Hints")

            for technology in technologies:
                print(
                    f"  [✓] {technology}"
                )

            report["technologies"] = technologies

    if args.username:
        username = args.username.strip()

        show_username(username)

        report["username"] = username

    if args.output:
        try:
            with open(
                args.output,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    report,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print(
                f"\n[✓] Report disimpan: "
                f"{args.output}"
            )

        except OSError as error:
            print(
                f"\n[!] Gagal membuat report: {error}"
            )

    print("\n=============================================")
    print("              ANALYSIS DONE")
    print("=============================================")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
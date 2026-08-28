#!/usr/bin/env python3

import argparse
import hashlib
import os
import re
from collections import Counter


IP_PATTERN = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)

URL_PATTERN = re.compile(
    r"https?://[^\s\"']+",
    re.IGNORECASE
)

METHOD_PATTERN = re.compile(
    r"\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b"
)

STATUS_PATTERN = re.compile(
    r"\b([1-5][0-9]{2})\b"
)

USER_AGENT_PATTERN = re.compile(
    r'"([^"]*(?:Mozilla|Chrome|Firefox|Safari|curl|Wget)[^"]*)"',
    re.IGNORECASE
)

SUSPICIOUS_PATTERNS = {
    "SQL Injection": [
        r"\bunion\s+select\b",
        r"\bselect\s+.*\s+from\b",
        r"\bor\s+1\s*=\s*1\b",
        r"\bdrop\s+table\b",
        r"\binformation_schema\b",
    ],
    "XSS": [
        r"<script",
        r"javascript:",
        r"onerror\s*=",
        r"onload\s*=",
    ],
    "Path Traversal": [
        r"\.\./",
        r"\.\.\\",
    ],
    "Command Injection": [
        r";\s*(?:id|whoami|uname|cat|ls)\b",
        r"\|\s*(?:id|whoami|uname|cat|ls)\b",
        r"\$\(",
        r"`[^`]+`",
    ],
    "Sensitive Files": [
        r"/etc/passwd",
        r"/etc/shadow",
        r"\.env\b",
        r"wp-config\.php",
    ],
}


def calculate_hash(path, algorithm):
    hasher = hashlib.new(algorithm)

    with open(path, "rb") as file:
        while True:
            chunk = file.read(1024 * 1024)

            if not chunk:
                break

            hasher.update(chunk)

    return hasher.hexdigest()


def valid_ip(ip):
    try:
        return all(
            0 <= int(part) <= 255
            for part in ip.split(".")
        )
    except ValueError:
        return False


def extract_ips(text):
    results = set()

    for ip in IP_PATTERN.findall(text):
        if valid_ip(ip):
            results.add(ip)

    return sorted(results)


def extract_urls(text):
    return sorted(
        set(URL_PATTERN.findall(text))
    )


def extract_methods(text):
    return METHOD_PATTERN.findall(text)


def extract_status_codes(text):
    return STATUS_PATTERN.findall(text)


def extract_user_agents(text):
    return USER_AGENT_PATTERN.findall(text)


def analyze_suspicious(text):
    findings = []

    for category, patterns in SUSPICIOUS_PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(
                pattern,
                text,
                re.IGNORECASE
            )

            if matches:
                findings.append(
                    (category, pattern, len(matches))
                )

    return findings


def show_file_info(path, lines):
    print("[+] Log File Information")

    print(f"  Name       : {os.path.basename(path)}")
    print(f"  Path       : {os.path.abspath(path)}")
    print(f"  Size       : {os.path.getsize(path)} bytes")
    print(f"  Lines      : {len(lines)}")
    print(f"  MD5        : {calculate_hash(path, 'md5')}")
    print(f"  SHA1       : {calculate_hash(path, 'sha1')}")
    print(f"  SHA256     : {calculate_hash(path, 'sha256')}")


def show_ips(text):
    print("\n[+] IP Addresses")

    ips = extract_ips(text)

    if not ips:
        print("  Tidak ditemukan IP address.")
        return

    for ip in ips:
        print(f"  {ip}")

    print(f"\n  Total unique IP: {len(ips)}")


def show_urls(text):
    print("\n[+] URLs / Paths")

    urls = extract_urls(text)

    if not urls:
        print("  Tidak ditemukan URL.")
        return

    for url in urls[:200]:
        print(f"  {url}")

    if len(urls) > 200:
        print(
            f"\n  ... {len(urls) - 200} lainnya"
        )


def show_methods(text):
    print("\n[+] HTTP Methods")

    methods = extract_methods(text)

    if not methods:
        print("  Tidak ditemukan HTTP method.")
        return

    counter = Counter(methods)

    for method, count in counter.most_common():
        print(f"  {method:<8} : {count}")


def show_status(text):
    print("\n[+] HTTP Status Codes")

    statuses = extract_status_codes(text)

    if not statuses:
        print("  Tidak ditemukan HTTP status code.")
        return

    counter = Counter(statuses)

    for status, count in sorted(
        counter.items(),
        key=lambda item: int(item[0])
    ):
        print(f"  {status:<8} : {count}")


def show_user_agents(text):
    print("\n[+] User Agents")

    agents = extract_user_agents(text)

    if not agents:
        print("  User-Agent tidak ditemukan.")
        return

    counter = Counter(agents)

    for agent, count in counter.most_common(50):
        print(f"  [{count}x] {agent}")


def show_failed_logins(text):
    print("\n[+] Failed Login Indicators")

    patterns = [
        r"failed login",
        r"login failed",
        r"authentication failed",
        r"invalid password",
        r"invalid credentials",
        r"unauthorized",
        r"401",
    ]

    total = 0

    for pattern in patterns:
        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        total += len(matches)

    if total == 0:
        print("  Tidak ditemukan indikator login gagal.")
    else:
        print(
            f"  Ditemukan sekitar {total} "
            "indikator login/authentication gagal."
        )


def show_suspicious(text):
    print("\n[+] Suspicious Requests")

    findings = analyze_suspicious(text)

    if not findings:
        print(
            "  Tidak ditemukan pola mencurigakan "
            "sederhana."
        )
        return

    for category, pattern, count in findings:
        print(f"\n  [{category}]")
        print(f"    Pattern : {pattern}")
        print(f"    Matches : {count}")


def show_keywords(text, keywords):
    print("\n[+] Keyword Search")

    if not keywords:
        print("  Tidak ada keyword.")
        return

    lower_text = text.lower()

    for keyword in keywords:
        count = lower_text.count(
            keyword.lower()
        )

        print(
            f"  {keyword:<20} : {count}"
        )


def show_ioc_summary(text):
    print("\n[+] IOC Summary")

    ips = extract_ips(text)
    urls = extract_urls(text)
    suspicious = analyze_suspicious(text)

    print(f"  Unique IPs        : {len(ips)}")
    print(f"  URLs / Paths      : {len(urls)}")
    print(f"  Suspicious groups : {len(suspicious)}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Midoo Log Analyzer - "
            "Log Analysis Toolkit"
        )
    )

    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="File log yang akan dianalisis"
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Tampilkan informasi file"
    )

    parser.add_argument(
        "--ips",
        action="store_true",
        help="Cari IP addresses"
    )

    parser.add_argument(
        "--urls",
        action="store_true",
        help="Cari URLs dan paths"
    )

    parser.add_argument(
        "--methods",
        action="store_true",
        help="Analisis HTTP methods"
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Analisis HTTP status codes"
    )

    parser.add_argument(
        "--user-agents",
        action="store_true",
        help="Tampilkan User-Agent"
    )

    parser.add_argument(
        "--failed-login",
        action="store_true",
        help="Cari indikator login gagal"
    )

    parser.add_argument(
        "--suspicious",
        action="store_true",
        help="Cari request mencurigakan"
    )

    parser.add_argument(
        "--keywords",
        nargs="+",
        help="Cari keyword tertentu"
    )

    parser.add_argument(
        "--ioc",
        action="store_true",
        help="Tampilkan ringkasan IOC"
    )

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(
            f"[!] File tidak ditemukan: {args.file}"
        )
        return 1

    try:
        with open(
            args.file,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as file:
            lines = file.readlines()

    except PermissionError:
        print(
            "[!] Tidak memiliki izin membaca file."
        )
        return 1

    text = "".join(lines)

    print("=============================================")
    print("            Midoo Log Analyzer")
    print("                  v1.0")
    print("=============================================\n")

    show_file_info(args.file, lines)

    no_option = not any(
        [
            args.info,
            args.ips,
            args.urls,
            args.methods,
            args.status,
            args.user_agents,
            args.failed_login,
            args.suspicious,
            args.keywords,
            args.ioc,
        ]
    )

    if no_option:
        print(
            "\n[i] Mode default: "
            "informasi file + IOC summary."
        )

    if args.ips:
        show_ips(text)

    if args.urls:
        show_urls(text)

    if args.methods:
        show_methods(text)

    if args.status:
        show_status(text)

    if args.user_agents:
        show_user_agents(text)

    if args.failed_login:
        show_failed_logins(text)

    if args.suspicious:
        show_suspicious(text)

    if args.keywords:
        show_keywords(
            text,
            args.keywords
        )

    if args.ioc or no_option:
        show_ioc_summary(text)

    print("\n=============================================")
    print("              ANALYSIS DONE")
    print("=============================================")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
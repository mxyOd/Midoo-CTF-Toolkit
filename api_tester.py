#!/usr/bin/env python3

import argparse
import json
import ssl
import time
import urllib.error
import urllib.request
from urllib.parse import urlencode, urlparse


USER_AGENT = "Midoo-API-Tester/1.0"


def parse_headers(values):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
    }

    for item in values or []:
        if ":" not in item:
            raise ValueError(
                f"Format header salah: {item}. Gunakan 'Nama: Nilai'."
            )

        name, value = item.split(":", 1)
        headers[name.strip()] = value.strip()

    return headers


def build_url(url, params):
    if not params:
        return url

    parsed = urlparse(url)
    query = urlencode(params)

    separator = "&" if parsed.query else "?"

    return url + separator + query


def send_request(url, method="GET", headers=None, body=None, timeout=10):
    data = None

    if body is not None:
        data = json.dumps(body).encode("utf-8")

        if not any(
            key.lower() == "content-type"
            for key in headers
        ):
            headers["Content-Type"] = "application/json"

    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method.upper(),
    )

    start = time.perf_counter()

    try:
        response = urllib.request.urlopen(
            request,
            timeout=timeout,
            context=ssl.create_default_context(),
        )

        elapsed = (time.perf_counter() - start) * 1000

        raw_body = response.read()

        return {
            "status": response.status,
            "reason": response.reason,
            "url": response.geturl(),
            "elapsed_ms": round(elapsed, 2),
            "headers": dict(response.headers),
            "body": raw_body.decode("utf-8", errors="replace"),
        }

    except urllib.error.HTTPError as error:
        elapsed = (time.perf_counter() - start) * 1000

        raw_body = error.read()

        return {
            "status": error.code,
            "reason": error.reason,
            "url": error.geturl(),
            "elapsed_ms": round(elapsed, 2),
            "headers": dict(error.headers),
            "body": raw_body.decode("utf-8", errors="replace"),
        }

    except urllib.error.URLError as error:
        raise RuntimeError(f"Request gagal: {error.reason}") from error


def print_response(result):
    print("\n========================================")
    print("               RESPONSE")
    print("========================================")

    print(f"Status        : {result['status']} {result['reason']}")
    print(f"Response Time : {result['elapsed_ms']} ms")
    print(f"URL           : {result['url']}")

    print("\nHeaders:")

    for key, value in result["headers"].items():
        print(f"  {key}: {value}")

    print("\nBody:")

    body = result["body"]

    try:
        parsed = json.loads(body)
        print(json.dumps(parsed, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(body[:5000])

        if len(body) > 5000:
            print("\n[!] Body dipotong menjadi 5000 karakter.")


def interactive_request(method):
    print("\n========================================")
    print(f"          Midoo API Tester - {method}")
    print("========================================")

    url = input("\nURL API: ").strip()

    if not url:
        print("[!] URL tidak boleh kosong.")
        return

    params = {}

    print("\nQuery Parameters")
    print("Masukkan dalam format key=value.")
    print("Kosongkan key untuk selesai.")

    while True:
        key = input("Key: ").strip()

        if not key:
            break

        value = input("Value: ")
        params[key] = value

    url = build_url(url, params)

    headers = parse_headers([])

    print("\nHeaders")
    print("Contoh: Authorization: Bearer TOKEN")
    print("Kosongkan nama header untuk selesai.")

    while True:
        item = input("Header: ").strip()

        if not item:
            break

        if ":" not in item:
            print("[!] Format harus: Nama: Nilai")
            continue

        name, value = item.split(":", 1)
        headers[name.strip()] = value.strip()

    body = None

    if method.upper() in ("POST", "PUT", "PATCH"):

        print("\nJSON Body")
        print("Contoh: {\"username\":\"mido\"}")
        body_text = input("Body: ").strip()

        if body_text:
            try:
                body = json.loads(body_text)

                if not isinstance(body, (dict, list)):
                    print("[!] JSON harus berupa object atau array.")
                    return

            except json.JSONDecodeError as error:
                print(f"[!] JSON tidak valid: {error}")
                return

    print("\n[•] Mengirim request...")

    try:
        result = send_request(
            url=url,
            method=method,
            headers=headers,
            body=body,
        )

        print("[✓] Request selesai.")
        print_response(result)

    except RuntimeError as error:
        print(f"[!] {error}")


def cors_check():
    print("\n========================================")
    print("               CORS CHECK")
    print("========================================")

    url = input("\nURL API: ").strip()

    if not url:
        return

    headers = parse_headers([
        "Origin: https://example.invalid"
    ])

    print("\n[•] Mengirim request dengan Origin pengujian...")

    try:
        result = send_request(
            url=url,
            method="GET",
            headers=headers,
        )

        acao = result["headers"].get(
            "Access-Control-Allow-Origin"
        )

        acac = result["headers"].get(
            "Access-Control-Allow-Credentials"
        )

        print(f"\nStatus : {result['status']}")
        print(
            f"Access-Control-Allow-Origin: "
            f"{acao or '(tidak ada)'}"
        )
        print(
            f"Access-Control-Allow-Credentials: "
            f"{acac or '(tidak ada)'}"
        )

        if acao == "https://example.invalid":
            print(
                "\n[!] Origin pengujian direfleksikan."
            )
        else:
            print(
                "\n[-] Tidak terlihat refleksi Origin "
                "pada response."
            )

        print(
            "\n[!] Ini pemeriksaan indikatif, "
            "bukan pembuktian konfigurasi CORS secara menyeluruh."
        )

    except RuntimeError as error:
        print(f"[!] {error}")


def security_headers():
    print("\n========================================")
    print("          API SECURITY HEADERS")
    print("========================================")

    url = input("\nURL API: ").strip()

    if not url:
        return

    try:
        result = send_request(url)

        interesting = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "Referrer-Policy",
            "Permissions-Policy",
        ]

        for header in interesting:
            value = result["headers"].get(header)

            if value:
                print(f"[+] {header}: {value}")
            else:
                print(f"[-] {header}: tidak ditemukan")

    except RuntimeError as error:
        print(f"[!] {error}")


def save_result(result, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print(f"\n[✓] Hasil disimpan: {filename}")


def cli_request(args):
    headers = parse_headers(args.header)

    body = None

    if args.data:
        try:
            body = json.loads(args.data)
        except json.JSONDecodeError as error:
            print(f"[!] JSON tidak valid: {error}")
            return

    url = build_url(args.url, dict(
        item.split("=", 1)
        for item in args.param
        if "=" in item
    ))

    try:
        result = send_request(
            url=url,
            method=args.method,
            headers=headers,
            body=body,
            timeout=args.timeout,
        )

        print_response(result)

        if args.output:
            save_result(result, args.output)

    except RuntimeError as error:
        print(f"[!] {error}")


def interactive_menu():
    while True:

        print("""
========================================
          Midoo API Tester v1.0
========================================
1. GET Request
2. POST Request
3. PUT Request
4. PATCH Request
5. DELETE Request
6. CORS Check
7. Security Headers
8. Exit
========================================
""")

        choice = input("Midoo API > ").strip()

        if choice == "1":
            interactive_request("GET")

        elif choice == "2":
            interactive_request("POST")

        elif choice == "3":
            interactive_request("PUT")

        elif choice == "4":
            interactive_request("PATCH")

        elif choice == "5":
            interactive_request("DELETE")

        elif choice == "6":
            cors_check()

        elif choice == "7":
            security_headers()

        elif choice == "8":
            print("Midoo API Tester terminated.")
            break

        else:
            print("[!] Pilihan tidak valid.")


def main():
    parser = argparse.ArgumentParser(
        description="Midoo API Tester - API testing utility"
    )

    parser.add_argument(
        "-u",
        "--url",
        help="URL API",
    )

    parser.add_argument(
        "-X",
        "--method",
        default="GET",
        choices=[
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        ],
        help="HTTP method",
    )

    parser.add_argument(
        "-H",
        "--header",
        action="append",
        help="Header dengan format 'Nama: Nilai'",
    )

    parser.add_argument(
        "-p",
        "--param",
        action="append",
        default=[],
        help="Query parameter dengan format key=value",
    )

    parser.add_argument(
        "-d",
        "--data",
        help="JSON body",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Simpan response ke file JSON",
    )

    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=10,
        help="Timeout dalam detik",
    )

    args = parser.parse_args()

    if args.url:
        cli_request(args)
    else:
        interactive_menu()


if __name__ == "__main__":
    main()

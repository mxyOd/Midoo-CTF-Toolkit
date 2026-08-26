import ssl
import socket
import urllib.error
import urllib.request
from urllib.parse import urlparse


USER_AGENT = "Midoo-HTTP-Analyzer/1.0"


def get_url():
    url = input("\nMasukkan URL: ").strip()

    if not url:
        print("[!] URL kosong.")
        return None

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    return url


def make_request(url):
    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*"
        }
    )

    try:
        response = urllib.request.urlopen(
            request,
            timeout=10
        )

        return response

    except urllib.error.HTTPError as error:
        return error

    except urllib.error.URLError as error:
        print(f"[!] Connection error: {error.reason}")
        return None

    except Exception as error:
        print(f"[!] Error: {error}")
        return None


def analyze_url():
    url = get_url()

    if not url:
        return

    response = make_request(url)

    if not response:
        return

    print("\n========================================")
    print("             HTTP ANALYSIS")
    print("========================================")

    print(f"URL          : {response.geturl()}")
    print(f"Status       : {response.status}")
    print(f"Reason       : {response.reason}")

    print(
        f"Content-Type : "
        f"{response.headers.get('Content-Type', '(none)')}"
    )

    print(
        f"Content-Length: "
        f"{response.headers.get('Content-Length', '(none)')}"
    )

    print(
        f"Server       : "
        f"{response.headers.get('Server', '(none)')}"
    )


def request_headers():
    url = get_url()

    if not url:
        return

    response = make_request(url)

    if not response:
        return

    print("\n========================================")
    print("            REQUEST HEADERS")
    print("========================================")

    print(f"User-Agent: {USER_AGENT}")
    print("Accept: */*")
    print("Method: GET")


def response_headers():
    url = get_url()

    if not url:
        return

    response = make_request(url)

    if not response:
        return

    print("\n========================================")
    print("           RESPONSE HEADERS")
    print("========================================")

    for key, value in response.headers.items():
        print(f"{key}: {value}")


def status_code():
    url = get_url()

    if not url:
        return

    response = make_request(url)

    if not response:
        return

    print("\n========================================")
    print("              STATUS CODE")
    print("========================================")

    print(f"Status : {response.status}")
    print(f"Reason : {response.reason}")


def redirect_information():
    url = get_url()

    if not url:
        return

    response = make_request(url)

    if not response:
        return

    print("\n========================================")
    print("          REDIRECT INFORMATION")
    print("========================================")

    print(f"Original URL : {url}")
    print(f"Final URL    : {response.geturl()}")

    if response.geturl() != url:
        print("[+] Redirect terjadi.")

        print(
            f"Location: "
            f"{response.headers.get('Location', '(not exposed)')}"
        )

    else:
        print("[-] Tidak ada redirect yang terdeteksi.")


def cookies():
    url = get_url()

    if not url:
        return

    response = make_request(url)

    if not response:
        return

    print("\n========================================")
    print("                COOKIES")
    print("========================================")

    cookie_headers = response.headers.get_all(
        "Set-Cookie"
    )

    if cookie_headers:

        for cookie in cookie_headers:
            print(cookie)

    else:
        print("[-] Server tidak mengirim Set-Cookie.")


def content_type():
    url = get_url()

    if not url:
        return

    response = make_request(url)

    if not response:
        return

    print("\n========================================")
    print("             CONTENT TYPE")
    print("========================================")

    content_type_value = response.headers.get(
        "Content-Type"
    )

    if content_type_value:
        print(content_type_value)

    else:
        print("[-] Content-Type tidak tersedia.")


def response_preview():
    url = get_url()

    if not url:
        return

    response = make_request(url)

    if not response:
        return

    print("\n========================================")
    print("           RESPONSE PREVIEW")
    print("========================================")

    try:
        data = response.read(2048)

        text = data.decode(
            "utf-8",
            errors="replace"
        )

        print(text)

        if len(data) >= 2048:
            print("\n[!] Preview dibatasi 2048 bytes.")

    except Exception as error:
        print(f"[!] Error: {error}")


def security_headers():
    url = get_url()

    if not url:
        return

    response = make_request(url)

    if not response:
        return

    print("\n========================================")
    print("            SECURITY HEADERS")
    print("========================================")

    headers = {
        "Content-Security-Policy":
            "CSP",

        "Strict-Transport-Security":
            "HSTS",

        "X-Content-Type-Options":
            "X-Content-Type-Options",

        "X-Frame-Options":
            "X-Frame-Options",

        "Referrer-Policy":
            "Referrer-Policy",

        "Permissions-Policy":
            "Permissions-Policy"
    }

    for header, label in headers.items():

        value = response.headers.get(header)

        if value:
            print(f"[+] {label}: {value}")

        else:
            print(f"[-] {label}: tidak ditemukan")


def tls_information():
    url = get_url()

    if not url:
        return

    parsed = urlparse(url)

    if parsed.scheme != "https":
        print("[!] URL bukan HTTPS.")
        return

    hostname = parsed.hostname

    if not hostname:
        print("[!] Hostname tidak valid.")
        return

    port = parsed.port or 443

    print("\n========================================")
    print("             TLS INFORMATION")
    print("========================================")

    try:
        context = ssl.create_default_context()

        with socket.create_connection(
            (hostname, port),
            timeout=10
        ) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=hostname
            ) as secure_socket:

                print(
                    f"TLS Version : "
                    f"{secure_socket.version()}"
                )

                cipher = secure_socket.cipher()

                if cipher:
                    print(
                        f"Cipher      : "
                        f"{cipher[0]}"
                    )

                certificate = secure_socket.getpeercert()

                subject = certificate.get(
                    "subject",
                    []
                )

                print("\nCertificate Subject:")

                for item in subject:
                    for key, value in item:
                        print(f"  {key}: {value}")

    except Exception as error:
        print(f"[!] TLS error: {error}")


def main():

    while True:

        print("""
========================================
          Midoo HTTP Analyzer
========================================
1. Analyze URL
2. Request Headers
3. Response Headers
4. Status Code
5. Redirect Information
6. Cookies
7. Content-Type
8. Response Preview
9. Security Headers
10. TLS Information
11. Exit
========================================
""")

        pilihan = input("Pilih: ").strip()

        if pilihan == "1":
            analyze_url()

        elif pilihan == "2":
            request_headers()

        elif pilihan == "3":
            response_headers()

        elif pilihan == "4":
            status_code()

        elif pilihan == "5":
            redirect_information()

        elif pilihan == "6":
            cookies()

        elif pilihan == "7":
            content_type()

        elif pilihan == "8":
            response_preview()

        elif pilihan == "9":
            security_headers()

        elif pilihan == "10":
            tls_information()

        elif pilihan == "11":
            print("Keluar...")
            break

        else:
            print("[!] Pilihan tidak valid.")


if __name__ == "__main__":
    main()
from urllib.parse import (
    urlparse,
    parse_qs,
    quote,
    unquote,
    urlunparse
)


def get_url():
    url = input("\nMasukkan URL: ").strip()

    if not url:
        print("[!] URL kosong.")
        return None

    return url


def parse_url():
    url = get_url()

    if not url:
        return

    parsed = urlparse(url)

    print("\n========================================")
    print("              URL ANALYSIS")
    print("========================================")

    print(f"Original   : {url}")
    print(f"Scheme     : {parsed.scheme or '(none)'}")
    print(f"Hostname   : {parsed.hostname or '(none)'}")
    print(f"Port       : {parsed.port or '(default/none)'}")
    print(f"Username   : {parsed.username or '(none)'}")
    print(f"Password   : {'***' if parsed.password else '(none)'}")
    print(f"Path       : {parsed.path or '/'}")
    print(f"Query      : {parsed.query or '(none)'}")
    print(f"Fragment    : {parsed.fragment or '(none)'}")


def extract_parameters():
    url = get_url()

    if not url:
        return

    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)

    print("\n========================================")
    print("           QUERY PARAMETERS")
    print("========================================")

    if not params:
        print("[-] Tidak ada query parameter.")
        return

    for key, values in params.items():

        for value in values:
            print(f"{key} = {value}")


def url_decode():
    value = input("\nMasukkan URL-encoded text: ")

    print("\n========================================")
    print("              URL DECODE")
    print("========================================")

    print(unquote(value))


def url_encode():
    value = input("\nMasukkan text: ")

    print("\n========================================")
    print("              URL ENCODE")
    print("========================================")

    print(quote(value, safe=""))


def normalize_url():
    url = get_url()

    if not url:
        return

    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    hostname = (parsed.hostname or "").lower()

    if not scheme:
        scheme = "http"

    if not hostname:
        print("[!] Hostname tidak ditemukan.")
        return

    username = parsed.username or ""
    password = parsed.password or ""

    userinfo = ""

    if username:
        userinfo = quote(username, safe="")

        if password:
            userinfo += ":" + quote(password, safe="")

        userinfo += "@"

    host = hostname

    if ":" in host and not host.startswith("["):
        host = f"[{host}]"

    port = parsed.port

    netloc = userinfo + host

    if port:
        netloc += f":{port}"

    path = parsed.path or "/"

    normalized = urlunparse((
        scheme,
        netloc,
        path,
        "",
        parsed.query,
        parsed.fragment
    ))

    print("\n========================================")
    print("             NORMALIZED URL")
    print("========================================")

    print(normalized)


def domain_info():
    url = get_url()

    if not url:
        return

    parsed = urlparse(url)

    hostname = parsed.hostname

    print("\n========================================")
    print("              DOMAIN INFO")
    print("========================================")

    if not hostname:
        print("[!] Hostname tidak ditemukan.")
        return

    parts = hostname.split(".")

    print(f"Hostname : {hostname}")

    if len(parts) >= 2:
        print(f"Domain   : {parts[-2]}.{parts[-1]}")

    if len(parts) >= 3:
        print(f"Subdomain: {'.'.join(parts[:-2])}")
    else:
        print("Subdomain: (none)")


def path_info():
    url = get_url()

    if not url:
        return

    parsed = urlparse(url)

    path = parsed.path or "/"

    print("\n========================================")
    print("               PATH INFO")
    print("========================================")

    print(f"Full path : {path}")

    segments = [
        segment
        for segment in path.split("/")
        if segment
    ]

    print(f"Segments  : {len(segments)}")

    if segments:
        for index, segment in enumerate(segments, 1):
            print(f"  [{index}] {segment}")
    else:
        print("  (root)")


def query_info():
    url = get_url()

    if not url:
        return

    parsed = urlparse(url)

    print("\n========================================")
    print("              QUERY INFO")
    print("========================================")

    if not parsed.query:
        print("[-] Tidak ada query string.")
        return

    print(f"Raw query: {parsed.query}")

    params = parse_qs(
        parsed.query,
        keep_blank_values=True
    )

    print("\nParameters:")

    for key, values in params.items():

        if len(values) == 1:
            print(f"  {key} = {values[0]}")

        else:
            print(f"  {key} = {values}")


def suspicious_parameters():
    url = get_url()

    if not url:
        return

    parsed = urlparse(url)
    params = parse_qs(
        parsed.query,
        keep_blank_values=True
    )

    print("\n========================================")
    print("        SUSPICIOUS PARAMETER HINTS")
    print("========================================")

    if not params:
        print("[-] Tidak ada parameter.")
        return

    keywords = {
        "id": "Object/reference parameter",
        "user": "User/account parameter",
        "username": "Username parameter",
        "file": "File/path parameter",
        "path": "Path parameter",
        "page": "Page parameter",
        "url": "URL parameter",
        "redirect": "Redirect parameter",
        "next": "Navigation/redirect parameter",
        "return": "Return URL parameter",
        "cmd": "Command-like parameter",
        "query": "Query parameter",
        "search": "Search parameter"
    }

    found = False

    for key in params:

        key_lower = key.lower()

        if key_lower in keywords:

            print(
                f"[!] {key}: "
                f"{keywords[key_lower]}"
            )

            found = True

    if not found:
        print(
            "[-] Tidak ditemukan parameter "
            "dengan nama yang umum."
        )

    print(
        "\n[!] Ini hanya heuristic untuk membantu "
        "analisis CTF."
    )


def main():

    while True:

        print("""
========================================
          Midoo URL Analyzer
========================================
1. Parse URL
2. Extract Parameters
3. URL Decode
4. URL Encode
5. Normalize URL
6. Domain Information
7. Path Information
8. Query Information
9. Suspicious Parameter Hints
10. Exit
========================================
""")

        pilihan = input("Pilih: ").strip()

        if pilihan == "1":
            parse_url()

        elif pilihan == "2":
            extract_parameters()

        elif pilihan == "3":
            url_decode()

        elif pilihan == "4":
            url_encode()

        elif pilihan == "5":
            normalize_url()

        elif pilihan == "6":
            domain_info()

        elif pilihan == "7":
            path_info()

        elif pilihan == "8":
            query_info()

        elif pilihan == "9":
            suspicious_parameters()

        elif pilihan == "10":
            print("Keluar...")
            break

        else:
            print("[!] Pilihan tidak valid.")


if __name__ == "__main__":
    main()
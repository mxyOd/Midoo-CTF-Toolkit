import base64
import json
import time
from datetime import datetime


def base64url_decode(data):
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def decode_json_part(part):
    try:
        decoded = base64url_decode(part)
        return json.loads(decoded.decode("utf-8"))
    except Exception:
        return None


def analyze_jwt():
    token = input("\nMasukkan JWT:\n").strip()

    parts = token.split(".")

    print("\n========================================")
    print("             JWT STRUCTURE")
    print("========================================")

    print(f"Parts: {len(parts)}")

    if len(parts) != 3:
        print("[!] JWT harus memiliki 3 bagian:")
        print("    HEADER.PAYLOAD.SIGNATURE")
        return

    header_part = parts[0]
    payload_part = parts[1]
    signature_part = parts[2]

    header = decode_json_part(header_part)
    payload = decode_json_part(payload_part)

    print("\n========================================")
    print("                HEADER")
    print("========================================")

    if header is None:
        print("[!] Header bukan JSON yang valid.")
    else:
        print(json.dumps(header, indent=4))

    print("\n========================================")
    print("                PAYLOAD")
    print("========================================")

    if payload is None:
        print("[!] Payload bukan JSON yang valid.")
    else:
        print(json.dumps(payload, indent=4))

    print("\n========================================")
    print("              SIGNATURE")
    print("========================================")

    print(signature_part)

    if header:
        print("\n========================================")
        print("          ALGORITHM INFORMATION")
        print("========================================")

        algorithm = header.get("alg")
        token_type = header.get("typ")

        print(f"Algorithm : {algorithm}")
        print(f"Type      : {token_type}")


def inspect_claims():
    token = input("\nMasukkan JWT:\n").strip()

    parts = token.split(".")

    if len(parts) != 3:
        print("[!] JWT tidak valid.")
        return

    payload = decode_json_part(parts[1])

    if payload is None:
        print("[!] Payload tidak valid.")
        return

    print("\n========================================")
    print("              JWT CLAIMS")
    print("========================================")

    for key, value in payload.items():

        if key in ["exp", "iat", "nbf"] and isinstance(value, int):
            try:
                date = datetime.fromtimestamp(value)
                print(f"{key:8}: {value} ({date})")
            except Exception:
                print(f"{key:8}: {value}")
        else:
            print(f"{key:8}: {value}")

    if "exp" in payload:
        exp = payload["exp"]

        if isinstance(exp, int):
            now = int(time.time())

            print("\n========================================")
            print("           EXPIRATION CHECK")
            print("========================================")

            if now < exp:
                remaining = exp - now
                print("[+] Token belum expired.")
                print(f"[+] Remaining: {remaining} seconds")
            else:
                print("[-] Token sudah expired.")


def decode_part():
    token = input("\nMasukkan JWT:\n").strip()

    parts = token.split(".")

    if len(parts) != 3:
        print("[!] JWT tidak valid.")
        return

    print("""
========================================
1. Header
2. Payload
========================================
""")

    pilihan = input("Pilih: ")

    if pilihan == "1":
        data = parts[0]

    elif pilihan == "2":
        data = parts[1]

    else:
        print("[!] Pilihan tidak valid.")
        return

    try:
        decoded = base64url_decode(data).decode("utf-8")

        print("\nDecoded:")
        print(decoded)

    except Exception:
        print("[!] Tidak dapat decode.")


def main():

    while True:

        print("""
========================================
           Midoo JWT Analyzer
========================================
1. Analyze JWT
2. Inspect Claims
3. Decode Header/Payload
4. Exit
========================================
""")

        pilihan = input("Pilih: ")

        if pilihan == "1":
            analyze_jwt()

        elif pilihan == "2":
            inspect_claims()

        elif pilihan == "3":
            decode_part()

        elif pilihan == "4":
            print("Keluar...")
            break

        else:
            print("[!] Pilihan tidak valid.")


if __name__ == "__main__":
    main()
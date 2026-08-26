import base64
import codecs


def base64_tool():
    print("\n1. Decode")
    print("2. Encode")
    pilihan = input("Pilih: ")

    data = input("Masukkan data: ")

    try:
        if pilihan == "1":
            result = base64.b64decode(data).decode()
            print(f"\nDecoded message:\n{result}")
        elif pilihan == "2":
            result = base64.b64encode(data.encode()).decode()
            print(f"\nEncoded message:\n{result}")
        else:
            print("[!] Pilihan tidak valid.")
    except Exception:
        print("[!] Data Base64 tidak valid.")


def hex_tool():
    print("\n1. Decode")
    print("2. Encode")
    pilihan = input("Pilih: ")

    data = input("Masukkan data: ")

    try:
        if pilihan == "1":
            result = bytes.fromhex(data).decode()
            print(f"\nDecoded message:\n{result}")
        elif pilihan == "2":
            result = data.encode().hex()
            print(f"\nEncoded message:\n{result}")
        else:
            print("[!] Pilihan tidak valid.")
    except Exception:
        print("[!] Data Hex tidak valid.")


def binary_tool():
    print("\n1. Decode")
    print("2. Encode")
    pilihan = input("Pilih: ")

    data = input("Masukkan data: ")

    try:
        if pilihan == "1":
            binary = data.split()
            result = "".join(chr(int(x, 2)) for x in binary)
            print(f"\nDecoded message:\n{result}")
        elif pilihan == "2":
            result = " ".join(format(ord(x), "08b") for x in data)
            print(f"\nEncoded message:\n{result}")
        else:
            print("[!] Pilihan tidak valid.")
    except Exception:
        print("[!] Data Binary tidak valid.")


def rot13_tool():
    print("\n1. Decode")
    print("2. Encode")
    pilihan = input("Pilih: ")

    data = input("Masukkan data: ")
    result = codecs.decode(data, "rot13")

    if pilihan in ["1", "2"]:
        print(f"\nResult:\n{result}")
    else:
        print("[!] Pilihan tidak valid.")


def caesar_tool():
    print("\n1. Decode")
    print("2. Encode")
    pilihan = input("Pilih: ")

    data = input("Masukkan data: ")

    try:
        shift = int(input("Masukkan shift: "))
    except ValueError:
        print("[!] Shift harus berupa angka.")
        return

    if pilihan == "1":
        shift = -shift
    elif pilihan != "2":
        print("[!] Pilihan tidak valid.")
        return

    result = ""

    for char in data:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char

    print(f"\nResult:\n{result}")


def atbash_tool():
    print("\n1. Decode")
    print("2. Encode")
    pilihan = input("Pilih: ")

    data = input("Masukkan data: ")

    if pilihan not in ["1", "2"]:
        print("[!] Pilihan tidak valid.")
        return

    result = ""

    for char in data:
        if char.isupper():
            result += chr(ord("Z") - (ord(char) - ord("A")))
        elif char.islower():
            result += chr(ord("z") - (ord(char) - ord("a")))
        else:
            result += char

    print(f"\nResult:\n{result}")


def xor_tool():
    print("\n--- XOR Tool ---")

    data = input("Masukkan text: ")
    key = input("Masukkan key: ")

    if not key:
        print("[!] Key tidak boleh kosong.")
        return

    result = ""

    for i, char in enumerate(data):
        result += chr(ord(char) ^ ord(key[i % len(key)]))

    print("\nXOR Result:")
    print(result)

    print("\nHex Result:")
    print(result.encode().hex())


def main():
    while True:
        print("""
========================================
            Midoo Crypto Tool
========================================
1. Base64
2. Hex
3. Binary
4. ROT13
5. Caesar Cipher
6. Atbash
7. XOR
8. Exit
========================================
""")

        pilihan = input("Pilih: ")

        if pilihan == "1":
            base64_tool()

        elif pilihan == "2":
            hex_tool()

        elif pilihan == "3":
            binary_tool()

        elif pilihan == "4":
            rot13_tool()

        elif pilihan == "5":
            caesar_tool()

        elif pilihan == "6":
            atbash_tool()

        elif pilihan == "7":
            xor_tool()

        elif pilihan == "8":
            print("Keluar...")
            break

        else:
            print("[!] Pilihan tidak valid.")


if __name__ == "__main__":
    main()
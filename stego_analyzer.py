import hashlib
import os
import re
import struct


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def get_file():
    path = input("\nMasukkan path file: ").strip()

    if not os.path.isfile(path):
        print("[!] File tidak ditemukan.")
        return None

    return path


def read_file(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception as error:
        print(f"[!] Error: {error}")
        return None


def image_information():
    path = get_file()

    if not path:
        return

    data = read_file(path)

    if not data:
        return

    print("\n========================================")
    print("           IMAGE INFORMATION")
    print("========================================")

    print(f"Filename : {os.path.basename(path)}")
    print(f"Size     : {len(data)} bytes")

    if data.startswith(PNG_SIGNATURE):
        print("Format   : PNG")

        if len(data) >= 24:
            width, height = struct.unpack(">II", data[16:24])

            bit_depth = data[24]
            color_type = data[25]

            print(f"Width    : {width}")
            print(f"Height   : {height}")
            print(f"Bit Depth: {bit_depth}")
            print(f"Color    : {color_type}")

    elif data.startswith(b"\xff\xd8\xff"):
        print("Format   : JPEG")

    elif data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        print("Format   : GIF")

    else:
        print("Format   : Unknown")


def metadata():
    path = get_file()

    if not path:
        return

    data = read_file(path)

    if not data:
        return

    print("\n========================================")
    print("              METADATA")
    print("========================================")

    # Basic PNG text chunks
    if data.startswith(PNG_SIGNATURE):

        offset = 8
        found = False

        while offset + 12 <= len(data):

            length = struct.unpack(
                ">I",
                data[offset:offset + 4]
            )[0]

            chunk_type = data[
                offset + 4:offset + 8
            ]

            chunk_data_start = offset + 8
            chunk_data_end = chunk_data_start + length

            chunk_data = data[
                chunk_data_start:chunk_data_end
            ]

            if chunk_type in [b"tEXt", b"zTXt", b"iTXt"]:

                found = True

                print(
                    f"\n[{chunk_type.decode(errors='ignore')}]"
                )

                print(
                    chunk_data.decode(
                        "utf-8",
                        errors="replace"
                    )
                )

            offset = chunk_data_end + 4

        if not found:
            print("[-] Tidak menemukan PNG text metadata.")

    else:
        print("[-] Metadata parser versi ini fokus pada PNG.")


def extract_strings():
    path = get_file()

    if not path:
        return

    data = read_file(path)

    if not data:
        return

    print("\n========================================")
    print("               STRINGS")
    print("========================================")

    strings = re.findall(
        rb"[\x20-\x7e]{4,}",
        data
    )

    if not strings:
        print("[-] Tidak ada printable strings.")
        return

    for item in strings[:100]:
        print(
            item.decode(
                "ascii",
                errors="ignore"
            )
        )

    print(
        f"\n[+] Total strings: {len(strings)}"
    )

    if len(strings) > 100:
        print("[!] Hanya 100 string pertama ditampilkan.")


def png_chunks():
    path = get_file()

    if not path:
        return

    data = read_file(path)

    if not data:
        return

    print("\n========================================")
    print("            PNG CHUNK ANALYSIS")
    print("========================================")

    if not data.startswith(PNG_SIGNATURE):
        print("[!] File bukan PNG.")
        return

    offset = 8
    count = 0

    while offset + 12 <= len(data):

        length = struct.unpack(
            ">I",
            data[offset:offset + 4]
        )[0]

        chunk_type = data[
            offset + 4:offset + 8
        ].decode(
            "ascii",
            errors="replace"
        )

        total_size = 12 + length

        print(
            f"{count + 1:3}. "
            f"{chunk_type:5} "
            f"Length: {length:10} "
            f"Offset: {offset}"
        )

        count += 1
        offset += total_size

        if chunk_type == "IEND":
            break

    print(f"\n[+] Total chunks: {count}")


def trailing_data():
    path = get_file()

    if not path:
        return

    data = read_file(path)

    if not data:
        return

    print("\n========================================")
    print("             TRAILING DATA")
    print("========================================")

    if not data.startswith(PNG_SIGNATURE):
        print("[!] File bukan PNG.")
        return

    offset = 8
    iend_end = None

    while offset + 12 <= len(data):

        length = struct.unpack(
            ">I",
            data[offset:offset + 4]
        )[0]

        chunk_type = data[
            offset + 4:offset + 8
        ]

        chunk_end = offset + 12 + length

        if chunk_type == b"IEND":
            iend_end = chunk_end
            break

        offset = chunk_end

    if iend_end is None:
        print("[!] IEND tidak ditemukan.")
        return

    trailing = data[iend_end:]

    print(f"IEND ends at : {iend_end}")
    print(f"File size    : {len(data)} bytes")
    print(f"Trailing     : {len(trailing)} bytes")

    if trailing:

        print("\n[!] Ada data setelah IEND!")

        print("\nHex preview:")
        print(trailing[:64].hex(" "))

    else:
        print("[+] Tidak ada trailing data.")


def search_flag():
    path = get_file()

    if not path:
        return

    data = read_file(path)

    if not data:
        return

    print("\n========================================")
    print("              FLAG SEARCH")
    print("========================================")

    keyword = input(
        "Keyword [default: Midoo{]: "
    ).strip()

    if not keyword:
        keyword = "Midoo{"

    pattern = re.escape(
        keyword.encode()
    )

    matches = re.findall(
        pattern + rb".{0,200}",
        data,
        re.IGNORECASE
    )

    if matches:

        print(f"\n[+] {len(matches)} match ditemukan:")

        for match in matches:
            print(
                match.decode(
                    "utf-8",
                    errors="replace"
                )
            )

    else:
        print(
            f"[-] '{keyword}' tidak ditemukan."
        )


def lsb_analysis():
    path = get_file()

    if not path:
        return

    data = read_file(path)

    if not data:
        return

    print("\n========================================")
    print("             LSB ANALYSIS")
    print("========================================")

    print("[*] Menganalisis byte terakhir...")
    print("[*] Ini adalah pemeriksaan statistik sederhana.")
    print("[*] Bukan decoder LSB gambar penuh.")

    if len(data) < 100:
        print("[!] File terlalu kecil.")
        return

    last_bits = [
        byte & 1
        for byte in data
    ]

    sample = last_bits[:256]

    bit_string = "".join(
        str(bit)
        for bit in sample
    )

    print("\nFirst 256 LSB bits:")
    print(bit_string)

    ones = sum(last_bits)
    zeros = len(last_bits) - ones

    print(f"\n0 bits : {zeros}")
    print(f"1 bits : {ones}")

    ratio = ones / len(last_bits)

    print(f"1-bit ratio: {ratio:.4f}")


def hex_preview():
    path = get_file()

    if not path:
        return

    data = read_file(path)

    if not data:
        return

    print("\n========================================")
    print("              HEX PREVIEW")
    print("========================================")

    size = input(
        "Jumlah byte [default: 128]: "
    ).strip()

    try:
        size = int(size) if size else 128
    except ValueError:
        print("[!] Harus berupa angka.")
        return

    preview = data[:size]

    for offset in range(0, len(preview), 16):

        chunk = preview[offset:offset + 16]

        hex_part = " ".join(
            f"{byte:02x}"
            for byte in chunk
        )

        ascii_part = "".join(
            chr(byte)
            if 32 <= byte <= 126
            else "."
            for byte in chunk
        )

        print(
            f"{offset:08x}  "
            f"{hex_part:<47}  "
            f"{ascii_part}"
        )


def main():

    while True:

        print("""
========================================
          Midoo Stego Analyzer
========================================
1. Image Information
2. Metadata
3. Strings
4. PNG Chunk Analysis
5. Trailing Data
6. Search Hidden Flag
7. LSB Analysis
8. Hex Preview
9. Exit
========================================
""")

        pilihan = input("Pilih: ")

        if pilihan == "1":
            image_information()

        elif pilihan == "2":
            metadata()

        elif pilihan == "3":
            extract_strings()

        elif pilihan == "4":
            png_chunks()

        elif pilihan == "5":
            trailing_data()

        elif pilihan == "6":
            search_flag()

        elif pilihan == "7":
            lsb_analysis()

        elif pilihan == "8":
            hex_preview()

        elif pilihan == "9":
            print("Keluar...")
            break

        else:
            print("[!] Pilihan tidak valid.")


if __name__ == "__main__":
    main()
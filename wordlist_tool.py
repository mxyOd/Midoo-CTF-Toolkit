#!/usr/bin/env python3

import argparse
import os
import sys


def check_file(path):
    if not os.path.isfile(path):
        print(f"[!] File tidak ditemukan: {path}")
        return False

    return True


def read_words(path):
    try:
        with open(
            path,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as file:
            return [
                line.rstrip("\r\n")
                for line in file
            ]

    except PermissionError:
        print(f"[!] Tidak memiliki izin membaca: {path}")
        return None

    except OSError as error:
        print(f"[!] Error membaca file: {error}")
        return None


def write_words(path, words):
    try:
        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:
            for word in words:
                file.write(word + "\n")

        return True

    except OSError as error:
        print(f"[!] Error menulis file: {error}")
        return False


def remove_duplicates(words):
    seen = set()
    result = []

    for word in words:
        if word not in seen:
            seen.add(word)
            result.append(word)

    return result


def generate_words(characters, minimum, maximum):
    import itertools

    words = []

    for length in range(minimum, maximum + 1):
        for combination in itertools.product(
            characters,
            repeat=length
        ):
            words.append("".join(combination))

    return words


def show_info(words):
    non_empty = [
        word for word in words
        if word
    ]

    unique = set(non_empty)

    lengths = [
        len(word)
        for word in non_empty
    ]

    print("\n[+] Wordlist Information")
    print(f"  Total entries : {len(words)}")
    print(f"  Non-empty     : {len(non_empty)}")
    print(f"  Unique        : {len(unique)}")

    if lengths:
        print(f"  Shortest      : {min(lengths)}")
        print(f"  Longest       : {max(lengths)}")


def search_words(words, keyword):
    keyword = keyword.lower()

    return [
        word
        for word in words
        if keyword in word.lower()
    ]


def filter_words(words, minimum, maximum):
    return [
        word
        for word in words
        if minimum <= len(word) <= maximum
    ]


def show_character_analysis(words):
    from collections import Counter

    counter = Counter(
        "".join(words)
    )

    print("\n[+] Character Analysis")

    if not counter:
        print("  Tidak ada karakter.")
        return

    for character, count in counter.most_common():
        if character == " ":
            display = "[SPACE]"
        elif character == "\t":
            display = "[TAB]"
        else:
            display = character

        print(
            f"  {display:<10} : {count}"
        )


def combine_files(files):
    combined = []

    for path in files:
        if not check_file(path):
            continue

        words = read_words(path)

        if words is not None:
            combined.extend(words)

    return combined


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Midoo Wordlist Toolkit - "
            "Wordlist Management Tool"
        )
    )

    parser.add_argument(
        "-f",
        "--file",
        help="Wordlist yang akan dianalisis"
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Tampilkan informasi wordlist"
    )

    parser.add_argument(
        "--unique",
        action="store_true",
        help="Hapus entry duplikat"
    )

    parser.add_argument(
        "--sort",
        action="store_true",
        help="Urutkan wordlist"
    )

    parser.add_argument(
        "--filter",
        action="store_true",
        help="Filter berdasarkan panjang"
    )

    parser.add_argument(
        "--min",
        type=int,
        default=0,
        help="Panjang minimum"
    )

    parser.add_argument(
        "--max",
        type=int,
        default=sys.maxsize,
        help="Panjang maksimum"
    )

    parser.add_argument(
        "--search",
        metavar="KEYWORD",
        help="Cari keyword dalam wordlist"
    )

    parser.add_argument(
        "--chars",
        help="Karakter untuk generate wordlist"
    )

    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate wordlist"
    )

    parser.add_argument(
        "--length",
        nargs=2,
        type=int,
        metavar=("MIN", "MAX"),
        help="Range panjang saat generate"
    )

    parser.add_argument(
        "--combine",
        nargs="+",
        metavar="FILE",
        help="Gabungkan beberapa wordlist"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="File output"
    )

    args = parser.parse_args()

    print("=============================================")
    print("          Midoo Wordlist Toolkit")
    print("                  v1.0")
    print("=============================================\n")

    # Generate
    if args.generate:
        if not args.chars:
            print(
                "[!] Gunakan --chars untuk menentukan karakter."
            )
            return 1

        if not args.length:
            print(
                "[!] Gunakan --length MIN MAX."
            )
            return 1

        minimum, maximum = args.length

        if minimum < 1 or maximum < minimum:
            print(
                "[!] Range panjang tidak valid."
            )
            return 1

        total = len(args.chars)

        print("[+] Generator")
        print(f"  Characters : {args.chars}")
        print(f"  Min length : {minimum}")
        print(f"  Max length : {maximum}")

        print(
            f"  Estimated entries: "
            f"{sum(total ** n for n in range(minimum, maximum + 1))}"
        )

        words = generate_words(
            args.chars,
            minimum,
            maximum
        )

        if args.output:
            if write_words(args.output, words):
                print(
                    f"\n[✓] Wordlist dibuat: {args.output}"
                )
        else:
            for word in words:
                print(word)

        return 0

    # Combine
    if args.combine:
        words = combine_files(args.combine)

        if args.unique:
            words = remove_duplicates(words)

        if args.sort:
            words.sort()

        print(
            f"[+] Entries setelah combine: {len(words)}"
        )

        if args.output:
            if write_words(args.output, words):
                print(
                    f"[✓] Output: {args.output}"
                )
        else:
            for word in words:
                print(word)

        return 0

    # File operations
    if not args.file:
        parser.print_help()
        return 1

    if not check_file(args.file):
        return 1

    words = read_words(args.file)

    if words is None:
        return 1

    if args.info:
        show_info(words)

    if args.unique:
        words = remove_duplicates(words)
        print(
            f"\n[✓] Unique entries: {len(words)}"
        )

    if args.sort:
        words.sort()
        print("\n[✓] Wordlist diurutkan.")

    if args.filter:
        words = filter_words(
            words,
            args.min,
            args.max
        )

        print(
            f"\n[✓] Setelah filter: {len(words)}"
        )

    if args.search:
        results = search_words(
            words,
            args.search
        )

        print(
            f"\n[+] Hasil pencarian "
            f"'{args.search}': {len(results)}"
        )

        for word in results:
            print(word)

        return 0

    show_character_analysis(words)

    if args.output:
        if write_words(args.output, words):
            print(
                f"\n[✓] Output disimpan: {args.output}"
            )
    else:
        print("\n[+] Preview")

        for word in words[:50]:
            print(f"  {word}")

        if len(words) > 50:
            print(
                f"\n  ... "
                f"{len(words) - 50} entries lainnya"
            )

    print("\n=============================================")
    print("              ANALYSIS DONE")
    print("=============================================")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
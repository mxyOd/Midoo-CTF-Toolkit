#!/usr/bin/env python3

import hashlib
import os
import shutil
import sqlite3


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def wait_enter():
    input("\nTekan Enter untuk kembali...")


def get_database():
    path = input(
        "\nMasukkan path database: "
    ).strip()

    if not path:
        print("\n[!] Path tidak boleh kosong.")
        wait_enter()
        return None

    if not os.path.isfile(path):
        print(f"\n[!] File tidak ditemukan: {path}")
        wait_enter()
        return None

    return path


def connect_database(path):
    try:
        return sqlite3.connect(
            f"file:{os.path.abspath(path)}?mode=ro",
            uri=True
        )
    except Exception as error:
        print(f"\n[!] Gagal membuka database: {error}")
        return None


def database_information():
    clear_screen()

    print("""
=============================================
       Midoo Database Information
=============================================
""")

    db = get_database()

    if not db:
        return

    connection = connect_database(db)

    if not connection:
        wait_enter()
        return

    try:
        cursor = connection.cursor()

        tables = cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """).fetchall()

        indexes = cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='index'
            ORDER BY name
        """).fetchall()

        print(f"File       : {os.path.basename(db)}")
        print(f"Size       : {os.path.getsize(db)} bytes")
        print(f"Tables     : {len(tables)}")
        print(f"Indexes    : {len(indexes)}")

        print("\nTables:")

        for table in tables:
            print(f"  - {table[0]}")

        print("\nSQLite Version:")

        version = cursor.execute(
            "SELECT sqlite_version()"
        ).fetchone()

        print(f"  {version[0]}")

    except Exception as error:
        print(f"\n[!] Error: {error}")

    finally:
        connection.close()

    wait_enter()


def table_enumeration():
    clear_screen()

    print("""
=============================================
          Midoo Table Enumeration
=============================================
""")

    db = get_database()

    if not db:
        return

    connection = connect_database(db)

    if not connection:
        wait_enter()
        return

    try:
        cursor = connection.cursor()

        rows = cursor.execute("""
            SELECT name, type
            FROM sqlite_master
            WHERE type IN ('table', 'view')
            ORDER BY type, name
        """).fetchall()

        if not rows:
            print("[-] Tidak ditemukan table/view.")
        else:
            for name, obj_type in rows:
                print(
                    f"[{obj_type.upper()}] {name}"
                )

    except Exception as error:
        print(f"\n[!] Error: {error}")

    finally:
        connection.close()

    wait_enter()


def schema_analysis():
    clear_screen()

    print("""
=============================================
            Midoo Schema Analysis
=============================================
""")

    db = get_database()

    if not db:
        return

    connection = connect_database(db)

    if not connection:
        wait_enter()
        return

    try:
        cursor = connection.cursor()

        tables = cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """).fetchall()

        if not tables:
            print("[-] Tidak ada table.")
        else:
            for (table,) in tables:

                print(
                    f"\n--- {table} ---"
                )

                columns = cursor.execute(
                    f'PRAGMA table_info("{table}")'
                ).fetchall()

                for column in columns:

                    cid, name, col_type, not_null, default, pk = column

                    print(
                        f"  {name}"
                        f" | TYPE={col_type}"
                        f" | PK={pk}"
                        f" | NOT_NULL={not_null}"
                    )

    except Exception as error:
        print(f"\n[!] Error: {error}")

    finally:
        connection.close()

    wait_enter()


def row_column_analysis():
    clear_screen()

    print("""
=============================================
         Midoo Row & Column Analysis
=============================================
""")

    db = get_database()

    if not db:
        return

    connection = connect_database(db)

    if not connection:
        wait_enter()
        return

    try:
        cursor = connection.cursor()

        tables = cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """).fetchall()

        for (table,) in tables:

            count = cursor.execute(
                f'SELECT COUNT(*) FROM "{table}"'
            ).fetchone()[0]

            columns = cursor.execute(
                f'PRAGMA table_info("{table}")'
            ).fetchall()

            print(f"\nTable : {table}")
            print(f"Rows  : {count}")
            print(f"Cols  : {len(columns)}")

    except Exception as error:
        print(f"\n[!] Error: {error}")

    finally:
        connection.close()

    wait_enter()


def search_database():
    clear_screen()

    print("""
=============================================
           Midoo Database Search
=============================================
""")

    db = get_database()

    if not db:
        return

    keyword = input(
        "\nMasukkan keyword: "
    ).strip()

    if not keyword:
        print("\n[!] Keyword tidak boleh kosong.")
        wait_enter()
        return

    connection = connect_database(db)

    if not connection:
        wait_enter()
        return

    try:
        cursor = connection.cursor()

        tables = cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """).fetchall()

        found = 0

        for (table,) in tables:

            columns = cursor.execute(
                f'PRAGMA table_info("{table}")'
            ).fetchall()

            for column in columns:

                column_name = column[1]

                try:
                    query = f'''
                        SELECT *
                        FROM "{table}"
                        WHERE CAST("{column_name}" AS TEXT)
                        LIKE ?
                    '''

                    rows = cursor.execute(
                        query,
                        (f"%{keyword}%",)
                    ).fetchall()

                    for row in rows:

                        print(
                            f"\n[+] Match"
                        )

                        print(
                            f"    Table  : {table}"
                        )

                        print(
                            f"    Column : {column_name}"
                        )

                        print(
                            f"    Row    : {row}"
                        )

                        found += 1

                except sqlite3.Error:
                    continue

        if found == 0:
            print(
                "\n[-] Tidak ditemukan hasil."
            )
        else:
            print(
                f"\n[+] Total match: {found}"
            )

    except Exception as error:
        print(f"\n[!] Error: {error}")

    finally:
        connection.close()

    wait_enter()


def sqlite_strings():
    clear_screen()

    print("""
=============================================
            Midoo SQLite Strings
=============================================
""")

    db = get_database()

    if not db:
        return

    try:
        with open(
            db,
            "rb"
        ) as file:

            data = file.read()

        current = bytearray()
        found = 0

        print("\n[+] Printable strings:\n")

        for byte in data:

            if 32 <= byte <= 126:
                current.append(byte)

            else:

                if len(current) >= 5:

                    text = current.decode(
                        "ascii",
                        errors="ignore"
                    )

                    print(text)

                    found += 1

                current.clear()

        print(
            f"\n[+] Strings ditemukan: {found}"
        )

    except Exception as error:
        print(f"\n[!] Error: {error}")

    wait_enter()


def database_hash():
    clear_screen()

    print("""
=============================================
             Midoo Database Hash
=============================================
""")

    db = get_database()

    if not db:
        return

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    try:
        with open(
            db,
            "rb"
        ) as file:

            while True:

                data = file.read(
                    1024 * 1024
                )

                if not data:
                    break

                md5.update(data)
                sha1.update(data)
                sha256.update(data)

        print(
            f"\nMD5    : {md5.hexdigest()}"
        )

        print(
            f"SHA1   : {sha1.hexdigest()}"
        )

        print(
            f"SHA256 : {sha256.hexdigest()}"
        )

    except Exception as error:
        print(f"\n[!] Error: {error}")

    wait_enter()


def export_table():
    clear_screen()

    print("""
=============================================
             Midoo Export Table
=============================================
""")

    db = get_database()

    if not db:
        return

    table = input(
        "\nMasukkan nama table: "
    ).strip()

    if not table:
        print("\n[!] Table tidak boleh kosong.")
        wait_enter()
        return

    output = input(
        "Nama output CSV [export.csv]: "
    ).strip()

    if not output:
        output = "export.csv"

    connection = connect_database(db)

    if not connection:
        wait_enter()
        return

    try:
        import csv

        cursor = connection.cursor()

        cursor.execute(
            f'SELECT * FROM "{table}"'
        )

        rows = cursor.fetchall()

        headers = [
            description[0]
            for description in cursor.description
        ]

        with open(
            output,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(headers)
            writer.writerows(rows)

        print(
            f"\n[✓] Export berhasil: {output}"
        )

        print(
            f"[+] Rows: {len(rows)}"
        )

    except Exception as error:
        print(f"\n[!] Error: {error}")

    finally:
        connection.close()

    wait_enter()


def integrity_check():
    clear_screen()

    print("""
=============================================
          Midoo Database Integrity
=============================================
""")

    db = get_database()

    if not db:
        return

    connection = connect_database(db)

    if not connection:
        wait_enter()
        return

    try:
        cursor = connection.cursor()

        result = cursor.execute(
            "PRAGMA integrity_check"
        ).fetchone()

        print(
            f"\nResult: {result[0]}"
        )

        if result[0] == "ok":
            print(
                "[✓] Database integrity OK."
            )
        else:
            print(
                "[!] Database memiliki masalah."
            )

    except Exception as error:
        print(f"\n[!] Error: {error}")

    finally:
        connection.close()

    wait_enter()


def free_page_analysis():
    clear_screen()

    print("""
=============================================
        Midoo SQLite Page Analysis
=============================================
""")

    db = get_database()

    if not db:
        return

    try:
        size = os.path.getsize(db)

        with open(
            db,
            "rb"
        ) as file:

            header = file.read(100)

        if header.startswith(
            b"SQLite format 3"
        ):

            print(
                "[✓] SQLite database signature detected."
            )

            page_size = int.from_bytes(
                header[16:18],
                "big"
            )

            print(
                f"[+] Page size : {page_size} bytes"
            )

            if page_size == 1:
                page_size = 65536

            pages = size // page_size

            print(
                f"[+] Approx pages : {pages}"
            )

        else:

            print(
                "[!] SQLite signature tidak ditemukan."
            )

    except Exception as error:
        print(f"\n[!] Error: {error}")

    wait_enter()


def tool_status():
    clear_screen()

    print("""
=============================================
        Midoo Database Tool Status
=============================================
""")

    print(
        "[✓] Python SQLite3 : Available"
    )

    print(
        f"[+] SQLite version : {sqlite3.sqlite_version}"
    )

    if shutil.which("sqlite3"):
        print(
            "[✓] sqlite3 CLI     : Installed"
        )
    else:
        print(
            "[-] sqlite3 CLI     : Not Found"
        )

    wait_enter()


def show_menu():

    print("""
=============================================
       Midoo Database Forensics Toolkit
                    v1.0
=============================================

    [1]  SQLite Analyzer
    [2]  Database Information
    [3]  Table Enumeration
    [4]  Schema Analysis
    [5]  Row & Column Analysis
    [6]  Search Database
    [7]  SQLite Strings
    [8]  Database Hash
    [9]  Page Analysis
    [10] Export Table
    [11] Database Integrity Check
    [12] Tool Status

    [0]  Kembali

=============================================
""")


def sqlite_analyzer():
    clear_screen()

    print("""
=============================================
             Midoo SQLite Analyzer
=============================================
""")

    db = get_database()

    if not db:
        return

    connection = connect_database(db)

    if not connection:
        wait_enter()
        return

    try:
        cursor = connection.cursor()

        tables = cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """).fetchall()

        print("\n[+] SQLite Tables\n")

        for (table,) in tables:

            print(f"Table: {table}")

            rows = cursor.execute(
                f'SELECT * FROM "{table}" LIMIT 10'
            ).fetchall()

            for row in rows:
                print(
                    f"  {row}"
                )

            print()

    except Exception as error:
        print(
            f"\n[!] Error: {error}"
        )

    finally:
        connection.close()

    wait_enter()


def main():

    while True:

        clear_screen()
        show_menu()

        pilihan = input(
            "Midoo Database > "
        ).strip()

        if pilihan == "0":
            break

        elif pilihan == "1":
            sqlite_analyzer()

        elif pilihan == "2":
            database_information()

        elif pilihan == "3":
            table_enumeration()

        elif pilihan == "4":
            schema_analysis()

        elif pilihan == "5":
            row_column_analysis()

        elif pilihan == "6":
            search_database()

        elif pilihan == "7":
            sqlite_strings()

        elif pilihan == "8":
            database_hash()

        elif pilihan == "9":
            free_page_analysis()

        elif pilihan == "10":
            export_table()

        elif pilihan == "11":
            integrity_check()

        elif pilihan == "12":
            tool_status()

        else:
            print(
                "\n[!] Pilihan tidak valid."
            )
            wait_enter()


if __name__ == "__main__":
    main()
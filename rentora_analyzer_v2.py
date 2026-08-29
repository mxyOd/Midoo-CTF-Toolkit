#!/usr/bin/env python3
import argparse
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlencode, urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms = []
        self.links = []
        self.form = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])

        if tag == "form":
            self.form = {
                "action": attrs.get("action", ""),
                "method": attrs.get("method", "GET").upper(),
                "fields": []
            }
            self.forms.append(self.form)

        if tag in ("input", "select", "textarea", "button"):
            if self.form is not None and attrs.get("name"):
                self.form["fields"].append({
                    "name": attrs["name"],
                    "type": attrs.get("type", "text"),
                    "value": attrs.get("value", ""),
                    "required": "required" in attrs
                })

    def handle_endtag(self, tag):
        if tag == "form":
            self.form = None


class RentoraAnalyzer:
    def __init__(self, url):
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        self.base = url.rstrip("/")
        self.forms = []
        self.candidates = set()

    def request(self, url, method="GET", data=None):
        try:
            body = urlencode(data).encode() if data else None
            req = Request(
                url,
                data=body,
                method=method,
                headers={
                    "User-Agent": "Midoo-Rentora-Analyzer/2.0",
                    "Accept": "*/*"
                }
            )
            response = urlopen(req, timeout=15)
            return response, response.read(2 * 1024 * 1024)
        except HTTPError as e:
            print(f"[!] HTTP {e.code}: {url}")
        except URLError as e:
            print(f"[!] Connection error: {e.reason}")
        except Exception as e:
            print(f"[!] Error: {e}")
        return None, None

    def inspect(self, url, content):
        text = content.decode("utf-8", errors="ignore")
        parser = Parser()

        try:
            parser.feed(text)
        except Exception:
            pass

        for form in parser.forms:
            form["action_url"] = urljoin(url, form["action"])
            self.forms.append(form)

        patterns = [
            r"[\"']([^\"']*(?:pdf|download|invoice|receipt|confirmation|document)[^\"']*)[\"']",
            r"(?:url|href|action)\s*[:=]\s*[\"']([^\"']+)[\"']"
        ]

        for pattern in patterns:
            for value in re.findall(pattern, text, re.I):
                absolute = urljoin(url, value)
                if urlparse(absolute).netloc == urlparse(self.base).netloc:
                    self.candidates.add(absolute)

        for link in parser.links:
            absolute = urljoin(url, link)
            if urlparse(absolute).netloc != urlparse(self.base).netloc:
                continue
            if any(word in absolute.lower() for word in (
                "pdf", "download", "invoice", "receipt",
                "confirmation", "booking", "document"
            )):
                self.candidates.add(absolute)

        return parser

    def show_forms(self):
        print("\n=============================================")
        print("                 BOOKING FORMS")
        print("=============================================")

        if not self.forms:
            print("[-] Tidak ditemukan form.")
            return

        for i, form in enumerate(self.forms, 1):
            print(f"\n[{i}] {form['method']} {form['action_url']}")
            for field in form["fields"]:
                req = " required" if field["required"] else ""
                print(f"    - {field['name']} [{field['type']}]{req}")

    def interactive_booking(self):
        if not self.forms:
            print("\n[-] Tidak ada form booking.")
            return

        print("\n=============================================")
        print("                  BOOKING FLOW")
        print("=============================================")

        for i, form in enumerate(self.forms, 1):
            print(f"[{i}] {form['method']} {form['action_url']}")

        choice = input("\nPilih form [0=batal]: ").strip()

        if choice == "0":
            return

        try:
            form = self.forms[int(choice) - 1]
        except (ValueError, IndexError):
            print("[!] Pilihan tidak valid.")
            return

        data = {}

        print("\nIsi field dengan data dummy/CTF yang diizinkan:")

        for field in form["fields"]:
            prompt = field["name"]
            if field["required"]:
                prompt += " [required]"
            if field["value"]:
                prompt += f" [{field['value']}]"

            value = input(prompt + ": ").strip()

            if not value:
                value = field["value"]

            if value:
                data[field["name"]] = value

        print(f"\n[*] Submit {form['method']} -> {form['action_url']}")

        if form["method"] == "GET":
            target = form["action_url"]
            query = urlencode(data)
            if query:
                target += ("&" if "?" in target else "?") + query
            response, body = self.request(target)
        else:
            response, body = self.request(
                form["action_url"],
                "POST",
                data
            )

        if not response:
            return

        print(f"[+] Status      : {response.status}")
        print(f"[+] Final URL   : {response.geturl()}")
        print(
            f"[+] Content-Type: "
            f"{response.headers.get('Content-Type', '-')}"
        )

        if body:
            self.inspect(response.geturl(), body)

    def run(self, interactive=False):
        print("=============================================")
        print("           Midoo Rentora Analyzer")
        print("                    v2.0")
        print("=============================================")
        print(f"Target: {self.base}")

        response, body = self.request(self.base)

        if response and body:
            print(f"\n[+] Status: {response.status}")
            print(
                f"[+] Type  : "
                f"{response.headers.get('Content-Type', '-')}"
            )
            self.inspect(self.base, body)

        self.show_forms()

        if interactive:
            self.interactive_booking()

        print("\n=============================================")
        print("              PDF / ENDPOINTS")
        print("=============================================")

        if self.candidates:
            for candidate in sorted(self.candidates):
                print(f"[+] {candidate}")
        else:
            print("[-] Belum ditemukan URL PDF/download.")

        print("\n=============================================")
        print("              ANALYSIS DONE")
        print("=============================================")


def main():
    parser = argparse.ArgumentParser(
        description="Midoo Rentora Analyzer - booking/PDF CTF helper"
    )
    parser.add_argument(
        "-u", "--url",
        required=True,
        help="Target URL"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Isi dan submit form yang ditemukan"
    )

    args = parser.parse_args()

    RentoraAnalyzer(args.url).run(args.interactive)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse, json, socket, ssl, time
from datetime import datetime
from urllib.parse import urlparse, urljoin
from urllib.request import Request, build_opener
from urllib.error import HTTPError, URLError

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
except ImportError:
    print("[!] Install dulu: python3 -m pip install rich")
    raise SystemExit(1)

console = Console()
UA = "Midoo-VulnScope/1.0"


def normalize(target):
    if not target.startswith(("http://", "https://")):
        target = "https://" + target
    p = urlparse(target)
    if not p.hostname:
        raise ValueError("Target tidak valid")
    return target.rstrip("/")


def get(opener, url, timeout):
    req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        return opener.open(req, timeout=timeout)
    except HTTPError as e:
        return e
    except URLError as e:
        raise RuntimeError(str(e.reason))


def step(msg):
    console.print(f"[cyan]•[/cyan] {msg}...", end="")
    time.sleep(.15)
    console.print(" [green]OK[/green]")


def finding(lst, title, severity, detail, recommendation):
    lst.append({"title": title, "severity": severity, "detail": detail, "recommendation": recommendation})


def scan(args):
    target = normalize(args.domain)
    p = urlparse(target)
    opener = build_opener()
    findings = []
    result = {"target": target, "started_at": datetime.now().astimezone().isoformat()}

    console.clear()
    console.print(Panel.fit("Midoo VulnScope v1.0\nWeb Security Scanner", border_style="cyan"))
    console.print(f"\n[bold]Target[/bold] : {target}\n")

    step("Resolving target")
    try:
        ip = socket.gethostbyname(p.hostname)
    except socket.gaierror as e:
        console.print(f"\n[red][!] DNS resolution gagal: {e}[/red]")
        return
    result["ip"] = ip
    console.print(f"  IP Address: {ip}")

    step("Requesting HTTP response")
    try:
        r = get(opener, target, args.timeout)
    except RuntimeError as e:
        console.print(f"\n[red][!] Request gagal: {e}[/red]")
        return

    h = r.headers
    result.update({"final_url": r.geturl(), "status_code": r.status, "headers": dict(h)})
    console.print(f"  Status: {r.status}")
    console.print(f"  Final URL: {r.geturl()}")

    step("Checking security headers")
    checks = {
        "Content-Security-Policy": ("Medium", "Tambahkan Content-Security-Policy yang sesuai."),
        "Strict-Transport-Security": ("Low", "Aktifkan HSTS setelah seluruh trafik menggunakan HTTPS."),
        "X-Content-Type-Options": ("Low", "Gunakan X-Content-Type-Options: nosniff."),
        "X-Frame-Options": ("Low", "Gunakan X-Frame-Options atau frame-ancestors CSP."),
        "Referrer-Policy": ("Low", "Tetapkan Referrer-Policy yang sesuai."),
        "Permissions-Policy": ("Low", "Batasi browser features yang tidak diperlukan."),
    }
    for name, (sev, rec) in checks.items():
        if not h.get(name):
            finding(findings, f"Missing {name}", sev, f"Header {name} tidak ditemukan.", rec)

    step("Checking information disclosure")
    if h.get("Server"):
        finding(findings, "Server Header Disclosure", "Info", f"Server: {h['Server']}", "Minimalkan informasi implementasi/version yang tidak diperlukan.")
    if h.get("X-Powered-By"):
        finding(findings, "X-Powered-By Disclosure", "Low", f"X-Powered-By: {h['X-Powered-By']}", "Hapus atau minimalkan header X-Powered-By.")

    step("Checking cookies")
    cookies = h.get_all("Set-Cookie") or []
    result["cookies"] = cookies
    for i, c in enumerate(cookies, 1):
        low = c.lower()
        if p.scheme == "https" and "secure" not in low:
            finding(findings, f"Cookie #{i} Missing Secure", "Medium", c.split(";",1)[0], "Tambahkan atribut Secure.")
        if "httponly" not in low:
            finding(findings, f"Cookie #{i} Missing HttpOnly", "Medium", c.split(";",1)[0], "Tambahkan HttpOnly jika cookie tidak perlu diakses JavaScript.")
        if "samesite" not in low:
            finding(findings, f"Cookie #{i} Missing SameSite", "Low", c.split(";",1)[0], "Pertimbangkan SameSite sesuai kebutuhan aplikasi.")

    step("Checking HTTPS")
    if p.scheme != "https":
        finding(findings, "HTTP Instead of HTTPS", "Medium", "Target menggunakan HTTP.", "Gunakan HTTPS untuk melindungi data saat transit.")

    step("Checking robots.txt and sitemap.xml")
    discovery = {}
    for path in ("/robots.txt", "/sitemap.xml"):
        try:
            x = get(opener, urljoin(r.geturl(), path), args.timeout)
            discovery[path] = x.status
        except Exception:
            discovery[path] = None
    result["discovery"] = discovery

    step("Checking TLS")
    tls = {}
    if p.scheme == "https":
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((p.hostname, p.port or 443), timeout=args.timeout) as sock:
                with ctx.wrap_socket(sock, server_hostname=p.hostname) as s:
                    tls["version"] = s.version()
                    tls["cipher"] = s.cipher()[0] if s.cipher() else None
        except Exception as e:
            tls["error"] = str(e)
    result["tls"] = tls
    result["findings"] = findings
    result["finished_at"] = datetime.now().astimezone().isoformat()

    table = Table(title="Vulnerability Summary", show_lines=True, expand=True)
    table.add_column("ID", justify="center", width=5)
    table.add_column("Finding")
    table.add_column("Severity", justify="center", width=10)
    table.add_column("Status", justify="center", width=12)
    order = {"Critical":0,"High":1,"Medium":2,"Low":3,"Info":4}
    findings.sort(key=lambda x: order.get(x["severity"], 99))
    for i, f in enumerate(findings, 1):
        sev = f["severity"]
        style = "red" if sev in ("Critical","High") else "yellow" if sev == "Medium" else "cyan" if sev == "Low" else "dim"
        table.add_row(str(i), f["title"], f"[{style}]{sev}[/{style}]", "[red]Detected[/red]")
    if not findings:
        table.add_row("-", "Tidak ada finding dari pemeriksaan ini", "[green]None[/green]", "[green]Clean[/green]")
    console.print("\n", table)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        console.print(f"\n[green]✓[/green] Hasil disimpan: [bold]{args.output}[/bold]")
    console.print("[green]✓ Scan selesai.[/green]")


def main():
    ap = argparse.ArgumentParser(description="Midoo VulnScope v1.0 - Web Security Scanner")
    ap.add_argument("-d", "--domain", required=True, help="Target URL/domain yang diizinkan")
    ap.add_argument("-o", "--output", help="File JSON hasil scan")
    ap.add_argument("-t", "--timeout", type=int, default=10, help="Timeout dalam detik")
    args = ap.parse_args()
    try:
        scan(args)
    except KeyboardInterrupt:
        console.print("\n[yellow][!] Scan dihentikan.[/yellow]")
    except ValueError as e:
        console.print(f"[red][!] {e}[/red]")


if __name__ == "__main__":
    main()

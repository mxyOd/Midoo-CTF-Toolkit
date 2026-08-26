# Midoo CTF Toolkit

A modular cybersecurity and Capture The Flag (CTF) toolkit written in Python.

Designed for CTF competitions, cybersecurity learning, digital forensics, and authorized security testing.

---

## Features

### Cryptography
- Base64
- Hex
- Binary
- ROT13
- Caesar Cipher
- Atbash
- XOR

### Digital Forensics
- File information
- Magic bytes
- Entropy analysis
- File hashing
- Printable strings

### Network Analysis
- IP information
- CIDR analysis
- DNS lookup
- Reverse DNS
- Connectivity check
- Port checking

### PCAP Analysis
- Packet analysis
- Protocol statistics
- IP statistics
- Port statistics
- DNS analysis
- HTTP analysis
- String and flag search

### Hash Analysis
- MD5
- SHA1
- SHA256
- SHA512
- File hashing
- Hash comparison
- Hash identification

### JWT Analysis
- JWT structure
- Header decoding
- Payload decoding
- Signature inspection
- Claims inspection
- Expiration checking

### Web Recon
- HTTP headers
- HTTP status code
- DNS information
- robots.txt
- sitemap.xml
- TLS information
- Page title
- Technology hints

### Steganography
- Image information
- PNG metadata
- Printable strings
- PNG chunk analysis
- Trailing data detection
- Hidden flag search
- Basic LSB analysis
- Hex preview

### URL Analysis
- URL parsing
- Parameter extraction
- URL encoding
- URL decoding
- URL normalization
- Domain information
- Path analysis
- Query analysis
- Suspicious parameter hints

---

## Installation

Clone the repository:

```bash
git clone https://github.com/mxyOd/Midoo-CTF-Toolkit.git
```

Enter the project directory:

```bash
cd Midoo-CTF-Toolkit
```

Run the toolkit:

```bash
python main.py
```

---

## Requirements

- Python 3.x

Most modules use the Python standard library.

Some network and PCAP functionality may require external tools depending on the implementation.

---

## Usage

Run the main launcher:

```bash
python main.py
```

The main menu provides access to all available modules:

```text
=============================================
              Midoo CTF Toolkit
=============================================

  [1] Crypto Tool
  [2] File Analyzer
  [3] Network Analyzer
  [4] PCAP Analyzer
  [5] Hash Analyzer
  [6] JWT Analyzer
  [7] Web Recon
  [8] Stego Analyzer
  [9] URL Analyzer

  [10] Exit

=============================================
```

Select a module by entering its corresponding number.

---

## Project Structure

```text
Midoo-CTF-Toolkit/
│
├── main.py
│
├── crypto_tool.py
├── file_analyzer.py
├── network_analyzer.py
├── pcap_analyzer.py
├── hash_analyzer.py
├── jwt_analyzer.py
├── web_recon.py
├── stego_analyzer.py
└── url_analyzer.py
```

---

## Modules

| Module | Description |
|---|---|
| `crypto_tool.py` | Encoding and classical cipher utilities |
| `file_analyzer.py` | File and forensic analysis |
| `network_analyzer.py` | Basic network analysis |
| `pcap_analyzer.py` | PCAP and packet analysis |
| `hash_analyzer.py` | Hash generation and identification |
| `jwt_analyzer.py` | JWT inspection and claim analysis |
| `web_recon.py` | Basic web reconnaissance |
| `stego_analyzer.py` | Image and steganography analysis |
| `url_analyzer.py` | URL and parameter analysis |
| `main.py` | Main toolkit launcher |

---

## Example

Clone and run:

```bash
git clone https://github.com/mxyOd/Midoo-CTF-Toolkit.git
cd Midoo-CTF-Toolkit
python main.py
```

Example workflow:

```text
Evidence
   ↓
File Analyzer
   ↓
Hash Analyzer
   ↓
Stego Analyzer
   ↓
Network / PCAP Analyzer
   ↓
URL Analyzer
   ↓
Web Recon
   ↓
CTF Flag
```

---

## Educational Purpose

Midoo CTF Toolkit is intended to support:

- Capture The Flag competitions
- Cybersecurity education
- Digital forensics practice
- Security research in authorized environments
- Personal cybersecurity labs

---

## Disclaimer

This project is intended for educational purposes, CTF competitions, and authorized security testing only.

Do not use this toolkit against systems, networks, applications, or data without proper authorization.

The author is not responsible for misuse of this software.

---

## Author

**Mido Reksa Putra**

GitHub: [@mxyOd](https://github.com/mxyOd)

---

## License

This project is currently provided for educational purposes.

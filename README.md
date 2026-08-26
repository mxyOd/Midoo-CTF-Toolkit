# Midoo CTF Toolkit

A modular cybersecurity and Capture The Flag toolkit written in Python.

## Features

- Crypto Tool
- File Analyzer
- Network Analyzer
- PCAP Analyzer
- Hash Analyzer
- JWT Analyzer
- Web Recon

## Installation

Clone repository:

```bash
git clone https://github.com/mxyOd/Midoo-CTF-Toolkit.git
```

Enter the directory:

```bash
cd Midoo-CTF-Toolkit
```

Run the toolkit:

```bash
python main.py
```

## Project Structure

```text
Midoo-CTF-Toolkit/
├── main.py
├── crypto_tool.py
├── file_analyzer.py
├── hash_analyzer.py
├── jwt_analyzer.py
├── network_analyzer.py
├── pcap_analyzer.py
└── web_recon.py
```

## Tools

### Crypto Tool

Supports common encoding and cipher operations:

- Base64
- Hex
- Binary
- ROT13
- Caesar Cipher
- Atbash
- XOR

### File Analyzer

Analyze files for:

- File type
- Magic bytes
- File size
- Entropy
- MD5
- SHA1
- SHA256
- Printable strings

### Network Analyzer

Provides basic network analysis:

- IP information
- CIDR calculation
- DNS lookup
- Reverse DNS
- Connectivity check
- Port check

### PCAP Analyzer

Analyze packet capture files:

- Packet summary
- Protocol statistics
- IP statistics
- Port statistics
- DNS queries
- HTTP requests
- Flag search
- Printable strings

### Hash Analyzer

Supports:

- MD5
- SHA1
- SHA256
- SHA512
- File hashing
- Hash comparison
- Hash identification

### JWT Analyzer

Inspect JWT tokens:

- Header
- Payload
- Signature
- Claims
- Expiration

### Web Recon

Basic web information gathering:

- HTTP headers
- Status code
- DNS information
- robots.txt
- sitemap.xml
- TLS information
- Page title
- Technology hints

## Requirements

Python 3.x

Some features may require additional tools such as TShark.

## Usage

Run the main launcher:

```bash
python main.py
```

Then select the tool from the menu.

## Disclaimer

This project is intended for educational purposes, CTF competitions, and authorized security testing only.

Do not use this toolkit against systems without permission.

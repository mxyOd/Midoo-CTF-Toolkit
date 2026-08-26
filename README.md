# Midoo CTF Toolkit

**Midoo CTF Toolkit** adalah toolkit modular berbasis Python yang dibuat untuk membantu proses belajar **Cyber Security, Capture The Flag (CTF), Digital Forensics, dan analisis keamanan**.

Toolkit ini menggabungkan beberapa tools sederhana dalam satu launcher sehingga lebih mudah digunakan saat mengerjakan challenge CTF.

---

## Fitur

### 🔐 Kriptografi

- Base64
- Hex
- Binary
- ROT13
- Caesar Cipher
- Atbash
- XOR

### 🔎 Digital Forensics

- Informasi file
- Magic bytes
- Analisis entropy
- MD5
- SHA1
- SHA256
- Printable strings

### 🌐 Network Analysis

- Informasi IP
- CIDR Calculator
- DNS Lookup
- Reverse DNS
- Connectivity Check
- Port Check

### 📡 PCAP Analysis

- Packet Summary
- Statistik protokol
- Statistik IP
- Statistik port
- DNS Queries
- HTTP Requests
- Pencarian string
- Pencarian flag

### 🔑 Hash Analysis

- MD5
- SHA1
- SHA256
- SHA512
- Hash file
- Perbandingan hash
- Identifikasi hash

### 🎫 JWT Analysis

- Analisis struktur JWT
- Decode Header
- Decode Payload
- Analisis Signature
- Analisis Claims
- Pemeriksaan Expiration

### 🕵️ Web Recon

- HTTP Headers
- HTTP Status Code
- DNS Information
- robots.txt
- sitemap.xml
- TLS Information
- Page Title
- Technology Hints

### 🖼️ Steganography

- Informasi gambar
- Metadata PNG
- Printable strings
- Analisis PNG chunks
- Deteksi trailing data
- Pencarian flag tersembunyi
- Analisis dasar LSB
- Hex Preview

### 🔗 URL Analysis

- Parsing URL
- Ekstraksi parameter
- URL Encode
- URL Decode
- Normalisasi URL
- Informasi domain
- Analisis path
- Analisis query
- Deteksi parameter yang umum digunakan dalam pengujian keamanan

---

## Instalasi

Clone repository:

```bash
git clone https://github.com/mxyOd/Midoo-CTF-Toolkit.git
```

Masuk ke folder:

```bash
cd Midoo-CTF-Toolkit
```

Jalankan:

```bash
python main.py
```

---

## Kebutuhan

- Python 3.x

Sebagian besar fitur menggunakan **Python Standard Library**, sehingga tidak membutuhkan banyak dependency tambahan.

Untuk beberapa fitur tertentu, mungkin diperlukan tools eksternal seperti **TShark**.

---

## Cara Menggunakan

Jalankan:

```bash
python main.py
```

Kemudian akan muncul menu utama:

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

Masukkan nomor sesuai dengan tool yang ingin digunakan.

---

## Struktur Project

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

## Modul

| File | Fungsi |
|---|---|
| `main.py` | Launcher utama toolkit |
| `crypto_tool.py` | Encoding dan cipher sederhana |
| `file_analyzer.py` | Analisis file dan forensics |
| `network_analyzer.py` | Analisis dasar jaringan |
| `pcap_analyzer.py` | Analisis file PCAP |
| `hash_analyzer.py` | Pembuatan dan analisis hash |
| `jwt_analyzer.py` | Analisis token JWT |
| `web_recon.py` | Information gathering pada website |
| `stego_analyzer.py` | Analisis steganografi |
| `url_analyzer.py` | Analisis URL dan parameter |

---

## Contoh Alur CTF

Toolkit ini dapat digunakan sesuai jenis evidence atau challenge yang ditemukan.

```text
            Evidence
                │
                ▼
        ┌───────────────┐
        │ File Analyzer │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │ Hash Analyzer │
        └───────┬───────┘
                │
                ▼
        ┌────────────────┐
        │ Stego Analyzer │
        └───────┬────────┘
                │
                ▼
        ┌────────────────┐
        │ PCAP Analyzer  │
        └───────┬────────┘
                │
                ▼
        ┌────────────────┐
        │ URL Analyzer   │
        └───────┬────────┘
                │
                ▼
          Web Recon
                │
                ▼
             Flag
```

Tidak semua challenge membutuhkan seluruh tahapan tersebut. Gunakan modul sesuai kebutuhan challenge.

---

## Tujuan Project

Project ini dibuat sebagai sarana untuk:

- Belajar Cyber Security
- Latihan CTF
- Belajar Digital Forensics
- Belajar Network Analysis
- Belajar Web Security
- Membuat tools keamanan sederhana dengan Python
- Eksperimen dan pengembangan tools pribadi

---

## Disclaimer

Midoo CTF Toolkit dibuat untuk **tujuan edukasi, kompetisi CTF, lab pribadi, dan pengujian keamanan yang telah mendapatkan izin**.

Jangan gunakan tools ini terhadap sistem, jaringan, aplikasi, atau data tanpa izin.

Penggunaan toolkit sepenuhnya menjadi tanggung jawab pengguna.

---

## Author

**Mido Reksa Putra**

GitHub: [@mxyOd](https://github.com/mxyOd)

---

## Lisensi

Project ini saat ini dibuat untuk tujuan edukasi dan pembelajaran.

# 🔐 RSA-OAEP-256 Encryption / Decryption

Implementasi software skema enkripsi dan dekripsi berdasarkan standar **RSA-OAEP-256** — dibuat dari nol tanpa library kriptografi pihak ketiga.

## 📋 Spesifikasi

| Aspek | Detail |
|---|---|
| Algoritma | RSA-OAEP (Optimal Asymmetric Encryption Padding) |
| Hash Function | SHA-256 (untuk MGF1 dan label hash) |
| Panjang Kunci | 2048-bit |
| Bahasa | Python 3.8+ |
| GUI | Tkinter |

## 🏗️ Struktur Proyek

```
rsa_oaep_256/
├── core/               # Implementasi kriptografi (buatan sendiri)
│   ├── bigint_math.py  # Aritmatika big integer
│   ├── miller_rabin.py # Primality test
│   ├── prime_gen.py    # Generate prime p, q
│   ├── rsa_keygen.py   # RSA key pair generation
│   ├── sha256.py       # SHA-256 from scratch
│   ├── mgf1.py         # Mask Generation Function 1
│   ├── oaep.py         # OAEP padding & unpadding
│   └── rsa_oaep.py     # High-level encrypt/decrypt
├── io_handler/         # File I/O dan key parsing
│   ├── key_parser.py   # Baca/tulis key file hex
│   ├── file_handler.py # Binary-safe file read/write
│   └── chunker.py      # Validasi plaintext & split ciphertext 256-byte
├── gui/                # Antarmuka pengguna (tkinter)
│   ├── app.py          # Entry point GUI
│   ├── encrypt_tab.py  # Tab enkripsi
│   ├── decrypt_tab.py  # Tab dekripsi
│   ├── keygen_tab.py   # Tab generate key pair
│   └── widgets.py      # Reusable widgets
├── tests/              # Unit & integration tests
├── keys/               # Key pair output (hex format)
└── main.py             # Entry point
```

## 🚀 Cara Menjalankan

```bash
# Jalankan GUI
python main.py

# Jalankan tests
python -m unittest discover tests/
```

## 📐 Cara Kerja

### Enkripsi
1. Baca file plaintext (binary-safe)
2. Validasi: plaintext harus <= 190 bytes
3. OAEP padding → RSA encrypt (modular exponentiation)
4. Tulis ciphertext 256 bytes ke file output

### Dekripsi
1. Baca file ciphertext
2. Split per 256 bytes
3. Setiap chunk: RSA decrypt → OAEP unpadding
4. Gabung plaintext chunks
5. Tulis ke file output (byte-perfect dengan aslinya)

## 📁 Format Key File (Hex)

**Public Key:**
```
n=<2048-bit modulus dalam hex>
e=<public exponent dalam hex>
```

**Private Key:**
```
n=<2048-bit modulus dalam hex>
d=<private exponent dalam hex>
```

## ⚠️ Catatan

- **Tidak menggunakan** library kriptografi pihak ketiga (`cryptography`, `pycryptodome`, `hashlib`, dll.)
- Hanya menggunakan Python standard library
- Key generation membutuhkan ~5-30 detik (primality testing)
- Plaintext di atas 190 bytes ditolak; untuk data besar gunakan skema hybrid
- Ukuran ciphertext: 256 bytes untuk setiap plaintext yang lolos validasi (<= 190 bytes)

## 📚 Referensi

- [RFC 8017](https://tools.ietf.org/html/rfc8017) — PKCS #1 v2.2 (OAEP scheme)
- [FIPS 180-4](https://csrc.nist.gov/publications/detail/fips/180/4/final) — SHA-256 (NIST)
- [FIPS 186-5](https://csrc.nist.gov/publications/detail/fips/186/5/final) — Digital Signature Standard

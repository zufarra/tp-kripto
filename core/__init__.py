"""
core — Modul implementasi kriptografi RSA-OAEP-256 (buatan sendiri).

Submodules:
    - bigint_math: Aritmatika big integer (modexp, gcd, modinv, I2OSP, OS2IP)
    - miller_rabin: Miller-Rabin primality test
    - prime_gen: Generate bilangan prima
    - rsa_keygen: RSA key pair generation
    - sha256: SHA-256 hash function from scratch
    - mgf1: Mask Generation Function 1 (MGF1-SHA256)
    - oaep: OAEP padding & unpadding
    - rsa_oaep: High-level RSA-OAEP encrypt/decrypt
"""

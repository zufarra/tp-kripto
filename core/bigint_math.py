"""Aritmatika dasar untuk RSA-OAEP-256.

Fokus modul ini hanya pada fungsi-fungsi yang dipakai cryptosystem:
- modular exponentiation
- extended Euclidean algorithm
- modular inverse
- konversi integer <-> octet string

Python sudah menyediakan arbitrary-precision integer, jadi kita tidak
mereimplementasi bigint dari nol.
"""

from __future__ import annotations

from typing import Tuple

__all__ = [
    "modexp",
    "gcd",
    "extended_gcd",
    "modinv",
    "lcm",
    "I2OSP",
    "OS2IP",
]


def modexp(base: int, exponent: int, modulus: int) -> int:
    """Modular exponentiation menggunakan built-in pow().

    Secara algoritma sama dengan square-and-multiply manual,
    tetapi built-in pow() diimplementasikan dalam C sehingga
    jauh lebih cepat untuk bilangan besar (2048-bit RSA).
    """
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    if exponent < 0:
        raise ValueError("exponent must be non-negative")
    return pow(base, exponent, modulus)


def gcd(a: int, b: int) -> int:
    """Greatest common divisor, always non-negative."""
    x = abs(a)
    y = abs(b)
    while y:
        x, y = y, x % y
    return x


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Return (g, x, y) such that ax + by = g = gcd(a, b)."""
    old_r, r = abs(a), abs(b)
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    if a < 0:
        old_s = -old_s
    if b < 0:
        old_t = -old_t
    return old_r, old_s, old_t


def modinv(a: int, modulus: int) -> int:
    """Multiplicative inverse of a modulo modulus."""
    if modulus <= 0:
        raise ValueError("modulus must be positive")

    g, x, _ = extended_gcd(a, modulus)
    if g != 1:
        raise ValueError("inverse does not exist")
    return x % modulus


def lcm(a: int, b: int) -> int:
    """Least common multiple."""
    if a == 0 or b == 0:
        return 0
    return abs(a // gcd(a, b) * b)


def I2OSP(x: int, x_len: int) -> bytes:
    """Integer-to-Octet-String Primitive (RFC 8017)."""
    if x_len < 0:
        raise ValueError("x_len must be non-negative")
    if x < 0:
        raise ValueError("integer must be non-negative")
    if x_len == 0:
        if x == 0:
            return b""
        raise ValueError("integer too large")
    if x >= 1 << (8 * x_len):
        raise ValueError("integer too large")
    return x.to_bytes(x_len, "big")


def OS2IP(x: bytes) -> int:
    """Octet-String-to-Integer Primitive (RFC 8017)."""
    if not isinstance(x, (bytes, bytearray, memoryview)):
        raise TypeError("x must be a bytes-like object")
    return int.from_bytes(bytes(x), "big")

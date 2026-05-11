"""High-level RSA-OAEP encrypt/decrypt helpers."""

from __future__ import annotations

from typing import Tuple

from .bigint_math import I2OSP, OS2IP, modexp
from .oaep import oaep_decode, oaep_encode

__all__ = [
    "encrypt_chunk",
    "decrypt_chunk",
    "rsa_oaep_encrypt",
    "rsa_oaep_decrypt",
]

_HASH_LEN = 32


def _k_from_modulus(n: int) -> int:
    if n <= 0:
        raise ValueError("modulus must be positive")
    return (n.bit_length() + 7) // 8


def rsa_oaep_encrypt(plaintext_chunk: bytes, n: int, e: int) -> bytes:
    """Encrypt a single plaintext chunk using RSA-OAEP."""
    k = _k_from_modulus(n)
    em = oaep_encode(plaintext_chunk, k)
    m = OS2IP(em)
    c = modexp(m, e, n)
    return I2OSP(c, k)


def rsa_oaep_decrypt(ciphertext_chunk: bytes, n: int, d: int) -> bytes:
    """Decrypt a single RSA-OAEP ciphertext chunk."""
    if not isinstance(ciphertext_chunk, (bytes, bytearray, memoryview)):
        raise TypeError("ciphertext_chunk must be a bytes-like object")
    k = _k_from_modulus(n)
    ciphertext = bytes(ciphertext_chunk)
    if len(ciphertext) != k:
        raise ValueError("ciphertext chunk has invalid length")
    c = OS2IP(ciphertext)
    m = modexp(c, d, n)
    em = I2OSP(m, k)
    return oaep_decode(em, k)


def encrypt_chunk(plaintext: bytes, n: int, e: int) -> bytes:
    """Alias used by the implementation plan interface contract."""
    return rsa_oaep_encrypt(plaintext, n, e)


def decrypt_chunk(ciphertext: bytes, n: int, d: int) -> bytes:
    """Alias used by the implementation plan interface contract."""
    return rsa_oaep_decrypt(ciphertext, n, d)

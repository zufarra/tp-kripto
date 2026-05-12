from __future__ import annotations
from typing import List

__all__ = [
    "MAX_PLAINTEXT_BYTES",
    "PLAINTEXT_CHUNK",
    "CIPHERTEXT_CHUNK",
    "split_encrypt",
    "split_decrypt",
    "join_chunks",
]

# 2048-bit RSA modulus = 256 bytes.
# With OAEP-SHA256, the maximum plaintext length is 256 - 2*32 - 2 = 190 bytes.
MAX_PLAINTEXT_BYTES = 190
PLAINTEXT_CHUNK = MAX_PLAINTEXT_BYTES
CIPHERTEXT_CHUNK = 256


def split_encrypt(data: bytes) -> List[bytes]:
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError("data must be a bytes-like object")

    plaintext = bytes(data)
    if len(plaintext) > MAX_PLAINTEXT_BYTES:
        raise ValueError(
            f"Panjang plaintext maksimal {MAX_PLAINTEXT_BYTES} bytes. "
            "RSA-OAEP tidak memecah plaintext otomatis."
        )
    return [plaintext]


def split_decrypt(data: bytes) -> List[bytes]:
    if not data:
        return []
        
    if len(data) % CIPHERTEXT_CHUNK != 0:
        raise ValueError(
            f"Panjang ciphertext tidak valid. Harus kelipatan {CIPHERTEXT_CHUNK} bytes, "
            f"tapi panjangnya {len(data)} bytes."
        )
        
    chunks = []
    for i in range(0, len(data), CIPHERTEXT_CHUNK):
        chunks.append(data[i : i + CIPHERTEXT_CHUNK])
    return chunks


def join_chunks(chunks: List[bytes]) -> bytes:
    return b"".join(chunks)

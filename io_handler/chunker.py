from __future__ import annotations
from typing import List

__all__ = [
    "PLAINTEXT_CHUNK",
    "CIPHERTEXT_CHUNK",
    "split_encrypt",
    "split_decrypt",
    "join_chunks",
]

PLAINTEXT_CHUNK = 190
CIPHERTEXT_CHUNK = 256


def split_encrypt(data: bytes) -> List[bytes]:
    if not data:
        return [b""]
        
    chunks = []
    for i in range(0, len(data), PLAINTEXT_CHUNK):
        chunks.append(data[i : i + PLAINTEXT_CHUNK])
    return chunks


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

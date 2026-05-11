from __future__ import annotations
import os
from .miller_rabin import is_prime

__all__ = ["generate_prime"]


def generate_prime(bits: int) -> int:
    if bits < 2:
        raise ValueError("bits must be at least 2")

    nbytes = (bits + 7) // 8
    mask = (1 << bits) - 1

    while True:
        candidate = int.from_bytes(os.urandom(nbytes), "big") & mask
        candidate |= (1 << (bits - 1)) | 1
        if is_prime(candidate, 40):
            return candidate

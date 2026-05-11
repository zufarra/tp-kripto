from __future__ import annotations
from .bigint_math import I2OSP
from .sha256 import sha256

__all__ = ["mgf1"]

_HASH_LEN = 32


def mgf1(seed: bytes, length: int) -> bytes:
    if not isinstance(seed, (bytes, bytearray, memoryview)):
        raise TypeError("seed must be a bytes-like object")
    if length < 0:
        raise ValueError("length must be non-negative")
    if length == 0:
        return b""

    seed_bytes = bytes(seed)
    output = bytearray()
    for counter in range((length + _HASH_LEN - 1) // _HASH_LEN):
        output.extend(sha256(seed_bytes + I2OSP(counter, 4)))
    return bytes(output[:length])

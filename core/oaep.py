from __future__ import annotations
import os
from typing import ByteString
from .mgf1 import mgf1
from .sha256 import sha256

__all__ = ["OAEPError", "oaep_encode", "oaep_decode"]

_HASH_LEN = 32


class OAEPError(ValueError):
    """Raised when OAEP padding or unpadding fails."""


def _xor_bytes(left: bytes, right: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(left, right))


def oaep_encode(M: bytes, k: int, label: bytes = b"") -> bytes:
    if not isinstance(M, (bytes, bytearray, memoryview)):
        raise TypeError("M must be a bytes-like object")
    if not isinstance(label, (bytes, bytearray, memoryview)):
        raise TypeError("label must be a bytes-like object")
    if k < 2 * _HASH_LEN + 2:
        raise OAEPError("intended encoded message length too short")

    message = bytes(M)
    label_bytes = bytes(label)
    if len(message) > k - 2 * _HASH_LEN - 2:
        raise OAEPError("message too long")

    l_hash = sha256(label_bytes)
    ps = b"\x00" * (k - len(message) - 2 * _HASH_LEN - 2)
    db = l_hash + ps + b"\x01" + message
    seed = os.urandom(_HASH_LEN)
    db_mask = mgf1(seed, k - _HASH_LEN - 1)
    masked_db = _xor_bytes(db, db_mask)
    seed_mask = mgf1(masked_db, _HASH_LEN)
    masked_seed = _xor_bytes(seed, seed_mask)
    return b"\x00" + masked_seed + masked_db


def oaep_decode(EM: bytes, k: int, label: bytes = b"") -> bytes:
    if not isinstance(EM, (bytes, bytearray, memoryview)):
        raise TypeError("EM must be a bytes-like object")
    if not isinstance(label, (bytes, bytearray, memoryview)):
        raise TypeError("label must be a bytes-like object")
    if k < 2 * _HASH_LEN + 2:
        raise OAEPError("intended encoded message length too short")

    em = bytes(EM)
    label_bytes = bytes(label)
    if len(em) != k:
        raise OAEPError("decryption error")
    if em[0] != 0:
        raise OAEPError("decryption error")

    masked_seed = em[1 : 1 + _HASH_LEN]
    masked_db = em[1 + _HASH_LEN :]
    seed_mask = mgf1(masked_db, _HASH_LEN)
    seed = _xor_bytes(masked_seed, seed_mask)
    db_mask = mgf1(seed, k - _HASH_LEN - 1)
    db = _xor_bytes(masked_db, db_mask)

    l_hash = sha256(label_bytes)
    if db[:_HASH_LEN] != l_hash:
        raise OAEPError("decryption error")

    rest = db[_HASH_LEN:]
    separator_index = rest.find(b"\x01")
    if separator_index == -1:
        raise OAEPError("decryption error")
    if any(byte != 0 for byte in rest[:separator_index]):
        raise OAEPError("decryption error")
    return rest[separator_index + 1 :]

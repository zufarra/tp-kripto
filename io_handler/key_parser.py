# RSA Hex Key Parser

from __future__ import annotations

from typing import Tuple

__all__ = [
    "load_public_key",
    "load_private_key",
    "save_public_key",
    "save_private_key",
]


def load_public_key(filepath: str) -> Tuple[int, int]:
    """Membaca public key dari file heksadesimal."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().splitlines()
    n = None
    e = None
    for line in content:
        line = line.strip()
        if line.startswith("n="):
            n = int(line[2:], 16)
        elif line.startswith("e="):
            e = int(line[2:], 16)
    
    if n is None or e is None:
        raise ValueError(f"Invalid public key format in {filepath}")
    
    return (n, e)


def load_private_key(filepath: str) -> Tuple[int, int]:
    """Membaca private key dari file heksadesimal."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().splitlines()
    n = None
    d = None
    for line in content:
        line = line.strip()
        if line.startswith("n="):
            n = int(line[2:], 16)
        elif line.startswith("d="):
            d = int(line[2:], 16)
            
    if n is None or d is None:
        raise ValueError(f"Invalid private key format in {filepath}")
        
    return (n, d)


def save_public_key(filepath: str, n: int, e: int) -> None:
    """Menyimpan public key ke file dalam format heksadesimal."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"n={hex(n)[2:]}\n")
        f.write(f"e={hex(e)[2:]}\n")


def save_private_key(filepath: str, n: int, d: int) -> None:
    """Menyimpan private key ke file dalam format heksadesimal."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"n={hex(n)[2:]}\n")
        f.write(f"d={hex(d)[2:]}\n")

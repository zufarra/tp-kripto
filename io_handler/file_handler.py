# Binary File IO Handler

from __future__ import annotations

__all__ = ["read_file", "write_file"]


def read_file(filepath: str) -> bytes:
    """Membaca keseluruhan isi file sebagai byte mentah."""
    with open(filepath, "rb") as f:
        return f.read()


def write_file(filepath: str, data: bytes) -> None:
    """Menuliskan data byte ke file (mode overwrite)."""
    with open(filepath, "wb") as f:
        f.write(data)

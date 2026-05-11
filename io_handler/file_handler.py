from __future__ import annotations

__all__ = ["read_file", "write_file"]


def read_file(filepath: str) -> bytes:
    with open(filepath, "rb") as f:
        return f.read()


def write_file(filepath: str, data: bytes) -> None:
    with open(filepath, "wb") as f:
        f.write(data)

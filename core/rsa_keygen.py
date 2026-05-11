"""RSA key pair generation for RSA-OAEP-256."""

from __future__ import annotations

from typing import Tuple

from .bigint_math import gcd, lcm, modinv
from .prime_gen import generate_prime

__all__ = ["generate_keypair"]

_PUBLIC_EXPONENT = 65537


def generate_keypair(bits: int = 2048) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Generate an RSA keypair.

    Returns:
        ((n, e), (n, d))
    """
    if bits < 32:
        raise ValueError("bits must be at least 32")

    p_bits = bits // 2
    q_bits = bits - p_bits

    while True:
        p = generate_prime(p_bits)
        q = generate_prime(q_bits)
        if p == q:
            continue

        n = p * q
        if n.bit_length() != bits:
            continue

        lam = lcm(p - 1, q - 1)
        if gcd(_PUBLIC_EXPONENT, lam) != 1:
            continue

        d = modinv(_PUBLIC_EXPONENT, lam)
        return (n, _PUBLIC_EXPONENT), (n, d)

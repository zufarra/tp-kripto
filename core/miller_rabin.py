"""Miller-Rabin probable prime test."""

from __future__ import annotations

import secrets

from .bigint_math import modexp

__all__ = ["is_prime"]

_SMALL_PRIMES = (
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
)


def is_prime(n: int, k: int = 40) -> bool:
    """Return True if n is probably prime."""
    if n < 2:
        return False
    for prime in _SMALL_PRIMES:
        if n == prime:
            return True
        if n % prime == 0:
            return False

    if n % 2 == 0:
        return False

    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    rounds = max(1, int(k))
    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = modexp(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = modexp(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

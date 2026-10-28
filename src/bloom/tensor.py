"""
Which ring member is signing, writte as  tensor product of small unit vectors.

Paper: Section 4, eq. (28)-(29).
"""
from __future__ import annotations
import numpy as np


def ring_size(d: int, base: int, k: int) -> int:
   """N = d * base^k, the number of public keys in the ring."""
   
   if d < 1 or base < 1 or k < 0:
         raise ValueError(f"need d >= 1, base >= 1, k >= 0, got d={d}, base={base}, k={k}")
   return d * base**k


def index_to_digits(i: int, d: int, base: int, k: int) -> list[int]:
    """i -> [a_1, ..., a_k, a_{k+1}], a_1 most significant.

    a_1..a_k are in [0, base); a_{k+1} is in [0, d).
    Example (d=8, base=2, k=2): 21 -> [1, 0, 5].
    """
    n = ring_size(d, base, k)
    if not 0 <= i < n:
        raise ValueError(f"index {i} is outside the ring [0, {n})")
    last = i % d  # least significant digit, base d
    i //= d
    digits = []
    for _ in range(
        k
    ):  # the remaining k digits, base `base`, collected least significant first
        digits.append(i % base)
        i //= base
    digits.reverse()  # so that a_1 (most significant) comes first
    return digits + [last]


def digits_to_index(digits: list[int], d: int, base: int) -> int:
    """Inverse of index_to_digits."""
    if not digits:
        raise ValueError("need at least one digit")
    *front, last = digits
    i = 0
    for a in front:
        if not 0 <= a < base:
            raise ValueError(f"digit {a} is outside [0, {base})")
        i = i * base + a
    if not 0 <= last < d:
        raise ValueError(f"last digit {last} is outside [0, {d})")
    return i * d + last


def unit_vector(length: int, pos: int) -> np.ndarray:
    """A length-`length` vector with a single 1 at index `pos`."""
    if not 0 <= pos < length:
        raise ValueError(f"position {pos} is outside [0, {length})")
    e = np.zeros(length, dtype=object)
    e[pos] = 1
    return e


def tensor(vectors: list[np.ndarray]) -> np.ndarray:
    """v_1 ⊗ v_2 ⊗ ... ⊗ v_last (Kronecker product).

    a ⊗ b = [a[0]*b, a[1]*b, ..., a[-1]*b] stacked into one long vector. The product is
    associative, so folding left to right gives the same vector as the paper's
    v_1 ⊗ (v_2 ⊗ (... ⊗ v_{k+1})).
    """
    if not vectors:
        raise ValueError("need at least one vector")
    out = np.asarray(vectors[0], dtype=object)
    for v in vectors[1:]:
        out = np.kron(out, np.asarray(v, dtype=object))
    return out


def index_to_unit_vectors(i: int, d: int, base: int, k: int) -> list[np.ndarray]:
    """i -> [v_1, ..., v_k, v_{k+1}]: k unit vectors of length `base`, then one of length d."""
    digits = index_to_digits(i, d, base, k)
    return [unit_vector(base, a) for a in digits[:-1]] + [unit_vector(d, digits[-1])]

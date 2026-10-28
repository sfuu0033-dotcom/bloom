"""Tests for bloom.tensor (Section 4, eq. (28)-(29)).

Toy parameters (d=8, base=2) are small enough to check by hand; the real ones are
d=64, base=8 from Fig. 10.
"""

import random

import numpy as np
import pytest

from bloom.tensor import (
    digits_to_index,
    index_to_digits,
    index_to_unit_vectors,
    ring_size,
    tensor,
    unit_vector,
)

TOY = dict(d=8, base=2)
REAL = dict(d=64, base=8)


def test_ring_size():
    # Fig. 10: N = 64 * 8^k for k = 0, 2, 4, 6
    assert [ring_size(64, 8, k) for k in (0, 2, 4, 6)] == [2**6, 2**12, 2**18, 2**24]
    assert ring_size(8, 2, 2) == 32


def test_worked_example():
    # 21 = (1*2 + 0)*8 + 5
    assert index_to_digits(21, 8, 2, 2) == [1, 0, 5]
    assert digits_to_index([1, 0, 5], 8, 2) == 21


def test_kronecker_definition():
    # [0,1] ⊗ [1,0,0] = [0*[1,0,0], 1*[1,0,0]] = [0,0,0,1,0,0]
    assert list(tensor([np.array([0, 1]), np.array([1, 0, 0])])) == [0, 0, 0, 1, 0, 0]


@pytest.mark.parametrize("k", [0, 1, 2, 3])
def test_roundtrip_every_toy_index(k):
    n = ring_size(k=k, **TOY)
    for i in range(n):
        digits = index_to_digits(i, k=k, **TOY)
        assert len(digits) == k + 1
        assert all(0 <= a < TOY["base"] for a in digits[:-1]) and 0 <= digits[-1] < TOY["d"]
        assert digits_to_index(digits, **TOY) == i


@pytest.mark.parametrize("k", [2, 6])
def test_roundtrip_real_params(k):
    rng = random.Random(k)
    n = ring_size(k=k, **REAL)
    for i in [0, n - 1] + [rng.randrange(n) for _ in range(200)]:
        assert digits_to_index(index_to_digits(i, k=k, **REAL), **REAL) == i


@pytest.mark.parametrize("k", [0, 1, 2, 3])
def test_tensor_of_digits_is_the_unit_vector(k):
    # eq. (29): e_i = v_1 ⊗ ... ⊗ v_{k+1}
    n = ring_size(k=k, **TOY)
    for i in range(n):
        vs = index_to_unit_vectors(i, k=k, **TOY)
        assert [len(v) for v in vs] == [TOY["base"]] * k + [TOY["d"]]
        assert np.array_equal(tensor(vs), unit_vector(n, i))


def test_T_times_tensor_picks_column_i():
    # eq. (28): T e_i is the i-th public key
    rng = random.Random(1)
    q, k = 101, 2
    n = ring_size(k=k, **TOY)
    T = np.array([[rng.randrange(q) for _ in range(n)] for _ in range(TOY["d"])], dtype=object)
    for i in range(n):
        e = tensor(index_to_unit_vectors(i, k=k, **TOY))
        assert np.array_equal(T.dot(e) % q, T[:, i])


def test_real_size_spot_check():
    # N = 4096 users but only 8 + 8 + 64 = 80 numbers to describe the signer
    vs = index_to_unit_vectors(1234, k=2, **REAL)
    assert sum(len(v) for v in vs) == 80
    assert np.array_equal(tensor(vs), unit_vector(4096, 1234))


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        index_to_digits(32, 8, 2, 2)          # N = 32, so 32 is out of range
    with pytest.raises(ValueError):
        index_to_digits(-1, 8, 2, 2)
    with pytest.raises(ValueError):
        digits_to_index([2, 0, 5], 8, 2)      # 2 is not a base-2 digit
    with pytest.raises(ValueError):
        digits_to_index([1, 0, 8], 8, 2)      # last digit must be < d
    with pytest.raises(ValueError):
        unit_vector(4, 4)
    with pytest.raises(ValueError):
        tensor([])

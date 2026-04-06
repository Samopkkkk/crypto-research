"""
Kyber Parameters
CRYSTALS-Kyber parameter sets
"""
from dataclasses import dataclass
from typing import Tuple


@dataclass
class KyberParams:
    """Kyber parameter set"""
    n: int           # Polynomial degree
    k: int           # Number of polynomials
    q: int           # Modulus
    eta: int         # Noise parameter
    du: int          # Public key compression
    dv: int          # Ciphertext compression
    pk_size: int     # Public key size (bytes)
    sk_size: int     # Secret key size (bytes)
    ct_size: int     # Ciphertext size (bytes)


# Kyber parameter sets
KYBER_512 = KyberParams(
    n=256,
    k=2,
    q=3329,
    eta=3,
    du=10,
    dv=4,
    pk_size=800,
    sk_size=1632,
    ct_size=768
)

KYBER_768 = KyberParams(
    n=256,
    k=3,
    q=3329,
    eta=2,
    du=10,
    dv=4,
    pk_size=1184,
    sk_size=2400,
    ct_size=1088
)

KYBER_1024 = KyberParams(
    n=256,
    k=4,
    q=3329,
    eta=2,
    du=11,
    da=5,
    pk_size=1568,
    sk_size=3168,
    ct_size=1568
)


# Useful constants
N = 256
Q = 3329
Q_INV = 3329  # Inverse of q mod 2^16 (not needed for simple impl)


def ntt_size() -> int:
    """Size for NTT"""
    return N


def poly_size() -> int:
    """Polynomial size in bytes"""
    return N * 2  # Each coeff 2 bytes

# Post-Quantum Cryptography - Kyber KEM

A practical implementation of Kyber (CRYSTALS-Kyber) key encapsulation mechanism.

## Project Structure

```
post-quantum/
├── kyber/           # Kyber KEM implementation
│   ├── __init__.py
│   ├── params.py   # Kyber parameters
│   ├── ntt.py      # Number Theoretic Transform
│   ├── polynomial.py # Polynomial operations
│   ├── kem.py      # Key Encapsulation Mechanism
│   └── test.py     # Tests
├── README.md
└── requirements.txt
```

## Quick Start

```python
from kyber import Kyber512

# Generate key pair
pk, sk = Kyber512.keygen()

# Encapsulate
c, ss = Kyber512.encaps(pk)

# Decapsulate
ss_check = Kyber512.decaps(sk, c)

# Verify
assert ss == ss_check
```

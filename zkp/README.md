# Zero-Knowledge Proof Tutorial

A practical introduction to ZK-SNARKs with simple implementations.

## Project Structure

```
zkp/
├── simple_zkp/       # Basic ZK proofs
│   ├── schnorr.py    # Schnorr identification protocol
│   └── pedersen.py   # Pedersen commitments
├── range_proof/      # Range proofs
│   └── bulletproof.py # Simplified Bulletproofs
├── snark_tutorial/   # zk-SNARK concepts
│   └── circuit.py    # Simple arithmetic circuit
└── README.md
```

## Quick Start

```python
from zkp.schnorr import SchnorrVerifier

# Verify a Schnorr proof
verifier = SchnorrVerifier()
is_valid = verifier.verify(proof, public_key, challenge)
print(f"Proof valid: {is_valid}")
```

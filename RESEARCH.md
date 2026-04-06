# Advanced Cryptography Research Survey

## Overview
Survey of cutting-edge cryptography research areas.

## 1. Post-Quantum Cryptography

### 1.1 Lattice-Based Cryptography
**Why Important**: Resistant to quantum computers

| Algorithm | Type | Status |
|-----------|------|--------|
| Kyber | KEM | NIST Standard |
| Dilithium | Signature | NIST Standard |
| Falcon | Signature | NIST Standard |
| NTRU | KEM | NIST Round 4 |

**Research Directions**:
- Implementation optimization
- Side-channel resistance
- Hardware acceleration

### 1.2 Hash-Based Signatures
- **SPHINCS+**: Stateless hash-based signatures
- **XMSS**: Stateful hash-based signatures
- **LMS**: Leighton-Micali signatures

### 1.3 Code-Based Cryptography
- **McEliece**: Classic code-based encryption
- **BIKE**: Lattice-coded KEM
- **HQC**: Hash-based code PKE

## 2. Zero-Knowledge Proofs

### 2.1 zk-SNARKs
**Applications**: Blockchain privacy, scaling

| Scheme | Setup | Trusted? |
|--------|-------|----------|
| Groth16 | Trusted | Yes |
| PLONK | Universal | Yes |
| STARK | Transparent | No |

**Implementations**:
- **circom**: Circuit compiler
- **snarkjs**: JS SNARK library
- **gnark**: Go implementation

### 2.2 zk-STARKs
- **Pros**: No trusted setup, quantum-resistant
- **Cons**: Large proof size, slower verification
- **Tools**: **RISC Zero**, **Polygon Miden**

### 2.3 zkEVM
- **Purpose**: Zero-knowledge Ethereum Virtual Machine
- **Projects**: 
  - Polygon zkEVM
  - zkSync
  - Scroll

### 2.4 Practical Applications
- **DeFi**: Private transactions
- **Identity**: Proof of identity without revealing data
- **Gaming**: Verify game state
- **ML**: Prove inference results

## 3. Homomorphic Encryption

### 3.1 Schemes

| Scheme | Operations | Use Case |
|--------|------------|----------|
| BFV | Integer arithmetic | Encrypted queries |
| CKKS | Approximate arithmetic | ML inference |
| BGV | Integer arithmetic | Secure computing |

### 3.2 Libraries
- **Microsoft SEAL**: BFV, CKKS, BGV
- **PALISADE**: Multiple schemes
- **HEAAN**: Bootstrappable CKKS
- **OpenFHE**: All schemes + FHE

### 3.3 Applications
- **Private ML**: Inference on encrypted data
- **Secure Outsourcing**: Cloud computation
- **Private Queries**: Database searches

## 4. Advanced Encryption

### 4.1 AEAD (Authenticated Encryption)
- **AES-GCM**: Standard
- **ChaCha20-Poly1305**: Alternative
- **GCM-SIV**: Nonce misuse resistant

### 4.2 Format-Preserving Encryption
- **Applications**: Encrypt sensitive data while preserving format
- **Use Cases**: Credit card numbers, SSN

### 4.3 Searchable Encryption
- **Searchable Symmetric Encryption (SSE)**
- **Public-key Encryption with Keyword Search (PEKS)**

## 5. Secure Multi-Party Computation

### 5.1 Techniques
- **Secret Sharing**: Shamir's scheme
- **Garbled Circuits**: Yao's protocol
- **MPC-in-the-Head**: IACR protocols

### 5.2 Frameworks
- **MPyC**: Python MPC
- **SCALE-MAMBA**: Lattice-based MPC
- **EMP-Toolkit**: Efficient MPC

### 5.3 Applications
- **Private Set Intersection**
- **Secure Voting**
- **Private ML Training**

## 6. Research Projects for This Repository

### 6.1 Post-Quantum Crypto
1. **Kyber Implementation**: Educational Kyber implementation
2. **NTRU vs Kyber**: Benchmark and compare
3. **Side-channel demo**: Timing attack demonstration

### 6.2 Zero-Knowledge Proofs
1. **zk-SNARK Tutorial**: Build simple zk-SNARK from scratch
2. **zk-Voting**: Private voting system
3. **zk-ML**: Prove neural network inference

### 6.3 Homomorphic Encryption
1. **CKKS Demo**: Encrypted addition/multiplication
2. **Private Inference**: Run simple model on encrypted data
3. **Performance Benchmark**: Compare libraries

### 6.4 Advanced Projects
1. **MPC Wallet**: Multi-party crypto wallet
2. **Encrypted Database**: Searchable encrypted DB
3. **Privacy Token**: Confidential transactions

## 7. Implementation Roadmap

### Phase 1: Basics
- [ ] Implement Kyber KEM
- [ ] Build simple zk-SNARK circuit
- [ ] Set up CKKS demo

### Phase 2: Intermediate
- [ ] Optimize implementations
- [ ] Add side-channel countermeasures
- [ ] Build MPC protocols

### Phase 3: Advanced
- [ ] zkEVM basics
- [ ] Private ML inference
- [ ] Production-ready libraries

---

*Last Updated: 2026-04-06*

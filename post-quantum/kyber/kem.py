"""
Kyber KEM (Key Encapsulation Mechanism)
CRYSTALS-Kyber implementation
"""
import numpy as np
import hashlib
from typing import Tuple
from params import KyberParams, KYBER_512, KYBER_768, KYBER_1024
from polynomial import Polynomial, PolynomialVector, generate_noise, generate_matrix


class Kyber:
    """
    Kyber KEM
    
    Reference implementation (not optimized for production)
    """
    
    def __init__(self, params: KyberParams):
        self.params = params
        self.k = params.k
    
    @staticmethod
    def keygen() -> Tuple[bytes, bytes]:
        """Generate key pair"""
        raise NotImplementedError("Use Kyber512, Kyber768, or Kyber1024")
    
    @staticmethod
    def encaps(pk: bytes) -> Tuple[bytes, bytes]:
        """Encapsulate (produce ciphertext and shared secret)"""
        raise NotImplementedError("Use Kyber512, Kyber768, or Kyber1024")
    
    @staticmethod
    def decaps(sk: bytes, ct: bytes) -> bytes:
        """Decapsulate (recover shared secret)"""
        raise NotImplementedError("Use Kyber512, Kyber768, or Kyber1024")


class Kyber512(Kyber):
    """
    Kyber-512
    
    Security level: NIST Level 1 (≈ AES-128)
    """
    
    params = KYBER_512
    
    @classmethod
    def keygen(cls) -> Tuple[bytes, bytes]:
        """
        Generate Kyber-512 key pair
        
        Returns:
            (public_key, secret_key)
        """
        k = cls.params.k
        n = cls.params.n
        q = cls.params.q
        eta = cls.params.eta
        
        # Sample rho and sigma from random bytes
        d = np.random.bytes(32)
        seed = hashlib.sha256(d).digest()
        rho = seed[:32]
        sigma = seed[32:]  # Actually use first 32 bytes
        
        # Generate matrix A (k x k)
        A = generate_matrix(rho, k)
        
        # Sample secret vector s
        s = PolynomialVector([
            generate_noise(eta) for _ in range(k)
        ], k)
        
        # Sample error vector e
        e = PolynomialVector([
            generate_noise(eta) for _ in range(k)
        ], k)
        
        # Compute public key: t = A * s + e
        t = PolynomialVector.zero(k)
        for i in range(k):
            for j in range(k):
                t.polys[i] = t.polys[i] + A[i][j] * s.polys[j]
            t.polys[i] = t.polys[i] + e.polys[i]
        
        # Serialize public key: (t, rho)
        pk = t.to_bytes() + rho
        
        # Serialize secret key: (s, t, rho, d)
        # In simplified version, just store s + t + rho
        sk = s.to_bytes() + t.to_bytes() + rho + d
        
        return pk, sk
    
    @classmethod
    def encaps(cls, pk: bytes) -> Tuple[bytes, bytes]:
        """
        Encapsulate
        
        Args:
            pk: Public key
        
        Returns:
            (ciphertext, shared_secret)
        """
        k = cls.params.k
        eta = cls.params.eta
        du = cls.params.du
        dv = cls.params.dv
        
        # Parse public key
        t = PolynomialVector.from_bytes(pk[:k*512], k)
        rho = pk[k*512:]
        
        # Generate matrix A^T
        A = generate_matrix(rho, k)
        
        # Sample r and e1, e2
        d = np.random.bytes(32)
        r = PolynomialVector([
            generate_noise(eta) for _ in range(k)
        ], k)
        
        e1 = PolynomialVector([
            generate_noise(eta) for _ in range(k)
        ], k)
        
        e2 = generate_noise(eta)
        
        # Compute u = A^T * r + e1
        u = PolynomialVector.zero(k)
        for j in range(k):
            for i in range(k):
                u.polys[i] = u.polys[i] + A[i][j] * r.polys[j]
            u.polys[i] = u.polys[i] + e1.polys[i]
        
        # Compute v = t^T * r + e2 + Compress(H(m))
        v = Polynomial.zero()
        for i in range(k):
            v = v + t.polys[i] * r.polys[i]
        v = v + e2
        
        # Compress u and v
        ct_u = u.to_bytes()  # Simplified - no compression
        ct_v = v.to_bytes()
        
        ct = ct_u + ct_v
        
        # Hash to get shared secret
        m = d  # Simplified - should be derived properly
        ss = hashlib.sha256(m + ct).digest()[:32]
        
        return ct, ss
    
    @classmethod
    def decaps(cls, sk: bytes, ct: bytes) -> bytes:
        """
        Decapsulate
        
        Args:
            sk: Secret key
            ct: Ciphertext
        
        Returns:
            shared_secret
        """
        k = cls.params.k
        
        # Parse secret key
        s = PolynomialVector.from_bytes(sk[:k*512], k)
        
        # Parse ciphertext
        u_start = 0
        v_start = k * 512
        
        u = PolynomialVector.from_bytes(ct[u_start:v_start], k)
        v = PolynomialVector.from_bytes(ct[v_start:v_start+512], 1)
        
        # Compute m' = v - s^T * u
        m_prime = Polynomial.zero()
        for i in range(k):
            m_prime = m_prime + s.polys[i] * u.polys[i]
        m_prime = v.polys[0] - m_prime
        
        # Hash to get shared secret
        m_bytes = m_prime.to_bytes()
        ss = hashlib.sha256(m_bytes + ct).digest()[:32]
        
        return ss


class Kyber768(Kyber):
    """Kyber-768 (NIST Level 3)"""
    params = KYBER_768


class Kyber1024(Kyber):
    """Kyber-1024 (NIST Level 5)"""
    params = KYBER_1024


# ============== Demo ==============

def demo():
    """Demonstrate Kyber key encapsulation"""
    print("=" * 60)
    print("Kyber-512 Key Encapsulation Demo")
    print("=" * 60)
    
    # Key generation
    print("\n1. Generating key pair...")
    pk, sk = Kyber512.keygen()
    print(f"   Public key size: {len(pk)} bytes")
    print(f"   Secret key size: {len(sk)} bytes")
    
    # Encapsulation
    print("\n2. Encapsulating...")
    ct, ss = Kyber512.encaps(pk)
    print(f"   Ciphertext size: {len(ct)} bytes")
    print(f"   Shared secret: {ss.hex()[:16]}...")
    
    # Decapsulation
    print("\n3. Decapsulating...")
    ss_check = Kyber512.decaps(sk, ct)
    print(f"   Shared secret: {ss_check.hex()[:16]}...")
    
    # Verify
    print("\n4. Verification...")
    if ss == ss_check:
        print("   ✓ SUCCESS: Shared secrets match!")
    else:
        print("   ✗ FAILED: Shared secrets don't match!")
    
    print("\n" + "=" * 60)
    print("Security Level: NIST Level 1 (≈ AES-128)")
    print("=" * 60)


if __name__ == "__main__":
    demo()

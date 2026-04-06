"""
Schnorr Identification Protocol
A simple zero-knowledge proof of knowledge of a discrete logarithm
"""
import hashlib
import random
from typing import Tuple


class SchnorrParameters:
    """Schnorr protocol parameters"""
    
    def __init__(self, p: int = None, g: int = None):
        # In production, use properly generated prime order groups
        # These are example values for demonstration
        self.p = p or 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.g = g or 2
        
        # Verify g is generator
        # In real implementation, use established groups


class SchnorrProver:
    """
    Schnorr Prover
    
    Proves knowledge of discrete logarithm without revealing it
    """
    
    def __init__(self, params: SchnorrParameters = None):
        self.params = params or SchnorrParameters()
        self.p = self.params.p
        self.g = self.params.g
        
        # Prover's secret key (private)
        self.x = random.randrange(1, self.p - 1)
        
        # Public key
        self.y = pow(self.g, self.x, self.p)
    
    def generate_proof(self, message: str = None) -> Tuple[int, int, int]:
        """
        Generate Schnorr proof
        
        Returns:
            (commitment_r, challenge_c, response_s)
        """
        # 1. Prover chooses random k
        k = random.randrange(1, self.p - 1)
        
        # 2. Compute commitment
        r = pow(self.g, k, self.p)
        
        # 3. Compute challenge
        if message:
            c = int(hashlib.sha256(
                str(r).encode() + message.encode()
            ).hexdigest(), 16) % self.p
        else:
            c = int(hashlib.sha256(str(r).encode()).hexdigest(), 16) % self.p
        
        # 4. Compute response: s = k + c*x (mod p-1)
        s = (k + c * self.x) % (self.p - 1)
        
        return r, c, s
    
    def get_public_key(self) -> int:
        """Get public key"""
        return self.y
    
    def get_secret_key(self) -> int:
        """Get secret key (for testing only!)"""
        return self.x


class SchnorrVerifier:
    """
    Schnorr Verifier
    
    Verifies Schnorr proofs
    """
    
    def __init__(self, params: SchnorrParameters = None):
        self.params = params or SchnorrParameters()
        self.p = self.params.p
        self.g = self.params.g
    
    def verify(self, proof: Tuple[int, int, int], 
               public_key: int, 
               message: str = None) -> bool:
        """
        Verify Schnorr proof
        
        Args:
            proof: (r, c, s)
            public_key: Prover's public key
            message: Optional message being proven
        
        Returns:
            True if proof is valid
        """
        r, c, s = proof
        
        # Verify: g^s = r * y^c (mod p)
        left = pow(self.g, s, self.p)
        right = (r * pow(public_key, c, self.p)) % self.p
        
        if left != right:
            return False
        
        # Verify challenge
        if message:
            expected_c = int(hashlib.sha256(
                str(r).encode() + message.encode()
            ).hexdigest(), 16) % self.p
        else:
            expected_c = int(hashlib.sha256(str(r).encode()).hexdigest(), 16) % self.p
        
        return c == expected_c


def demo():
    """Demonstrate Schnorr protocol"""
    print("=" * 60)
    print("Schnorr Identification Protocol Demo")
    print("=" * 60)
    
    # Setup
    params = SchnorrParameters()
    
    # Prover generates key pair
    print("\n1. Prover generates key pair...")
    prover = SchnorrProver(params)
    pk = prover.get_public_key()
    print(f"   Public key (y): {pk}")
    print(f"   Secret key (x): {prover.get_secret_key()} (keep secret!)")
    
    # Generate proof
    print("\n2. Prover generates proof...")
    message = "Hello,Verifier!"
    proof = prover.generate_proof(message)
    print(f"   Commitment (r): {proof[0]}")
    print(f"   Challenge (c): {proof[1]}")
    print(f"   Response (s): {proof[2]}")
    
    # Verify
    print("\n3. Verifier checks proof...")
    verifier = SchnorrVerifier(params)
    is_valid = verifier.verify(proof, pk, message)
    
    print(f"   Proof valid: {is_valid}")
    
    if is_valid:
        print("\n✓ SUCCESS: Proof verified!")
        print("   The prover proved knowledge of x without revealing it.")
    else:
        print("\n✗ FAILED: Invalid proof!")
    
    print("\n" + "=" * 60)
    print("Security: Based on discrete logarithm hardness")
    print("=" * 60)


if __name__ == "__main__":
    demo()

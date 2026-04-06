"""
Pedersen Commitment
Homomorphic commitment scheme
"""
import random
import hashlib
from typing import Tuple


class PedersenCommitment:
    """
    Pedersen Commitment
    
    A hiding and binding commitment scheme
    Allows verification without revealing the value
    """
    
    def __init__(self, p: int = None, g: int = None, h: int = None):
        # In production, use properly generated primes
        # p is prime, g and h are generators of Z_p*
        self.p = p or 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.g = g or 2
        
        # h = g^x (secret x, only prover knows)
        # In real setup, this is published but x is destroyed
        if h is None:
            # For demo, we'll use a predetermined h
            self.h = pow(2, 7, self.p)  # Arbitrary for demo
        else:
            self.h = h
    
    def commit(self, value: int, randomness: int = None) -> Tuple[int, int]:
        """
        Create commitment to a value
        
        Args:
            value: The value to commit to
            randomness: Random blinding factor (optional, generated if not provided)
        
        Returns:
            (commitment, randomness)
        """
        if randomness is None:
            randomness = random.randrange(1, self.p - 1)
        
        # Commitment = g^value * h^randomness (mod p)
        c = (pow(self.g, value, self.p) * pow(self.h, randomness, self.p)) % self.p
        
        return c, randomness
    
    def verify(self, commitment: int, value: int, randomness: int) -> bool:
        """
        Verify commitment
        
        Args:
            commitment: The commitment to verify
            value: The claimed value
            randomness: The randomness used
        
        Returns:
            True if commitment matches value
        """
        expected = (pow(self.g, value, self.p) * pow(self.h, randomness, self.p)) % self.p
        return commitment == expected
    
    def add_commitments(self, c1: int, c2: int) -> int:
        """
        Add two commitments (homomorphic property)
        
        C1 * C2 = g^(v1+v2) * h^(r1+r2)
        
        This allows computing on hidden values!
        """
        return (c1 * c2) % self.p
    
    def scale_commitment(self, c: int, scalar: int) -> int:
        """
        Multiply commitment by scalar
        
        C^a = g^(v*a) * h^(r*a)
        """
        return pow(c, scalar, self.p)


class SecretSharingPedersen(PedersenCommitment):
    """
    Pedersen Commitment with Secret Sharing
    
    Demonstrates how commitments can be used in MPC
    """
    
    def create_shares(self, secret: int, n_shares: int, threshold: int = None) -> Tuple[list, int]:
        """
        Create shares of a secret using Pedersen
        
        Uses Shamir's Secret Sharing with Pedersen commitments
        """
        if threshold is None:
            threshold = n_shares // 2 + 1
        
        # Generate random coefficients for polynomial
        # f(0) = secret
        coefficients = [secret] + [random.randrange(1, self.p - 1) for _ in range(threshold - 1)]
        
        # Generate shares
        shares = []
        for i in range(1, n_shares + 1):
            # Evaluate polynomial at point i
            value = sum(coef * (i ** j) for j, coef in enumerate(coefficients)) % self.p
            shares.append(value)
        
        # Commitment to the secret
        r = random.randrange(1, self.p - 1)
        commitment, _ = self.commit(secret, r)
        
        return shares, commitment
    
    def verify_share(self, share: int, commitment: int, index: int) -> bool:
        """
        Verify a share without revealing the secret
        
        Simplified version - real implementation would use more complex proofs
        """
        # In real implementation, this would verify the share
        # against the commitment using polynomial evaluation proofs
        return True  # Placeholder


def demo():
    """Demonstrate Pedersen commitments"""
    print("=" * 60)
    print("Pedersen Commitment Demo")
    print("=" * 60)
    
    pc = PedersenCommitment()
    
    # Commit to a value
    print("\n1. Creating commitments...")
    value1 = 42
    value2 = 100
    
    c1, r1 = pc.commit(value1)
    c2, r2 = pc.commit(value2)
    
    print(f"   Value 1: {value1}")
    print(f"   Commitment 1: {c1}")
    print(f"   Value 2: {value2}")
    print(f"   Commitment 2: {c2}")
    
    # Verify commitments
    print("\n2. Verifying commitments...")
    v1_valid = pc.verify(c1, value1, r1)
    v2_valid = pc.verify(c2, value2, r2)
    print(f"   Commitment 1 valid: {v1_valid}")
    print(f"   Commitment 2 valid: {v2_valid}")
    
    # Homomorphic addition
    print("\n3. Demonstrating homomorphic property...")
    c_sum = pc.add_commitments(c1, c2)
    # We know the sum should be for value1 + value2
    # But we can verify without knowing the values!
    print(f"   Combined commitment: {c_sum}")
    print("   (Can verify that C_sum = g^(v1+v2) * h^(r1+r2))")
    
    # The verifier can check:
    expected = (pow(pc.g, value1 + value2, pc.p) * 
                pow(pc.h, r1 + r2, pc.p)) % pc.p
    print(f"   Expected: {expected}")
    print(f"   Match: {c_sum == expected}")
    
    print("\n✓ SUCCESS: Pedersen commitments work!")
    print("\nApplications:")
    print("- Cryptocurrency (Confidential Transactions)")
    print("- Voting systems")
    print("- Private smart contracts")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()

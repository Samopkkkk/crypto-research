"""
Polynomial Operations
Polynomial arithmetic modulo X^N + 1
"""
import numpy as np
from typing import List
from params import N, Q


class Polynomial:
    """
    Polynomial in Z_q[X]/(X^N + 1)
    
    Coefficients are stored as integers in [0, q)
    """
    
    def __init__(self, coeffs: List[int] = None):
        if coeffs is None:
            self.coeffs = [0] * N
        else:
            self.coeffs = coeffs[:N] + [0] * max(0, N - len(coeffs))
    
    @staticmethod
    def random(seed: bytes = None) -> 'Polynomial':
        """Generate random polynomial from seed"""
        import hashlib
        
        if seed is None:
            seed = np.random.bytes(32)
        
        # Simple PRNG using SHAKE
        h = hashlib.shake_256(seed)
        coeffs = []
        while len(coeffs) < N:
            # Generate random bytes and convert to coefficients
            buf = h.read(4)
            val = int.from_bytes(buf, 'little')
            coeffs.append(val % Q)
        
        return Polynomial(coeffs)
    
    @staticmethod
    def zero() -> 'Polynomial':
        """Zero polynomial"""
        return Polynomial([0] * N)
    
    def __add__(self, other: 'Polynomial') -> 'Polynomial':
        """Addition"""
        return Polynomial([
            (a + b) % Q for a, b in zip(self.coeffs, other.coeffs)
        ])
    
    def __sub__(self, other: 'Polynomial') -> 'Polynomial':
        """Subtraction"""
        return Polynomial([
            (a - b) % Q for a, b in zip(self.coeffs, other.coeffs)
        ])
    
    def __neg__(self) -> 'Polynomial':
        """Negation"""
        return Polynomial([(-a) % Q for a in self.coeffs])
    
    def __mul__(self, other: 'Polynomial') -> 'Polynomial':
        """Multiplication (schoolbook - not optimized)"""
        # Convolution modulo X^N + 1
        result = [0] * (2 * N)
        
        for i in range(N):
            for j in range(N):
                result[i + j] += self.coeffs[i] * other.coeffs[j]
        
        # Reduce modulo X^N + 1
        # X^N = -1, so X^(N+i) = -X^i
        for i in range(N, 2 * N):
            result[i - N] = (result[i - N] - result[i]) % Q
        
        return Polynomial(result[:N])
    
    def multiply_ntt(self, other: 'Polynomial') -> 'Polynomial':
        """Multiplication using NTT (placeholder)"""
        # Full NTT implementation would go here
        return self * other
    
    def compress(self, d: int) -> bytes:
        """
        Compress polynomial to d bits per coefficient
        
        Simplified version
        """
        # This is a simplified compression
        # Real implementation uses more sophisticated methods
        data = bytearray()
        for c in self.coeffs:
            # Compress to d bits
            c_compressed = (c * (2**d) + Q // 2) // Q
            c_compressed = c_compressed % (2**d)
            data.extend(c_compressed.to_bytes(d // 8, 'little'))
        return bytes(data)
    
    def decompress(self, d: int, data: bytes) -> 'Polynomial':
        """Decompress polynomial from d bits"""
        coeffs = []
        bytes_per_coeff = d // 8
        
        for i in range(N):
            c_compressed = int.from_bytes(
                data[i*bytes_per_coeff:(i+1)*bytes_per_coeff], 
                'little'
            )
            c = (c_compressed * Q + (1 << (d - 1))) >> d
            coeffs.append(c % Q)
        
        return Polynomial(coeffs)
    
    def to_bytes(self) -> bytes:
        """Convert to bytes (little-endian, 2 bytes per coeff)"""
        data = bytearray()
        for c in self.coeffs:
            data.extend(c.to_bytes(2, 'little'))
        return bytes(data)
    
    @staticmethod
    def from_bytes(data: bytes) -> 'Polynomial':
        """Convert from bytes"""
        coeffs = []
        for i in range(N):
            c = int.from_bytes(data[2*i:2*i+2], 'little')
            coeffs.append(c)
        return Polynomial(coeffs)
    
    def barrett_reduce(self) -> 'Polynomial':
        """Barrett reduction (placeholder)"""
        # Real implementation would use Barrett reduction
        return Polynomial([c % Q for c in self.coeffs])
    
    def centered_reduce(self) -> 'Polynomial':
        """Centered reduction to [-q/2, q/2)"""
        return Polynomial([
            c if c <= Q // 2 else c - Q 
            for c in self.coeffs
        ])


class PolynomialVector:
    """
    Vector of polynomials
    """
    
    def __init__(self, polys: List[Polynomial] = None, k: int = 1):
        self.k = k
        if polys is None:
            self.polys = [Polynomial() for _ in range(k)]
        else:
            self.polys = polys
    
    def __add__(self, other: 'PolynomialVector') -> 'PolynomialVector':
        return PolynomialVector([
            a + b for a, b in zip(self.polys, other.polys)
        ])
    
    def __sub__(self, other: 'PolynomialVector') -> 'PolynomialVector':
        return PolynomialVector([
            a - b for a, b in zip(self.polys, other.polys)
        ])
    
    def __mul__(self, scalar: int) -> 'PolynomialVector':
        return PolynomialVector([
            p * Polynomial([scalar] + [0] * (N-1)) for p in self.polys
        ])
    
    def __rmul__(self, scalar: int) -> 'PolynomialVector':
        return self * scalar
    
    def to_bytes(self) -> bytes:
        """Serialize to bytes"""
        return b''.join(p.to_bytes() for p in self.polys)
    
    @staticmethod
    def from_bytes(data: bytes, k: int) -> 'PolynomialVector':
        """Deserialize from bytes"""
        poly_size = 2 * N
        polys = []
        for i in range(k):
            poly_data = data[i*poly_size:(i+1)*poly_size]
            polys.append(Polynomial.from_bytes(poly_data))
        return PolynomialVector(polys, k)


# ============== Utility Functions ==============

def generate_noise(eta: int, seed: bytes = None) -> Polynomial:
    """Generate noise polynomial (Bennett distribution)"""
    import hashlib
    
    if seed is None:
        seed = np.random.bytes(32)
    
    # Use SHAKE for cryptographic randomness
    h = hashlib.shake_256(seed)
    coeffs = []
    
    while len(coeffs) < N:
        # Generate random bytes
        buf = h.read(eta * 2)
        
        # Convert to signed coefficients
        for i in range(0, len(buf), 2):
            if len(coeffs) >= N:
                break
            d = int.from_bytes(buf[i:i+2], 'little')
            # Centered binomial distribution approximation
            x = (d & ((1 << eta) - 1)) - eta // 2
            coeffs.append(x % Q)
    
    return Polynomial(coeffs)


def generate_matrix(seed: bytes, k: int) -> List[List[Polynomial]]:
    """Generate matrix A from seed (CBA2 construction)"""
    import hashlib
    
    A = [[Polynomial() for _ in range(k)] for _ in range(k)]
    
    # Use SHAKE to derive matrix elements
    h = hashlib.shake_256(seed)
    
    for i in range(k):
        for j in range(k):
            # Generate polynomial from seed
            poly_seed = h.read(32)
            A[i][j] = Polynomial.random(poly_seed)
    
    return A


if __name__ == "__main__":
    # Test
    p1 = Polynomial.random()
    p2 = Polynomial.random()
    
    p3 = p1 + p2
    p4 = p1 * p2
    
    print(f"Polynomial test: {len(p3.coeffs)} coeffs")
    print(f"Multiplication test: {len(p4.coeffs)} coeffs")

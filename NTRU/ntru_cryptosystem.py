
###########################################################
# NTRU Cryptosytem                                                                            
###########################################################     

# Public parameters:
# (N, p, q, d)
# N and p -> prime
# gcd(p, q) = gcd(N,q) = 1
# q > (6d + 1)p

# Private keys:     . f in T(d + 1, d) invertible in R_q and R_p
#                   . g in T(d, d)
#
# Public key:       . h = (F_q = inverse of f in R_q) * g

import convolutional_ring_arithmetic as conv
import ntru_aux
from random import randint

class ntru:

    def __init__(self, N, p, q, d, f = None, F_p = None, g = None, h = None):
        self.N = N
        self.p = p
        self.q = q
        self.d = d
        self.f = f
        self.F_p = F_p
        self.g = g
        self.h = h

    # Generate private keys
    def random_keys(self):
        N = self.N
        p = self.p
        q = self.q
        d = self.d

        # Private keys
        g = ntru_aux.ternary(d, d, N)
        
        # Find f in T(d +  1, d) invertible in R_p and R_q
        while 1:
            f = ntru_aux.ternary(d +  1, d, N)
            F_p = conv.euclidean_poly_inverse(f, p, N)
            
            if isinstance(F_p, list):
                F_q = conv.euclidean_poly_inverse(f, q, N)
                if isinstance(F_q, list):
                    break
        
        # Public key
        h = conv.product_in_R_q(F_q, g, q, N, 0)
        return (f, g, h)

    # Encrypt message in R_p with public key h
    def encrypt(self, m, h):
        
        # Random r in T(d, d)
        r = ntru_aux.ternary(self.d, self.d, self.N)

        # Encryption 
        c = conv.product_in_R_q([self.p] +  [0 for i in range(self.N - 1)], r, self.q, self.N, 1)
        c = conv.product_in_R_q(c, h, self.q, self.N, 0)
        c = conv.addition_in_R_q(c, ntru_aux.center_lift(m, self.p), self.q, self.N)
        c = ntru_aux.fill_zeros(c, self.N - len(c))

        return c

    # Decrypt cipher in R_p with private keys f and g
    def decrypt(self, c, f):

        # Inverse of f in R_p
        F_p = conv.euclidean_poly_inverse(f, self.p, self.N)
        
        m = conv.product_in_R_q(f, c, self.q, self.N, 0)
        m = ntru_aux.center_lift(m, self.q)
        m = [i % self.p for i in m]
        m = conv.product_in_R_q(F_p, m, self.p, self.N, 0)
        m = ntru_aux.center_lift(m, self.p)
        m = [i % self.p for i in m]

        return m
        

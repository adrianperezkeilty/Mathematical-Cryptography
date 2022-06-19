
############################################################
# Primality Tests
############################################################

import random
import math

# Miller-Rabin primality test
# n -> integer to test
# w -> witness
class mr:

    def __init__(self, n):
        self.n = n
        self.w = None

    # t -> number of tries
    def witness(self, t):
        n = self.n
        
        # Write n-1 = 2^k*q
        k = 1
        
        while (n-1)%2**k==0: k += 1
        k = k - 1
        q = (n - 1) // 2**k
        L = []
        
        while len(L) < t and self.w is None:
            a = random.randint(1, n-1)
            if a not in L:
                L.append(a)
                
                if math.gcd(a,n)!=1: self.w = a
                elif a**q%n!=1 and n-1 not in [a**(2**i*q) % n for i in range(k)]: self.w = a

        return self.w


# Primes in [a,b] according to mr test with k tries
def primes(a,b,k):
    L=[]
    for i in range(a,b+1):
        if mr(i).witness(k) is None:
            L.append(i)
    return L


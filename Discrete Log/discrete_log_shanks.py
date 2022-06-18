
##################################################
# DLP solving algorithms
##################################################

import math
import random
import string
import finite_field_arithmetic

# Shank's babystep-giantstep algorithm

# Solve a^x = b (mod n) where <a> = Z_n*
def shanks(a, b, n):
    
    m = math.ceil(math.sqrt(n))
    Z = finite_field_arithmetic.Z_p_star(n)
    a_inv = Z.inverse(a)
    u = Z.fast_powering_algorithm(a_inv, m)
    match = 0
    B,G = [],[]
    k1 = k2 = 1 

    while not match:
        k1 = (k1 * a) % n
        k2 = (k2 * u) % n
        B.append(k1)
        G.append((b * k2) % n)
        
        if set(B) & set(G):
            match = list(set(B)&set(G))[0]

    return B.index(match)+1+(G.index(match)+1)*m

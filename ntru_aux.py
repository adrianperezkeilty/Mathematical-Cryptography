###########################
# NTRU auxiliary functions
###########################

from random import randint

# Obtain gcd(a, b) and ua +  vb = gcd(a, b)
def extended_euclidean_efficient(a, b):
    (u, g, x, y) = (1, a, 0, b)
    
    while y:
        (q, t) = (int(g/y), g % y)
        s = u - q*x
        (u, g) = (x, y)
        (x, y) = (s, t)
    v = int((g - a*u)/b)
    
    return g, u, v

# Return random valid ternary polynomial
def ternary(d1, d2, N):
    n = N
    (L, aux) = ([0 for i in range(N)], [i for i in range(N)])
    (D1, D2) = ([], [])
    
    for i in range(d1):
        j = randint(0, n - 1)
        D1.append(aux[j])
        aux.remove(aux[j])
        n = n - 1
        
    for i in range(d2):
        j = randint(0, n - 1)
        D2.append(aux[j])
        aux.remove(aux[j])
        n = n - 1
        
    for i in D1: L[i] = 1
    for i in D2: L[i] =  - 1

    return L

def center_lift(m, q):
    a = m.copy()
    
    for i in range(len(a)):
        if a[i] > int(q/2):
            a[i] = a[i] - q

    return a
            

def fill_zeros(a, n):
    return a +  [0 for i in range(n)]


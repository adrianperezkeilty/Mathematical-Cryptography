###########################################################
# Auxiliary functions for ECC                             
###########################################################

import math
from finite_field_arithmetic import field
import matplotlib.pyplot as plt

# Encoding of integer onto elliptic curve over F_p
# p             -> Prime
# n             -> Integer
# ec = (a,b)    -> Elliptic curve parameters
# K             -> Error tolerance
# Decrypt by computing x // K
def ec_koblitz_encode(p, n, ec, K):
    (a, b) = ec

    for j in range(K):
        x = (K * n +  j) % p
        z = (x**3 +  a * x +  b) % p
        y = (z**((p + 1) // 4)) % p
        if (y**2) % p == z:
            break
        
    return [x, y]

# Addition in E(F_p)
def ec_add(p, ec, P, Q):
    (a, b) = ec
    
    if P == 'O': return Q
    elif Q == 'O': return P
    
    ((x1, y1), (x2, y2)) = (P, Q)
    if x1 == x2 and y1 ==  - y2: return 'O'
    
    elif P == Q:
        d = math.gcd(2*y1, p)
        mu = ((3 * x1**2 +  a) * field(p).inverse(2 * y1)) % p
        
    else:
        d = math.gcd(x2 - x1, p)
        mu = ((y2 - y1) * field(p).inverse(x2 - x1)) % p
            
    x3 = (mu ** 2 - x1 - x2) % p
    y3 = (mu * (x1 - x3) - y1) % p
    if y3 >= (p +  1) // 2: y3 = y3 - p
    
    return [x3, y3]

# Double and add algorithm
def ec_double_and_add(p, ec, P, n):
    (Q, R) = (P, 'O')
    
    while n > 0:
        
        if n % 2: R = ec_add(p, ec, R, Q)
        Q = ec_add(p, ec, Q, Q)
        n = n // 2
        
    return R

# Return list of points of ec over F_p
def ec_points_over_F_p(p, ec, only_first):
    (a, b) = ec
    
    if p % 4!= 3: raise Exception(p, ' is not equal to 3 (mod 4)')
    L = []
    for x in range(p):
        z = (x**3 +  a*x +  b) % p
        y = field(p).fast_powering_algorithm(z, (p +  1) // 4)
        
        if (y**2) % p == z:
            if y >= int((p +  1)/2):
                y = y - p
            if only_first:
                return [x, y]
            L.append([x, y])
            
    return L

# Check if P is on ec
def ec_point_check(p, ec, P):
    (a, b) = ec
    x, y = P[0], P[1]
    
    if y ** 2 != x**3 +  a*x +  b:
        return 0
    else:
        L = [i for i in range(p)]
        if len(set(L) & {x, y}) != 2:
            if x != y or (x not in L): return 0
        else:
            return 1

# Plot ec
def ec_plot_elliptic(ec):
    (a, b) = ec
    
    y,  x  =  np.ogrid[ -5:5:100j, -5:5:100j]
    plt.contour(x.ravel(),y.ravel(), y**2 - x**3 - a*x - b, [0])
    plt.grid()
    plt.show()

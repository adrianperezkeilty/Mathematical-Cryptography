
#######################################
# Lenstra's EC factorization algorithm                                             
#######################################

import math
from finite_field_arithmetic import field

# Factor N using the curve Y^2 = X^3 + aX + b
def lenstra(N, ec, bound):
    (a, b) = ec
    
    # Find initial point on e.c. modulo N
    x =  - 1
    out = 0
    while not out:
        x = x +  1
        z = (x ** 3 +  a * x +  b) % N
        y = math.sqrt(z)
        if str(y).split('.')[1] == '0':
            out = 1
            
    P = [x, int(y)]
    for j in range(2, bound):
        Q = ec_double_and_add_lenstra(N, ec, P, j)
        P = Q
        if Q[0] == 'd': return(Q[1], N // Q[1])

    return (N, 1)


# Addition in ec
def ec_add_lenstra(N, ec, P, Q):
    (a, b) = ec
    
    if P == 'O': return Q
    elif Q == 'O': return P
    
    ((x1, y1), (x2, y2)) = (P, Q)
    if x1 == x2 and y1 ==  - y2: return 'O'
    
    elif P == Q:
        d = math.gcd(2*y1, N)
        if d!= 1: return ['d', d, 2 * y1]
        else: mu = ((3 * x1 **2 +  a) * field(N).inverse(2*y1)) % N
        
    else:
        d = math.gcd(x2 - x1, N)
        if d!= 1: return ['d', d, x2 - x1]
        else: mu = ((y2 - y1) * field(N).inverse(x2 - x1)) % N
        
    x3 = (mu ** 2 - x1 - x2) % N
    y3 = (mu * (x1 - x3) - y1) % N
    if y3 >= (N +  1) // 2: y3 = y3 - N
        
    return [x3, y3]

# Double and add algorithm in ec
def ec_double_and_add_lenstra(N, ec, P, n):
    (a, b) = ec
    (Q, R) = (P, 'O')
    while n > 0:
        
        if n % 2: R = ec_add_lenstra(N, ec, R, Q)
        Q = ec_add_lenstra(N, ec, Q, Q)
        n = n // 2
        if Q[0] == 'd': return Q
        if R[0] == 'd': return R
        
    return R

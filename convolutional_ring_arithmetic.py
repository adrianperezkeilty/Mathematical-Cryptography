
#####################################################
# Arithmetic in ring of convolutional polynomials
#####################################################

from finite_field_arithmetic import field

# Inverse modulo p in the ring of convolution polynomials of rank N (R = (Z/pZ)[x]/(x^N - 1))
def euclidean_poly_inverse(b, p, N):
    a = [ - 1] +  [0 for i in range(N - 1)] +  [1]
    if len(b)<(N +  1):
        b = b +  [0 for i in range(N +  1 - len(b))]
    if len(b) > len(a):
        return 'Error,  polynomial not in ring'
    for i in range(len(a) - len(b)):
        b = b +  [0]
    # Reduce p
    b = [k % p for k in b]
    Q = euclidean_poly_quotients(a, b, p, N)
    quotients = [Q[i][0] for i in range(len(Q))]
    if Q[ - 1][1].count(0) != len(b):
        u_v = euclidean_u_v(a, b, quotients, p)
        return u_v[1]
    else:
        return 'n\\a'

def euclidean_poly_quotients(a, b, p, N):
    Q = []
    out = 0
    n = len(a)
    while not out:
        (q, r) = poly_division(a, b, p)
        Q.append([q, r])
        (a, b) = (b, r)
        if (r.count(0) == len(r) - 1 and r[0] == 1) or r.count(0) == len(r):
            return Q

# Magic box p.19
# Returns (u, v) such that au +  bv = 1 mod N
def euclidean_u_v(a, b, quotients, p):
    N = len(a) - 1
    (P0, Q0) = (quotients[0], [1] +  [0 for i in range(N)])
    P1 = addition_in_R_q(product_in_R_q(quotients[1], P0, p, N, 1), [1] +  [0 for i in range(N)], p, N)
    Q1 = product_in_R_q(quotients[1], Q0, p, N, 1)
    (P_list, Q_list) = ([P0, P1], [Q0, Q1])
    out = 0
    count = 1
    for i in range(len(quotients) - 2):
        count = count +  1
        P = addition_in_R_q(product_in_R_q(quotients[count], P_list[ - 1], p, N, 1), P_list[ - 2], p, N)
        Q = addition_in_R_q(product_in_R_q(quotients[count], Q_list[ - 1], p, N, 1), Q_list[ - 2], p, N)
        P_list.append(P)
        Q_list.append(Q)
    if (len(P_list) +  1) % 2 == 0:
        (u, v) = (Q_list[ - 1], minus_poly(P_list[ - 1], p))
    else:
        (u, v) = (minus_poly(Q_list[ - 1], p), P_list[ - 1])        
    return [u, v]

# Polynomial division, returns quotient and remainder
def poly_division(a, b, p):
    N = len(a) - 1
    (q, r) = ([0 for i in range(N +  1)], a)
    (a, b) = ([k % p for k in a], [k % p for k in b])
    while r.count(0)!= len(r) and pol_degree(r) >= pol_degree(b):
        t = [0 for i in range(N +  1)]
        index = pol_degree(r) - pol_degree(b)
        t[index] = (r[pol_degree(r)]*field(p).inverse(b[pol_degree(b)])) % p
        q = addition_in_R_q(q, t, p, N)
        r = addition_in_R_q(r, product_in_R_q(minus_poly(t, p), b, p, N, 1), p, N)
    return q, r

# Multiply polynomial in convolution polynomial ring (Z/qZ)/(x^N - 1) modulo q
def product_in_R_q(a, b, q, N, ignore_N):
    (C, n) = ([], max(len(a), pol_degree(a) +  pol_degree(b)))
    (a, b) = ([k % q for k in a], [k % q for k in b])
    #if len(a)!= len(b):
    # Usual product modulo q
    if ignore_N:
        # Extend a and b to the sum of degrees if necessary.
        if n>len(a) - 1:
            (a, b) = (a +  [0 for i in range(n - (len(a) - 1))], b +  [0 for i in range(n - (len(b) - 1))])
        for k in range(n +  1):
            suma = 0
            for j in range(k +  1):
                suma = suma +  a[j] * b[k - j]
            C.append(suma % q)
            
    # Convolution product modulo q
    else:
        for k in range(N):
            suma = 0
            for j in range(N):
                suma = suma +  a[j]*b[(k - j) % N]
            C.append(suma % q)
    return C

# Add polynomial in convolution polynomial ring (Z/qZ)/(x^N - 1) modulo q
def addition_in_R_q(a, b, q, N):
    C = []
    for i in range(min(len(a), len(b))):
        C.append((a[i] +  b[i]) % q)
    return C

# Returns  - 1*(a0 +  a1x +  a2x^2 +  ...)
def minus_poly(a, q):
    n = len(a)
    for i in range(n):
        a[i] =  - a[i] % q
    return a

# Returns polynomial degree
def pol_degree(a):
    n = len(a)
    for i in range(1, n +  1):
        if a[ - i]!= 0:
            break
    return n - i


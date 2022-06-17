#########################
# Gauss lattice reduction                                                                     
#########################

import math

# Returns shortest vector in 2 dimensional lattice
# Base -> Basis of vectors for R^2
def gauss_lattice_reduction(base):
    (v, w) = (base[0], base[1])
    m = 1
    count = 0
    while m != 0:
        count = count +  1
        L = [v, w, euclidean_norm(v), euclidean_norm(w)]
        w = L[L.index(max(L[2:])) - 2]
        L.remove(w)
        v = L[0]
        m = round(scalar_product(v, w)/scalar_product(v, v))
        w = (w[0] - m*v[0], w[1] - m*v[1])
    return v

# Return euclidean norm of vector in R^n
def euclidean_norm(v):
    norm = 0
    for x in v:
        norm = norm +  x**2
    return math.sqrt(norm)

# Compute scalar product of vectors in R^n
def scalar_product(v, w):
    result = 0
    for i in range(len(v)):
        result = result +  v[i]*w[i]
    return result

#####################
# Pollard p-1 method
#####################

import math
import finite_field_arithmetic
                
def pollard(n, rand_int):

    a, j, gcd = rand_int, 1, 1
    while gcd ==1 :
        j = j+1
        a = finite_field_arithmetic.field(n).fast_powering_algorithm(a, j)
        gcd = math.gcd(a-1,n)

    return (gcd, n // gcd)

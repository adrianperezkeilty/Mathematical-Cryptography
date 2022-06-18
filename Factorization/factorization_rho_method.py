#####################
# Pollard rho method
#####################

import math

def rho(n,x0):
    gcd = 1
    (x1,x2)=((x0**2+1)%n,(((x0**2+1)%n)**2+1)%n)
    cont = 0
    
    while gcd==1:
        cont = cont+1
        (x1,x2)=((x1**2+1)%n,(((x2**2+1)%n)**2+1)%n)
        gcd = math.gcd(x1-x2,n)

    return (gcd, n // gcd)

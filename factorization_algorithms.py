
############################################################
# Factorization algorithms
############################################################

import math
import random
import string
import finite_field_arithmetic

                

# Pollard p-1 method
############################################################

def pollard(n,rand_int):

    a, j, gcd = rand_int, 1, 1
    while gcd ==1 :
        j = j+1
        a = finite_field_arithmetic.Z_p_star(n).fast_powering_algorithm(a, j)
        gcd = math.gcd(a-1,n)

    return (gcd, n // gcd)

# Pollard rho method
############################################################

def rho(n,x0):
    gcd = 1
    (x1,x2)=((x0**2+1)%n,(((x0**2+1)%n)**2+1)%n)
    cont = 0
    
    while gcd==1:
        cont = cont+1
        (x1,x2)=((x1**2+1)%n,(((x2**2+1)%n)**2+1)%n)
        gcd = math.gcd(x1-x2,n)

    return (gcd, n // gcd)

# Quadratic sieve
# Return system of congruence equations
# for manual resolution.
# Pending on automatization.
############################################################

def quadratic_sieve(n,length_sieve):

    a = math.floor(math.sqrt(n))+1
    
    # Recommended upper bound 
    B = int(math.exp(math.sqrt(math.log(n)*math.log(math.log(n)))))
    
    # Factor base: list of primes smaller than or equal to B
    P = erastosthenes(B)
    
    # We want to find numbers a and b such that a^2 = b^2 mod n
    # List A stores the potential values for a and B their small factors
    (A,B_smooth)=([t for t in range(a,a+length_sieve)],[[] for t in range(a,a+length_sieve)])
    
    # List of numbers for sieving using polynomial F(t)=t^2-n and list with corresponding found factors
    L=[t**2-n for t in range(a,a+length_sieve)]
    print('Initial list:')
    print(L)
    print(' ')
    
    # Sieving process
    i=-1
    finished_1 = 0
    while i<len(P)-1:
        finished_2 = 0
        
        # Increase to next prime
        i = i+1
        p = P[i]
        exp = 0
        while not finished_2:
            
            # Increase prime exponent
            exp += 1
            
            # Determine if t^2 = n mod (p^n) has solutions or not
            p_exp = p**exp
            (t,sol_found)=(0,0)
            while (not sol_found) and (t<a+length_sieve): #and (p_exp-t<a+length_sieve): #t<p_exp:
                t += 1
                if t**2%p_exp==(n%p_exp):
                    sol_found = 1
                    
            # Sieve only if solutions have been found
            if sol_found:
                sols=[t,p_exp-t]
                
                # In case p = 2,exp = 1 there is only one solution (1=-1 mod 2)
                if sols.count(t)==2:
                    sols.remove(sols[1])
                    
                # Sieve away a factor of p at every pth entry starting from sols[0] and sols[1]
                L_indexes=[]
                for s in sols:
                    (t,L_index,out)=(a-1,-1,0)
                    
                    # Find corresponding indexes mod p_exp and sieve 
                    while not out and t<a+length_sieve:
                        (t,L_index)=(t+1,L_index+1)
                        if t%p_exp==s:
                            L_indexes.append(L_index)
                            out = 1
                            
                            # We keep a look out for the separation
                            # of indexes modulo each solution so that there are no overlaps in the sieving (e.g, p^2 = 4)
                            if len(L_indexes)==1 or (len(L_indexes)==2 and ((L_indexes[0]-L_indexes[1])%p_exp!=0)):
                                for k in range(L_index,length_sieve,p_exp):
                                    L[k]=int(L[k]/p)
                                    B_smooth[k].append(p)
                                    
                # If no solutions found then continue to the next prime in the factor base
            else:
                finished_2 = 1
                
    print('List after sieving:')
    print(L)
    print(' ')
    print('Integers with prime factors smaller than or equal to',B,':')
    cont = 0
    for t in range(len(L)):
        if L[t]==1:
            cont = cont+1
            print(str(cont).rjust(5),str(A[t])+'^2 ='+str(B_smooth[t]).ljust(30)+' mod',n)

# Return factor base based on Erastosthenes' sieve
def erastosthenes(B):
    (L,i)=([k for k in range(2,B+1)],-1)
    for k in L:
        for j in L[k:]:
            if j%k==0 and j!=k:
                L.remove(j)
    return(L)

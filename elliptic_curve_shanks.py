
#######################################################
# Shanks algorithm for solving ECDLP (Q = nP in E(F_p))
#######################################################

from elliptic_curve_aux import ec_add, ec_double_and_add
from random import randint

def ec_shanks(p, ec, P, Q):

    L_j = [i for i in range(1, p)]
    L_k = [i for i in range(1, p)]
    (L1, L2, L3, L4) = ([], [], [], [])
    match = 0

    while not match:
        
        (j, k) = (L_j[randint(0, len(L_j))], L_k[randint(0, len(L_k))])
        L_j.remove(j)
        L_k.remove(k)
        L1_point = ec_double_and_add(p, ec, P, j)
        L2_point = ec_add(p, ec, ec_double_and_add(p, ec, P, k), Q)
        L1.append(L1_point)
        L2.append(L2_point)
        L3.append(j)
        L4.append(k)

        if L1_point in L2: match = L1_point
        if L2_point in L1: match = L2_point

    (j, k) = (L3[L1.index(match)], L4[L2.index(match)])
    
    return (j - k)

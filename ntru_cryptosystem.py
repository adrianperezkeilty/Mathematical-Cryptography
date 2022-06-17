
# PENDING ON SCALABILITY  !

# At the moment:
# NTRU encrypt and decrypt operations
# Creates random valid polynomials and a random message to encrypt and decrypt

## Execution example:

##>>> ntru_cryptosystem.NTRU(13,5,73,2)
##------------------------------------------------------------------------------------------
##PARAMETERS:                              (N, p, q, d) = (13, 5, 73, 2)
##------------------------------------------------------------------------------------------
##f(x) in T(3, 2):                         [1, 1, 1, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0]
##g(x) in T(2, 2):                         [0, 0, -1, 1, 0, 0, 1, -1, 0, 0, 0, 0, 0]
##F_73(x) = f^( - 1)(x) in R_73:           [0, 0, 0, 72, 1, 0, 0, 1, 72, 0, 0, 0, 1, 0]
##F_5(x) = f^( - 1)(x) in R_5:             [0, 0, 0, 4, 1, 0, 0, 1, 4, 0, 0, 0, 1, 0]
##------------------------------------------------------------------------------------------
##PUBLIC KEY: h(x) = F_73(x)*g(x)          [1, 70, 2, 0, 0, 2, 70, 1, 0, 71, 4, 71, 0]
##------------------------------------------------------------------------------------------
##Message m:                               [0, 1, 2, 2, -1, -1, 1, 0, -2, -1, -1, 2, 1]
##Random r(x) in T(2, 2):                  [-1, 1, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0]
##------------------------------------------------------------------------------------------
##ENCRYPTION -------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------
##e(x) = 5r(x)                             [68, 5, 0, 0, 0, 68, 0, 0, 0, 0, 5, 0, 0, 0]
##e(x) = 5r(x)*h(x)                        [68, 30, 38, 5, 5, 58, 30, 63, 68, 10, 38, 30, 68]
##e(x) = 5r(x)*h(x) +  m                   [68, 31, 40, 7, 4, 57, 31, 63, 66, 9, 37, 32, 69]
##------------------------------------------------------------------------------------------
##DECRYPTION -------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------
##a(x) = f(x)*e(x):                        [8, 1, 10, 3, 5, 72, 64, 14, 61, 67, 65, 67, 4]
##Center lift a(x)(mod 73) :               [8, 1, 10, 3, 5, -1, -9, 14, -12, -6, -8, -6, 4]
##Reduce a(x) (mod 5):                     [3, 1, 0, 3, 0, 4, 1, 4, 3, 4, 2, 4, 4]
##F_5(x)*a(x):                             [0, 1, 2, 2, 4, 4, 1, 0, 3, 4, 4, 2, 1]
##------------------------------------------------------------------------------------------
##DECRYPTED MESSAGE ------------------------------------------------------------------------
##------------------------------------------------------------------------------------------
##Center lift F_5(x)*a(x) (mod 5):         [0, 1, 2, 2, -1, -1, 1, 0, -2, -1, -1, 2, 1]
##>>> 

###########################################################
# NTRU Cryptosytem                                                                            
###########################################################     

import convolutional_ring_arithmetic as conv
import ntru_aux
from random import randint

def NTRU(N, p, q, d):
    out = 0
    tries = 0

    # Find f in T(d +  1, d) invertible in R_p and R_q
    while not out:
        tries = tries +  1
        f = ntru_aux.ternary(d +  1, d, N)
        F_p = conv.euclidean_poly_inverse(f, p, N)
        if isinstance(F_p, list):
            F_q = conv.euclidean_poly_inverse(f, q, N)
            if isinstance(F_q, list):
                break

    print(''.ljust(90, '-'))
    print('PARAMETERS:'.ljust(40, ' ') +  ' (N, p, q, d) = ' +  str((N, p, q, d)))
    print(''.ljust(90, '-'))
    print(('f(x) in T(' +  str(d +  1) +  ', ' +  str(d) +  '):').ljust(40, ' '), f)
    g = ntru_aux.ternary(d, d, N)
    print(('g(x) in T(' +  str(d) +  ', ' +  str(d) +  '):').ljust(40, ' '), g)
    print(('F_' +  str(q) +  '(x) = f^( - 1)(x) in R_' +  str(q) +  ':').ljust(40, ' '), F_q)
    print(('F_' +  str(p) +  '(x) = f^( - 1)(x) in R_' +  str(p) +  ':').ljust(40, ' '), F_p)
    
    # Public key
    h = conv.product_in_R_q(F_q, g, q, N, 0)
    print(''.ljust(90, '-'))
    print(('PUBLIC KEY: h(x) = F_' +  str(q) +  '(x)*g(x)').ljust(40, ' '), h)
    print(''.ljust(90, '-'))
        
    # Message in R_p
    m = [randint(0, p - 1) for i in range(N)]
    m = ntru_aux.center_lift(m, p)
    print('Message m:'.ljust(40, ' '), m)
    #print(''.ljust(90, '-'))
    
    # Random r in T(d, d)
    r = ntru_aux.ternary(d, d, N)
    #r = [ - 1, 1, 0, 0, 0,  - 1, 1, 0]
    print(('Random r(x) in T(' +  str(d) +  ', ' +  str(d) +  '):').ljust(40, ' '), r)
    print(''.ljust(90, '-'))

    # Encryption e = pr*h +  m (mod q)
    print('ENCRYPTION '.ljust(90, '-'))
    print(''.ljust(90, '-'))
    p_pol = [p] +  [0 for i in range(N - 1)]
    e = conv.product_in_R_q(p_pol, r, q, N, 1)
    print(('e(x) = ' +  str(p) +  'r(x)').ljust(40, ' '), e)
    e = conv.product_in_R_q(e, h, q, N, 0)
    print(('e(x) = ' +  str(p) +  'r(x)*h(x)').ljust(40, ' '), e)
    e = conv.addition_in_R_q(e, m, q, N)
    e = ntru_aux.fill_zeros(e, N - len(e))
    print(('e(x) = ' +  str(p) +  'r(x)*h(x) +  m').ljust(40, ' '), e)
    print(''.ljust(90, '-'))

    # Decryption
    print('DECRYPTION '.ljust(90, '-'))
    print(''.ljust(90, '-'))
    a = conv.product_in_R_q(f, e, q, N, 0)
    print('a(x) = f(x)*e(x):'.ljust(40, ' '), a)
    # Center lift
    a = ntru_aux.center_lift(a, q)
    print(('Center lift a(x)(mod ' +  str(q) +  ') :').ljust(40, ' '), a)
    a = [i % p for i in a]
    print(('Reduce a(x) (mod ' +  str(p) +  '):').ljust(40, ' '), a)
    a = conv.product_in_R_q(F_p, a, p, N, 0)
    print(('F_' +  str(p) +  '(x)*a(x):').ljust(40, ' '), a)
    print(''.ljust(90, '-'))
    a = ntru_aux.center_lift(a, p)

    print('DECRYPTED MESSAGE '.ljust(90, '-'))
    print(''.ljust(90, '-'))
    print(('Center lift F_' +  str(p) +  '(x)*a(x) (mod ' +  str(p) +  '):').ljust(40, ' '), a)

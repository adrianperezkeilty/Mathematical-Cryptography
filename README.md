# Mathematical Cryptography, custom implementations.
 
## DLP algorithms, factoring and primality tests
- discrete_log_shanks.py  
- factorization_pollard.py  
- factorization_rho_method.py  
- factorization_quadratic_sieve.py  
- miller_rabin_primality_test.py

## Elliptic curve cryptography
$p$ $\rightarrow$ prime  
$ec = (a,b)$ $\rightarrow$ Elliptic curve  
$P, Q$ $\rightarrow$ points in ec  

- elliptic_curve_elgamal.py  
```
>>> x = elliptic_curve_elgamal.elgamal_ec(prime = 175783, ec = (1, 1), P = [0, 1])
>>> Q = elliptic_curve_elgamal.ec_double_and_add(p = x.p, ec = x.ec, P = x.P, n = 33)
>>> C = x.elgamal_ec_encrypt( Q, 'helloxelgamal' )
>>> x.elgamal_ec_decrypt(n = 33, cipher = C)
'helloxelgamalxx'
```
- elliptic_curve_shanks.py  
Solve $P = nQ$ in $E(\mathbb F_p)$.
```
>>> (p, ec, P, n) = (175783, (1,1), [0, 1], 33)
>>> Q = elliptic_curve_shanks.ec_double_and_add(p, ec, P, n)
>>> elliptic_curve_shanks.ec_shanks(p, ec, P, Q)
33
```
- elliptic_curve_lenstra.py  
```
>>> elliptic_curve_lenstra.lenstra(N = 561793, ec = (1,7), bound = 100)
(347, 1619)
```

## Arithmetic in convolution polynomial rings
- convolutional_ring_arithmetic.py

## Lattices. Gauss base reduction for solving SVP in two dimensions
-  lattices_gauss_reduction.py

## NTRU cryptosystem (under construction for scalability)
- ntru_cryptosystem.py

## Pseudo Random Number Generators (under construction for scalability)
- prng_bbs.py  
- prng_lcg.py  

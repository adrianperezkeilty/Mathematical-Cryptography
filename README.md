# Mathematical Cryptography (custom implementations)
 
## DLP algorithms, factoring and primality tests
- discrete_log_shanks.py  
- factorization_pollard.py  
- factorization_rho_method.py  
- factorization_quadratic_sieve.py  
- miller_rabin_primality_test.py

## Elliptic curve cryptography
$p$ $\rightarrow$ prime  
$ec = (a,b)$ $\rightarrow$ Elliptic curve $y^2=x^3+ax+b$  
$P, Q$ $\rightarrow$ points in $ec$

- ElGamal cryptosystem using 3-letter blocks (elliptic_curve_elgamal.py) 
```
>>> x = elliptic_curve_elgamal.elgamal_ec(prime = 175783, ec = (1, 1), P = [0, 1])
>>> Q = elliptic_curve_elgamal.ec_double_and_add(p = x.p, ec = x.ec, P = x.P, n = 33)
>>> C = x.elgamal_ec_encrypt( Q, 'helloxelgamal' )
>>> x.elgamal_ec_decrypt(n = 33, cipher = C)
'helloxelgamalxx'
```
- ECDLP Shanks: Solve $P = nQ$ in $E(\mathbb F_p)$ (elliptic_curve_shanks.py)  

```
>>> (p, ec, P, n) = (175783, (1,1), [0, 1], 33)
>>> Q = elliptic_curve_shanks.ec_double_and_add(p, ec, P, n)
>>> elliptic_curve_shanks.ec_shanks(p, ec, P, Q)
33
```
- Lenstra factorization of integers in $E(\mathbb F_p)$ (elliptic_curve_lenstra.py)
```
>>> elliptic_curve_lenstra.lenstra(N = 561793, ec = (1,7), bound = 100)
(347, 1619)
```
## Lattices 
-  SVP in two dimensions (lattices_gauss_reduction.py)
```
>>> lattices_gauss_reduction.gauss_lattice_reduction( base = [[9876,865],[9865,7432]])
(-11, 6567)
```

## NTRU Public key cryptosystem
- ntru_cryptosystem.py
```
>>> (N, p, q, d) = (13,5,73,2)
>>> x = ntru_cryptosystem.ntru(N, p, q, d)
>>> (f, g, h) = x.random_keys()
>>> m = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2]
>>> c = x.encrypt(m, h)
>>> x.decrypt(c, f) == m
True
```

## Pseudo Random Number Generators (under construction for scalability)
- prng_bbs.py  
- prng_lcg.py  

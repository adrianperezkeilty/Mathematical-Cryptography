# Mathematical Cryptography (custom implementations)
 
## DLP, factoring and primality tests
- Solving $a^x = b \mod{n}$: Shanks' babystep-giantstep algorithm (discrete_log_shanks.py)
```
>>> (a, b, n) = (26,2861,3079)
>>> discrete_log_shanks.shanks(a, b, n)
101
```
- Pollard's $p-1$ method for factoring integers (factorization_pollard.py)
```
>>> factorization_pollard.pollard(n = 5619877, rand_int = 3)
(323, 17399)
```
- Pollard's $\rho$ method (factorization_rho_method.py)
```
>>> factorization_rho_method.rho(n = 56198779982311, x0 = 14)
(90031, 624215881)
```
- Quadratic sieve (factorization_quadratic_sieve.py)  
Returns system of congruencial equations for manual resolution:
```
>>> factorization_quadratic_sieve.quadratic_sieve(n = 221, length_sieve = 15)

Initial list:
[4, 35, 68, 103, 140, 179, 220, 263, 308, 355, 404, 455, 508, 563, 620]
 
List after sieving:
[1, 1, 1, 103, 1, 179, 1, 263, 1, 71, 101, 1, 127, 563, 31]
 
Integers with prime factors smaller than or equal to 20 :
    1 15^2 =[2, 2]                         mod 221
    2 16^2 =[5, 7]                         mod 221
    3 17^2 =[2, 2, 17]                     mod 221
    4 19^2 =[2, 2, 5, 7]                   mod 221
    5 21^2 =[2, 2, 5, 11]                  mod 221
    6 23^2 =[2, 2, 7, 11]                  mod 221
    7 26^2 =[5, 7, 13]                     mod 221
```
- Miller Rabin primality test (miller_rabin_primality_test.py)
```
>>> x = miller_rabin_primality_test.mr(5617)
>>> x.witness(3)
1224
```
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

## Pseudo Random Number Generators (statistical tests)
- Blum Blum Shub (BBS) generator (prng_bbs.py)  
- Linear Congruential Generator (LCG) (prng_lcg.py)

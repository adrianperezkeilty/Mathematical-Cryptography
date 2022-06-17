
##################################################################################
# ElGamal elliptic curve public key cryptosystem (ascii_lowercase 3-letter blocks)
##################################################################################

import numpy as np
import string
from ecc_aux import ec_add, ec_double_and_add, ec_points_over_F_p, ec_koblitz_encode, ec_point_check
from random import randint

# Private key:  n               -> Element in F_p
#
# Public keys:  p               -> Prime
#               ec = (a, b)     -> Elliptic curve coefficients
#               P, Q = n * P    -> Points in E(F_p)

class elgamal_ec:

    def __init__(self, prime, ec, P = None):
        self.p = prime
        self.ec = ec

        if P is None: self.P = ec_points_over_F_p(self.p, self.ec, 1)
        else:
            if ec_point_check(self.p, ec, P): self.P = P
            else: raise Exception(str(P) + ' not in elliptic curve ' + str(ec)) 

    def elgamal_ec_encrypt(self, Q, plain):

        if None in {self.ec, self.p} or self.P is None: raise Exception('Missing public key')

        # Koblitz error tolerance for plaintext representation
        K = 10

        # Generate alphabet & convert message to lower case & initialize counter
        (alphabet, orig_m, count) = (string.ascii_lowercase, (plain.lower()), 0)

        # Pad the message with 'x' if necessary
        orig_m = orig_m.ljust(len(plain) +  ((len(plain) % 3)*2) % 3, 'x')
        
        # Encode message a - >01, ..., z - >26
        plain = orig_m
        for letter in alphabet:
            count = count +  1
            plain = plain.replace(letter, str(count).rjust(2, '0'))
            if not (set(plain) & set(alphabet)): break

        # Split into 3 - letter block
        L = [plain[i*6:(i + 1)*6] for i in range(int(len(plain)/6))]

        # Convert blocks to integers (they are written in base 26)
        # ex: '010418'  - > (1 - 1)*26^2 +  (4 - 1)*26^1 +  18*26^0  =  96
        cipher = []
        for block in L:
            m = (int(block[:2]) - 1)*26**2 +  (int(block[2:4]) - 1)*26 +  int(block[4:])
            
            # Represent M in E(F_p) using Koblitz's algorithm and K = 10
            M = ec_koblitz_encode(self.p, m, self.ec, K)
            if M[1] > int((self.p +  1)/2):
                M[1] = M[1] - self.p
                
            # Choose random integer k between 1 and 100 (if larger, algorithm becomes inefficient)
            k = randint(1, 100)

            # Compute C1 = kP,  C2 = M +  kQ.
            C1 = ec_double_and_add(self.p, self.ec, self.P, k)
            C2 = ec_add(self.p, self.ec, ec_double_and_add(self.p, self.ec, Q, k), M)
            cipher.append([C1, C2])

        # Avoid 4 to 1 message expansion
        for c in cipher:
            for i in [0, 1]:
                if c[i][1] < 0:
                    c[i] = [c[i][0], 0]
                else:
                    c[i] = [c[i][0], 1]

        return cipher

    # n -> private key
    def elgamal_ec_decrypt(self, n, cipher):
        
        (a, b) = self.ec

        # Koblitz error tolerance for plaintext representation
        K = 10
        L = []
        for c in cipher:

            # Retrieve 'y' value given the bit 0 (negative) or 1 (positive)
            for i in [0, 1]:

                # Compute square roots modulo p
                x = c[i][0]
                z = (x**3 +  a * x +  b) % self.p
                y = (z**((self.p +  1) // 4)) % self.p
                
                if y >= (self.p +  1) // 2:
                    y = self.p - y
                if c[i][1] == 0:
                    c[i][1] =  - y
                else:
                    c[i][1] = y

            (C1, C2) = (c[0], c[1])

            # Retrieve M = C2 +  n( - C1)
            M = ec_add(self.p, self.ec, ec_double_and_add(self.p, self.ec, [C1[0],  - C1[1]], n), C2)
            m = M[0] // K
            
            # From base 26 to base 10:
            s = ''
            while m !=0 :
                r = m % 26
                s = str(r+1).rjust(2,'0') + s
                m = m // 26
            L.append(s[:len(s)-2]+str(int(s[-2:])-1))

        # Decode into plaintext
        plain = ''
        for word in L:
            for i in range(3):
                plain += string.ascii_lowercase[int(word[i * 2:i * 2 + 2])-1]
         
        return plain

# UNDER CONSTRUCTION FOR SCALABILITY !

################################
# Linear congruential generator 
################################

import random

def lcg(a, b, n):
    
    sample = random.sample(range(0,  454), 10)
    print('seed'.ljust(20, ' '), 'bits')
    print(''.ljust(130, '-'))
    
    for x in sample + [130]:
        seed = x
        bits = ''
        
        for i in range(100):
            bits = bits +  format(x,'b')[ - 1]
            x = (a*x +  b) % n
            
        print(str(seed).ljust(20, ' '), bits)

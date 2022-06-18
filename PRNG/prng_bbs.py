# UNDER CONSTRUCTION FOR SCALABILITY !

# At the moment:
# Random selection of seeds + statistical tests
##>>> BBS(13)
##Seed       Period     Bit sequence LSB               Bit sequence 2 LSB            
##------------------------------------------------------------------------------------------
##177        1          10111111111111111111           01000101010101010101          
##66         1          01111111111111111111           10010101010101010101          
##145        2          10111111111111111111           01001101110111011101          
##184        2          00111111111111111111           00001101110111011101          
##125        1          10111111111111111111           01000101010101010101          
##133        2          11111111111111111111           01011101110111011101          
##200        1          00111111111111111111           00000101010101010101          
##157        1          11111111111111111111           01010101010101010101          
##110        2          00111111111111111111           10100111011101110111          
##162        2          00111111111111111111           10100111011101110111          
##------------------------------------------------------------------------------------------
##Computing chi squared tests on 100 trials each consisting on 100 samples of the 100 first bits of the output function...
##------------------------------------------------------------------------------------------
##statistic                      mean                 variance            
##------------------------------------------------------------------------------------------
##Frequency LSB                  2.902                0.0                 
##Frequency 2 LSB                3.69783              0.073471            
##Serial test k = 2 on LSB       0.051                0.0                 
##Serial test k = 2 on 2 LSB     0.19225              2.8e-05             
##Serial test k = 3 on LSB       0.055                0.0                 
##Serial test k = 3 on 2 LSB     0.13807              3.1e-05             
##>>> 

################
# BBS generator                                 
################

import numpy as np
import random
import math

def bbs(n):
    
    print('Seed'.ljust(10, ' '), 'Period'.ljust(10, ' '), 'Bit sequence LSB'.ljust(30, ' '), 'Bit sequence 2 LSB'.ljust(30, ' '))
    print(''.ljust(90, '-'))
    (sample, test_data) = (random.sample(range(0,  252),  10), [])

    # Show 10 random seeds wih their period and 20 first bits (least significant and 2 least significant)
    for x in sample:
        atributes = BBS_atributes(n, x)
        period = str(atributes[0])
        bits1 = atributes[1]
        bits2 = atributes[2]
        # Store first 100 bits for frequency and serial testing
        test_data.append([x, bits1, bits2])
        print(str(x).ljust(10, ' '), period.ljust(10, ' '), bits1[:20].ljust(30, ' '), bits2[:20].ljust(30, ' ')) 
    print(''.ljust(90, '-'))

    # Chi squared tests

    # Number of trials and samples on each trial
    (N, n_samples) = (100, 100) 
    print('Computing chi squared tests on ' +  str(N) +  ' trials each consisting on ' +  str(n_samples) +  ' samples of the 100 first bits of the output function...')
    
    statistic_list = []
    for i in range(N):
        (sample, test_data) = (random.sample(range(0,  252), n_samples), [])

        # Initialization of statistics
        (X1_freq, X2_freq, X1_serial_k_2, X1_serial_k_3, X2_serial_k_2, X2_serial_k_3) = (0, 0, 0, 0, 0, 0)
        for x in sample:
            atributes = BBS_atributes(n, x)
            bits1 = atributes[1]
            bits2 = atributes[2]
            test_data.append([x, bits1, bits2])

            # Chi square frequency and serial tests (k = 2, 3) for bits1 (least sig. bit) 
            if [test_data[i][1] for i in range(len(test_data))].count(bits1) == 1:
                # Frequency: O_i = number of zeros/bit length; E_i = 1/2
                X1_freq = X1_freq +  (((bits1.count('0')/len(bits1) - 0.5)**2)/0.5)

                # Serial test on bits1 k = 2:
                (o11, o12, o13, o14) = (0, 0, 0, 0)
                e = 1/4
                length_k_2 = int(len(bits1)/2)
                
                for i in range(0, 2*length_k_2 +  1, 2):
                    
                    if bits1[i:i +  2] == '00':
                        o11 = o11 +  1
                    if bits1[i:i +  2] == '01':
                        o12 = o12 +  1
                    if bits1[i:i +  2] == '10':
                        o13 = o13 +  1
                    if bits1[i:i +  2] == '11':
                        o14 = o14 +  1

                result = ((o11/length_k_2) - (1/4))**2 +  ((o12/length_k_2) - (1/4))**2 +  ((o13/length_k_2) - (1/4))**2 +  ((o14/length_k_2) - (1/4))**2
                result = (1/n_samples)*math.sqrt(result)
                X1_serial_k_2 = X1_serial_k_2 +  result

                # Serial test on bits1 k = 3:
                (o11, o12, o13, o14, o15, o16, o17, o18) = (0, 0, 0, 0, 0, 0, 0, 0)
                e = 1/8
                length_k_3 = int(len(bits1)/3)
                
                for i in range(0, 3*length_k_3 +  1, 3):

                    if bits1[i:i +  3] == '000':
                        o11 = o11 +  1
                    if bits1[i:i +  3] == '001':
                        o12 = o12 +  1
                    if bits1[i:i +  3] == '010':
                        o13 = o13 +  1
                    if bits1[i:i +  3] == '011':
                        o14 = o14 +  1
                    if bits1[i:i +  3] == '100':
                        o15 = o15 +  1
                    if bits1[i:i +  3] == '101':
                        o16 = o16 +  1
                    if bits1[i:i +  3] == '110':
                        o17 = o17 +  1
                    if bits1[i:i +  3] == '111':
                        o18 = o18 +  1

                result = ((o11/length_k_3) - e)**2 +  ((o12/length_k_3) - e)**2 +  ((o13/length_k_3) - e)**2 +  ((o14/length_k_3) - e)**2
                result = result +  ((o15/length_k_3) - e)**2 +  ((o16/length_k_3) - e)**2 +  ((o17/length_k_3) - e)**2 +  ((o18/length_k_3) - e)**2
                result = (1/n_samples)*math.sqrt(result)
                X1_serial_k_3 = X1_serial_k_3 +  result


            # Chi square frequency and serial tests (k = 2, 3) for bits2 (least 2 sig. bits)     
            if [test_data[i][2] for i in range(len(test_data))].count(bits2) == 1:
                
                X2_freq = X2_freq +  (((bits2.count('0')/len(bits2) - 0.5)**2)/0.5)

                # Serial test on bits2 k = 2:
                (o21, o22, o23, o24) = (0, 0, 0, 0)
                length_k_2 = int(len(bits1)/2)
                
                for i in range(0, 2*length_k_2 +  1, 2):
                        
                    # Bits2
                    if bits2[i:i +  2] == '00':
                        o21 = o21 +  1
                    if bits2[i:i +  2] == '01':
                        o22 = o22 +  1
                    if bits2[i:i +  2] == '10':
                        o23 = o23 +  1
                    if bits2[i:i +  2] == '11':
                        o24 = o24 +  1

                result = ((o21/length_k_2) - e)**2 +  ((o22/length_k_2) - e)**2 +  ((o23/length_k_2) - e)**2 +  ((o24/length_k_2) - e)**2
                result = (1/n_samples)*math.sqrt(result)
                X2_serial_k_2 = X2_serial_k_2 +  result

                # Serial test on bits2 k = 3:
                (o21, o22, o23, o24, o25, o26, o27, o28) = (0, 0, 0, 0, 0, 0, 0, 0)
                e = 1/8
                length_k_3 = int(len(bits1)/3)
                
                for i in range(0, 3*length_k_3 +  1, 3):
                        
                    # Bits2
                    if bits2[i:i +  3] == '000':
                        o21 = o21 +  1
                    if bits2[i:i +  3] == '001':
                        o22 = o22 +  1
                    if bits2[i:i +  3] == '010':
                        o23 = o23 +  1
                    if bits2[i:i +  3] == '011':
                        o24 = o24 +  1
                    if bits2[i:i +  3] == '100':
                        o25 = o25 +  1
                    if bits2[i:i +  3] == '101':
                        o26 = o26 +  1
                    if bits2[i:i +  3] == '110':
                        o27 = o27 +  1
                    if bits2[i:i +  3] == '111':
                        o28 = o28 +  1

                result = ((o21/length_k_3) - e)**2 +  ((o22/length_k_3) - e)**2 +  ((o23/length_k_3) - e)**2 +  ((o24/length_k_3) - e)**2
                result = result +  ((o25/length_k_3) - e)**2 +  ((o26/length_k_3) - e)**2 +  ((o27/length_k_3) - e)**2 +  ((o28/length_k_3) - e)**2
                result = (1/n_samples)*math.sqrt(result)
                X2_serial_k_3 = X2_serial_k_3 +  result

        statistic_list.append([round(X1_freq, 3), round(X2_freq, 3), round(X1_serial_k_2, 3), round(X2_serial_k_2, 3), round(X1_serial_k_3, 3), round(X2_serial_k_3, 3)])

    print(''.ljust(90, '-'))
    print('statistic'.ljust(30, ' '), 'mean'.ljust(20, ' '), 'variance'.ljust(20, ' '))
    print(''.ljust(90, '-'))
    
    # Retrieve data
    X1_freq_list = [statistic_list[i][0] for i in range(len(statistic_list))]
    X2_freq_list = [statistic_list[i][1] for i in range(len(statistic_list))]
    X1_serial_k_2_list = [statistic_list[i][2] for i in range(len(statistic_list))]
    X2_serial_k_2_list = [statistic_list[i][3] for i in range(len(statistic_list))]
    X1_serial_k_3_list = [statistic_list[i][4] for i in range(len(statistic_list))]
    X2_serial_k_3_list = [statistic_list[i][5] for i in range(len(statistic_list))]

    # Mean and variance of statistics 
    (X1_freq_mean, X1_freq_var) = (np.mean(X1_freq_list), np.var(X1_freq_list))
    (X2_freq_mean, X2_freq_var) = (np.mean(X2_freq_list), np.var(X2_freq_list))
    (X1_serial_k_2_mean, X1_serial_k_2_var) = (np.mean(X1_serial_k_2_list), np.var(X1_serial_k_2_list))
    (X2_serial_k_2_mean, X2_serial_k_2_var) = (np.mean(X2_serial_k_2_list), np.var(X2_serial_k_2_list))
    (X1_serial_k_3_mean, X1_serial_k_3_var) = (np.mean(X1_serial_k_3_list), np.var(X1_serial_k_3_list))
    (X2_serial_k_3_mean, X2_serial_k_3_var) = (np.mean(X2_serial_k_3_list), np.var(X2_serial_k_3_list))
     
    print('Frequency LSB'.ljust(30, ' '), str(round(X1_freq_mean, 6)).ljust(20, ' '), str(round(X1_freq_var, 6)).ljust(20, ' '))
    print('Frequency 2 LSB'.ljust(30, ' '), str(round(X2_freq_mean, 6)).ljust(20, ' '), str(round(X2_freq_var, 6)).ljust(20, ' '))
    print('Serial test k = 2 on LSB'.ljust(30, ' '), str(round(X1_serial_k_2_mean, 6)).ljust(20, ' '), str(round(X1_serial_k_2_var, 6)).ljust(20, ' '))
    print('Serial test k = 2 on 2 LSB'.ljust(30, ' '), str(round(X2_serial_k_2_mean, 6)).ljust(20, ' '), str(round(X2_serial_k_2_var, 6)).ljust(20, ' '))
    print('Serial test k = 3 on LSB'.ljust(30, ' '), str(round(X1_serial_k_3_mean, 6)).ljust(20, ' '), str(round(X1_serial_k_3_var, 6)).ljust(20, ' '))
    print('Serial test k = 3 on 2 LSB'.ljust(30, ' '), str(round(X2_serial_k_3_mean, 6)).ljust(20, ' '), str(round(X2_serial_k_3_var, 6)).ljust(20, ' '))
    
##    plot_distribution([statistic_list[i][0] for i in range(len(statistic_list))], 0.05, 'X1 chi squared frequency distribution')
##    plot_distribution([statistic_list[i][1] for i in range(len(statistic_list))], 0.05, 'X2 chi squared frequency distribution')
    

def BBS_atributes(n, seed):
    (x, bits1, bits2) = (seed, format(seed,'b')[ - 1], format(seed,'b').rjust(2, '0')[ - 2:])
    (L, period, count) = ([x], 0, 0)
    
    # Work with first 100 bits of the sequence
    while count<100 or not period:
        count = count +  1
        x = (x**2) % n
        
        # Least significant bits
        (bits1, bits2) = (bits1 +  format(x,'b')[ - 1], bits2 +  format(x,'b').rjust(2, '0')[ - 2:])
        L.append(x)
        if L.count(x)>1 and not period:
            # Period
            period = (len(L) - 1) - L.index(L[ - 1])
    return period, bits1, bits2

# Convert binary to integer
def bits_to_int(bits):
    n = 0
    exp = 0
    for i in bits[:: -1]:
        if i == '1':
            n = n +  2**exp
        exp = exp +  1
    return n



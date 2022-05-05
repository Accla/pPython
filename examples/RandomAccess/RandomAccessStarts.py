import numpy as np

# import gridPython functions
from uint64 import *

def RandomAccessStarts(n):
    """Utility routine to start random number generator at Nth step
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering RandomAccessStarts')

    # Define constants used in random number generator.
    # PERIOD = uint64(1317624576693539401)
    # PERIOD = bitset(bitset(bitset(uint64(1317624576693539401),7),4),1)
    POLY = uint64(7)
    
    # Get the number of locations that we are starting.
    BLOCKSIZE = len(n)
    if DEBUG:
        print('BLOCKSIZE = %d'%(BLOCKSIZE))
    
    # Allocate variables.
    m2 = np.zeros(64,'uint64')
    temp = uint64(1)
    
    ran = np.zeros(BLOCKSIZE,'uint64')
    ran[:] = uint64(2)
    
    # UNLIKELY WE WILL ENCOUNTER THESE LIMITS SO IGNORE
    # # Modulate
    # while (n < 0) n = n + PERIOD
    # while (n > PERIOD) n -= PERIOD
    
    # Build up m2 table.
    
    # defind bitget64 lambda function for uint64 number
    # x: uint64
    # n: bit position
    # no good for array: bitget64 = lambda x,n: 1 if x & uint64(2**(n-1)) else 0
    # return True/False (dtype is matched with the input)
    bitget64 = lambda x,n: (np.bitwise_and(x,np.uint64(2**(n-1))))>0

    for i in range(64):
    
        # Initialize m2.
        m2[i] = temp
        # temp = (temp << 1) ^ ((s64Int) temp < 0 ? POLY : 0)
        # temp = (temp << 1) ^ ((s64Int) temp < 0 ? POLY : 0)
    
        # Equivalent to above 2 lines of C code.
        for j in range(2):
            # Check if bit 64 is set.
            if bitget64(temp,64):
                temp = temp << uint64(1)
                temp = np.bitwise_xor(temp,POLY)
            else:
                temp = temp << uint64(1)
    
    # Allocate indices.
    ii = np.zeros(BLOCKSIZE,'int')
    
    # Initialize index table ii for each starting point.
    # Use "vectorized" method.
    for j in range(62,-1,-1):
        # Shift n by i, and check first bit,
        # then find all instance where this statement is true.
        i_hit = (np.where(np.bitwise_and(np.uint64(n)>>j,np.uint64(1))==True))[0]
        
        if i_hit.size:
            # Set index to first i_hit. (Note: python index starts from zero.)
            ii[i_hit] = max(np.amax(ii[i_hit]),j)

    # Compute ran for these  starting points.
    # To do this in a "vectorized" manner we
    # replace if statements with finds.
    
    temp = np.zeros(BLOCKSIZE,'uint64')
    
    # Find subset jj where ii > 0.
    jj = (np.where(ii > 0))[0]
    while jj.size:
    
        # Initalize jj subset temp.
        temp[jj] = uint64(0)

        for j in range(64):
            
            # Left shift ran by j and check first bit,
            # then find sub-subset where this is true.
            jjj = (np.where(np.bitwise_and(ran[jj]>>j,uint64(1))==True))[0]

            if jjj.size:
                # XOR the sub-subset jj(jjj) by m2.
                temp[jj[jjj]] = np.bitwise_xor(temp[jj[jjj]],m2[j])

        # Copy subset to ran and decrement ii.
        ran[jj] = temp[jj]
        ii[jj] = ii[jj] - 1
    
        # Left shift n by ii over the set jj
        # then find the sub-subset where the first bit is true.
        jjj = (np.where(np.bitwise_and(uint64(n[jj])>>uint64(ii[jj]),uint64(1))==True))[0]

        if jjj.size:
    
            # Find the sub-sub-subset where the 64th bit is set.
            jjjj = (np.where(bitget64(ran[jj[jjj]],64)==True))[0]
    
            # Right shift the sub-subset jj(jjj)  by 1.
            ran[jj[jjj]] = ran[jj[jjj]]<<1
            if jjjj.size:
    
                # XOR the sub-sub-subset jj(jjj(jjjj)) with POLY.
                ran[jj[jjj[jjjj]]] = np.bitwise_xor(ran[jj[jjj[jjjj]]],POLY)

        # See if there are more left to compute.
        jj = (np.where(ii > 0))[0]
    
    # Set all cases where n = 0 to 1.
    ran[(np.where(n == 0))[0]] = uint64(1)

    if DEBUG:
        print('<-- Exiting RandomAccessStarts')

    return ran


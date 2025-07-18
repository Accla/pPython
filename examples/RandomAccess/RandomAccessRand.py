import numpy as np

from pPython.dmat import uint64

def RandomAccessRand(ran):
    """
    Core of RandomAccess benchmark using Tree communication pattern
    """

    # Create random 64 bit numbers for
    # RandomAccess benchmark.

    # Define constants used in random number generator.
    POLY = uint64(7)

    # Get blocksize.
    BLOCKSIZE = len(ran)

    # Vectorized approach.
    # Get elements in ran that set 64th bit set.
    bitget64 = lambda x,n: (np.bitwise_and(x,np.uint64(2**(n-1))))>0

    i_bit64 = (np.where(bitget64(ran,64)==True))[0]

    # Do shift.
    ran = ran<<1

    # Apply XOR.
    if i_bit64.size:
        ran[i_bit64] =  np.bitwise_xor(ran[i_bit64],POLY)

    return ran


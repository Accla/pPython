from math import ceil,floor

from GridFalls import *
from LineSgmt import *
from lcm import *
from ls_intersection import *

def falls_intersection(f1, f2):
    """
    FALLS_INTERSECTION Given two FALLS, find the intersection FALLS
    F1 and F2 each contain at most a single FALLS, since unevenly
    divisible dimensions are represented using a single FALLS and local
    length.
    
    FALLS data structure F:
    F.L - beginning index of the first block of elements
    F.R - ending index of the first block of elements
    F.S - strides between successive L's
    F.N - number of equally spaced, equally sized blocks
    
    Returns fi as a list of GridFalls objects. returns an empty list 
    when not a Falls instance or when no intersection.
    
    Python version: Dr. Chansup Byun
    Author:   Nadya Travinin
    
    References: Shankar Ramaswamy and Prithviraj Banerjee. Automatic Generation of Efficient Array
    Redistribution Routines for Distributed Memory Multicomputers. IEEE 1995.
    """ 
    
    DEBUG = 1
    if DEBUG:
        print('--> Entering falls_intersection')
    
    #  check to see if either f1 or f2 are -1's
    if not isinstance(f1,GridFalls) or not isinstance(f2,GridFalls):
        fi = []
        return fi

    
    # compute intersection period (fp), m1 and m2
    fp = lcm(f1.s, f2.s)
    m1 = fp/f1.s
    m2 = fp/f2.s
    
    fi = []
    I1 = int(max(0, ceil((f2.l-f1.r)/f1.s)))
    l1 = LineSgmt()
    l2 = LineSgmt()
    li = LineSgmt()
    temp = GridFalls()
    for i1 in range(I1,int(min(I1+m1-1, f1.n-1)+1)):
        l1.l = f1.l+i1*f1.s
        l1.r = f1.r+i1*f1.s
        for i2 in range(int(max(0, ceil((i1*f1.s+f1.l-f2.r)/f2.s))),int(min(floor((i1*f1.s+f1.r-f2.l)/f2.s), m2-1, f2.n-1)+1)):
            l2.l = f2.l+i2*f2.s
            l2.r = f2.r+i2*f2.s
            li = ls_intersection(l1,l2)
            # don't have to check that intersection is non-empty since we
            # are guaranteed intersection by iterating over the above
            # specified loop bounds
            temp.l = li.l
            temp.r = li.r
            temp.s = fp
            temp.n = floor(min((f1.n-i1-1)/m1, (f2.n-i2-1)/m2) + 1)
            # last global index of the intersection
            fi_block_size = temp.r-temp.l+1 # block size
            fi_last_ind = temp.r+temp.s*(temp.n-1)
            # last global index of f1
            if (f1.complete_block and f1.complete_cycle):
                f1_last_ind  = f1.r+f1.s*(f1.n-1)
            elif f1.complete_block:
                f1_last_ind = f1.r+f1.s*(f1.n-2)
            else:
                f1_block_size = f1.r-f1.l+1
                f1_rem_block = f1.local_len%f1_block_size
                f1_last_ind = f1.r + f1.s*(f1.n-1) - (f1_block_size-f1_rem_block)

            # last global index of f2
            if (f2.complete_block and f2.complete_cycle):
                f2_last_ind  = f2.r+f2.s*(f2.n-1)
            elif f2.complete_block:
                f2_last_ind = f2.r+f2.s*(f2.n-2)
            else:
                f2_block_size = f2.r-f2.l+1
                f2_rem_block = f2.local_len%f2_block_size
                f2_last_ind = f2.r+f2.s*(f2.n-1) - (f2_block_size-f2_rem_block)
    
            if (fi_last_ind <= f1_last_ind) and (fi_last_ind <= f2_last_ind):
                temp.local_len = temp.n*fi_block_size
                temp.complete_cycle = True
                temp.complete_block = True
            else:
                last_ind = min(f1_last_ind, f2_last_ind)
                diff_ind = fi_last_ind - last_ind
                temp.local_len = temp.n*fi_block_size - diff_ind
                if diff_ind >= fi_block_size:  # !!!
                    temp.complete_cycle = False
                    temp.complete_block = True
    
                elif diff_ind < fi_block_size:
                    temp.complete_cycle = False
                    temp.complete_block = False
            fi.append(temp)
    return fi


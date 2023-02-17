from math import ceil,floor

from Falls import *
from LineSgmt import *
from lcm import *
from ls_intersection import *
from print_falls import *

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
    
    Returns fi as a list of Falls objects. returns an empty list 
    when not a Falls instance or when no intersection.
    
    Python version: Dr. Chansup Byun
    Author:   Nadya Travinin
    
    References: Shankar Ramaswamy and Prithviraj Banerjee. Automatic Generation of Efficient Array
    Redistribution Routines for Distributed Memory Multicomputers. IEEE 1995.

    Python version: Dr. Chansup Byun
    """ 
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering falls_intersection')
    
    #  check to see if either f1 or f2 are -1's
    if not isinstance(f1,Falls) or not isinstance(f2,Falls):
        fi = []
        return fi

    # compute intersection period (fp), m1 and m2
    fp = lcm(f1.s, f2.s)
    m1 = fp/f1.s
    m2 = fp/f2.s
    
    fi = []
    I1 = int(max(0, ceil((f2.l-f1.r)/f1.s)))
    L1 = LineSgmt()
    L2 = LineSgmt()
    LS = LineSgmt()
    temp = Falls()
    for i1 in range(I1,int(min(I1+m1-1, f1.n-1)+1)):
        #CB: This has to be modified for the recent update for FALLS fix 
        L1.l = f1.l+i1*f1.s
        L1.r = f1.r+i1*f1.s
        for i2 in range(int(max(0, ceil((i1*f1.s+f1.l-f2.r)/f2.s))),int(min(floor((i1*f1.s+f1.r-f2.l)/f2.s), m2-1, f2.n-1)+1)):
            #CB: This has to be modified for the recent update for FALLS fix 
            L2.l = f2.l+i2*f2.s
            L2.r = f2.r+i2*f2.s
            LS = ls_intersection(L1,L2)
            if DEBUG:
                print('Line segments: L1:(%d,%d), L2:(%d,%d)'%(L1.l,L1.r,L2.l,L2.r))
                print('Overlao segments: LS:(%d,%d)'%(LS.l,LS.r))
    
            # don't have to check that intersection is non-empty since we
            # are guaranteed intersection by iterating over the above
            # specified loop bounds
            #CB: This has to be modified for the recent update for FALLS fix 
            temp.l = LS.l
            temp.r = LS.r
            temp.s = fp
            temp.n = floor(min((f1.n-i1-1)/m1, (f2.n-i2-1)/m2) + 1)
            temp.dist = f1.dist #CB, added with change
            # last global index of the intersection
            fi_block_size = temp.r-temp.l+1 # block size
            fi_last_ind = temp.r+temp.s*(temp.n-1)

            # last global index of f1
            if (f1.complete_block and f1.complete_cycle):
                f1_last_ind  = f1.r+f1.s*(f1.n-1)+1
            elif f1.complete_block:
                #CB: To fix empty work asignment with block distribution, subtract by 1 additionally 
                f1_last_ind = f1.r+f1.s*(f1.n-1)
            else:
                #CB: not sure when this case happens yet     
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
    
            temp.local_len = temp.r-temp.l+1
            if (fi_last_ind <= f1_last_ind) and (fi_last_ind <= f2_last_ind):
                # temp.local_len = temp.n*fi_block_size
                temp.complete_cycle = True
                temp.complete_block = True
            else:
                last_ind = min(f1_last_ind, f2_last_ind)
                diff_ind = fi_last_ind - last_ind
                # temp.local_len = temp.n*fi_block_size - diff_ind
                #CB if diff_ind >= fi_block_size:  # !!!
                if diff_ind > fi_block_size:  # !!!
                    temp.complete_cycle = False
                    temp.complete_block = True
    
                #CB elif diff_ind < fi_block_size:
                elif diff_ind <= fi_block_size:
                    temp.complete_cycle = False
                    temp.complete_block = False
            if DEBUG:
                print('fi_block_size: %d, fi_last_ind: %d'%(fi_block_size,fi_last_ind))
                print('f1_last_ind: %d, f2_last_ind: %d'%(f1_last_ind,f2_last_ind))
                print('Falls: temp')
                print_falls(temp)
            fi.append(temp)
    if DEBUG:
        print('<-- Exiting falls_intersection')
    return fi

########################################################
# pMatlab: Parallel Matlab Toolbox
# Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
# Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
# MIT Lincoln Laboratory
########################################################
# Copyright (c) 2005, Massachusetts Institute of Technology All rights 
# reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are 
# met:
#      * Redistributions of source code must retain the above copyright 
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright 
#        notice, this list of conditions and the following disclaimer in
#        the documentation and/or other materials provided with the
#        distribution.
#      * Neither the name of the Massachusetts Institute of Technology nor 
#        the names of its contributors may be used to endorse or promote 
#        products derived from this software without specific prior written 
#        permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


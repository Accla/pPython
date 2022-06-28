import math
import numpy as np

from Falls import *
from n_dim_find import *
from print_pitfalls import *
from print_falls import *

def get_local_falls(pitfalls, grid, rank):
    """Given the PITFALLS object, the grid and local processor rank, 
    returns an array of local FALLS objects (one for each dimension of the
    distributed object).
    
    Usage:
    ------
    local_falls = GET_LOCAL_FALLS(PITFALLS, GRID, RANK)
    
    PITFALLS: an array of PITFALLS structures for each dimension of
        the distributed object, i.e. pf is a PITFALLS
        representation of the i-th dimension
    GRID: n-dimensional array that specifies the layout of processors
        on which the object is distributed
    RANK: processor rank
 
    LOCAL_FALLS:
        Array of FALLS objects, one for each dimension of the distributed
        object. FALLS[i] is a 4-tuple (l,r,s,n). In addition FALLS[i]
        stores information regarding local length of data to take care of
        cases with non-evenly divisible dimensions without implementing
        extra FALLS. 
        The following are the fields of each FALLS[i]
            L - starting index of the first block
            R - ending index of the first block
            S - stride between successive L's
            N - number of equally spaced, equally sized blocks of elements
            LOCAL_LEN - local length of the data on the local processor
                NOTE: If dimensions are evenly divisible, LOCAL_LEN is
                always (R-L+1)*N
            COMPLETE_CYCLE - flag that indicates whether the processor has
            incomplete cycles
            COMPLETE_BLOCK - flag that indicates whether the processor has
            incomplete blocks
 
    Original Author: Nadya Travinin (pMatlab)
    Author: Dr. Chansup Byun (pPython)
 
    References: Shankar Ramaswamy and Prithviraj Banerjee. Automatic Generation of Efficient Array 
              Redistribution Routines for Distributed Memory Multicomputers. IEEE 1995.
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering get_local_falls.')
    
    dim = len(pitfalls)
    ifound = False
    ind = []
    local_falls = []
    
    if dim <= 4:

        ind = n_dim_find(grid,rank)
        if DEBUG:
            print('get_local_falls: index posititon for given rank, %d'%(rank))
            # print(ind)
            
        if len(ind):
            for i in range(dim):
                # Create an empty Falls class.
                f = Falls()

                pid = ind[i]
                pf = pitfalls[i]
                # if DEBUG:
                #     print('axis, i, in %d direction.'%(i))
                #     print_pitfalls(pf)
                f.l = pf.l+(pid)*pf.d
                f.r = pf.r+(pid)*pf.d
                f.s = pf.s
                f.n = pf.n
                # additional info used to calculate global index in get_global_ind()
                f.dist = pf.dist
            
                # compute local length
                block_size = f.r-f.l+1 # block size 
            
                if block_size == pf.d: # no overlap
                    if pf.rem_cycle==0:
                        f.local_len = f.n*block_size
                        f.complete_cycle = True # flag that signifies that the local data has no incomplete cycles
                        f.complete_block = True # flag that signifies that the local data has no incomplete blocks
                        # (i.e. local indices can be computed directly from the falls info without 
                        # dealing with local length)
                    else: # rem_cycle != 0
                        # number of blocks in the incomplete cycle (both complete and incomplete)
                        num_blocks = math.ceil(pf.rem_cycle/block_size)
                        # the length of incomplete block (if one exists)
                        rem_block = pf.rem_cycle%block_size
                        # Treat block distribution separately
                        if pf.dist == 'b':
                            if (pid)<pf.rem_cycle:
                                # local processor does not have an incomplete cycle
                                # and has no incomplete blocks
                                f.local_len = (f.n)*block_size
                                f.complete_cycle = True
                                f.complete_block = True
                            else:
                                # local processor has an incomplete cycle with an
                                # incomplete block
                                f.local_len = (f.n)*block_size-1
                                f.complete_cycle = False
                                f.complete_block = False
                                # adjustment for incomplete cycle & incomple block
                                f.l = pf.l+pid*pf.d-(pid-pf.rem_cycle)
                                f.r = pf.r+pid*pf.d-(pid-pf.rem_cycle)-1
                                if DEBUG:
                                    print('f.l & f.r changed (incomplete cycle, incomplete block): %d,%d'%(f.l,f.r))
                        else: 
                            if (pid+1)<num_blocks:
                                # local processor does not have an incomplete cycle
                                # and has no incomplete blocks
                                f.local_len = f.n*block_size
                                f.complete_cycle = True
                                f.complete_block = True
                            elif (pid+1)>num_blocks:
                                # local processor has one less block (incomplete cycle)
                                # but no imcomplete blocks
                                f.local_len = (f.n-1)*block_size  
                                f.complete_cycle = False
                                f.complete_block = True
                            elif (pid+1)==num_blocks:
                                if rem_block==0:
                                    # local processor has no incomplete cycles or blocks
                                    f.local_len = f.n*block_size
                                    f.complete_cycle = True
                                    f.complete_block = True
                                else:
                                    # local processor has an incomplete cycle with an
                                    # incomplete block
                                    f.local_len = (f.n-1)*block_size+rem_block
                                    f.complete_cycle = False
                                    f.complete_block = False
                else: # overlap, rem_cycle should always be greater than 0 
                    # Not handled in gen_falls(). To Do later
                    if f.r <= pf.rem_cycle:
                        f.local_len = block_size
                        f.complete_cycle = True
                        f.complete_block = True
                    else:
                        f.local_len = pf.rem_cycle - f.l+1
                        f.complete_cycle = False
                        f.complete_block = False
            
                    #CB: For the last block, check if f.r > max. data dimension
                    #    With the block distribution, pf.rem_cycle is always the max dimension (right?)
                    if f.r >= pf.rem_cycle:
                        f.r = pf.rem_cycle - 1
                        f.local_len = f.r - f.l +1

                # store the FALLS structure 
                local_falls.append(f)
                # if DEBUG:
                #     print_falls(f)
        else:
            # Empty index list, ind
            for i in range(dim):
                local_falls.append(None)
    else:
        print('ERROR(get_local_falls): Only objects up to 4-D are supported')
        # exit()
        
    if DEBUG:
        print('**** get_local_falls: aggragated falls ****')
        for i in range(len(local_falls)):
            lf = local_falls[i]
            print_falls(lf)
        print('<-- Exiting get_local_falls.')
        
    return local_falls


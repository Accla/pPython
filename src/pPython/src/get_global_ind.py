from Falls import *

def get_global_ind(falls, grid_dims=None):
    """Returns a list array of global indices stored locally given
    a FALLS object (list array of FALLS, one for each dimension)
    
    Usage:
    ------
    ind = get_global_ind(falls)
    ind = get_global_ind(falls,grid_dim)
    
    FALLS: array of FALLS objects
    grid_dims:
    IND:
        len(IND) is equal to the number of dimensions of the distributed
        object. IND(i) is of the form [ind1 ind2 ind3 ...] where ind_i is a
        global index of the distributed object that is local to the current
        processor. Eachi ind_i is a tuple of range objects (could be one or more)
        
        This is a dictionary variable
        Each value is a tuple of ranges of indices instead of list of indices (save memory usage)
        
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering get_global_ind')
    
    dim = len(falls)
    if not grid_dims:
        grid_dims=[]
    
    if dim <= 4:
        ind = dict()
        for i in range(dim):
            # Change from a list to a tuple of ranges to save memory usage (pFFT benchmark)
            temp = tuple()
            falls_i = falls[i]
            if isinstance(falls_i,Falls):
                # falls is an instance of Falls class
                if (len(grid_dims)>0) and (grid_dims[i] == 1): 
                    # dimension is not distributed
                    # print('get_global_ind: To be checked, am i here?')
                    temp += (range(int(falls_i.local_len)),)
                else: #dimension is distributed
                    # get the indices for the first n-1 cycles
                    # NOTE: This takes care of the case when complete_cycle==0 and
                    #       complete_block==1
                    if DEBUG:
                        print('falls_i.n-1 = %d'%(falls_i.n-1))
                    for j in range(0,falls_i.n-1):
                        lval = falls_i.l+j*falls_i.s
                        rval = falls_i.r+j*falls_i.s+1
                        temp += (range(lval,rval),)
                        if DEBUG:
                            print('j = %d'%(j))
                            print('(Left,Right): %d,%d'%(lval,rval))
                            print(temp)
                        
                    # get indices for the n-th cycle, if it exists
                    if (falls_i.complete_cycle and falls_i.complete_block): 
                        # complete n-th cycle, complete block
                        if DEBUG:
                            print('complete n-th cycle & complete block')
                            print(falls_i.l+(falls_i.n-1)*falls_i.s)
                            print(falls_i.r+(falls_i.n-1)*falls_i.s+1)
                        i_left = int(falls_i.l+(falls_i.n-1)*falls_i.s)
                        i_rght = int(falls_i.r+(falls_i.n-1)*falls_i.s+1)
                        temp += (range(i_left,i_rght),)
 
                    elif (not falls_i.complete_cycle) and (not falls_i.complete_block):
                        if DEBUG:
                            print('incomplete n-th cycle & incomplete block')
                            print('falls_i.r = %d, falls_i.l = %d'%(falls_i.r,falls_i.l))
                        # incomplete n-th cycle, incomplete block  
                        block_size = falls_i.r-falls_i.l+1
                        if DEBUG:
                            print('block_size = falls_i.r-falls_i.l+1: %d'%(block_size))
                        if block_size > 0:
                            rem_block = falls_i.local_len%block_size
                        else:
                            raise Exception('Problem dimension is smaller than Np. Reduce Np or Increase problem size.')

                        if falls_i.dist == 'b':
                            temp += (range(falls_i.l,falls_i.r+1),)
                        else:
                            i_left = falls_i.l+(falls_i.n-1)*falls_i.s
                            i_rght = falls_i.l+(falls_i.n-1)*falls_i.s+rem_block
                            temp += (range(i_left,i_rght),)
                            # temp += (range(falls_i.l+(falls_i.n-1)*falls_i.s,falls_i.l+(falls_i.n-1)*falls_i.s+rem_block),)
            else:
                print('falls instance is not Falls type.')
                
            # store temp in ind
            ind[i] = temp
                
    else:
        raise Exception('ERROR(get_global_ind): Only objects up to 4-D are supported')

    if DEBUG:
        # print(ind)
        print('<-- Exiting get_global_ind')

    return ind

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

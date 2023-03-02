import numpy as np

def partition_1d(n,m):
    """Calculate data distribution in 1 dimensional space with MPI processes.
    It distributes n elements over m processes uniformly if n is divisible by m.
    If not, the remainder is distributed one element per each MPI process, starting
    the lowest process, MPI rank 0.
    
    Usage: 
    ------
    
    d_index,d_sizes = partition_1d(n,m)
    
    n: number of elements to be distributed
    m: number of MPI processes
    
    d_index: the beginning and ending indices of a partition assigned to each
             MPI processes
    d_sizes: the number of elements assigned to each MPI process
    
    """
    
    # Arrays to handle non-uniform data distribution
    d_sizes = np.zeros(m)
    
    # A dictionary to store the beginning and ending indices of each chunk
    # d_index['Pid']['beg'] and d_index['Pid']['end']
    d_index = dict()

    d_size = int(n/m)
    remainder = n%m

    # Calculate the number of elements per each MPI process
    if remainder:
        # if the size is NOT divisible by m
        icnt = 0
        for iam in range(m):
            d_index[iam] = dict()
            if icnt < remainder:
                d_index[iam]['beg'] = (d_size)*iam + icnt
                d_index[iam]['end'] = d_index[iam]['beg'] + d_size
                icnt = icnt + 1
            else:
                d_index[iam]['beg'] = (d_size)*iam + icnt
                d_index[iam]['end'] = d_index[iam]['beg'] + d_size - 1
    else:
        # if the size is divisible by m
        for iam in range(m):
            d_index[iam] = dict()
            d_index[iam]['beg'] = (d_size)*iam
            d_index[iam]['end'] = d_index[iam]['beg'] + d_size - 1
        
    # Store the chunk size for each MPI process    
    for iam in range(m):
        # Calculate the chunk size of each MPI process
        d_sizes[iam] = d_index[iam]['end'] - d_index[iam]['beg'] + 1

    return d_index,d_sizes

########################################################
# pPython: Parallel Python Programming Tool
# Python extension: Dr. Chansup Byun (cbyun@ll.mit.edu)
# Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
# Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
# MIT Lincoln Laboratory
########################################################
# Copyright (c) 2023, Massachusetts Institute of Technology All rights
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

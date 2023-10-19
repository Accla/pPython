import numpy as np
from math import ceil

from MPI_Send import *
from MPI_Recv import *

import pPython as GPC
from find import *

def multicast(src=None, dst=None, data=None):
    """
    MULTICAST  Sends data from a single source to multiple destinations.
    DATA = MULTICAST(SRC, DST, DATA) sends DATA from SRC to DST.
    DATA will be returned to all destinations as well as the
    source.  Note that SRC and DST cannot share any common ids
    that is, INTERSECT(SRC, DST) = [].
    
    This method uses O(log2(n)) messages, where n = length(DST).
    
    Author: Edmund Wong (elwong@ll.mit.edu)
    Python version: Dr. Chansup Byun (cbyun@ll.mit.edu)
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering multicast')
        print('Source type: %s'%(type(src)))
        print('Destination type: %s'%(type(dst)))
        print('maxGap = size(dst) / 2, %d'%(np.size(dst)/2))
        
    # Tag management.
    GPC.tag_num += 1
    GPC.tag = 'tag-'+str(GPC.tag_num)
    
    # Quick check
    if isinstance(src,type(None)) or isinstance(dst,type(None)):
        # Either src nor dst is not defined
        raise Exception('Error (multicast): either source or destination is not defined.')
    elif (len(src)==0) or (len(dst)==0):
        # Either src nor dst is empty
        raise Exception('Error (multicast): either source or destination is empty.')
    elif isinstance(dst,list):
        if src == np.array(dst).all():
            # if src is equal to dst, no op
            if DEBUG:
                print('<-- Exiting multicast (no op due to src == dst)')
            return data
    
    # Initialize needed variables.
    gap = 1
    maxGap = np.size(dst)/2.
    # Assuming src and dst are list types, construct the whole list including src at the first location.
    dst = np.concatenate((np.array(src), np.array(dst)), axis=None)
    # Extract the index number since find() returns a list
    myIndex = find(dst == GPC.Pid)[0]
    
    if DEBUG:
        print(src)
        print(dst)
        print('Maximum Gap: %f'%(maxGap))
        print('Length of new dst list: %d'%(len(dst)))
        print('my index: %d'%(myIndex))

    # Communications pattern:
    #  1. dst(1)                    => dst(2)
    #  2. dst(1), dst(2)            => dst(3), dst(4)
    #  ...
    #  n. dst(1), ..., dst(2^(n-1)) => dst(2^(n-1)+1), ..., dst(2^n)
    #
    # Do this until the gap reaches more than halfway across the
    # destination list.
    while gap <= maxGap:
        # send from dst(i) to dst(i+gap)
        if myIndex < gap:
            if DEBUG:
                print('Case gap <= maxGap: Sending data to destination: %d'%(dst[myIndex+gap][0]))
                print(data)
            # Need to add [0] to extract the value from dst
            MPI_Send(dst[myIndex+gap][0], GPC.tag, GPC.comm, data)
        elif myIndex < 2*gap:
            if DEBUG:
                print('Case gap <= maxGap: Received data from source: %d'%(dst[myIndex-gap][0]))
            # Need to add [0] to extract the value from dst
            [data] = MPI_Recv(dst[myIndex-gap][0], GPC.tag, GPC.comm)
            if DEBUG:
                print(data)
        gap = gap*2
    
    # Finish off any remaining destinations.
    if myIndex < np.size(dst)-gap:
        if DEBUG:
            print('Finish: Sending data to destination: %d'%(dst[myIndex+gap][0]))
            print(data)
        MPI_Send(dst[myIndex + gap][0], GPC.tag, GPC.comm, data)
    elif myIndex >= gap:
        if DEBUG:
            print('Finish: Received data from source: %d'%(dst[myIndex-gap][0]))
        [data] = MPI_Recv(dst[myIndex-gap][0], GPC.tag, GPC.comm)
        if DEBUG:
            print(data)

    if DEBUG:
        print('<-- Exiting multicast')

    return data

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

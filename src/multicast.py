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
        
    # Tag management.
    GPC.tag_num += 1
    GPC.tag = 'tag-'+str(GPC.tag_num)
    
    # Quick check
    if (not src) or (not dst):
        # Either src nor dst is not defined or empty
        # no op
        if DEBUG:
            print('<-- Exiting multicast')
        return data
    elif (src == dst):
        # if src is equal to dst, no op
        if DEBUG:
            print('<-- Exiting multicast')
        return data
    
    # Initialize needed variables.
    gap = 1
    maxGap = len(dst)/2.
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
                print('Sending data to destination: %d'%(dst[myIndex+gap][0]))
                print(data)
            # Need to add [0] to extract the value from dst
            MPI_Send(dst[myIndex+gap][0], GPC.tag, GPC.comm, data)
        elif myIndex < 2*gap:
            # Need to add [0] to extract the value from dst
            [data] = MPI_Recv(dst[myIndex-gap][0], GPC.tag, GPC.comm)
            if DEBUG:
                print('Received data from source: %d'%(dst[myIndex-gap][0]))
                print(data)
        gap = gap*2
    
    # Finish off any remaining destinations.
    if myIndex < len(dst)-gap:
        if DEBUG:
            print('Sending data to destination: %d'%(dst[myIndex+gap][0]))
            print(data)
        MPI_Send(dst[myIndex + gap][0], GPC.tag, GPC.comm, data)
    elif myIndex >= gap:
        [data] = MPI_Recv(dst[myIndex-gap][0], GPC.tag, GPC.comm)
        if DEBUG:
            print('Received data from source: %d'%(dst[myIndex-gap][0]))
            print(data)

    if DEBUG:
        print('<-- Exiting multicast')

    return data


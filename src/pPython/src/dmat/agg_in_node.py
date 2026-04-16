import os
import numpy as np
from sympy.ntheory import factorint
from timeit import default_timer as timer

from MPI_Recv import *
from MPI_Send import *

import pPython as GPC

def agg_in_node(d):
    """
    The first part of topology-aware AGG, which aggregates the parts of a distributed matrix on
    the leader processor within a node using an extended binary tree of a given list of Pids.

    This is a generalization of binary-tree based aggregation when the number of processes
    on a node is NOT a power of two number.
    
    This functions increments GLOBAL message TAG.

    Date:   November 22, 2022
    Author: Dr. Chansup Byun (cbyun@ll.mit.edu)
    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    DEBUG_TIMING = 0
    if DEBUG or DEBUG_TIMING:
        time_start = timer()
        print('--> Entering agg_in_node')

    Np = GPC.Np
    Pid = GPC.Pid
    
    #increment tag
    GPC.tag_num += 1
    GPC.tag = 'tag-'+str(GPC.tag_num)
    
    ## Aggregation based on binary tree shown below
    #  Rank PIDMIN will collect the dmat among the processes on a node
    #  where PIDMIN is defined by the triples mode job launch
    #                          0
    #             0                          8               k = 4 (8 Units)
    #       0           4            8              12       k = 3 (4 Units)
    #    0     2     4     6     8      10      12     14    k = 2 (2 Units)
    #  0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  k = 1 (1 Unit)
    #
    if DEBUG:
        zero_clock = timer()
    # The folloiwng only works with the triples mode jobs
    # (Unique jobs available on LLSC environment)
    #
    # Obtain local Pid information (min and max Pid on each node):
    PIDMIN = int(os.getenv('PIDSTART'))
    PIDMAX = int(os.getenv('PIDEND'))
    
    #
    # Assuming contiguous but not a requirement
    local_pid_list = list(range(PIDMIN,PIDMAX+1))
    nproc = len(local_pid_list)
    
    if DEBUG:
        print('local process Pid list:',end='')
        print(local_pid_list)
        print('Length of local Pid list: %d'%(nproc))
    
    # Dictionary varialbe to hold the locally aggregated messages within a node
    send_buf = dict()
    # how to handle a GPU array?
    try:
        # assuming d.local is a GPU array and extract the value before sending.
        send_buf[0] = d.local.get()
    except:
        # Fallback to a CPU array
        send_buf[0] = d.local
    imsg_pos = 0

    if nproc == 1:
        # No in-node aggregation needed.
        # just return the local array packaged in a dictionary variable.
        if DEBUG or DEBUG_TIMING:
            time_end = timer() - time_start
            print('agg_in_node time: %f (sec)'%(time_end))
            print('local Pid list has only one Pid. Just return the local d.local array')
            print('<-- Exiting agg_in_node')
                # Non-leader prepares to send its local data
        return send_buf
    
    # Check if nproc is power of two
    if( (nproc & (nproc-1) == 0) and (nproc > 0)): 
        POTN = nproc
        # print('Nproc is %d'%(nproc))
    else:
        # nproc is NOT a power of two number
        # Find the next power of two number
        k = 0
        POTN = 1
        while ( Np > POTN):
            k = k + 1
            POTN = POTN * 2
        # print('The next power of two number is %d'%(POTN))
    # Generate a new binary tree using the power of two number
    tree = factorint(POTN, multiple=True)
    
    # Store Pid's that participates with msg communication at the current level
    pid_list = list(range(POTN))
    # Need to keep the initial Pid list to identify the messengers while moving up the binary tree optimization
    pid_keep = list(range(POTN))
    pid_post = list(range(POTN))    # Pid position in pid_list
    #
    btMax = len(tree)  # the max level of binary tree for a given POTN
    bt = 1  # the starting binary tree level
    
    if d.dim > 4:
        raise Exception('DMAT/AGG_IN_NODE: Only up to 4-D objects currently supported')
    dim = d.map['grid'].shape

    # if DEBUG:
    #     time_03 = timer()
    #     print('Initial op for local array for hierarchical agg: %f (sec)'%(time_03-time_01))

    # Now aggregate the message within each node, concurrently and independently.
    # Walk up the binary tree.
    while (bt <= btMax):
        # Compute msg units transferred at this level
        msgUnit = 2**(bt-1)
        # Find my Pid position in pid_list
        # (Search is limited to the active Pid list)
        # (There are ficticious virtual Pid numbers >= len(local_pid_list) when len(local_pid_list) != POTN)
        # pid_list(1:length(pid_post))
        #
        # Convert the actual Pid into a virtual Pid so that vPid ranges 0:len(local_pid_list)-1
        vPid = Pid - PIDMIN
        [tmp1] = np.where( np.array(pid_list[0:len(pid_post)]) == vPid)
        # tmp1 is an array 
        if (len(tmp1)):
            pid_pos = tmp1[0]
            # Pid participates in communication at this level
            if ( (pid_pos+1)%2 ):
                # Odd position from the left. In Python, first odd position is zero.
                # Receive message from my right neighbor, pid_list(pid_pos+1)
                fromRank = PIDMIN + pid_list[pid_pos+1]
                if DEBUG: print('  pid_pos+1 = %d, fromRank = %d)'%(pid_pos+1,fromRank))
                if fromRank in local_pid_list:  # Only receive data if fromRank is in the local processor list
                    # if DEBUG: print('agg_in_node() recv: Pid = %d, fromRank %d w/ msg unit = %d'%(Pid,fromRank,msgUnit))
                    # if DEBUG: time_04 = timer()
                    [recv_buf] = MPI_Recv(fromRank, GPC.tag, GPC.comm)
                    # if DEBUG:
                    #     time_05 = timer()
                    #     print('Time for MPI_Recv call: %f (sec)'%(time_05-time_04))
                    #
                    # Within a node, the binary tree aggregation continues to accumulate the data
                    # in the send_buf so that, at the end, the PIDMIN processor can send the locally
                    # aggregated result to the global leader (Pid 0 for now)
                    #
                    for imsg in range(len(recv_buf)):
                        send_buf[imsg_pos+imsg+1] = recv_buf[imsg]
                    imsg_pos = imsg_pos + len(recv_buf)
            else:
                # Even position from the left. In Python, first even position is one.
                # Send message to my left neighbor, pid_list(pid_pos-1)
                toRank = PIDMIN + pid_list[pid_pos-1]
                if Pid in local_pid_list: # Only send data if processor is in the local processor list
                    if DEBUG: print('agg_in_node() sent: Pid = %d, toRank %d w/ msg unit = %d'%(Pid,toRank,msgUnit))
                    if DEBUG: print('  len(send_buf) = %d' %(len(send_buf)))
                    MPI_Send(toRank, GPC.tag, GPC.comm, send_buf)           
        #
        # Prepare for the next level (reduce size in half)
        bt += 1
        pid_post = list(range(int(len(pid_post)/2)))   # Pid position in half at the next level
        for inp in range(len(pid_post)):
            pid_list[inp] = pid_list[2*inp]

    #  Return the send_buf at the end of the in-node aggregation.
    if Pid == PIDMIN: # agg() leader
        mat = send_buf
    else:
        try:
            # assuming d.local is a GPU array and extract the value before sending.
            mat = d.local.get()
        except:
            # Fallback to a CPU array
            mat = d.local
    
    if DEBUG or DEBUG_TIMING:
        time_end = timer() - time_start
        print('agg_in_node time: %f (sec)'%(time_end))
        print('<-- Exiting agg_in_node')
    
    return mat

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


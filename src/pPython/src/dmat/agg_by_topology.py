import os
import numpy as np
from sympy.ntheory import factorint
from timeit import default_timer as timer

from MPI_Recv import *
from MPI_Send import *

from grid import *
from size import *
from reconstruct import *
from agg_in_node import *

import pPython as GPC

def agg_by_topology(d):
    """
    Execute the first part and the second part of topology-aware AGG, which aggregates the parts of 
    a distributed matrix among the leader processors, one per each node, using an extended binary tree of 
    a given list of Pids.
    This is a generalization of binary-tree based aggregation when the number of processes
    is NOT a power of two number.
         
    Date:   November 22, 2022
    Author: Dr. Chansup Byun (cbyun@ll.mit.edu)
    Python version: Dr. Chansup Byun
    """
    Np = GPC.Np
    Pid = GPC.Pid
    comm = GPC.comm
    
    DEBUG = 0
    DEBUG_TIMING = 0
    if DEBUG or DEBUG_TIMING:
        print('--> Entering agg_by_topology')
        # print(comm)
    
    if (Np == 1):
        # If a single process run, no need to go further.
        # Just return the local data
        return d.local
    
    ## Part 1: Aggregation within a node
    
    # How to extract the Pid list of the leader process on each node?
    #
    leader_pid_list = list(sorted(set(comm['leader'])))
    if DEBUG or DEBUG_TIMING:
        print(' ')
        print('Part 1: Aggregation within a node')
    #
    # Aggregation within each node concurrently
    #
    if Pid in leader_pid_list:
        # I am one of the leader processes    
        # Complete the first part of agg() with the processes within a node
        # Then, move on to the 2nd part
        send_buf = agg_in_node(d)
        imsg_pos = len(send_buf)-1
    else:
        # I am NOT any of the leader processes
        # Complete the first part of agg() with the processes within a node
        # Then, no further operation needed. Just return my local portion of 
        # the distributed array, d
        return agg_in_node(d)
    
    ## Part 2: Aggregation among the leader processes
    
    if DEBUG or DEBUG_TIMING:
        time_part_2_start = timer()

    ## Aggregation based on binary tree shown below for the 2nd part of 
    #  topology-aware agg() among the leader processes across all the nodes
    #
    #  (Rank Pid 0 will collect the dmat among the leader processes on the nodes)
    #                          0
    #             0                          8               k = 4 (8 Units)
    #       0           4            8              12       k = 3 (4 Units)
    #    0     2     4     6     8      10      12     14    k = 2 (2 Units)
    #  0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  k = 1 (1 Unit)
    #
    
    #
    # The folloiwng only works with the triples mode jobs
    #
    # Obtain local Pid information (min and max Pid on each node):
    PIDMIN = min(leader_pid_list)
    PIDMAX = max(leader_pid_list)
    if DEBUG or DEBUG_TIMING:
        print('Part 2: Aggregation among the leader processes')
        print('PIDMIN = %d, PIDMAX = %d'%(PIDMIN,PIDMAX))
        print('leader_pid_list: ',end='')
        print(leader_pid_list)
    #
    # Assuming that Pid numbers are NOT contiguous
    nproc = len(leader_pid_list)

    if d.dim > 4:
        raise Exception('DMAT/agg_by_topology: Only up to 4-D objects currently supported')
    
    #dim[1] - number of grid rows, dim[2] - number of grid col
    temp_mat = dict()
    
    if (Pid == PIDMIN): # agg() leader process
        # unpack the locally aggregated data on the node into temp_mat dictionary variable
        if DEBUG:
            print('Number of local message to unpack: %d' %(len(send_buf)))
        for imsg in range(len(send_buf)):
            vPid = Pid+imsg  # Pid is contiguous within a node
            if d.dim==2:
                # Two dimensional array
                if DEBUG:
                    print('Msg from Pid = %d' %(vPid))
                # Find the position in the processor grid for the given Pid
                [i,j] = np.where(d.map.grid == vPid)
                i = int(i); j = int(j)
                if DEBUG:
                    print('i,j,imsg=%d,%d,%d'%(i,j,imsg))
                    print('len(send_buf) = %d'%(len(send_buf)))
                if i not in temp_mat:
                    temp_mat[i] = dict()
                temp_mat[i][j] = send_buf[imsg]                    

            elif d.dim==3:
                # Three dimensional array
                # Find the position in the processor grid for the given Pid
                [i,j,k] = np.where(d.map.grid == vPid)
                i = int(i); j = int(j); k = int(k)
                if DEBUG:
                    print('i,j,k,imsg=%d,%d,%d'%(i,j,k,imsg))
                    print('len(send_buf) = %d'%(len(send_buf)))
                if i not in temp_mat:
                    temp_mat[i] = dict()
                if j not in temp_mat[i]:
                    temp_mat[i][j] = dict()
                temp_mat[i][j][k] = send_buf[imsg]        
                        
            elif d.dim==4:
                # Four dimensional array
                # Find the position in the processor grid for the given Pid
                [i,j,k,m] = np.where(d.map.grid == vPid)
                i = int(i); j = int(j); k = int(k); m = int(m)
                if DEBUG:
                    print('i,j,k,m,imsg=%d,%d,%d'%(i,j,k,m,imsg))
                    print('len(send_buf) = %d'%(len(send_buf)))
                if i not in temp_mat:
                    temp_mat[i] = dict()
                if j not in temp_mat[i]:
                    temp_mat[i][j] = dict()
                if k not in temp_mat[i][j]:
                    temp_mat[i][j][k] = dict()
                temp_mat[i][j][k][m] = send_buf[imsg]        
    
    if nproc == 1:
        # No reduction across nodes is needed.
        # Update the distributed array, d, and return.
        if DEBUG_TIMING:
            time_part_2 = timer() - time_part_2_start
            print('Time for agg part 2: %f (sec)'%(time_part_2))
        return reconstruct(d.pitfalls, d.map.grid, temp_mat, d.shape)
    
    # Fix the tag for the final aggregation among the node leaders
    # Since only part of the pPython processes are involved, it should not be chnaged.
    # Otherwise, the tag will be out of sync among the all pPython processes.
    # GPC.tag_num += 1
    # GPC.tag = 'tag-'+str(GPC.tag_num)
    
    # Check if nproc is power of two
    if( (nproc & (nproc-1) == 0) and (nproc > 0)):
        POTN = nproc
        if DEBUG:
            print('Nproc is %d'%(nproc))
    else:
        # nproc is NOT a power of two number
        # Find the next power of two number
        k = 0
        POTN = 1
        while ( nproc > POTN):
            k = k + 1
            POTN = POTN * 2
        if DEBUG:
            print('The next power of two number is %d'%(POTN))
    # Generate a new binary tree using the power of two number
    tree = factorint(POTN, multiple=True)
    
    # Store Pid's that participates with msg communication at the current level
    pid_list = list(range(POTN))
    # Need to keep the initial Pid list to identify the messengers while moving up the binary tree optimization
    pid_keep = list(range(POTN))
    pid_post = list(range(POTN))   # Pid position in pid_list
    #
    btMax = len(tree)  # the max level of binary tree for a given POTN
    bt = 1  # the starting binary tree level
    
    # Now aggregate the message among the nodes, concurrently and independently.
    # Only the leader process on each node gets involved.
    # Walk up the binary tree.
    while (bt <= btMax):
        if DEBUG:
            print(' ')
            print(' ')
            print('Reduction at level %d'%(bt))
        # Compute msg units transferred at this level
        msgUnit = 2**(bt-1)
        # Find my Pid position in pid_list
        # (Search is limited to the active Pid list)
        # (There are ficticious virtual Pid numbers >= len(leader_pid_list) when len(leader_pid_list) != POTN)
        # pid_list(1:length(pid_post))
        #
        # Convert the actual Pid into a virtual Pid so that vPid ranges 0:len(leader_pid_list)-1
        [tmp1] = np.where( np.array(leader_pid_list) == Pid)
        if DEBUG:
            print('Screen only for the leader processes:',end='')
            print(tmp1)
        # Screen only for the leader processes
        if len(tmp1):
            vPid = tmp1[0]  # With Python, vPos == vPid
            # To recover the actual Pid who sent message to me, use the mod()
            #
            [tmp2] = np.where(np.array(pid_list[0:len(pid_post)]) == vPid)
            if DEBUG:
                print('Virtual Pid location:',end='')
                print(tmp2)
            # tmp2 is an array 
            if len(tmp2):
                vPidPos = tmp2[0]
            else:
                print('No more message to send. Exitinting.')
                if DEBUG or DEBUG_TIMING:
                    time_part_2 = timer() - time_part_2_start
                    print('Time for agg part 2: %f (sec)'%(time_part_2))
                    print('<-- Exiting agg_by_topology')
                return d.local

            if DEBUG:
                print('vPisPos = %d' %(vPidPos))

            #if ~isempty(vPidPos)
            # Another screen to select only the Pid that
            # participates in communication at this level
            if ( (vPidPos+1)%2 ):
                # Odd position from the left. In Python, first odd position is zero.
                # Receive message from my right neighbor, pid_list(vPidPos+1)
                if DEBUG:
                    print('pid_list[vPidPos+1] = %d' %(pid_list[vPidPos+1]))
                [tmp3] = np.where( np.array(pid_keep) == pid_list[vPidPos+1])
                # tmp3 is an array 
                if len(tmp3):
                    myPidPos = tmp3[0]
                else:
                    raise Exception('ERROR(agg_by_topology): failed to find the Pid position when aggregating among the node leader processes')
                if DEBUG:
                    print('  myPidPos+1 = %d, fromRank = %d' %(myPidPos+1,pid_keep[myPidPos]))
                #CB if ~isempty(find(leader_pid_list==fromRank))
                # Only receive data if fromRank is in the leader processor list
                if myPidPos < nproc:
                    # Recover the real Pid
                    fromRank = leader_pid_list[myPidPos]
                    if DEBUG:
                        print('agg_by_topology() recv: Pid = %d, fromRank %d, msg tag = %s w/ msg unit = %d' %(Pid,fromRank,GPC.tag,msgUnit))
                    [recv_buf] = MPI_Recv(fromRank, GPC.tag, GPC.comm)
                    # if DEBUG:
                    #     print('  len(recv_buf) = %d' %(len(recv_buf)))
                    #
                    # Across the nodes, the binary tree aggregation continues to accumulate the data
                    # in the send_buf so that, at the end, the leader processor in each node can send the locally
                    # aggregated result to the global leader (Pid 0 for now) in a binary tree reduction 
                    #
                    if (Pid == PIDMIN): # agg() leader process
                        # Unpack the message into temp_mat
                        for imsg in range(len(recv_buf)):
                            vPid = fromRank+imsg   # virtual Pid of the sender in the leader Pid list.
                            if d.dim==2:
                                # Two dimensional array
                                # print('Msg from Pid = %d' %(pid_keep[recvPidPos+imsg]))
                                # Find the position in the processor grid for the given vPid
                                [i,j] = np.where(d.map.grid == vPid)
                                if DEBUG:
                                    print('i,j,imsg=%d,%d,%d'%(i,j,imsg),end='')
                                    print('len(recv_buf) = %d'%(len(recv_buf)))
                                    # print(recv_buf)
                                i = int(i); j = int(j)
                                if i not in temp_mat:
                                    temp_mat[i] = dict()
                                temp_mat[i][j] = recv_buf[imsg]
                            elif d.dim==3:
                                # Three dimensional array
                                # Find the position in the processor grid for the given vPid
                                [i,j,k] = np.where(d.map.grid == vPid)
                                i = int(i); j = int(j); k = int(k)
                                if i not in temp_mat:
                                    temp_mat[i] = dict()
                                if j not in temp_mat[i]:
                                    temp_mat[i][j] = dict()
                                temp_mat[i][j][k] = recv_buf[imsg]
                            elif d.dim==4:
                                # Four dimensional array
                                # Find the position in the processor grid for the given vPid
                                [i,j,k,m] = np.where(d.map.grid == vPid)
                                i = int(i); j = int(j); k = int(k); m = int(m)
                                if i not in temp_mat:
                                    temp_mat[i] = dict()
                                if j not in temp_mat[i]:
                                    temp_mat[i][j] = dict()
                                if k not in temp_mat[i][j]:
                                    temp_mat[i][j][k] = dict()
                                temp_mat[i][j][k][m] = recv_buf[imsg]
                    else:
                        # Others puts the received msg to a buffer for the next level
                        # msg aggregation. Always store the local first and then, the
                        # msg from the right neighbors sequentially
                        for imsg in range(len(recv_buf)):
                            send_buf[imsg_pos+imsg+1] = recv_buf[imsg]
                        imsg_pos = imsg_pos + len(recv_buf)
            else:
                # Even position from the left. In Python, first even position is one.
                # Send message to my left neighbor, leader_pid_list(vPos-1) among the leader processes
                [tmp3] = np.where( np.array(pid_keep) == pid_list[vPidPos-1])
                # tmp3 is an array 
                if DEBUG:
                    print('Even position from the left',end='')
                    print(tmp3)
                if len(tmp3):
                    myPidPos = tmp3[0]
                else:
                    raise Exception('ERROR(agg_by_topology): failed to find the Pid position when aggregating among the node leader processes')
                if DEBUG:
                    print('pid_list[vPidPos-1] = %d' %(pid_list[vPidPos-1]))
                toRank = leader_pid_list[myPidPos]
                if Pid in leader_pid_list: # Only send data if processor is in the leader process list
                    MPI_Send(toRank, GPC.tag, GPC.comm, send_buf)
                    if DEBUG:
                        print('  len(send_buf) = %d' %(len(send_buf)))
                        print('agg_by_topology() sent: Pid = %d, toRank %d, msg tag = %s w/ msg unit = %d' %(Pid,toRank,GPC.tag,msgUnit))

        #
        # Prepare for the next level (reduce size in half)
        bt = bt + 1
        pid_post = list(range(int(len(pid_post)/2)))   # Pid position in half at the next level
        for inp in range(len(pid_post)):
            pid_list[inp] = pid_list[2*inp]
        if DEBUG:
            print('Next pid_post for communication: ',end='')
            print(pid_post)
            print('Next pid_list for communication: ',end='')
            print(pid_list[0:len(pid_post)])
    #
    # Finalize on the leader processor
    if (Pid == PIDMIN): # agg() leader
        # Reconstruct the matrix from the local pieces
        # This is a NO-OP for block distributions
        mat = reconstruct(d.pitfalls, d.map.grid, temp_mat, d.shape)
    else:
        mat = d.local
    
    if DEBUG or DEBUG_TIMING:
        time_part_2 = timer() - time_part_2_start
        print('Time for agg part 2: %f (sec)'%(time_part_2))
        print('<-- Exiting agg_by_topology')

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


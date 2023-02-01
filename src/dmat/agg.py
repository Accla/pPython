import numpy as np
from sympy.ntheory import factorint
from timeit import default_timer as timer

from MPI_Recv import *
from MPI_Send import *

import pPython as GPC
from Dmat import *

from inmap import *
from reconstruct import *


def agg(d, leader=None):
    """Hierarchical agg() aggregates the parts of a distributed matrix on the leader processor
     using an extended binary tree..
    
     AGG(D) aggregates the parts of a distributed matrix into a whole and 
     returns it as a regular matrix.
     If the current processor is the LEADER, returns the aggreagated matrix, 
     otherwise, returns the local part.
     
     This functions increments GLOBAL message TAG.
    
     NOTE: Currently, it doesn't matter whether or not the leader is in the
     map - the global matrix is returned on the leader regardless. 

     Hierarchical AGG(D) is a generalization of binary-tree based AGG(D) when Np is NOT a power of two.
 
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    2010-05-03: Binary-tree based aggregation algoritm implemented in pMatlab
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering agg')

    if not isinstance(d,Dmat):
        return d

    Pid = GPC.Pid
    Np = GPC.Np
    # Return immediately if Np = 1
    if Np == 1:
        mat = d.local
        return mat
    
    # Set the leader for aggregation
    if hasattr(GPC, 'leader'):
        # GPC has attribute, leader, defined.
        map_leader = GPC.leader
    if leader:
        map_leader = leader
    
    # increment tag
    if hasattr(GPC, 'leader'):
        GPC.tag_num += 1
    else:
        GPC.tag_num = 0
    GPC.tag = 'tag-'+str(GPC.tag_num)
    
    # Aggregation based on binary tree shown below
    #
    #  (Rank 0 will collect the result if pMATLAB.leader = 0)
    #                          0
    #             0                          8               k = 4 (8 Units)
    #       0           4            8              12       k = 3 (4 Units)
    #    0     2     4     6     8      10      12     14    k = 2 (2 Units)
    #  0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  k = 1 (1 Unit)
    #
    if DEBUG:
        zero_clock = timer()
    # Check if Np is power of two
    if( (Np & (Np-1) == 0) and (Np > 0)): # number is power of 2 
        POTN = Np
    else:
        # Np is NOT a power of two
        # Find the next power of two number
        k = 0
        POTN = 1
        while ( Np > POTN):
            k = k + 1
            POTN = POTN * 2
    # Generate a new binary tree using the next power of two number
    tree = factorint(POTN, multiple=True)

    pidList = list(range(POTN))  # Store Pid's that participates with msg communication at the current level
    if map_leader > 0:
        # Shift the pidList so that GPC.leader (map_leader) be at the 1st position of pidList
        # Keep the fictitious nodes at the end
        # Only move the real Pid's around
        pidList[0:Np-map_leader]   = list(range(map_leader,Np)) 
        pidList[Np-map_leader:Np] = list(range(map_leader))
        
    # Need to keep the initial Pid list to identify the messengers while moving up the binary tree optimization
    # This is not a separate memory location: pidKeep = pidList;
    pidKeep = list(range(POTN))  
    pidPost = list(range(POTN))   # Pid position in pidList
    # 
    btMax = len(tree)   # the max level of binary tree for a given POTN
    bt = 1   # the starting binary tree level

    if d.dim > 4:
        raise Exception('DMAT/AGG: Only up to 4-D objects currently supported')
        
    dim = d.map.grid.shape
    # dim(1) - number of processor grid rows, dim(2) - number of grid col
    totalProcs = 1
    for i in range(len(dim)):
        totalProcs = totalProcs * dim[i]

    if (totalProcs < Np):
        # If totalProcs doesn't match with Np, use the old serialized agg()
        print('agg: something went wrong with the hierachical agg. switched back to old agg.')
        return oagg(d)

    if DEBUG:
        time_01 = timer()
        print('Setup time for hierarchical agg: %f (sec)'%(time_01-zero_clock))

    # Generate relation between process rank and grid map
    # gridIndex = mapGridRank(d);
    # No need to create this array, use np.where with d.map.grid processor grid array
    # For example, 2-D array
    # [i,j] = np.where(dmat_proc_grid == 3)

    # Create a temporary buffer, temp_mat, as a multi-level dictionary variable
    temp_mat = dict()

    if (Pid == map_leader):   # agg() leader
        # local data
        if d.dim==2:
            # Two dimensional array
            # Find the position in the processor grid for the given Pid
            [i,j] = np.where(d.map.grid == Pid)
            # i & j are np.array
            i = int(i); j = int(j)
            # if DEBUG: 
            #     print('Process position [i,j] = [%d, %d]'%(i,j))
            #     print('Type: %s'%(type(i)))
            if i not in temp_mat:
                temp_mat[i] = dict()
            if j not in temp_mat[i]:
                temp_mat[i][j] = dict()
            temp_mat[i][j] = d.local
        elif d.dim==3:
            # Three dimensional array
            # Find the position in the processor grid for the given Pid
            [i,j,k] = np.where(d.map.grid == Pid)
            i = int(i); j = int(j); k = int(k)
            # if DEBUG: print('Process position [i,j,k] = [%d,%d,%d]'%(i,j,k))
            if i not in temp_mat:
                temp_mat[i] = dict()
            if j not in temp_mat[i]:
                temp_mat[i][j] = dict()
            if k not in temp_mat[i][j]:
                temp_mat[i][j][k] = dict()
            temp_mat[i][j][k] = d.local
        elif d.dim==4:
            # Four dimensional array
            # Find the position in the processor grid for the given Pid
            [i,j,k,m] = np.where(d.map.grid == Pid)
            i = int(i); j = int(j); k = int(k); m = int(m)
            # if DEBUG: print('Process position [i,j,k,m] = [%d,%d,%d,%d]'%(i,j,k,m))
            if i not in temp_mat:
                temp_mat[i] = dict()
            if j not in temp_mat[i]:
                temp_mat[i][j] = dict()
            if k not in temp_mat[i][j]:
                temp_mat[i][j][k] = dict()
            if m not in temp_mat[i][j][k]:
                temp_mat[i][j][k][m] = dict()
            temp_mat[i][j][k][m] = d.local
        else:
            raise Exception('Error (agg): d.dim>4. it should not be here.')
    else:
        # Non-leader returns the local data
        mat = d.local
        # Non-leader prepares to send its local data
        sendBuf = dict()
        sendBuf[0] = d.local
        imsgLast = 0   # pointer to manage send buffer location

    # if DEBUG:
    #     time_03 = timer()
    #     print('Initial op for local array for hierarchical agg: %f (sec)'%(time_03-time_01))

    # Walk up the binary tree.
    while (bt <= btMax):
        # Compute msg units transferred at this level
        msgUnit = 2**(bt-1)
        # Find my Pid position in pidList
        # (Search is limited to the active Pid list)
        # (There are ficticious Pid numbers >= Np when Np != POTN)
        # pidList[1:len(pidPost)]
        [tmp1] = np.where( np.array(pidList[0:len(pidPost)]) == Pid)
        # tmp1 is an array 
        if (len(tmp1)):
            myPidPos = tmp1[0]
            # Pid participates in communication at this level
            if ( (myPidPos+1)%2 ):
                # Odd position from the left. In Python, first odd position is zero.
                # Receive message from my right neighbor, pidList(myPidPos+1)
                fromRank = pidList[myPidPos+1]
                if DEBUG: print('  myPidPos+1 = %d, fromRank = %d)'%(myPidPos+1,fromRank))
                if inmap(d.map, fromRank):  # Only receive data if fromRank is in the map
                    # if DEBUG: print('agg() recv: Pid = %d, fromRank %d w/ msg unit = %d'%(Pid,fromRank,msgUnit))
                    # if DEBUG:
                    #     time_04 = timer()
                    [recvBuf] = MPI_Recv(fromRank, GPC.tag, GPC.comm)
                    # if DEBUG:
                    #     time_05 = timer()
                    #     print('Time for MPI_Recv call: %f (sec)'%(time_05-time_04))

                    # if DEBUG: print('  len(recvBuf) = %d' %(len(recvBuf)))
                    if (Pid == map_leader):
                        # agg() leader puts the received msg into temp dmat
                        # imsg represents the number of Pid's who sent messages to me
                        # To recover the actual Pid who sent message to me, use the mod()
                        #
                        [tmp2] = np.where( np.array(pidKeep[0:Np]) == fromRank)
                        # tmp2 is an array 
                        if len(tmp2):
                            recvPidPos = tmp2[0]
                            for imsg in range(len(recvBuf)):
                                if d.dim==2:
                                    # Two dimensional array
                                    # if DEBUG: print('imsg=%s, Msg from Pid = %d' %(imsg,pidKeep[recvPidPos+imsg]))
                                    # Find the position in the processor grid for the given Pid
                                    [i,j] = np.where(d.map.grid == pidKeep[recvPidPos+imsg])
                                    i = int(i); j = int(j)
                                    if DEBUG:
                                        print('i,j,imsg=%d,%d,%d'%(i,j,imsg))
                                        print('len(recvBuf) = %d'%(len(recvBuf)))
                                    if i not in temp_mat:
                                        temp_mat[i] = dict()
                                    temp_mat[i][j] = recvBuf[imsg]
                                elif d.dim==3:
                                    # Three dimensional array
                                    [i,j,k] = np.where(d.map.grid == pidKeep[recvPidPos+imsg])
                                    i = int(i); j = int(j); k = int(k)
                                    if i not in temp_mat:
                                        temp_mat[i] = dict()
                                    if j not in temp_mat[i]:
                                        temp_mat[i][j] = dict()
                                    temp_mat[i][j][k] = recvBuf[imsg]
                                elif d.dim==4:
                                    # Four dimensional array
                                    [i,j,k,m] = np.where(d.map.grid == pidKeep[recvPidPos+imsg])
                                    i = int(i); j = int(j); k = int(k); m = int(m)
                                    if i not in temp_mat:
                                        temp_mat[i] = dict()
                                    if j not in temp_mat[i]:
                                        temp_mat[i][j] = dict()
                                    if k not in temp_mat[i][j]:
                                        temp_mat[i][j][k] = dict()
                                    temp_mat[i][j][k][m] = recvBuf[imsg]
                                    # if DEBUG: print('i,j,k,m = %d,%d,%d,%d '%(i,j,k,m))
                    else:
                        # Others puts the received msg to a buffer for the next level
                        # msg aggregation. Always store the local first and then, the
                        # msg from the right neighbors sequentially
                        for imsg in range(len(recvBuf)):
                            sendBuf[imsgLast + imsg+1] = recvBuf[imsg]
                        imsgLast = imsgLast + len(recvBuf)
            else:
                # Even position from the left. In Python, first even position is one.
                # Send message to my left neighbor, pidList(myPidPos-1)
                toRank = pidList[myPidPos-1]
                if inmap(d.map, Pid):   # Only send data if processor is in the map
                    # if DEBUG: print('agg() sent: Pid = %d, toRank %d w/ msg unit = %d'%(Pid,toRank,msgUnit))
                    # if DEBUG: print('  len(sendBuf) = %d' %(len(sendBuf)))
                    MPI_Send(toRank, GPC.tag, GPC.comm, sendBuf);           
        #
        # Prepare for the next level (reduce size in half)
        bt = bt + 1
        pidPost = list(range(int(len(pidPost)/2)))   # Pid position in half at the next level
        for inp in range(len(pidPost)):
            pidList[inp] = pidList[2*inp]

    # Finalize on the leader processor
    if (Pid == map_leader):   # agg() leader
        # Reconstruct the matrix from the local pieces
        # This is a NO-OP for block distributions
        mat = reconstruct(d.pitfalls,  d.map.grid, temp_mat, d.shape)

    if DEBUG:
        time_02 = timer()
        print('Collection time for hierarchical agg: %f (sec)'%(time_02-time_01))
        print('d.local.shape')
        print(d.local.shape)
        print('mat.shape')
        print(mat.shape)
        print('--> Exiting agg')
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

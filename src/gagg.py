import numpy as np
from sympy import primefactors,factorint

from RecvMsg import *
from SendMsg import *

import pPython as GPC
from D4M.assoc import Assoc

from gagg_add import *

def gagg(m,dest=0,ops='+',plist=None):
    """GAGG(m) gathers the parts of an array on the leader processor
    or does global reduction on a variable on the leader processor.
    GAGG(M) gathers the parts of an array on the remote processes
    into a whole array on the leader process. 
    If the current processor is the LEADER, returns 
    the aggreagated array, otherwise, returns the 
    local part.
    
    This functions increments GLOBAL message TAG.

    GAGG(M)
    GAGG(M, Destination, Operator, pid_subset)
      M:  Data to be gathered
      Dest:      Destination where the data is to be gathered
                 With only M, Destination is Pid=0 by default
      Operator:  Operator to be used for the gather operation   
      pid_subset: List of Pid subset for the aggregation operation
                 Destination must be a member of pid_subset

    Author: Dr. Chansup Byun
    Python version: Dr. Chansup Byun
    """
 
    DEBUG = 0
    if DEBUG:
        print('--> Entering gagg')

    #  MPI information
    comm = GPC.comm
    Np = GPC.Np
    Pid = GPC.Pid
    
    if Np == 1:
         return m
    else:
        # increment tag
        GPC.tag_num += 1
        GPC.tag = 'tag-'+str(GPC.tag_num)

    # ops  = '+'                # Default operator
    if plist == None:
        # set loc_Np as Np for the full Pid list
        loc_Np = Np
        plist = list(range(Np)) # List of all process Pids by default
        is_subset = 0
    else:
        is_subset = 1            # Use a subset of Pid list for aggregation
        pid_subset = plist
        
        # Check if the destination is a member of pid_subset
        if dest not in pid_subset:
            raise Exception('gagg: the destination rank, %d, is not a member of the Pid subset list.'%(dest))

        # For mapping between pid_subset (list of real Pids) 
        # and imaginary virtual contiguous Pid list
        # Create the matching virtual Pid list, starting from 0.
        loc_Np = len(pid_subset)
        plist = list(range(loc_Np)) # List of process Pids
          
        # Example mapping: pid_subset = [ 5, 6, 7, 8, 9, 10] when loc_Np = 6
        #                  pids_comm    = [ 0, 1, 2, 3, 4, 5] 
        #       
        # Assuming there is only one dest in pid_subset, 
        # mapping between the virtual and real Pid, dest, is shown below.
        # Mapping to virtual Pid:  vPid = find(pid_subset==dest) - 1
        # Mapping to real Pid:     rPid = pid_subset(vPid+1)

    str_type = type(m)
    if not isinstance(m, (type(Assoc('','','')),type(Matrix.sparse(float)),float,np.float64,np.ndarray)): 
        raise Exception('Current gagg() does not support class, %s, object.'%(str_type))

    # Gathering based on binary tree shown below
    # 
    #   (Rank 0 will collect the result)
    #                           0
    #              0                          8               k = 4 (8 Units)
    #        0           4            8              12       k = 3 (4 Units)
    #     0     2     4     6     8      10      12     14    k = 2 (2 Units)
    #   0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  k = 1 (1 Unit)
    # 
    tree = primefactors(loc_Np)          
    # Check if loc_Np is power of two
    if (np.where(np.array(tree)==2))[0].size == len(tree):
        POTN = loc_Np
        # disp(['The Np is ', num2str(loc_Np)])
    else:
        # Np is NOT a power of two
        # Find the next closest power of two number
        k = 0
        POTN = 1
        while ( loc_Np > POTN):
            k = k + 1
            POTN = POTN * 2
        # (['The next power of two number is ', num2str(POTN)])
        # Generate a new binary tree using the next power of two number
    tree = factorint(POTN)  # factorint returns a dictionary with the key as the prime number & value as frequency
    btMax = tree[2]  # the max level of binary tree for a given POTN

    pids_comm = list(range(POTN)) # Store Pids that participates with msg communication at the current level
    #
    # Map dest into a virtual Pid when using pid_subset
    #
    if is_subset:
        # Virtual Pid for the destination:  vPid = find(pid_subset==dest) - 1
        loc_dest = np.where(np.array(pid_subset)==dest)[0][0]
    else:
        loc_dest = dest

    if DEBUG:
        print('gagg: local POTN (virtual if pid_subset used) = %d'%(POTN))
        print('gagg: local destination rank (virtual if pid_subset used) = %d'%(loc_dest))
        print('gagg: local Np (virtual if pid_subset used) = %d'%(loc_Np))

    if loc_dest > 0:
        # Shift the pids_comm so that the dest process be at the 1st position of pids_comm
        # Keep the fictitious nodes at the end
        # Only move the real Pid's around
        pids_comm[0:loc_Np-loc_dest] = list(range(loc_dest,loc_Np))
        pids_comm[loc_Np-loc_dest:loc_Np] = list(range(loc_dest))

    # Need to keep the initial Pid list to identify the messengers while moving up the binary tree optimization
    # pidKeep = pids_comm
    pidPost = list(range(POTN))  # Pid position in pids_comm

    bt = 1  # the starting binary tree level
    # Walk up the binary tree.
    while (bt <= btMax):
        # Find my Pid position in pids_comm
        # (Search is limited to the active Pid list)
        # (There are ficticious Pid numbers >= Np when Np != POTN)
        # pids_comm(1:length(pidPost))
        if is_subset:
            locPid = np.where(np.array(pid_subset)==Pid)[0][0]
        else:
            locPid = Pid

        # The following logic built on the assumpotion that the index of the 1st position is 1(one) in Matlab.
        # However, in Python, the index starts from 0 (zero). 
        # So if locPid is NOT in the current list of Pids in communication, myPidPos = -1
        try:
            myPidPos = np.where(np.array(pids_comm[0:len(pidPost)]) == locPid)[0][0]
        except:
            myPidPos = -1
        if (myPidPos>-1):
            # Pid participates in communication at this level
            if not (myPidPos%2):  # Identify even number Pids including 0
                # Receive message from my right neighbor, pids_comm(myPidPos+1)
                # only if my right neighbor is real Pid
                fromRank = pids_comm[myPidPos+1]
                if DEBUG:
                     print('  myPidPos+1 = %d, fromRank = %d'%(myPidPos+1,fromRank))
                if fromRank < loc_Np:  # Receive data only if fromRank is a REAL Pid
                    #
                    #Convert fromRank to the real Pid if is_subset
                    #
                    if is_subset:
                        # Real Pid can be retrieved by rPid = pid_subset(vPid+1)
                        fromRank = pid_subset[fromRank+1]
                    if DEBUG:
                        print('gagg() recv: Pid = %d fromRank %d'%(Pid,fromRank))
                    [m_recv] = RecvMsg(fromRank,GPC.tag)
                    m = gagg_add(m, m_recv, ops)
            else:  # Identify odd number Pids
                # Send message to my left neighbor, pids_comm(myPidPos-1)
                toRank = pids_comm[myPidPos-1]
                if toRank < loc_Np:  # Send data only if toRank is a REAL Pid
                    if is_subset:
                        # Real Pid can be retrieved by rPid = pid_subset(vPid+1)
                        toRank = pid_subset[toRank+1]
                    if DEBUG:
                        print('gagg() sent: Pid = %d toRank %d'%(Pid,toRank))
                        # res = whos('m')
                        # not sure what to use to calculate byte size yet
                        # print('             MsgSize(bytes) = ' num2str(res.bytes)])
                    SendMsg(toRank, GPC.tag, m)
        
        # Prepare for the next level (reduce size in half)
        bt += 1
        pidPost = list(range(int(len(pidPost)/2)))
        for idx in range(len(pidPost)):
            pids_comm[idx] = pids_comm[2*idx]

    if DEBUG:
        print('<-- Exiting gagg')

    return m

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

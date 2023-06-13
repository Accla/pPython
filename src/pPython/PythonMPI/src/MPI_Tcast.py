import os
import numpy as np
from sympy.ntheory import factorint
from timeit import default_timer as timer

from MPI_Recv import *
from MPI_Send import *
from gen_new_list import *

import pPython as GPC

def MPI_Tcast(source, dest, tag, comm, *argv):
    """Broadcast variables to everyone in destination list using a binary-tree.
 
    Usage:
    ======
    [var1,var2,...] = MPI_Tcast(source,dest,tag,comm,var1,var2,...)
 
    Broadcast variables to everyone in dest using a binary-tree communicaiton structure.
 
    Sender blocks until all the messages are received,
    unless pyMPI_Save_messages(1) has been called.
    
    Python version: Dr. Chansup Byun
    2023-05-31: First implementation
    """
    
    DEBUG = 0
    DEBUG_TIMING = 0
    if DEBUG or DEBUG_TIMING:
        time_start = timer()
        print('--> Entering MPI_Tcast.')
    
    # Get processor rank.
    Pid = GPC.Pid
    Np = GPC.Np
     
    ## Broadcast based on binary tree, where an example is shown below
    #  Source will send the message among the processes given as a destination list
    #  As the message level goes down, more processes are sending messages to their 
    #  corresponding pairs.
    #                          0
    #             0                          8               k = 4 (8 Units)
    #       0           4            8              12       k = 3 (4 Units)
    #    0     2     4     6     8      10      12     14    k = 2 (2 Units)
    #  0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  k = 1 (1 Unit)
    #    
    #
    # Check whether the source is in the destination 
    # and create a new list where the source is at the left most position
    #
    local_pid_list = gen_new_list(source, dest)
    nproc = len(local_pid_list)
    
    if DEBUG:
        print('local process Pid list:',end='')
        print(local_pid_list)
        print('Length of local Pid list: %d'%(nproc))
    
    if nproc == 1:
        # No in-node broadcast needed.
        # just return the message in a dictionary variable.
        if DEBUG or DEBUG_TIMING:
            time_end = timer() - time_start
            print('MPI_Tcast time: %f (sec)'%(time_end))
            print('local Pid list has only one Pid. Just return the local d.local array')
            print('<-- Exiting MPI_Tcast')
                # Non-leader prepares to send its local data
        return argv
    
    """
    # Dictionary varialbe to hold the message if there are multiple variables in the message
    if Pid == source:
        msg = dict()
        ii = 0
        if DEBUG:
            print('Length of argv: %d'%(len(argv)))
        for arg in argv:
            if DEBUG:
                print(arg)
            msg[ii] = arg
            ii = ii + 1
    """

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
    # Generate a new binary tree using the power of two number
    tree = factorint(POTN, multiple=True)
    if DEBUG:
        print('The next power of two number is %d'%(POTN))
        print('Tree:')
        print(tree)
    
    # Store Pid's that participates with msg communication at the current level
    # pid_list = list(range(POTN))
    #
    btMax = len(tree)  # the max level of binary tree for a given POTN
    bt = btMax        # the starting binary tree level

    # Now broadcast the message with the given Pid list, concurrently and independently.
    # Walk with the binary tree based on the communication level.
    proc_list_com_level = dict()
    for com_level in range(len(tree)):
        # Calculate the list of pairs to broadcast message at the given communication level
        proc_list_com_level[com_level] = []
        n_proc_pairs = 2**(com_level+1)
        proc_inc = POTN/(n_proc_pairs)
        # proc_inc = len(pid_list)/(n_proc_pairs)
        for i in range(n_proc_pairs):
            proc_list_com_level[com_level].append(int(proc_inc*i))
        if DEBUG:
            print('')
            # print('Message level: %d, Pid list at this level:'%(com_level))
            # print(proc_list_com_level[com_level])
    
        # Find my Pid position in proc_list_com_level
        # (Search is limited to the active Pid list)
        # (There are ficticious virtual Pid numbers >= len(local_pid_list) when len(local_pid_list) != POTN)
        #
        # Convert the actual Pid into a virtual Pid so that vPid ranges 0:len(local_pid_list)-1
        if Pid in local_pid_list:
            vPid = local_pid_list.index(Pid)
        else:
            # skip to the next communicaiton level
            continue
        [tmp1] = np.where( np.array(proc_list_com_level[com_level]) == vPid)
        # tmp1 is an array 
        # skip if vPid (or Pid) is not invoved at this communication level
        if (len(tmp1)):
            pid_pos = tmp1[0]
            if DEBUG:
                print('pid_pos: %d'%(pid_pos))
            # Pid participates in communication at this level
            if ( (pid_pos+1)%2 ):
                # Odd position from the left. In Python, first odd position is zero.
                # Send message to my neighbor to the right
                vPidPos = proc_list_com_level[com_level][pid_pos+1]
                if vPidPos < nproc:  # Only send data if toRank is in local_pid_list
                    toRank = local_pid_list[vPidPos]
                    if DEBUG: print('  pid_pos+1 = %d, toRank = %d)'%(pid_pos+1,toRank))
                    if DEBUG: print('  MPI_Tcast() send: Pid = %d, toRank %d'%(Pid,toRank))
                    if DEBUG_TIMING: time_04 = timer()
                    MPI_Send(toRank, tag, comm, argv)
                    if DEBUG_TIMING:
                        time_05 = timer()
                        print('    Time for MPI_Send call (sec): %f'%(time_05-time_04))
            else:
                # Even position from the left. In Python, first even position is one.
                # Receive message from my left neighbor in the virtual Pid list
                vPidPos = proc_list_com_level[com_level][pid_pos-1]
                if vPidPos < nproc: # Receive data only if processor is in the local processor list
                    fromRank = local_pid_list[vPidPos]
                    if DEBUG: print('  MPI_Tcast() received: Pid = %d, fromRank %d'%(Pid,fromRank))
                    if DEBUG_TIMING: time_06 = timer()
                    [argv] = MPI_Recv(fromRank, tag, comm)  
                    if DEBUG_TIMING:
                        time_07 = timer()
                        print('    Time for MPI_Recv call (sec): %f'%(time_07-time_06))
                # Note: the received msg may be sent to my neighbor at the next communicaiton level
    
    if DEBUG or DEBUG_TIMING:
        time_end = timer() - time_start
        if DEBUG:
            print('argv: ')
            print(argv)
        else:
            print('MPI_Tcast time (sec): %f'%(time_end))
        print('<-- Exiting MPI_Tcast')
    
    return argv


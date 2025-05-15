import os
from timeit import default_timer as timer
import sys

import checkOS as OS
from dict_with_pickle import save_dict_to_pickle
from pyMPI_Buffer_file import *
from pyMPI_Lock_file import *
from pyMPI_Sleep import *
from pyMPI_Wait import *
from MPI_Comm_rank import *
from MPI_Comm_size import *
from MPI_Recv import *
from MPI_Tcast import *

def MPI_Bcast( source, tag, comm, *argv ):
    """MPI_Bcast - broadcast variables to everyone.

    Usage:
    ------
    var1, var2, ... = MPI_Bcast( source, tag, comm, var1, var2, ...)

    Broadcast variables to everyone in comm.

    Sender blocks until all the messages are received,
    unless MatMMPI_Save_messages(1) has been called.

    source: an iteger from 0 to comm_size-1
    tag:    any integer
    comm:   MPI communicator  (dtype: dictionary)
    var1,var2,...: variable number of MPI messages 
    
    Python version: Dr. Chansup Byun
    """
    DEBUG = 0
    DEBUG_TIMING = 0
    if DEBUG or DEBUG_TIMING:
        t_start = timer()
        print('--> Entering MPI_Bcast.')
    
    # Get processor rank.
    my_rank = MPI_Comm_rank(comm)
    comm_size = MPI_Comm_size(comm)

    if comm_size == 1:
        return argv

    # Check whether to use local filesystem or not
    grid_config = comm['grid_config']
    # Check if using mixed messaging kernels for interactive triples mode jobs
    if DEBUG:
        mixed_fs = grid_config['mixed_fs']
    if grid_config['local_fs'] == 1 :
        local_fs  = 1
        tmpdir = comm['tmpdir']
        # MPI_COMM_WORLD['machine_db']['machine'] is defined as a dictionary in pyMPI_Comm_init()
        machines =  comm['machine_db']['machine']  
        pidlist  = comm['group']
    else:
        local_fs  = 0

    if DEBUG:
        if local_fs:
            print('Use local filesystem:')

    # Set some strings for special characters.
    qq = '"'
    sp = ' '
    nl = '\n'
    # Get single quote character. 
    q = '\''
    dir_sep = os.sep

    if local_fs:
        ##
        # Use local filesystem
        # Stage 1: Message broadcast to the leader process at the node level:
        # The leader processor on each node receives the broadcast message from the source
        #
        leader = comm['leader']
        destOON = set(leader)
        if DEBUG:
            print('--> Calling MPI_Tcast among the leaders of each compute node.')
            print('--> leader:',end=" ")
            print(leader)
            print(" ")
            print('--> Destination:',end=" ")
            print(destOON)
            print(" ")
        #
        # ToDO: If source is not a member of destOON, check the following work?
        #
        if (my_rank == source) or (my_rank in destOON):
            # Communicaiton among source and the leader processes on each node
            [argv] = MPI_Tcast(source, destOON, tag, comm, argv)

        if DEBUG or DEBUG_TIMING:
            t_end_s1 = timer()
            if DEBUG:
                print('argv:')
                print(argv)
            elif DEBUG_TIMING:
                id = 0
                for arg in argv:
                    print('  MsgID: %d, size: %d'%(id,sys.getsizeof(arg)))
                    id += 1
                print('  MPI_Bcast: Time for broadcasting the message among the leader processes (sec): %f'%(t_end_s1-t_start))
            print('<-- Stage 1 finished MPI_Tcast among node leaders.')

        ##
        # Stage 2:
        # The leader on each node broadcast the message to other processses on the same node
        # Now all processes are calling MPI_Tcast() with different source and destination
        #
        # Figure out the list of processes on the same nodes
        # my compute node
        machine_id_rank = comm['machine_id'][my_rank]
        hostname = machines[machine_id_rank]
        # list of Pid's on the same compute node
        destINN = comm['local_pids'][hostname]
        # source is the smallest Pid among the destination
        source = min(destINN)
        if DEBUG:
            #
            # With the triples mode, we need to use machine id, instead of rank.
            #
            if mixed_fs and my_rank == 0:
                print('--> MPI_Bcast: source rank = %d, host = %s' %(my_rank,machines[machine_id_rank]))
            else:
                print('--> MPI_Bcast: source rank = %d, host = %s, local path = %s' %(my_rank,machines[machine_id_rank],tmpdir[machine_id_rank]))
            print('--> calling MPI_Tcast among the processes on the same compute node.')
            print('')
            print('source: %d' %(source))
            print('destination:',end=" ")
            print(destINN)
            print(" ")
        #
        # Communicaiton within a node
        # The leader on each node broadcast the message to the oters on the same node
        [argv] = MPI_Tcast(source, destINN, tag, comm, argv)
        if DEBUG or DEBUG_TIMING:
            t_end_s2 = timer()
            if DEBUG:
                print('argv:')
                print(argv)
            elif DEBUG_TIMING:
                id = 0
                for arg in argv:
                    print('  MsgID: %d, size: %d'%(id,sys.getsizeof(arg)))
                    id += 1
                print('  MPI_Bcast: Time for broadcasting the message among the processes within a ndoe (sec): %f'%(t_end_s2-t_end_s1))
            print('<-- Stage 2 finished MPI_Tcast among processes on the same compute node.')

    else:
        if DEBUG:
            print('Original broadcasting algorithm (no optimization)')
        # Original broadcasting algorithm (no optimization)
        # ToDo: 
        # Broadcasting in a reverse binary tree (oposite to what is implemented in agg)
        #
        # If not the source, then receive the data.
        # Make sure to return a Python dictionary
        if my_rank != source:
            # MPI_Recv returns a list
            return MPI_Recv(source, tag, comm)
        #
        # Only source execute the following code
        #
        # If the source, then send the data.
        # Create data file [only once in the central filesystem]
        buffer_file = pyMPI_Buffer_file(my_rank,source,tag,comm)
            
        # Save varargin to file [Duplicated from MPI_Send()]
        # Save argv to file directly without creating intermediate dictionary array
        # Write the message into a file.
        save_dict_to_pickle(argv, buffer_file)
    
        # Loop over everyone in comm and create link to data file.
        if (OS.ispc):
            link_command = 'echo off'+nl
        else:
            link_command = ''
        for ii in range(0,comm_size):
            # Don't do source.
            if ii != source:
                # Create buffer link name.
                buffer_link = pyMPI_Buffer_file(my_rank,ii,tag,comm)
                if (OS.ismac):
                    # Append to link_command. MacOS sym links are not recognized by Linux.
                    link_command = link_command+'cp '+buffer_file+' '+buffer_link+nl
                elif (OS.islinux):
                    # Append to link_command.
                    link_command = link_command+'ln -s '+buffer_file+' '+buffer_link+nl
                elif (OS.ispc):
                    # Append to link_command.
                    link_command = link_command+'copy '+qq+buffer_file+qq+' '+qq+buffer_link+qq+nl
                else:
                    raise Exception('MPI_Bcast: none of ismac, islinux and ispc defined.')
    
        # Write unix commands to .sh text file
        # [Was used to fix Matlab's problem with very long commands sent to unix().
        # Maybe not applicable to Python but needs to check [ToDo]
        if OS.ispc:
            link_script = 'PythonMPI'+dir_sep+'Link_Commands_t'+str(tag)+'.bat'
        else:
            link_script = 'PythonMPI'+dir_sep+'Link_Commands_t'+str(tag)+'.sh'
        fid = open(link_script,'w')
        fid.write(link_command)
        fid.close()
        # Execute the link script.
        if (OS.ispc):
            os.startfile(link_script)
        else:
            os.system('/bin/bash '+link_script)
        #
        # Wait a little bit
        pyMPI_Sleep(0.5)
    
        # os.remove(link_script)
    
        # Loop over everyone in comm and create lock file.
        for ii in range(0,comm_size):
            # Don't do source.
            if ii != source:
                # Get lock file name.
                lock_file = pyMPI_Lock_file(my_rank,ii,tag,comm)
                # Create lock file.
                fid=open(lock_file,'w')
                fid.close()
    
        # Loop over lock files.
        # Loop over everyone in comm and create lock file.
        for ii in range(0,comm_size):
            # Don't do source.
            if ii != source:
                # Get lock file name.
                lock_file = pyMPI_Lock_file(my_rank,ii,tag,comm)
                # Spin on lock file until it is deleted.
                # Spin on lock file until it is created.
                # Wait until all lock files are gone, which means that all receiving processes
                # have received the broadcasted message
                pyMPI_Wait('MPI_Bcast', lock_file, True)
    
        # Now all processes have received the broadcasted message.
        # Check if the message is to be saved.
        if not(comm['save_message_flag']):
            # Delete the source buffer file.
            os.remove(buffer_file)
       
    if DEBUG:
        print('argv: ')
        print(argv)
        print('<-- Exiting MPI_Bcast.')
    return argv

########################################################
# MatlabMPI
# Dr. Jeremy Kepner
# MIT Lincoln Laboratory
# kepner@ll.mit.edu
########################################################
# Copyright 2002 Massachusetts Institute of Technology
#
# Permission is herby granted, without payment, to copy, modify, display
# and distribute this software and its documentation, if any, for any
# purpose, provided that the above copyright notices and the following
# three paragraphs appear in all copies of this software.  Use of this
# software constitutes acceptance of these terms and conditions.
#
# IN NO EVENT SHALL MIT BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
# SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
# THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF MIT HAS BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# MIT SPECIFICALLY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
#
# THIS SOFTWARE IS PROVIDED "AS IS," MIT HAS NO OBLIGATION TO PROVIDE
# MAINTENANCE, SUPPORT, UPDATE, ENHANCEMENTS, OR MODIFICATIONS.

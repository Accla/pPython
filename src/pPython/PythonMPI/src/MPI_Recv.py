import os
import sys
from timeit import default_timer as timer

from dict_with_pickle import load_dict_from_pickle
from pyMPI_Buffer_file import *
from pyMPI_Lock_file import *
from pyMPI_Sleep import *
from pyMPI_Wait import *
from MPI_Comm_rank import *

def MPI_Recv( source, tag, comm ):
    """MPI_Recv  -  Receives message from source.

    Usage:
    ------
    [var1, var2, ...] = MPI_Recv( source, tag, comm )

    Receives message from source with a given tag
    and returns the variables in the message as a list.

    source: an iteger from 0 to comm_size-1
    tag:    any integer
    comm:   an MPI Communicator (typically a copy of MPI_COMM_WORLD)

    Python version: Dr. Chansup Byun
    2022-12-05: Updated to support message kernel using local filesystem (Dr. Chansup Byun)
    """

    DEBUG = 0
    DEBUG_TIMING = 0
    if DEBUG or DEBUG_TIMING:
        t_start = timer()
        print('--> Entering MPI_Recv')
   
    # Get processor rank.
    my_rank = MPI_Comm_rank(comm)

    # read messages locally, which was securely transferred via scp from a remote host 
    # or saved by a local process on the same node.
    innode = 1
    grid_config = comm['grid_config']
    if grid_config['local_fs'] == 1 :
        local_fs = 1
        mixed_fs = grid_config['mixed_fs']
        tmpdir = comm['tmpdir']
        machines =  comm['machine_db']['machine']
        #
        # With the triples mode, we need to use machine id, instead of rank.
        #
        machine_id_dest = comm['machine_id'][my_rank]
        machine_id_source = comm['machine_id'][source]
        if DEBUG:
            print('With using local filesystem:')
            print(machines)
            print(tmpdir)
            print('source = %d, my rank = %d'%(source,my_rank))
            print('machine_id_source = %d, machine_id_dest = %d'%(machine_id_source,machine_id_dest))
        if machines[machine_id_source] != machines[machine_id_dest] :
            innode = 0
    else:
        local_fs = 0
        mixed_fs = 0

    if DEBUG:
        if innode == 0 :
            print('MPI_Recv: out-of-node message from source rank=%d to destination rank=%d'%(source,my_rank))
        else:
            print('MPI_Recv: in-node message from source rank=%d to destination rank=%d'%(source,my_rank))
        if local_fs:
            if not (mixed_fs and (machine_id_source == 0 or machine_id_dest == 0)):
                # only when message is exchanged between the compute nodes on the grid
                print('Use local filesystem:')
                print('--> MPI_Recv: source rank = %d, host = %s, local path = %s'%(source,machines[machine_id_source],tmpdir[machine_id_source])) 
                print('--> MPI_Recv: destination rank = %d, host = %s, local path = %s'%(my_rank,machines[machine_id_dest],tmpdir[machine_id_dest]))

    # Create buffer and lock files [updated to support message kernel using local filesystem]
    buffer_file = pyMPI_Buffer_file(source,my_rank,tag,comm,local_fs=local_fs,msg_type='recv',innode=innode)
    lock_file   = pyMPI_Lock_file(source,my_rank,tag,comm,local_fs=local_fs,msg_type='recv',innode=innode)
    if DEBUG or DEBUG_TIMING:
        print('  Buffer file: %s'%(buffer_file))
        print('  Lock file: %s'%(lock_file))

    # Spin on lock file until it is created.
    pyMPI_Wait('MPI_Recv', lock_file, False)
            
    # Spin on buffer file until it is created.
    pyMPI_Wait('MPI_Recv', buffer_file, False)
            
    if DEBUG_TIMING:
        t_st_2 = timer()
        print('  MPI_Recv: time to create message and lock files (sec): %f'%(t_st_2 - t_start))
    # Read all data out of buffer_file.
    buf = load_dict_from_pickle(buffer_file)
    
    # Delete buffer and lock files.
    if (not(comm['save_message_flag'])):
        os.remove(buffer_file);
        # pyMPI_Sleep(0.02)
        # If innode, the file is cross-referenced by the sender so that
        # the sender know that the message was received by the receiver on the same node
        # when it's removed.
        os.remove(lock_file);

    if DEBUG or DEBUG_TIMING:
        if DEBUG_TIMING:
            t_st_3 = timer()
            print('  MPI_Recv: time to receive message file (sec): %f'%(t_st_3 - t_st_2))
        elif DEBUG:
            print(buf.values())
        print('<-- Exiting MPI_Recv')
    # Get variable out of buf.
    return list(buf.values())

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

import os

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

    Python author: Dr. Chansup Byun
    2022-12-05: Updated to support message kernel using local filesystem (Dr. Chansup Byun)
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering MPI_Recv')
   
    # Get processor rank.
    my_rank = MPI_Comm_rank(comm)

    # read messages locally, which was securely transferred via scp from a remote host 
    # or saved by a local process on the same node.
    innode = 1
    grid_config = comm['grid_config']
    if grid_config['local_fs'] == 1 :
        local_fs  = 1;
        tmpdir = comm['tmpdir']
        machines =  comm['machine_db']['machine']
        if machines[my_rank] != machines[source] :
            innode = 0
    else:
        local_fs  = 0

    if DEBUG:
        if innode == 0 :
            print('MPI_Recv: out-of-node message from source rank=%d to destination rank=%d'%(source,my_rank))
        else:
            print('MPI_Recv: in-node message from source rank=%d to destination rank=%d'%(source,my_rank))
        if local_fs:
            print('Use local filesystem:')
            print('--> MPI_Recv: source rank = %d, host = %s, local path = %s'%(source,machines[source],tmpdir[source])) 
            print('--> MPI_Recv: destination rank = %d, host = %s, local path = %s'%(my_rank,machines[my_rank],tmpdir[my_rank]))

    # Create buffer and lock files [updated to support message kernel using local filesystem]
    buffer_file = pyMPI_Buffer_file(source,my_rank,tag,comm,local_fs=local_fs,msg_type='recv',innode=innode)
    lock_file   = pyMPI_Lock_file(source,my_rank,tag,comm,local_fs=local_fs,msg_type='recv',innode=innode)
    if DEBUG:
        print('Buffer file: %s'%(buffer_file))
        print('Lock file: %s'%(lock_file))

    # Spin on lock file until it is created.
    pyMPI_Wait('MPI_Recv', lock_file, False)
            
    # Spin on buffer file until it is created.
    pyMPI_Wait('MPI_Recv', buffer_file, False)
            
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

    if DEBUG:
        print(buf.values())
        print('<-- Exiting MPI_Recv')
    # Get variable out of buf.
    return list(buf.values())


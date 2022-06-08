import os

from dict_to_hdf5 import *
from StopExecution import *
from pyMPI_Buffer_file import *
from pyMPI_Lock_file import *
from pyMPI_Sleep import *
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

    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering MPI_Recv')
    
    # Get processor rank.
    my_rank = MPI_Comm_rank(comm)

    # Get buffer and lock file names.
    buffer_file = pyMPI_Buffer_file(source,my_rank,tag,comm)
    lock_file = pyMPI_Lock_file(source,my_rank,tag,comm)
    if DEBUG:
        print(buffer_file)

    # Spin on lock file until it is created.
    loop = 0;
    while os.path.exists(lock_file) == False :
        # Sleep statement allows cleaner profiling, but adds latency.
        pyMPI_Sleep(0.2);
        if loop > 100:
            print('MPI_Recv: failed to find the %s file.'%(lock_file))
            raise StopExecution
        loop = loop + 1
            
    # Read all data out of buffer_file.
    buf = load_dict_from_hdf5(buffer_file)
    
    # Delete buffer and lock files.
    if (not(comm['save_message_flag'])):
        os.remove(buffer_file);
        # pyMPI_Sleep(0.02)
        os.remove(lock_file);

    if DEBUG:
        print(buf.values())
        print('<-- Exiting MPI_Recv')
    # Get variable out of buf.
    return list(buf.values())


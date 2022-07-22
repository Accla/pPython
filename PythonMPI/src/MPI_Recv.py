import os
from dict_with_pickle import load_dict_from_pickle

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
   
    # How much the pause time gets increased each iteration
    pause_rate = 0.03
    # Initial pause time
    pause_init = 0.3

    # Get processor rank.
    my_rank = MPI_Comm_rank(comm)

    # Get buffer and lock file names.
    buffer_file = pyMPI_Buffer_file(source,my_rank,tag,comm)
    lock_file = pyMPI_Lock_file(source,my_rank,tag,comm)
    if DEBUG:
        print(buffer_file)

    # Spin on lock file until it is created.
    loop = 0;
    sum = 0;
    pause_time = pause_init
    while os.path.exists(lock_file) == False :
        # Sleep statement allows cleaner profiling, but adds latency.
        sum += pause_time
        pyMPI_Sleep(pause_time);
        if loop > 100:
            print('MPI_Recv: failed to find the %s file.'%(lock_file))
            print('Loop: %d, total wait time: %f, last pause interval: %f'%(loop,sum,pause_time))
            raise StopExecution
        loop = loop + 1
        pause_time += pause_time * pause_rate
            
    # Spin on buffer file until it is created.
    loop = 0;
    pause_time = pause_init
    while os.path.exists(buffer_file) == False :
        # Sleep statement allows cleaner profiling, but adds latency.
        pyMPI_Sleep(pause_time);
        if loop > 100:
            print('MPI_Recv: failed to find the %s file.'%(buffer_file))
            raise StopExecution
        loop = loop + 1
        pause_time += pause_time * pause_rate

    # Read all data out of buffer_file.
    buf = load_dict_from_pickle(buffer_file)
    
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


#
from dict_with_pickle import save_dict_to_pickle

from StopExecution import *
from pyMPI_Buffer_file import *
from pyMPI_Lock_file import *
from MPI_Comm_rank import *

def MPI_Send(dest, tag, comm, *argv):
    """ MPI_Send  -  Sends variables to dest.

    Usage:
    ------
    MPI_Send( dest, tag, comm, var1, var2, ...)

    Send message containing variables to dest with a given tag

    dest:  an iteger from 0 to comm_size-1
    tag:   any integer
    comm:  an MPI Communicator (typically a copy of MPI_COMM_WORLD)
    *argv: variable number of MPI messages

    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering MPI_Send')

    # Get processor rank.
    my_rank = MPI_Comm_rank(comm)

    # Create buffer and lock file.
    buffer_file = pyMPI_Buffer_file(my_rank,dest,tag,comm)
    lock_file   = pyMPI_Lock_file(my_rank,dest,tag,comm)
    # print(buffer_file)

    # Save buf to file after packing the message into a dictionary
    msg = dict()
    ii = 0
    if DEBUG:
        print('Length of argv: %d'%(len(argv)))
    for arg in argv:
        # Serialize object with pickle
        if DEBUG:
            print(arg)
        msg[ii] = arg
        ii = ii + 1
    # Write the message into a file.
    if DEBUG:
        print(msg.values())
    try:
        save_dict_to_pickle(msg,buffer_file)
    except:
        print('MPI_Send: fail to create a message file')
        raise StopExecution
    
    # Create lock file.
    fid = open(lock_file,'w+')
    fid.close()

    # Spin on lock file until it is created.
    loop = 0;
    while os.path.exists(lock_file) == False :
        # Sleep statement allows cleaner profiling, but adds latency.
        pyMPI_Sleep(0.1);
        fid = open(lock_file,'w+')
        fid.close()
        if loop > 1000:
            print('MPI_Send: failed to create the %s file.'%(lock_file))
            raise StopExecution
        loop = loop + 1

    if DEBUG:
        print('<-- Exiting MPI_Send')


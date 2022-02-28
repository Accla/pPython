import os

from pyMPI_Dir_translate import *

def pyMPI_Lock_file(source,dest,tag,comm):
    """MatMPI_Lock_file  -  function for creating lock file name.

    Usage:
    ------
    lock_file = MatMPI_Lock_file(source,dest,tag,comm)

    source: MPI rank of the sending procdess (dtype: int)
    dest:   MPI rank of the receiving process (dtype: int)
    tag:    tag associated with the MPI message (dtype: int)
    comm:   MPI communicator  (dtype: dictionary)
    
    """

    machine_id = comm['machine_id'][dest]
    dir = comm['machine_db']['dir'][str(machine_id)]
    
    # Translate dir if needed
    dir = pyMPI_Dir_translate(comm['machine_db'],dir)

    # string concatenation
    sep = os.sep
    lock_file = dir+sep+'p'+str(source)+'_p'+str(dest)+'_t'+str(tag)+'_lock.h5'

    return lock_file


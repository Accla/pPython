import os

from pyMPI_Dir_translate import *

def pyMPI_Buffer_file(source,dest,tag,comm):
    """pytMPI_Buffer_file  -  Helper function for creating buffer file name.

    Usage
    -------
    buffer_file = pyMPI_Buffer_file(source,dest,tag,comm)
    
    source: MPI rank of the sending procdess (dtype: int)
    dest:   MPI rank of the receiving process (dtype: int)
    tag:    tag associated with the MPI message (dtype: int)
    comm:   MPI communicator  (dtype: dictionary)

    Note: All dictionary keys are string type.
          Convert integer into string

    """

    DEBUG = 0
    if DEBUG:
        print('--> entering pyMPI_Buffer_file:')
        print(comm)
    machine_id = comm['machine_id'][dest]
    dir = comm['machine_db']['dir'][machine_id]
    if DEBUG:
        print('machine_id = %d'%(machine_id))
        print('dir = %s'%(dir))
    
    # Translate dir if needed
    dir = pyMPI_Dir_translate(comm['machine_db'],dir)

    # string concatenation
    sep = os.sep
    buffer_file = dir+sep+'p'+str(source)+'_p'+str(dest)+'_t'+str(tag)+'_buffer.pkl'

    if DEBUG:
        print('<-- exiting pyMPI_Buffer_file:')
    return buffer_file


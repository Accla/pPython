import os

from pyMPI_Dir_translate import *

def pyMPI_Buffer_file(source, dest, tag, comm, **argv):
    """
    MatMPI_Buffer_file  -  Helper function for creating buffer file name.
    
    Usage:
    ------
    buffer_file = MatMPI_Buffer_file(source,dest,tag,comm,local_fs=0/1,msg_type='send/recv',innode=0/1)
    
    source: MPI rank of the sending procdess (dtype: int)
    dest:   MPI rank of the receiving process (dtype: int)
    tag:    tag associated with the MPI message (dtype: int)
    comm:   MPI communicator  (dtype: dictionary)

    **argv pass the following key, value pairs:
    local_fs: does it use a local filesystem for message kernel
    msg_type: send/recv string 
    innode: determine whether the message communication is in-node between two processes
    
    return buffer_file
    
    Python author: Dr. Chansup Byun
    2022-12-05: Updated to support message kernel using local filesystem (Dr. Chansup Byun)
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering pyMPI_Buffer_file')
    
    # Expand the additional argument for advanced features
    # - Use local filesystem
    local_fs = 0
    for key in argv:
        if key == 'local_fs':
            local_fs = argv[key]
        elif key == 'msg_type':
            msg_type = argv[key]
        elif key == 'innode':
            innode = argv[key]
        else:
            raise Exception('ERROR(pyMPI_Buffer_file): additional argument has a wrong key,value pair as input.')
    # grid_job
    grid_job = False
    if 'grid_config' in comm:
        grid_job = comm['grid_config']['grid_job']
            
    if local_fs:
        # if using local filesystem
        if (msg_type == 'send'):
            # Send process
            if innode:
                # if in-node message, temporary directory is the same for the destination process
                # this allows for source process to exit before the message is received by the receiver
                dir = comm['tmpdir'][dest]
            else:
                # if out-of-node message, temporary directory is for the source process before scp
                dir = comm['tmpdir'][source]
        else:
            # Receive process
            if innode:
                # if in-node message, temporary directory is the same for the source process
                dir = comm['tmpdir'][dest]
                #CB dir = comm['tmpdir'][source]
            else:
                # if out-of-node message, temporary directory is for the destination process
                dir = comm['tmpdir'][dest]
    else:
        # Using a central filesystem
        if DEBUG:
            print('pyMPI_Buffer_file.py: Using a central filesystem.')
        machine_id_source = comm['machine_id'][source]
        dir = comm['machine_db']['dir'][machine_id_source]

    # Translate dir if needed
    if grid_job and (not local_fs):
        dir = pyMPI_Dir_translate(comm['machine_db'],dir)

    if DEBUG:
        print('machine_id_dest = %d'%(machine_id_dest))
        print('dir = %s'%(dir))
        
    # string concatenation
    sep = os.sep
    buffer_file = dir+sep+'p'+str(source)+'_p'+str(dest)+'_t'+str(tag)+'_buffer.pkl'

    if DEBUG:
        print('<-- exiting pyMPI_Buffer_file:')
    return buffer_file


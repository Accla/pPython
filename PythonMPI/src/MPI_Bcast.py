import os

import checkOS as OS
from dict_to_hdf5 import *
from StopExecution import *
from pyMPI_Buffer_file import *
from pyMPI_Lock_file import *
from pyMPI_Sleep import *
from MPI_Comm_rank import *
from MPI_Comm_size import *
from MPI_Recv import *

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
    
    """

    # Get processor rank.
    my_rank = MPI_Comm_rank(comm);
    comm_size = MPI_Comm_size(comm);

    # If not the source, then receive the data.
    # Make sure to return a cell array for varargout
    if my_rank != source:
        # MPI_Recv returns a list
        return MPI_Recv(source, tag, comm)
 
    #
    # Only source execute the following code
    #
    # Set some strings for special characters.
    qq = '"'
    sp = ' '
    nl = '\n'
    # Get single quote character. 
    q = '\''
    dir_sep = os.sep

    # If the source, then send the data.
    # Create data file [only once in the central filesystem]
    buffer_file = pyMPI_Buffer_file(my_rank,source,tag,comm)
        
    # Save varargin to file [Duplicated from MPI_Send()]
    # Save buf to file after packing the message into a dictionary
    msg = dict()
    ii = 0
    # print('Length of argv: %d'%(len(argv)))
    for arg in argv:
        msg[ii] = arg
        ii = ii + 1
    # Write the message into a file.
    save_dict_to_hdf5(msg, buffer_file)   

    # Loop over everyone in comm and create link to data file.
    if (OS.ispc):
        link_command = 'echo off'+nl
    else:
        link_command = ''
    for ii in range(0,comm_size):
        # Don't do source.
        if ii != source:
            # Create buffer link name.
            buffer_link = pyMPI_Buffer_file(my_rank,ii,tag,comm);
            if (OS.ismac):
                # Append to link_command. MacOS sym links are not recognized by Linux.
                link_command = link_command+'cp '+buffer_file+' '+buffer_link+'; '
            elif (OS.islinux):
                # Append to link_command.
                link_command = link_command+'ln -s '+buffer_file+' '+buffer_link+'; '
            elif (OS.ispc):
                # Append to link_command.
                link_command = link_command+'copy '+qq+buffer_file+qq+' '+qq+buffer_link+qq+nl
            else:
                print('MPI_Bcast: none of ismac, islinux and ispc defined.')
                raise StopExecution

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

    os.remove(link_script)

    # Loop over everyone in comm and create lock file.
    for ii in range(0,comm_size):
        # Don't do source.
        if ii != source:
            # Get lock file name.
            lock_file = pyMPI_Lock_file(my_rank,ii,tag,comm);
            # Create lock file.
            fid=open(lock_file,'w')
            fid.close()

    # Check if the message is to be saved.
    if not(comm['save_message_flag']):
        # Loop over lock files.
        # Wait until all lock files are gone, which means that all receiving processes
        # have received the broadcasted message
        # Loop over everyone in comm and create lock file.
        for ii in range(0,comm_size):
            # Don't do source.
            if ii != source:
                # Get lock file name.
                lock_file = pyMPI_Lock_file(my_rank,ii,tag,comm);
                # Spin on lock file until it is deleted.
                # Spin on lock file until it is created.
                loop = 0;
                while os.path.exists(lock_file) == True :
                    loop = loop + 1;
                    # Sleep statement allows cleaner profiling, but adds latency.
                    pyMPI_Sleep(0.05);
                    if loop > 200:
                        print('MPI_Bcast: the %s file is not deleted yet.'%(lock_file))
                        raise StopExecution

        # Now all processes have received the broadcasted message.
        # Delete the source buffer file.
        os.remove(buffer_file)
   
    return argv


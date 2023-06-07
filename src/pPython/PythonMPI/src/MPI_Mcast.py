import os
import numpy as np

import checkOS as OS
from set_remote_cc import *
from exec_shell_cmd import *

from dict_with_pickle import save_dict_to_pickle
from pyMPI_Buffer_file import *
from pyMPI_Lock_file import *
from pyMPI_Sleep import *
from pyMPI_Wait import *
from MPI_Comm_rank import *
from MPI_Recv import *

def MPI_Mcast(source, dest, tag, comm, *argv):
    """Broadcast variables to everyone.
 
    Usage:
    ======
    [var1,var2,...] = MPI_Mcast(source,dest,tag,comm,var1,var2,...)
 
    Broadcast variables to everyone in dest.
 
    Sender blocks until all the messages are received,
    unless pyMPI_Save_messages(1) has been called.
    
    Python version: Dr. Chansup Byun
    2022-12-06: Update to support the message kernel using local filesystem
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering MPI_Mcast.')
    
    # Get processor rank.
    my_rank = MPI_Comm_rank(comm)

    # Check whether to use local filesystem or not
    grid_config = comm['grid_config']
    # Additional parameter when using mixed messaging kernels
    mixed_fs = grid_config['mixed_fs']
    if grid_config['local_fs'] == 1 :
        local_fs  = 1
        tmpdir = comm['tmpdir']
        machines =  comm['machine_db']['machine']
        if DEBUG:
            print('tmpdir:')
            print(tmpdir)
            print('machines:')
            print(machines)
        #
        # With the triples mode, we need to use machine id, instead of rank.
        #
        machine_id_rank = comm['machine_id'][my_rank]
    else:
        local_fs  = 0

    if DEBUG:
        if local_fs:
            print('Use local filesystem:')
            if (mixed_fs and my_rank == 0):
                print('--> MPI_Mcast: source rank = %d, host = %s' %(my_rank,machines[machine_id_rank]))
            else:
                print('--> MPI_Mcast: source rank = %d, host = %s, local path = %s' %(my_rank,machines[machine_id_rank],tmpdir[machine_id_rank]))
            if isinstance(dest,(int,np.int32,np.int64)):
                machine_id_dest = comm['machine_id'][dest]
                if (mixed_fs and my_rank == 0):
                    print('--> MPI_Mcast: destination rank = %d, host = %s' %(dest,machines[machine_id_dest]))
                else:
                    print('--> MPI_Mcast: destination rank = %d, host = %s, local path = %s' %(dest,machines[machine_id_dest],tmpdir[machine_id_dest]))
            else:
                for ii in dest:
                    if ii == source:
                        continue
                    machine_id_ii = comm['machine_id'][ii]
                    if (mixed_fs and my_rank == 0):
                        print('--> MPI_Mcast: destination rank = %d, host = %s' %(ii,machines[machine_id_ii]))
                    else:
                        print('--> MPI_Mcast: destination rank = %d, host = %s, local path = %s' %(ii,machines[machine_id_ii],tmpdir[machine_id_ii]))

    # If not the source, then receive the data.
    if (my_rank != source):
        return MPI_Recv( source, tag, comm )
        
    # Set some strings for special characters.
    qq = '"'
    sp = ' '
    nl = '\n'
    # Get single quote character. 
    q = '\''
    dir_sep = os.sep

    # If the source, then send the data.
    if (my_rank == source):
        # Create data buffer file to myself.
        innode = 1
        buffer_file = pyMPI_Buffer_file(my_rank,source,tag,comm,local_fs=local_fs,msg_type='send',innode=innode)

        # Save msg_dict to file.
        # print(buffer_file)

        # Save buf to file after packing the message into a dictionary
        msg = dict()
        ii = 0
        # print('Length of argv: %d'%(len(argv)))
        for arg in argv:
            # Serialize object with pickle
            msg[ii] = arg
            ii = ii + 1
        # Write the message into a file.
        save_dict_to_pickle(msg, buffer_file)   
        
        if DEBUG:
            print('Messae is saved to %s'%(buffer_file))

        # Loop over everyone in comm and create link to data file.
        if (OS.ispc):
            link_command = 'echo off'+nl
        else:
            link_command = ''
            
        if local_fs:
            # open a shell script to control the scp processes as background jobs
            shcmd = '#!/bin/bash'+nl
            shcmd = shcmd+'# generate all backgrounded scp processes to send the lock files'+nl
        
        # Create the remote execution command object
        ecmd = ExecShellCmd(set_remote_cc())
        if (OS.ispc):
            myhostname = os.getenv('computername')
        else:
            myhostname = os.uname()[1]

        if DEBUG:
            print('My hostname is %s'%(myhostname))

        for ii in dest:
            # Don't do source.
            if ii == source:
                continue
            machine_id_ii = comm['machine_id'][ii]
                
            if DEBUG:
                print('MPI_Mcast: Message to my_rank = %d'%(ii))
            # identify whether the message communication is in-node or out-of-node
            innode = 0
            if local_fs:
                machine_id_source = comm['machine_id'][source]
                if machines[machine_id_ii] == machines[machine_id_source]:
                    innode = 1
            
            # Create buffer link name.
            buffer_link = pyMPI_Buffer_file(my_rank,ii,tag,comm,local_fs=local_fs,msg_type='send',innode=innode)
            if DEBUG:
                print(buffer_link)
            buffer_link_basename = os.path.basename(buffer_link)            
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
                raise Execution('MPI_Mcast: none of ismac, islinux and ispc defined.')

            # out-of-node message, scp the buffer and lock files to the remote receiver
            if local_fs and (not innode) and (not (mixed_fs and my_rank == 0)):
                # when using local filesystem and the message needs to be sent out of node
                # Except when Pid=0 broadcast message with interactive triples mode job 
                status = 0

                # scp may cause DDoS attack if too many instances opened to the same host
                # 3 sec delay may not able to fix the issue with 48 scp calls at the same time.
                pauseTime = 1
                done_scp = False
                try_counter = 0
                try_max = 10
                scp_cmd = 'scp '
                # Copy the message before the actual link gets created.
                if (mixed_fs and my_rank == 0):
                    cmd1 = scp_cmd+buffer_file+' '+machines[machine_id_ii]+':'+tmpdir[machine_id_ii]+'/'+buffer_link_basename
                else: 
                    cmd1 = scp_cmd+buffer_file+' '+machines[machine_id_ii]+':'+tmpdir[machine_id_ii]+'/'+buffer_link_basename
                # generate a shell command
                shcmd = shcmd+cmd1+'&'+nl
    
                if DEBUG:
                    print('command: %s'%(cmd1))

                while not done_scp:
                    try_counter = try_counter + 1
                    # transfer the message to the remote host
                    status = True
                    ecmd.run(cmd1)
                    status = ecmd.get_stderr()
                    if status:
                        print('Error [MPI_Mcast]: failed to scp the message to the remote host.')
                        if try_counter >= try_max:
                            raise Exception('Error (MPI_Mcast): fail to scp a buffer file.')
                        else:
                            if DEBUG:
                                print('. . . scp failed. continue for next scp . . . ')
                            pyMPI_Sleep(pauseTime)
                    else:
                        done_scp = True

        # Write unix commands to .sh text file
        # [Was used to fix Matlab's problem with very long commands sent to unix().
        # Maybe not applicable to Python but needs to check [ToDo]
        TMPDIR = os.getenv('TMPDIR',default='')
        if OS.ispc:
            if len(TMPDIR)>0:
                link_script = TMPDIR+dir_sep+'Link_Commands_t'+str(tag)+'.bat'
            else:
                link_script = 'PythonMPI'+dir_sep+'Link_Commands_t'+str(tag)+'.bat'
        else:
            if len(TMPDIR)>0:
               link_script = TMPDIR+dir_sep+'Link_Commands_t'+str(tag)+'.sh'
            else:
               link_script = 'PythonMPI'+dir_sep+'Link_Commands_t'+str(tag)+'.sh'
        if DEBUG:
            print('Link script name: %s'%(link_script))
            print('Link command: %s'%(link_command))

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
        # pyMPI_Sleep(0.5)
        os.remove(link_script)

        rmcmd = ''
        # Loop over everyone in dest and create lock file.
        # generate a shell command
        if local_fs and (not innode) and (not (mixed_fs and my_rank == 0)):
            # Except when Pid=0 broadcast message with interactive triples mode job `:
            shcmd = shcmd+'# wait for all backgrounded scp processes to send the buffer files'+nl 
            shcmd = shcmd+'wait'+nl 
            shcmd = shcmd+'# generate all backgrounded scp processes to send the lock files'+nl
    
        # Loop over everyone in comm and create lock file.
        for ii in dest:
            # Don't do source.
            if (ii == source):
                continue
            # identify whether the message communication is in-node or out-of-node
            innode = 0
            if local_fs:
                machine_id_ii = comm['machine_id'][ii]
                machine_id_source = comm['machine_id'][source]
                if machines[machine_id_ii] == machines[machine_id_source]:
                    innode = 1    
            # Create lock file.
            lock_file = pyMPI_Lock_file(my_rank,ii,tag,comm,local_fs=local_fs,msg_type='send',innode=innode)
            fid = open(lock_file,'w+')
            fid.close()

            
            # if out-of-node message, scp the buffer and lock files to the remote receiver
            if local_fs and (not innode) and (not (mixed_fs and my_rank == 0)):
                # Except when Pid=0 broadcast message with interactive triples mode job `
                done_scp = False
                try_counter = 0;
                cmd1 = scp_cmd+lock_file+' '+machines[machine_id_ii]+':'+tmpdir[machine_id_ii]
                # generate a shell command
                rmcmd = rmcmd+'rm -f '+lock_file+nl
                # generate a shell command
                shcmd = shcmd+cmd1+'&'+nl
                while not done_scp:
                    try_counter = try_counter + 1
                    # transfer the lock to the remote host
                    ecmd.run(cmd1)
                    status = ecmd.get_stderr()
                    if status:
                        print('Error [MPI_Mcast]: failed to scp the lock file to the remote host.')
                        if try_counter >= 3:
                            raise Exception('Error (MPI_Mcast): fail to scp lock file.')
                        else:
                            pyMPI_Sleep(1)
                    else:
                        done_scp = True                
                        # remove lock file once both buffer and lock files are copied to the out-of-node receiver
                        os.remove(lock_file)
                
                # Create buffer link name.
                buffer_link = pyMPI_Buffer_file(my_rank,ii,tag,comm,local_fs=local_fs,msg_type='send',innode=innode)
                if os.path.exists(buffer_link):
                    os.remove(buffer_link)
                    rmcmd = rmcmd+'rm -f '+buffer_link+nl

        # generate a shell command
        if local_fs and (not innode) and (not (mixed_fs and my_rank == 0)):
            # Except when Pid=0 broadcast message with interactive triples mode job 
            shcmd = shcmd+'# wait for all backgrounded scp processes to send the lock files'+nl
            shcmd = shcmd+'wait'+nl
            shcmd = shcmd+'#'+nl
            shcmd = shcmd+'# End of scp commands. Now you can delete the buffer and lock files.'+nl
            shcmd = shcmd+'#'+nl
            shcmd = shcmd+rmcmd+nl
            # Future update for backgrounding scp calls
            if DEBUG:
                print(shcmd)
            
        # Check if the message is to be saved.
        # Loop over lock files.
        # Wait until all lock files are gone, which means that all receiving processes
        # have received the broadcasted message
        # Loop over everyone in comm and create lock file.
        for ii in dest:
            # Don't do source.
            if ii == source:
                continue
            # identify whether the message communication is in-node or out-of-node
            innode = 0
       	    if local_fs:
                machine_id_ii = comm['machine_id'][ii]
                machine_id_source = comm['machine_id'][source]
                if machines[machine_id_ii] == machines[machine_id_source]:
                     innode = 1
            # Get lock file name.
            lock_file = pyMPI_Lock_file(my_rank,ii,tag,comm,local_fs=local_fs,msg_type='send',innode=innode)
            # Spin on lock file until it is deleted.
            pyMPI_Wait('MPI_Mcast', lock_file, True)

        # Now all processes have received the broadcasted message.
        if not(comm['save_message_flag']):
            # Delete the source buffer file.
            os.remove(buffer_file)

    if DEBUG:
        print('<-- Exiting MPI_Mcast.')
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

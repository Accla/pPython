import sys
from timeit import default_timer as timer

import checkOS as OS
from set_remote_cc import *
from exec_shell_cmd import *

from dict_with_pickle import save_dict_to_pickle
from pyMPI_Buffer_file import *
from pyMPI_Lock_file import *
from pyMPI_Sleep import *
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

    Python version: Dr. Chansup Byun
    2022-12-05: Updated to support message kernel using local filesystem (Dr. Chansup Byun)
    """

    DEBUG = 0
    DEBUG_TIMING = 0
    if DEBUG or DEBUG_TIMING:
        t_start = timer()
        print('--> Entering MPI_Send')
        # print(comm)

    # Get processor rank.
    my_rank = MPI_Comm_rank(comm)
    
    # save locally and read by scp remotely if out-of-node or read locally if in-node msg.
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
        machine_id_source = comm['machine_id'][my_rank]
        machine_id_dest = comm['machine_id'][dest]
        if DEBUG:
            print('With using local filesystem:')
            print(machines)
            print(tmpdir)
            print('source = %d, destition rank = %d'%(my_rank,dest))
            print('machine_id_source = %d, machine_id_destination = %d'%(machine_id_source,machine_id_dest))
        if machines[machine_id_source] != machines[machine_id_dest] :
            innode = 0
    else:
        local_fs = 0
        mixed_fs = 0

    if DEBUG:
        if innode == 0 :
            print('MPI_Send: out-of-node message from source rank=%d to destination rank=%d'%(my_rank,dest))
        else:
            print('MPI_Send: in-node message from source rank=%d to destination rank=%d'%(my_rank,dest))
        if local_fs:
            if not (mixed_fs and (machine_id_source == 0 or machine_id_dest == 0)):
                # only when message is exchanged between the compute nodes on the grid
                print('Use local filesystem:')
                print('--> MPI_Send: source rank = %d, host = %s, local path = %s'   %(my_rank,machines[machine_id_source],tmpdir[machine_id_source]))
                print('--> MPI_Send: destination rank = %d, host = %s, local path = %s' %(dest,machines[machine_id_dest],tmpdir[machine_id_dest]))

    # Create buffer and lock files [updated to support message kernel using local filesystem]
    buffer_file = pyMPI_Buffer_file(my_rank,dest,tag,comm,local_fs=local_fs,msg_type='send',innode=innode)
    lock_file   = pyMPI_Lock_file(my_rank,dest,tag,comm,local_fs=local_fs,msg_type='send',innode=innode)
    if DEBUG or DEBUG_TIMING:
        print(buffer_file)

    # No need to create a msg dictionary. Just passs the argv vector
    # Write the message into a file.
    try:
        save_dict_to_pickle(argv,buffer_file)
        if DEBUG:
            print(argv)
    except:
        raise Exception('MPI_Send: fail to create a message file, %s'%(buffer_file))
    if DEBUG_TIMING:
        t_st_1 = timer()
        print('  MPI_Send: time to save the message (sec): %f'%(t_st_1 - t_start))
    
    # Create lock file.
    fid = open(lock_file,'w+')
    fid.close()

    # Spin on lock file until it is created.
    loop = 0;
    while os.path.exists(lock_file) == False :
        # Sleep statement allows cleaner profiling, but adds latency.
        pyMPI_Sleep(0.01);
        fid = open(lock_file,'w+')
        fid.close()
        if loop > 1000:
            raise Execution('MPI_Send: fail to create the lock file, %s'%(lock_file))
        loop = loop + 1

    if DEBUG_TIMING:
        t_st_2 = timer()
        print('  MPI_Send: time to create the lock file (sec): %f'%(t_st_2 - t_st_1))
        print('  --> MPI_Send: created lock file, %s'%(lock_file))

    if local_fs and (not innode):
        # when using local filesystem and the message needs to be sent out of node
        if not (mixed_fs and (machine_id_source == 0 or machine_id_dest == 0)):
            # only when message is exchanged between the compute nodes on the grid
            status1 = 0
            status2 = 0
            if (OS.ispc):
                myhostname = os.getenv('computername')
            else:
                myhostname = os.uname()[1]

            # scp may cause DDoS attack if too many instances opened to the same host
            # 3 sec delay may not able to fix the issue with 48 scp calls at the same time.
            pauseTime = 1
            done_scp = False
            try_counter = 0
            try_max = 5
            scp_cmd = 'scp '
            cmd1 = scp_cmd+buffer_file+' '+machines[machine_id_dest]+':'+tmpdir[machine_id_dest]
            cmd2 = scp_cmd+lock_file+' '+machines[machine_id_dest]+':'+tmpdir[machine_id_dest]
            # Create the remote execution command object
            ecmd = ExecShellCmd(set_remote_cc())

            while not done_scp:
                try_counter = try_counter + 1;
                # transfer the message to the remote host, return status with 0 when successful
                status1 = 1
                try:
                    ecmd.run(cmd1)
                    status1 = ecmd.get_stderr()
                    if status1:
                        print('scp failed on Rank = %d on %s with command, %s' %(my_rank,myhostname,cmd1))
                        print('Status: %s'%(status1)) 
                except:
                    print('Try Error [MPI_Send]: failed to scp the buffer file to the remote host.')

                if not status1:
                    done_scp = True
                else:
                    if try_counter > try_max:
                        raise Exception('Error [MPI_Send]: attempts to scp buffer file exceeds '+str(try_counter)+' tries.')
                    else:
                        if DEBUG:
                            print('. . . scp failed. continue for next scp . . . ')
                        pyMPI_Sleep(pauseTime)
                        pauseTime = pauseTime + 0.1

            try_counter = 0
            done_scp = False
            pauseTime = 1
            while not done_scp:
                try_counter = try_counter + 1;
                # transfer the message to the remote host, return status with 0 when successful
                status2 = 1
                try:
                    ecmd.run(cmd2)
                    status2 = ecmd.get_stderr()
                    if status2:
                        print('scp failed by Rank = %d on %s with command, %s' %(my_rank,myhostname,cmd2))
                        print('status: %s'%(status2)) 
                except:
                    print('Try Error [MPI_Send]: failed to scp the lock file to the remote host.')
                
                if not status2:
                    done_scp = True
                else:
                    if try_counter > try_max:
                        raise Exception('Error [MPI_Send]: attempts to scp lock file exceeds '+str(try_counter)+' tries.')
                    else:
                        if DEBUG:
                            print('. . . scp failed. continue for next scp . . . ')
                        pyMPI_Sleep(pauseTime)
                        pauseTime = pauseTime + 0.1

            os.remove(buffer_file)
            os.remove(lock_file)
            if DEBUG_TIMING:
                t_st_3 = timer()
                print('  MPI_Send: time to scp the message and lock file (sec): %f'%(t_st_3 - t_st_2))

    if DEBUG or DEBUG_TIMING:
        print('<-- Exiting MPI_Send')
    return

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

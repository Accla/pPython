#
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

    Python author: Dr. Chansup Byun
    2022-12-05: Updated to support message kernel using local filesystem (Dr. Chansup Byun)
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering MPI_Send')
        # print(comm)

    # Get processor rank.
    my_rank = MPI_Comm_rank(comm)
    
    # save locally and read by scp remotely if out-of-node or read locally if in-node msg.
    innode = 1
    grid_config = comm['grid_config']
    if grid_config['local_fs'] == 1 :
        local_fs  = 1;
        tmpdir = comm['tmpdir']
        machines =  comm['machine_db']['machine']
        if machines[my_rank] != machines[dest] :
            innode = 0
    else:
        local_fs  = 0

    if DEBUG:
        if innode == 0 :
            print('MPI_Send: out-of-node message from source rank=%d to destination rank=%d'%(my_rank,dest))
        else:
            print('MPI_Send: in-node message from source rank=%d to destination rank=%d'%(my_rank,dest))
        if local_fs:
            print('Use local filesystem:')
            print('--> MPI_Send: source rank = %d, host = %s, local path = %s' %(my_rank,machines[my_rank],tmpdir[my_rank]))
            print('--> MPI_Send: destination rank = %d, host = %s, local path = %s' %(dest,machines[dest],tmpdir[dest]))

    # Create buffer and lock files [updated to support message kernel using local filesystem]
    buffer_file = pyMPI_Buffer_file(my_rank,dest,tag,comm,local_fs=local_fs,msg_type='send',innode=innode)
    lock_file   = pyMPI_Lock_file(my_rank,dest,tag,comm,local_fs=local_fs,msg_type='send',innode=innode)
    if DEBUG:
        print(buffer_file)
        print(lock_file)

    # Save buf to file after packing the message into a dictionary
    msg = dict()
    ii = 0
    if DEBUG:
        print('Length of argv: %d'%(len(argv)))
    for arg in argv:
        # Serialize object with pickle
        # if DEBUG:
        #     print(arg)
        msg[ii] = arg
        ii = ii + 1
    # Write the message into a file.
    # if DEBUG:
    #     print(msg.values())
    try:
        save_dict_to_pickle(msg,buffer_file)
    except:
        raise Exception('MPI_Send: fail to create a message file, %s'%(buffer_file))
    
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
        if loop > 100:
            raise Execution('MPI_Send: fail to create the lock file, %s'%(lock_file))
        loop = loop + 1

    if DEBUG:
        print('--> MPI_Send: created lock file, %s'%(lock_file))

    if local_fs and (not innode):
        # when using local filesystem and the message needs to be sent out of node
        status1 = 0
        status2 = 0
        if (OS.ispc):
            myhostname = os.getenv('computername')
        else:
            myhostname = os.uname()[1]

        # scp may cause DDoS attack if too many instances opened to the same host
        # 3 sec delay may not able to fix the issue with 48 scp calls at the same time.
        pauseTime = 4
        done_scp = False
        try_counter = 0
        try_max = 10
        scp_cmd = 'scp '
        cmd1 = scp_cmd+buffer_file+' '+machines[dest]+':'+tmpdir[dest]
        cmd2 = scp_cmd+lock_file+' '+machines[dest]+':'+tmpdir[dest]
        # Create the remote execution command object
        ecmd = ExecShellCmd(set_remote_cc())

        while not done_scp:
            try_counter = try_counter + 1;
            # transfer the message to the remote host, return status with 0 when successful
            status1 = True
            try:
                ecmd.run(cmd1)
                status1 = ecmd.get_stderr()
                if status1:
                    print('scp failed on Rank = %d on %s with command, %s' %(my_rank,myhostname,cmd1))
                    print('Status: %s'%(status1)) 
            except:
                    print('Try Error [MPI_Send]: failed to scp the buffer file to the remote host.')
            status2 = True
            try:
                ecmd.run(cmd2)
                status2 = ecmd.get_stderr()
                if status2:
                    print('scp failed by Rank = %d on %s with a command, %s' %(my_rank,myhostname,cmd2))
                    print('status: %s'%(status2)) 
            except:
                    print('Try Error [MPI_Send]: failed to scp the lock file to the remote host.')
            if (not status1) and (not status2):
                done_scp = True
            else:
                if try_counter > try_max:
                    raise Exception('Error [MPI_Send]: attempts to scp buffer or lock file exceeds 3 tries.')
                else:
                    if DEBUG:
                        print('. . . scp failed. continue for next scp . . . ')
                    pyMPI_Sleep(pauseTime)

        os.remove(buffer_file)
        os.remove(lock_file)

    if DEBUG:
        print('<-- Exiting MPI_Send')


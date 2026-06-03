import os
from math import ceil
import numpy as np
from time import sleep

from pyMPI_Sleep import *

import grid_config as grid
from exec_shell_cmd import *
from set_remote_cc import *
from dict_with_pickle import save_dict_to_pickle,load_dict_from_pickle
from slurm_jobid_host_association import slurm_jobid_host_association

import pPython as GPC

def slurm2hostmap():
    """
    Create a host to MPI rank mapping, PythonMPI/SLURM2HOSTMAP.pkl
    Add the following additional information:
        MPI_COMM_WORLD['tmpdir'] 
        MPI_COMM_WORLD['leader'] for (nProcs)
        MPI_COMM_WORLD['pidmax'] for (nProcs)
        MPI_COMM_WORLD['local_pids'][hostname] saves the local pid list for the given machine name as key
    Update MPI_COMM_WORLD['machine_db']['machine'] with the actual compute node name
    
    hostmap{i} contains "SLURM_ARRAY_TASK_ID JOBID(unique) NODELIST"
    which is obtained by the following Slurm command:
    squeue ... --format="#15K                #15A          #N"

    This is an auxiliary function to support message kernel using local filesystem.

    Author: Dr. Chansup Byun
    Date: November 28, 2022
    """

    DEBUG = 1
    if DEBUG:
        print('--> Entering slurm2hostmap')
    
    MPI_COMM_WORLD = GPC.comm
    if DEBUG:
        print(MPI_COMM_WORLD)
    Pid = GPC.Pid
    
    # Recover grid_config from MPI_COMM_WORLD
    grid.grid_config = MPI_COMM_WORLD['grid_config']
    TMPDIR = grid.grid_config['TMPDIR']
    USE_MPI_4PY = grid.grid_config['USE_MPI4PY']

    if DEBUG:
        print('slurm2hostmap: Pid = %d' %(Pid))
        print('slurm2hostmap: grid.grid_config["mixed_fs"] = ',end="")
        print(grid.grid_config['mixed_fs'])
        print('slurm2hostmap: grid.grid_config["srun"] = ',end="")
        print(grid.grid_config['srun'])
        print(f'TMPDIR: {TMPDIR}')
        print(f'USE_MPI_4PY: {USE_MPI_4PY}')
        print("")
        # print("slurm2hostmap: grid.grid_config['srun'] = %s"%(grid.grid_config['srun']))
    
    maxIteration = 40
    pauseTime = 6
    
    #
    nl = '\n'
    q = "'"
    #
    # Set the appropriate nTasks (number of Slurm compute task scripts)
    #
    # For the triples mode jobs, ntasks != nprocs
    nTasks = grid.grid_config['ntasks'] 
    EPPAC    = grid.grid_config['EPPAC']  
    IMPLICIT_EPPAC    = grid.grid_config['IMPLICIT_EPPAC']  
    
    if EPPAC:
        nnode   = grid.grid_config['nnode']
        nppn   = grid.grid_config['nppn']
        # Only 1 slurm task script per each compute node with PPYTHON_MANYCORE mode
        # Do not use nTasks (slurm) for total number of process because of interactive jobs
        nProcs    = nnode * nppn 
        # For the triples mode jobs, ntasks != nprocs
        nTasks = nnode
    elif IMPLICIT_EPPAC:
        nnode   = grid.grid_config['nnode']
        nppn   = grid.grid_config['nppn']
        # Keep the old style Np as ntasks in grid_config
        nProcs    = grid.grid_config['ntasks']  
        # For the implicit triples mode jobs, ntasks != nprocs
        nTasks = nnode
    else:
        # Traditional jobs (number of Slurm tasks == Np of pPython)
        nProcs    = grid.grid_config['ntasks']  

    if DEBUG:
        print('slurm2hostmap: nTasks = %d' %(nTasks))
    
    ## Mixed messaging kernel enhancement
    mixed_fs = grid.grid_config['mixed_fs']
    if mixed_fs:
        # central shared filesystem for rank 0
        # local filesystem for the rest of MPI ranks 
        # So the leader MPI rank be 1 when using mixed kernel 
        leader = 1
    else:
        # The leader MPI rank be 0
        leader = 0

    if DEBUG:
        
        print('slurm2hostmap: mixed_fs = %d' %(leader))
    
    ## Prelimenary implementation
    #
    # Rank 0 process obtains the host-to-rank map information from the scheduler
    # TaskID (#K), JobID (#A), NodeName (#N) from the squeue command
    iter = 0
    hostmap = dict()

    if Pid == leader:
        # Extract the host-to-rank map information and save to other processes to read it from
        # Create the remote execution command object
        ecmd = ExecShellCmd(set_remote_cc())

        
        if grid.grid_config['srun']:
            # pPython is launched with the Slurm srun command
            # This is for future implementation for the backgrounded triples mode jobs [ToDo]
            SLURM_JOB_ID = os.getenv('SLURM_JOB_ID')
            cmdstr = 'squeue -h -j '+SLURM_JOB_ID+' --format="%15A %N"'
            ecmd.run(cmdstr)
            output = ecmd.get_output()
            jobNumber,slurm_nodelist = output.split()
            cmdstr = 'scontrol show hostname '+slurm_nodelist
            ecmd.run(cmdstr)
            output = ecmd.get_output()
            # print(output)
            # Start from 1 to match with the default Slurm task ID numbering
            # Need to confirm if the nodelist is matching with node ID [ToDo]
            i = 1
            for host in output.split():
                hostmap[i] = str(i)+' '+jobNumber+' '+host
                i += 1
        else:
            # pPython is launched with either MPI4PY or PythonMPI
            if USE_MPI_4PY:
                SLURM_JOB_ID = os.getenv('SLURM_JOB_ID')
                if DEBUG:
                    if SLURM_JOB_ID:
                        print('slurm2host (MPI4PY): SLURM_JOB_ID = %s'%(SLURM_JOB_ID))
                    else:
                        raise Exception('ERROR(slurm2host:MPI4PY): SLURM_JOB_ID is NOT defined.')
                hostmap = slurm_jobid_host_association(hostmap,SLURM_JOB_ID)
            else:
                SLURM_ARRAY_JOB_ID = os.getenv('SLURM_ARRAY_JOB_ID')
                if DEBUG:
                    if SLURM_ARRAY_JOB_ID:
                        print('slurm2host: SLURM_ARRAY_JOB_ID = %s'%(SLURM_ARRAY_JOB_ID))
                    else:
                        raise Exception('ERROR(slurm2host): SLURM_ARRAY_JOB_ID is NOT defined.')
                hostmap = slurm_jobid_host_association(hostmap,SLURM_ARRAY_JOB_ID)

        if DEBUG:
            print('Hostmap:')
            print(hostmap)

        ## Repeat until all the tasks are launched
        while len(hostmap) < nTasks:
            if DEBUG:
                print('slurm2hostmap [Pid=%d]: current number tasks: %d should be %d' %(Pid,len(hostmap),nTasks))

            if MPI4PY:
                raise Exception('ERROR(slurm2hostmap:MPI4PY): failed to get hostmap with Slurm.')

            # Wiat for pauseTime before checking again
            pyMPI_Sleep(pauseTime)
            
            if grid.grid_config['srun']:
                # pPython is launched with the Slurm srun command
                # This is for future implementation for the backgrounded triples mode jobs [ToDo]
                raise Exception('ERROR(slurm2hostmap): failed to get hostmap with Slurm srun.')
            else:
                # An array job
                hostmap = slurm_jobid_host_association(hostmap,SLURM_ARRAY_JOB_ID)
            
            if iter > maxIteration:
                raise Exception('ERROR(slurm2hostmap): failed to get hostmap within the maximum iteration.')
            iter = iter + 1
            
        # Save the host-to-rank map information
        done_saving = False
        try_counter = 0
        while not done_saving:
            try:
                try_counter = try_counter + 1
                # Save hostmap into a file.
                pkl_file = 'PythonMPI/SLURM2HOSTMAP.pkl'
                save_dict_to_pickle(hostmap, pkl_file)   
                done_saving = True
            except:
                raise Exception('slurm2hostmap: Error saving hostmap in ./PythonMPI/SLURM2HOSTMAP.pkl')

        # create a lock file
        fid = open('./PythonMPI/SLURM2HOSTMAP_lock.pkl','w+')
        fid.close()
    else:
        # Read the host-to-rank map information from the saved data
        # [status,s1] = system('squeue -h -j $SLURM_ARRAY_JOB_ID --format="#15K #15A #N"')
        pyMPI_Sleep(pauseTime)
        while(1):
            if os.path.exists('./PythonMPI/SLURM2HOSTMAP_lock.pkl'):
                # Read all data out of buffer_file.
                hostmap = load_dict_from_pickle('./PythonMPI/SLURM2HOSTMAP.pkl')
                break
            else:
                pyMPI_Sleep(pauseTime)
                iter = iter+1
                pauseTime = pauseTime + pauseTime
            if iter > maxIteration:
                raise Exception('slurm2hostmap[Pid=%d]: failed to read the host to rank map'%(Pid))
            if DEBUG:
                print('slurm2hostmap [Pid=%d]:  waiting ./PythonMPI/SLURM2HOSTMAP.pkl file . . . '%(Pid))

    #
    # Now for all pPython processes . . . 
    #
    # Modify MPI_COMM_WORLD to save the host to rank map along with TMPDIR
    MPI_COMM_WORLD['tmpdir'] = dict()
    MPI_COMM_WORLD['local_pids'] = dict()
    # To store the leader Pid on each node for every pPython process
    MPI_COMM_WORLD['leader'] = np.zeros(nProcs,dtype=int)
    MPI_COMM_WORLD['pidmax'] = np.zeros(nProcs,dtype=int)
    # Slurm plugin set TMPDIR differently between array job and srun job
    if not (mixed_fs and Pid == 0):
        # With interactive triples mode/job, the Pid = 0 process is running on a local machine
        # So no TMPDIR defined in general.
        tmpdir  = os.getenv('TMPDIR').split('.')
    
    if EPPAC or IMPLICIT_EPPAC:
        # For the triples mode jobs
        # nTasks is equivalent to number of compute nodes on the grid
        if DEBUG:
            print('nTasks =  %d, nProcs = %d, nppn = %d'%(nTasks,nProcs,nppn))
        for i in range(nTasks):
            # hostmap key is a positive integer 
            # Adjust for mixed messaging kernel
            tmp = hostmap[i+1+mixed_fs].split()
            if DEBUG:
                # print('Slurm TaskID: %s, JobID: %s, Hostname: %s'%(tmp[0],tmp[1],tmp[2]))
                print('pPython Machine ID: %s, JobID: %s, Hostname: %s'%(tmp[0],tmp[1],tmp[2]))
            my_node_rank = int(tmp[0])-1
            # tmp[1] is job ID
            # tmp[2] is compute node name
            MPI_COMM_WORLD['local_pids'][tmp[2]]=[]
            # Adjust for mixed messaging kernel
            if DEBUG:
                print('store %s at %d in machine_db:machine'%(tmp[2],i+mixed_fs))
            MPI_COMM_WORLD['machine_db']['machine'][i+mixed_fs] = tmp[2]
            #
            if not (mixed_fs and Pid == 0):
                # Skip if Pid = 0 with mixed_fs = 1
                # Otherwise, set MPI_COMM_WORLD['tmpdir'][i+mixed_fs]
                # Construct the TMPDIR given by Slurm on LLSC environment?
                if grid.grid_config['srun']:
                    if len(tmpdir) >= 2:
                        MPI_COMM_WORLD['tmpdir'][i+mixed_fs] = os.path.join(TMPDIR,tmp[1]+'.'+tmpdir[1]+'.'+str(my_node_rank))
                    else:
                        MPI_COMM_WORLD['tmpdir'][i+mixed_fs] = os.path.join(TMPDIR,tmp[1]+'.'+SLURM_JOB_ID+'.'+str(my_node_rank))
                else:
                    if len(tmpdir) >= 3:
                        MPI_COMM_WORLD['tmpdir'][i+mixed_fs] = os.path.join(TMPDIR,tmp[1]+'.'+tmpdir[1]+'.'+tmpdir[2])
                    else:
                        MPI_COMM_WORLD['tmpdir'][i+mixed_fs] = os.path.join(TMPDIR,tmp[1]+'.'+SLURM_ARRAY_JOB_ID)
                if DEBUG:
                   print("slurm2hostmap: MPI_COMM_WORLD['tmpdir'][%d] = %s"%(i+mixed_fs,MPI_COMM_WORLD['tmpdir'][i+mixed_fs]))
            # For IMPLICIT_EPPAC, nppn may be changed at the last machine
            for j in range(nppn):
                ipos = (my_node_rank - mixed_fs)*nppn+j 
                if i == 0 and j == 0 and mixed_fs and nppn > 1:
                    # when mixed_fs, the Pid = 0 is local process.
                    # skip
                    continue
                if grid.grid_config['interactive'] and nppn == 1:
                    ipos = ipos + 1
                if (ipos > nProcs-1):
                    # skip
                    continue
                # Introduce pid list for those on the same compute ndoe 
                MPI_COMM_WORLD['local_pids'][tmp[2]].append(ipos)
            if DEBUG:
                print('local_pids key = %s, '%(tmp[2]),end="")
                print(MPI_COMM_WORLD['local_pids'][tmp[2]])
        machines = MPI_COMM_WORLD['machine_db']['machine']
        if mixed_fs:
            # machines[0]]  is the local machine and always executes Pid = 0 process
            MPI_COMM_WORLD['local_pids'][machines[0]] = [0]
    else:
        # As a Slurm array job (not a triples mode job, though)
        for i in range(nProcs):
            # The key is equivalent to Slurm task number, starting from 1
            tmp = hostmap[i+1].split()
            ipos = int(tmp[0])-1
            MPI_COMM_WORLD['machine_db']['machine'][ipos] = tmp[2]
            # Construct the TMPDIR given by Slurm on LLSC environment?
            # MPI_COMM_WORLD['tmpdir'][ipos] = '/state/partition1/slurm_tmp/'+tmp[1]+'.'+tmpdir[1]+'.'+tmpdir[2]
            #
            MPI_COMM_WORLD['tmpdir'][ipos] = os.path.join(TMPDIR,tmp[1]+'.'+tmpdir[1]+'.'+tmpdir[2])

        # Generate pid list on the same node
        machines = MPI_COMM_WORLD['machine_db']['machine']
        for hostname in sorted( set( machines.values() ) ):
            member_keys = [key for key, val in machines.items() if val == hostname]
            MPI_COMM_WORLD['local_pids'][hostname] = member_keys

    # Generate the leader Pid information
    pidlist  = MPI_COMM_WORLD['group']
    if DEBUG:
        print('machines:')
        print(machines)
        print('pidlist:')
        print(pidlist)
        # print(grid.grid_config)

    # for hostname in sorted( set( machines.values() ) ):
    for hostname in sorted( set( machines.values() ) ):
        local_pid_list = MPI_COMM_WORLD['local_pids'][hostname]
        # Assuming that the key is equivalent the Pid of pPython process
        # save the leader Pid for all pPyton processes on the same compute node 
        for i in local_pid_list:
            pidmin      = min(local_pid_list)
            pidmax      = max(local_pid_list)
            MPI_COMM_WORLD['leader'][i] = pidmin
            MPI_COMM_WORLD['pidmax'][i] = pidmax

    if DEBUG:
        print("MPI_COMM_WORLD['machine_id']")
        print(MPI_COMM_WORLD['machine_id'])
        print("MPI_COMM_WORLD['machine_db']['machine']")
        print(MPI_COMM_WORLD['machine_db']['machine'])
        print("MPI_COMM_WORLD['leader']")
        print(MPI_COMM_WORLD['leader'])
        print("MPI_COMM_WORLD['pidmax']")
        print(MPI_COMM_WORLD['pidmax'])
        print("MPI_COMM_WORLD['local_pids']")
        print(MPI_COMM_WORLD['local_pids'])
        if not (mixed_fs and Pid == 0):
            print("MPI_COMM_WORLD['tmpdir']")
            print(MPI_COMM_WORLD['tmpdir'])
        print('<-- Exiting slurm2hostmap')
    return

########################################################
# gridMatlab
# Dr. Albert Reuther
# reuther@ll.mit.edu
# MIT Lincoln Laboratory
########################################################
# Copyright 2003-9 Massachusetts Institute of Technology
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

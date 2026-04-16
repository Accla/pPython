import os
from math import ceil
import numpy as np
from time import sleep

from pyMPI_Sleep import *

import grid_config as grid
from exec_shell_cmd import *
from set_remote_cc import *
from dict_with_pickle import save_dict_to_pickle,load_dict_from_pickle

import pPython as GPC

def slurm_jobid_host_association(hostmap,SLURM_JOB_ID):
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

    DEBUG = 0
    if DEBUG:
        print('--> Entering slurm2hostmap')
    
    MPI_COMM_WORLD = GPC.comm
    if DEBUG:
        print(MPI_COMM_WORLD)
    Pid = GPC.Pid
    
    # Recover grid_config from MPI_COMM_WORLD
    grid.grid_config = MPI_COMM_WORLD['grid_config']
    USE_MPI_4PY = grid.grid_config['USE_MPI4PY']

    if DEBUG:
        print('slurm2hostmap: Pid = %d' %(Pid))
        print('slurm2hostmap: grid.grid_config["mixed_fs"] = ',end="")
        print(grid.grid_config['mixed_fs'])
        print('slurm2hostmap: grid.grid_config["srun"] = ',end="")
        print(grid.grid_config['srun'])
        print(f'USE_MPI_4PY: {USE_MPI_4PY}')
        print("")
        # print("slurm2hostmap: grid.grid_config['srun'] = %s"%(grid.grid_config['srun']))
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
    
    ## Mixed messaging kernel enhancement
    mixed_fs = grid.grid_config['mixed_fs']
        
    
    ## Prelimenary implementation
    #
    # Rank 0 process obtains the host-to-rank map information from the scheduler
    # TaskID (#K), JobID (#A), NodeName (#N) from the squeue command

    if SLURM_JOB_ID:
        ecmd = ExecShellCmd(set_remote_cc())
        # Wait until all array job tasks are deployed
        deployed_all = False
        while not deployed_all:
            cmdstr = 'squeue -h -j '+SLURM_JOB_ID+' --Format="ArrayTaskID:14,JobID:15,NodeList,NumCPUs,NumNodes,NumTasks,cpus-per-task"'
            ecmd.run(cmdstr)
            output = ecmd.get_output().strip()
            lines = output.split('\n')
            nlines = len(lines)
            if DEBUG:
                print('len(lines) = %d'%(nlines))
                print(output)

            if USE_MPI_4PY:
                # MPI4PY
                #
                # Expect single line
                #
                slurm_nodelist = ''
                for line in lines:
                    if DEBUG:
                        print('Line: %s'%(line))
                    tmp = line.split()
                    if len(tmp)<3:
                        continue
                    else:
                        # Take care of multiple nodes
                        slurm_nodelist = tmp[2]
                        cmdstr = 'scontrol show hostname '+slurm_nodelist
                        ecmd.run(cmdstr)
                        output = ecmd.get_output()
                        hosts = output.split('\n')
                        slurm_node_list = []
                        for host in hosts:
                            slurm_node_list.append(host)

                        total_cpus = int(tmp[3])
                        num_nodes = int(tmp[4])
                        num_tasks = int(tmp[5])
                        cpus_per_tasks = int(tmp[6])
                        # max_num_tasks_per_node (with --distribution=nopack)
                        max_num_tasks_per_node = int((num_tasks-1) / num_nodes) + 1

                        i_rank = 0
                        # Generate revers order index
                        for j in range(num_nodes-1, -1, -1):
                            for i in range(max_num_tasks_per_node):
                                hostmap[i_rank] = str(i_rank)+' '+jobNumber+' '+slurm_node_list[j]
                                i_rank += 1
                                if i_rank == num_tasks:
                                    break

                        deployed_all = True
            else:
                # PythonMPI
                if nlines == nTasks:
                     deployed_all = True
                else:
                     sleep(3)
                #
                # Expect multiple lines
                #
                slurm_nodelist = ''
                for line in lines:
                    # print('Line: %s'%(line))
                    tmp = line.split()
                    if len(tmp)<3:
                        continue
                    else:
                        # if mixed messaging kernel, the first host is local machine
                        jobArrayIndex = int(tmp[0]) + mixed_fs
                        jobNumber = tmp[1]
                        slurm_node = tmp[2]
                        if jobArrayIndex not in hostmap:
                            hostmap[jobArrayIndex] = str(jobArrayIndex)+' '+jobNumber+' '+slurm_node 
    else:
        # Not a batch job
        for j in range(nProcs):
            hostmap[j+1] = str(j+1)+' '+'not_a_batch_job localhost'

    if DEBUG:
        print('Hostmap:')
        print(hostmap)

    return hostmap

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

import math
import os

import checkOS as OS
from convert_to_dict import *
from grid_resource_policy import *
from check_triples import *

def check_runtime( n_proc, machines, grid_config ):
    """Check runtime environment for pPython
    
    check_runtime  -  check the runtime environment and 
                      set various variables accordingly.

    Usage:
    ------
    check_runtime( py_file, n_proc_req, machines )

    n_proc:   total number of MPI processes (dtype: int or triples of a list)
    
    machines = 'grid'   (dtype: string)
        Run on a LLGrid system interactively.
    machines = 'grid&'   (dtype: string)
        Run on a LLGrid system in a backgrounded mode.
    machines: 'grid' or 'grid&'
              extended to 'grid-cpu_type' or 'grid-cpu_type&'

    grid_config: runtime parameters, return after update

    Called before the check_allowance function
    
    Note: refactored from part of pRUN() in gridMatlab

    Python author: Dr. Chansup Byun
    """

    DEBUG = 0

    if DEBUG:
        print('--> Entering check_runtime.')
        print('check_runtime: isunix, ismac, islinux, ispc = %d,%d,%d,%d'%(OS.isunix, OS.ismac, OS.islinux, OS.ispc))
    
    cluster_name = grid_config['cluster_name']
    
    # Unix vs. Windows file seperator.
    dir_sep = os.sep

    # Unix vs. Windows host name.
    if (OS.isunix):
        host = os.uname()[1]
    elif (OS.ispc):
        host = os.getenv('computername')

    # Determine whether it is an interactive or backgrounded job
    if DEBUG:
        print('check_runtime: cluster_name = %s'%(cluster_name))
        print('check_runtime: machines = %s'%(machines))
              
    if isinstance(machines,(dict,list,set)):
        endStr = ''
        interactive = 1
        grid_job = False  # meaning no scheduler is involved
    else:
        if machines[-1] == '&':
            # Backgrounded job
            endStr = '&'
            interactive = 0
            grid_job = True
        else:
            # Interacttive job
            endStr = ''
            interactive = 1
            if machines[:4] == 'grid':
                grid_job = True
            else:
                grid_job = False
    
    # Determine if a specific CPU type is requested
    # Old partition also requires partition name 
    # But new partition, starting xeon-p8, does not need partition name 
    # to submit jobs to the grid.
    if len(machines) > 5:
        # 'grid-xeon-e5[&]'
        if endStr == '&':
            cpu_type = machines[5:-1]
        else:
            cpu_type = machines[5:]
    else:
        # if cpu_type is not provided with the grid option
        # set the default cpu_type
        if grid_config['cpu_type']:
            # default cpu_type is set in the local grid configuraiton
            cpu_type = grid_config['cpu_type']
        else:
            # not defined at all
            if (cluster_name == 'txgreen') or (cluster_name == 'txe1') or (cluster_name == 'txc'):
                cpu_type = 'xeon-p8'
            else:
                # exit since no cpu_type id set
                raise Exception('ERROR(check_runtime): no cpu_type is set.')
            
    # Set the partition (queue) name if cpu_type is specified
    # This is required for old partition name
    if len(cpu_type):
        if DEBUG:
            print('CPU type, grid_config[\'cpu_type\'] = %s'%(cpu_type))
        grid_config['cpu_type'] = cpu_type
        # Update the queue name (partition name) accordingly
        # The following is specific to TX-Green 
        # Check grid_config['cluster_name'] in $HOME/ppython_conf/grid_config_local.py
        # for future support with other clusters
        #
        if cluster_name == 'txgreen':
            if (cpu_type == 'xeon64c'):
                grid_config['q_name'] = 'manycore'
            elif (cpu_type == 'xeon-p8'):
                grid_config['q_name'] = 'xeon-p8'
            elif (cpu_type == 'xeon-g6'):
                grid_config['q_name'] = 'gaia'
            elif (cpu_type == 'xeon-e5'):
                # Only on TX-Green
                grid_config['q_name'] = 'normal'
        else:
            raise Exception('ERROR(check_runtime): %s is not a supported cluster.'%(grid_config['cluster_name']))

    # check and process the triples mode job request if needed
    n_proc_req, grid_config = check_triples(cluster_name,cpu_type,n_proc,grid_config)
    EPPAC = grid_config['EPPAC'] 
    #
    # number of cores to be allocated from the grid
    # At this point, n_proc_req is already translated into number of cores (int) if triples mode is used.
    #
    # ToDo: Need to skip when submitting to the grid with Slurm srun
    #
    requested,unclaimed_procs,unclaimed_nodes = grid_resource_policy(grid_config, n_proc_req, interactive)
    n_proc_req = requested + interactive
    
    # Create a fictious machine list when 'grid[&]' is used
    if grid_job:
        machines = []
        # set the Pid=0 machine for an interactive job
        if interactive:
            machines.append(host)
        if grid_config['nnode'] > 0: 
            # Triples modes, pPython MPI processes on the same node are aggregated into a single scheduler task
            grid_config['ntasks'] = grid_config['nnode']
            # Figure out how many digits are needed to represent the number of requested nodes
            n_digits = int(math.log10(grid_config['nnode'])+1)
            for i in range(grid_config['nnode']):
                node_strid = str(i+1).zfill(n_digits)
                machines.append('grid_slurm_'+node_strid)
        else:
            # Non-triple modes
            if interactive:
                grid_config['ntasks'] = n_proc_req-1
            else:
                grid_config['ntasks'] = n_proc_req
            if DEBUG:
                print('n_proc_req = %d'%(n_proc_req))
                print("grid_config['ntasks'] = %d"%(grid_config['ntasks']))
            if grid_config['ntasks']>0:
                # Figure out how many digits are needed to represent the number of requested tasks
                n_digits = int(math.log10(grid_config['ntasks'])+1)
            else:
                n_digits = 1

            for i in range(grid_config['ntasks']):
                node_strid = str(i+1).zfill(n_digits)
                machines.append('grid_slurm_'+node_strid)
    
    # Convert machines into a dictionary variable if needed
    machines,islocal = convert_to_dict(machines,host)
    #
    # Override islocal based on interactive
    if interactive or (not grid_job):
        islocal = 1
    else:
        islocal = 0
    OS.islocal = islocal
    # save to grid_config['islocal'] which will be saved in MPI_COMM_WORLD
    grid_config['islocal'] = islocal
    grid_config['grid_job'] = grid_job
    grid_config['interactive'] = interactive

    #
    # Override if PPYTHON_LOCAL_FS is defined
    local_fs = 1
    PPYTHON_LOCAL_FS = os.getenv('PPYTHON_LOCAL_FS',default='yes')
    if DEBUG:
        print('PPYTHON_LOCAL_FS: %s'%(PPYTHON_LOCAL_FS))
    if (PPYTHON_LOCAL_FS.lower() == 'no'):
        local_fs = 0
    else:
        local_fs = 1
    # Set local_fs = 0 for non grid jobs
    if not grid_job:
        local_fs = 0
    grid_config['local_fs'] = local_fs
    # Check compatibality between interactive job versus messaging kernel using local filesystem
    grid_config['mixed_fs'] = 0

    if local_fs: 
        if interactive and EPPAC:
            # Special case: interactive triples-mode jobs
            # Turn on mixed messaging kernel to support communication between the head process (Pid = 0) and the rest
            # with a shared filesystem based messaging kernel while all other communication is accomplished by using
            # a local filesystem based messaging kernel
            grid_config['mixed_fs'] = 1
        elif (not grid_job) or interactive :
            # Messaging kernel using local filesystem is only supported when
            # 1. grid_job, 2. backgrounded job (interactive = 0)
            # Both non-triples or triples mode jobs are supported as long as they are backgrounded grid jobs.
            raise Exception('ERROR(pRUN_Parallel_wrapper): the default messaging kernel using local filesystem is only supported when \n1. grid_job, 2. backgrounded job (interactive = 0)\nUse either the messaging kernel using the central filesystem or run as a backgrounded job.')
        
    if DEBUG:
        print("grid_config['mixed_fs'] = %d"%(grid_config['mixed_fs']))
        print("grid_config['local_fs'] = %d"%(grid_config['local_fs']))
        print('OS.islocal = %d'%(OS.islocal))
        print('<-- Exiting check_runtime')
        
    return n_proc_req, machines, grid_config

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

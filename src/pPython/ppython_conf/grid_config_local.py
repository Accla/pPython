import os
import re
import platform

import checkOS as OS

def grid_config_local(grid_config):
    """Update local grid_config parameters. 

    Usage:
    ------

    grid_config = grid_config_local(grid_config)

    Update the following information.

    grid_config['remote_host']: the fully qualified hostname to access the scheduler
    grid_config['remote_user']: username on the grid
    grid_config['remote_launch']: command used to access the remote host
    grid_config['remote_flags']: flags used by the remote launch command

    grid_config['q_name']: the queue (partition) name where the job is submitted to
    grid_config['cpu_type']: the CPU type for the nodes in the queue (deprecated in the future compute nodes
                             bacause each queue will have only one CPU-type node)
    grid_config['default_q_name']: default queue (partition) name
    grid_config['default_cpu_type']: default CPU type name 

    grid_config['LL_FILE_SERVER'] = file server name to mount grid home directory locally

    grid_config['GRID_HOME_PATH']: home directory path on the grid for the remote user
    grid_config['GRID_MOUNT_PATH']: locally mounted path for GRID_HOME_PATH
    grid_config['PPYTHON_PATH']: pPython source installation path
    grid_config['PYTHONMPI_PATH']: PythonMPI source installation path
    grid_config['DMAP_PATH']: distributed map source installation path
    grid_config['DMAT_PATH']: distributed array source installation path
    grid_config['LOCAL_PYTHONMPI_CONFIG_PATH']: path for remote user configuration customization files
    grid_config['CWD_PATH']: current working directory path where you submit a job (automatically detected)

    New pPython environment variables for additional features:
    grid_config['srun']: [Only for backgrounded triples mode jobs] pPython uses Slrum srun to launch 
                         pPython job as a single Slurm job instead of a Slurm array job if it's set 
                         to True (automatically set when there is no resources available for immediate job 
                         launch for backgrounded triples mode job)

    Author: Dr. Chansup Byun
    """

    # Define grid configuration parameters
    #

    DEBUG = 0
    if DEBUG:
        print('--> Entering grid_config_local in ~/ppython_config')

    # Am I on a LLGrid system?
    # Set the cluster name to work with
    cluster_name = 'noname'
    if os.path.exists('/etc/llgrid.id'):
        with open('/etc/llgrid.id') as f:
            lines = f.readlines()
        for line in lines:
            # print(line)
            if re.search('txgreen',line,re.IGNORECASE):
                cluster_name = 'txgreen'
            elif re.search('txe1',line,re.IGNORECASE):
                cluster_name = 'txe1'
            elif re.search('txc',line,re.IGNORECASE):
                cluster_name = 'txc'
    else:
        # Manually define for other systems
        cluster_name = 'txgreen'
    grid_config['cluster_name'] = cluster_name

    # Grid user (ToDo: need a better way to set the grid username)
    # pick up the local username
    if OS.ispc:
        USER = os.getenv('USERNAME')
    else:
        USER = os.getenv('USER')
    
    if isinstance(USER,type(None)):
        if cluster_name == 'txgreen':
            grid_config['remote_user'] = 'ch21778'
        elif cluster_name == 'txe1':
            grid_config['remote_user'] = 'cbyun'
        elif cluster_name == 'aicr':
            grid_config['remote_user'] = 'cbyun_mit'
        else:
            raise Exception('grid_config_local: Unsupported system. Exited.')
    else:
        # The following line will not work if local username is differen from the grid username
        grid_config['remote_user'] = USER

    # Remote access
    if cluster_name == 'txgreen':
        grid_config['remote_host'] = 'txg-login.llgrid.ll.mit.edu'
    elif cluster_name == 'txe1':
        grid_config['remote_host'] = 'txe1-login.mit.edu'
    elif cluster_name == 'aicr':
        grid_config['remote_host'] = 'login.aicr.ai'
    else:
        # print('grid_config_local: Unsupported system. Exited.')
        print('grid_config_local: This is not a LLSC system. ')

    grid_config['remote_launch'] = 'ssh'
    grid_config['remote_flags'] = '-q -x'
    #
    # Define default resource for a given cluster system
    if cluster_name == 'aicr':
        grid_config['default_q_name'] = 'rtx-devel'
        grid_config['default_cpu_type'] = 'amd-e9575'
    else:
        grid_config['default_q_name'] = 'xeon-p8'
        grid_config['default_cpu_type'] = 'xeon-p8'
    grid_config['q_name'] = grid_config['default_q_name']
    grid_config['cpu_type'] = grid_config['default_cpu_type']
    #
    # Paths for PythonMPI installation location and customization
    if cluster_name == 'aicr':
        # AIRC systems
        grid_config['GRID_HOME_PATH'] = os.path.join('/home',grid_config['remote_user'])
    else:
        # LLSC systems
        grid_config['GRID_HOME_PATH'] = os.path.join('/home/gridsan',grid_config['remote_user'])
    
    # LLGrid Filesystem
    if cluster_name == 'aicr':
        # AICR systems
        grid_config['LL_FILE_SERVER'] = 'login.aicr.ai'
    else:
        # LLSC SuperCloud systems
        grid_config['LL_FILE_SERVER'] = 'txe1-login.mit.edu'
    
    # HOME directory path
    HOME= os.getenv('HOME')

    # locally mounted GRID_HOME_PATH
    if os.path.exists('/etc/llgrid.id') or (cluster_name == 'aicr') :
        # path on the grid
        GRID_MOUNT_PATH = grid_config['GRID_HOME_PATH']
    else:
        # path on the local machines (required to run jobs on the grid)
        if OS.ispc:
            GRID_MOUNT_PATH = 'Z:'
        elif OS.islinux:
            GRID_MOUNT_PATH = '/home/gridsan/'+USER
        elif OS.ismac:
            GRID_MOUNT_PATH = '/Volumes/'+USER

    # pPython installation path
    try:
        if cluster_name == 'aicr':
            PPYTHON_HOME = os.getenv('PPYTHON_HOME','/home/cbyun_mit/.local/lib/python3.12/site-packages/pPython')
        else:
            PPYTHON_HOME = os.getenv('PPYTHON_HOME')
        # print('grid_config_local: PPYTHON_HOME = %s'%(PPYTHON_HOME))
        PPYTHON_PATH = os.path.join(PPYTHON_HOME,"src")
        # PythonMPI installation path
        PYTHONMPI_PATH = os.path.join(PPYTHON_HOME,"PythonMPI","src")
        # PythonMPI customization path for an individual user
        if os.path.exists(GRID_MOUNT_PATH):
            LOCAL_PYTHONMPI_CONFIG_PATH = os.path.join(GRID_MOUNT_PATH,"ppython_conf")
        else:
            LOCAL_PYTHONMPI_CONFIG_PATH = os.path.join(HOME,"ppython_conf")
        # pPython path (codes for scheduler integration)
        GRIDPYTHON_PATH = os.path.join(PPYTHON_HOME,"sched")
        # Current working directory path
        CWD_PATH = os.getcwd()
    except Exception:
        raise Exception('grid_config_local: Failed to setup environment variables')


    # Additional paths for PGAS using the distributed map and array construction
    DMAP_PATH = PPYTHON_PATH+os.sep+"map"
    DMAT_PATH = PPYTHON_PATH+os.sep+"dmat"

    # Save in the grid_config variable
    grid_config['GRID_MOUNT_PATH'] =  GRID_MOUNT_PATH
    grid_config['PPYTHON_PATH'] = PPYTHON_PATH
    grid_config['PYTHONMPI_PATH'] = PYTHONMPI_PATH
    grid_config['LOCAL_PYTHONMPI_CONFIG_PATH'] = LOCAL_PYTHONMPI_CONFIG_PATH
    grid_config['GRIDPYTHON_PATH'] = GRIDPYTHON_PATH
    grid_config['CWD_PATH'] = CWD_PATH

    # Additional paths for PGAS using the distributed map and array construction
    grid_config['DMAP_PATH'] = DMAP_PATH
    grid_config['DMAT_PATH'] = DMAT_PATH

    # Set TMPDIR
    PPYTHON_TMPDIR = os.getenv('PPYTHON_TMPDIR','')
    if PPYTHON_TMPDIR:
        grid_config['TMPDIR'] = PPYTHON_TMPDIR
    else:
        if cluster_name == 'aicr':
            grid_config['TMPDIR'] = '/tmp'
        else:
            grid_config['TMPDIR'] = '/state/partition1/slurm_tmp'
    if DEBUG:
        print('grid_config_local: Set pPYTHON to use TMPDIR = %s'%(grid_config['TMPDIR']))

    # Additional pPython variables to switch between MPI4PY and PythonMPI
    # Set default False as a bool data type
    PPYTHON_USE_MPI4PY = os.getenv('PPYTHON_USE_MPI4PY','')
    if PPYTHON_USE_MPI4PY:
        if DEBUG:
            print('Set pPYTHON to use MPI4PY')
        grid_config['USE_MPI4PY'] = True
    else:
        if DEBUG:
            print('Set pPYTHON to use PythonMPI')
        grid_config['USE_MPI4PY'] = False

    # Triples modes releated
    grid_config['nnode'] = 0

    # Scheduler information
    grid_config['scheduler'] = 'slurm'
    grid_config['ntasks'] = 1

    # Additional pPython environment variables for new features
    # It can be overridden by setting environment variable before pRUN()
    grid_config['srun'] = False
    # if set to 1, use message kernel with local filesystem. PPYTHON_LOCAL_FS='no' can make to use the central filesystem
    grid_config['local_fs'] = 0
    # For now, no mnaycore optimization
    grid_config['PPYTHON_MANYCORE'] = 'no'

    if DEBUG:
        print(grid_config)
        print('--> Exiting grid_config_local')

    return grid_config

########################################################
# pPython: Parallel Python Programming Tool
# Dr. Jeremy Kepner and Dr. Chansup Byun
# (kepner@ll.mit.edu and cbyun@ll.mit.edu)
# MIT Lincoln Laboratory
########################################################
# Copyright (c) 2023, Massachusetts Institute of Technology All rights
# reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in
#        the documentation and/or other materials provided with the
#        distribution.
#      * Neither the name of the Massachusetts Institute of Technology nor
#        the names of its contributors may be used to endorse or promote
#        products derived from this software without specific prior written
#        permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

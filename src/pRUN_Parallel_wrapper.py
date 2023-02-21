import time
from datetime import datetime
import os
from timeit import default_timer as timer

import pyMPI_COMM_WORLD as pyMCW

import pPython as GPC
from pPython_init import *
from pPython_finalize import *
from slurm2hostmap import *

def pRUN_Parallel_wrapper(py_file):
    """
    pRUN parallel wrapper to launch all pPython processes in parallel.
    
    Python version: Dr. Chansup Byun
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering pRUN_Parallel_wrapper.')
        print(pyMCW.MPI_COMM_WORLD)
    
    MPI_COMM_WORLD = pyMCW.MPI_COMM_WORLD
    LAUNCH_TIMING = False
    if 'grid_config' in MPI_COMM_WORLD:
        # The default mode is defined in the grid_config_local
        grid_config = MPI_COMM_WORLD['grid_config']
        local_fs = grid_config['local_fs']
        islocal = grid_config['islocal']
        grid_job = grid_config['grid_job']
        interactive = grid_config['interactive']
        EPPAC = grid_config['EPPAC']
        # Passed from pRUN()
        LAUNCH_TIMING = grid_config['LAUNCH_TIMING']
    else:
        raise Exception('ERROR(pRUN_Parallel_wrapper): local_fs is not defined in grid_config with MPI_COMM_WORLD')
    
    if LAUNCH_TIMING:
        # Current time
        time_now = time.time()
        print(' ')
        print('pRUN_Parallel_Wrapper: after pPython parallel wrapper started (Epoch in sec) = %d'%(int(time_now)))
        print('pRUN_Parallel_Wrapper: after pPython parallel wrapper started (Current time) = %s' %(datetime.fromtimestamp(time_now)))
        print(' ')
    
    # Generat the host-to-rank map with TMPDIR only if using local filesystem
    pPython_init()
    
    #
    local_fs = grid_config['local_fs']
    if DEBUG:
        print(' ')
        print('pRUN_Parallel_Wrapper: local_fs = %d'%(local_fs))
        print(' ')

    if (grid_job==True) and EPPAC:
        tic = timer()
        # update MPI_COMM_WORLD
        # add mixed messaging kernel support
        slurm2hostmap()
        h2mtime = timer()-tic
        GPC.comm = MPI_COMM_WORLD
        print('Time for the host-to-rank map with TMPDIR (sec): %.3f' %(h2mtime))

    # Display the start of the program for the many-core jobs
    if grid_config['PPYTHON_MANYCORE'].lower() == 'yes':
        myhostname = os.uname()[1]
        print('MANYCORE JOB, BEGIN: on %s'%(myhostname))

    if LAUNCH_TIMING:
        time_now = time.time()
        print(' ')
        print('pRUN_Parallel_Wrapper: Application starts at (Epoch in sec) = %d'%(int(time_now)))
        print('pRUN_Parallel_Wrapper: Application starts at (Current time) = %s' %(datetime.fromtimestamp(time_now)))
    
    # Start the program
    exec(open(py_file).read())
    
    if LAUNCH_TIMING:
        # Current time
        time_now = time.time()
        print(' ')
        print('pRUN_Parallel_Wrapper: Application finished at (Epoch in sec) = %d'%(int(time_now)))
        print('pRUN_Parallel_Wrapper: Application finished at (Current time) = %s' %(datetime.fromtimestamp(time_now)))
        print(' ')
    
    # Display the end of the program for the many-core jobs
    if grid_config['PPYTHON_MANYCORE'].lower() == 'yes':
        print('MANYCORE JOB, DONE: on %s'%(myhostname))

        if grid_config['manycore_implicit']:
            if DEBUG:
                print("pRUN_Parallel_Wrapper: grid_config['manycore_implicit'] = 1,"+\
                      " reset PPYTHON_MANYCORE & grid_config['manycore_implicit'] = 0")
            grid_config['manycore_implicit'] = 0
            grid_config['PPYTHON_MANYCORE'] = ''
            os.environ['PPYTHON_MANYCORE'] = ''
        else:
            if DEBUG:
                print("pRUN_Parallel_Wrapper: grid_config['manycore_implicit'] = 0")
                print('pRUN_Parallel_Wrapper: os.getenv(PPYTHON_MANYCORE) = %s'%(os.getenv('PPYTHON_MANYCORE')))

        grid_config['srun'] = False
    else:
        if DEBUG:
            print("pRUN_Parallel_Wrapper: grid_config['PPYTHON_MANYCORE'] is NOT yes.")
            print('pRUN_Parallel_Wrapper: os.getenv(PPYTHON_MANYCORE) = %s'%(os.getenv('PPYTHON_MANYCORE')))

    os.environ['PPYTHON_CPU_TYPE'] = ''
    
    pPython_finalize()
    GPC.Pid = 0
    GPC.Np = 1
    
    if DEBUG:
        print('<-- Exiting pRUN_Parallel_wrapper.')

    return

########################################################
# pMatlab: Parallel Matlab Toolbox
# Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
# Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
# MIT Lincoln Laboratory
########################################################
# Copyright (c) 2005, Massachusetts Institute of Technology All rights
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

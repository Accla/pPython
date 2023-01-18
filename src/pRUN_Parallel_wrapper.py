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

    if local_fs and (grid_job==True):
        # update MPI_COMM_WORLD
        tic = timer()
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


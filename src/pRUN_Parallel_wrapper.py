import datetime
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
    if LAUNCH_TIMING:
        # Current time
        t = datetime.datetime.now()
        print('pRUN_Parallel_Wrapper: after pPython started. (Epoch in sec) = %d'%(int(t.strftime('%s'))))
        print('pRUN_Parallel_Wrapper: after pPython started. (Current time) = %s' %(t))
    
    pPython_init()
    
    # Generat the host-to-rank map with TMPDIR only if using local filesystem
    if 'grid_config' in MPI_COMM_WORLD:
        # The default mode is defined in the grid_config_local
        grid_config = MPI_COMM_WORLD['grid_config']
        local_fs = grid_config['local_fs']
        islocal = grid_config['islocal']
        grid_job = grid_config['grid_job']
        interactive = grid_config['interactive']
    else:
        raise Exception('ERROR(pRUN_Parallel_wrapper): local_fs is not defined in grid_config with MPI_COMM_WORLD')
    #
    # Override if PPYTHON_LOCAL_FS is defined
    PPYTHON_LOCAL_FS = os.getenv('PPYTHON_LOCAL_FS')
    if (PPYTHON_LOCAL_FS):
        if (PPYTHON_LOCAL_FS.lower() == 'yes'):
            local_fs = 1
        else:
            local_fs = 0
        grid_config['local_fs'] = local_fs

    if DEBUG:
        print(' ')
        print('pRUN_Parallel_Wrapper: local_fs = %d'%(local_fs))
        print(' ')

    if local_fs and (grid_job==True):
        if interactive:
            raise Exception('ERROR(pRUN_Parallel_wrapper): Interactive grid job does not support message using local filesystem. Use backgrounded mode.')
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

    if DEBUG:
        t = datetime.datetime.now()
        print('pRUN_Parallel_Wrapper: Program starts. (Epoch in sec) = %d'%(int(t.strftime('%s'))))
        print('pRUN_Parallel_Wrapper: Program starts. (Current time) = %s' %(t))
    
    # Start the program
    exec(open(py_file).read())
    
    # Display the end of the program for the many-core jobs
    if grid_config['PPYTHON_MANYCORE'].lower() == 'yes':
        print('MANYCORE JOB, END: on %s'%(myhostname))

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

        grid_config['PPYTHON_SRUN'] = ''
    else:
        if DEBUG:
            print("pRUN_Parallel_Wrapper: grid_config['PPYTHON_MANYCORE'] is NOT yes.")
            print('pRUN_Parallel_Wrapper: os.getenv(PPYTHON_MANYCORE) = %s'%(os.getenv('PPYTHON_MANYCORE')))

    os.environ['PPYTHON_CPU_TYPE'] = ''
    
    pPython_finalize()
    GPC.Pid = 0
    GPC.Np = 1
    
    if DEBUG:
        # Current time
        t = datetime.datetime.now()
        print('pRUN_Parallel_Wrapper: Exited. (Epoch in sec) = %d'%(int(t.strftime('%s'))))
        print('pRUN_Parallel_Wrapper: Exited. (Current time) = %s' %(t))
        print('<-- Exiting pRUN_Parallel_wrapper.')

    return


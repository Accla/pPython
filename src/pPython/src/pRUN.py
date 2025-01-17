import time
from datetime import datetime
import re
import os
import sys
from timeit import default_timer as timer

LAUNCH_TIMING = False
if LAUNCH_TIMING:
    # Current time
    time_now = time.time()
    print(' ')
    print('pRUN start time (Epoch in sec) = %d'%(int(time_now)))
    print('pRUN (Current time) = %s' %(datetime.fromtimestamp(time_now)))
    print(' ')

# Set pPython & PythonMPI search path and import it
PPYTHON_HOME = os.getenv('PPYTHON_HOME')
if isinstance(PPYTHON_HOME,type(None)):
    raise Exception('ERROR(pRUN): PPYTHON_HOME is not set.')
if not os.path.exists(PPYTHON_HOME):
    raise Exception('ERROR(pRUN): PPYTHON_HOME path, %s, does not exist.'%(PPYTHON_HOME))
PPYTHON_PATH = PPYTHON_HOME+os.sep+'src'

# Assuming PythonMPI is distributed with pPython as shown below
# PythonMPI path must be added first
PYTHONMPI_PATH = PPYTHON_HOME+os.sep+'PythonMPI'+os.sep+'src'
sys.path.append(PYTHONMPI_PATH)

# Additional paths for distributed map and array support
DMAP_PATH = PPYTHON_PATH+os.sep+'map'
sys.path.append(DMAP_PATH)
DMAT_PATH = PPYTHON_PATH+os.sep+'dmat'
sys.path.append(DMAT_PATH)

# Additional path for gridPython (code for scheduler integration)
GRIDPYTHON_PATH = PPYTHON_HOME+os.sep+"grid"
sys.path.append(GRIDPYTHON_PATH)

# Assuming local configuration is available from $HOME/ppython_conf directory.
LOCAL_PYTHONMPI_CONFIG_PATH = os.getenv('HOME')+os.sep+'ppython_conf'
if os.path.exists(LOCAL_PYTHONMPI_CONFIG_PATH):
    sys.path.append(LOCAL_PYTHONMPI_CONFIG_PATH)
else:
    raise Exception('ERROR(pRUN): LOCAL_PYTHONMPI_CONFIG_PATH path, %s, does not exist.'%(LOCAL_PYTHONMPI_CONFIG_PATH))

if os.path.exists(PYTHONMPI_PATH):
    sys.path.append(PPYTHON_PATH)
    import checkOS as OS
    # from PythonMPI import *
    from pyMPI_Delete_all import *
    from pyMPI_Sleep import *
    # print('Minimum PythonMPI functions are loaded for pRUN().')
else:
    raise Exception('ERROR(pRUN): PythonMPI package path, %s, does not exist.'%(PYTHONMPI_PATH))
    
if os.path.exists(GRIDPYTHON_PATH):
    import grid_config as grid
    # from pPython import *
    from check_allowance import *
    from grid_abort import *
    from grid_config_init import *
    from grid_run import *
    from check_runtime import *
    # print('gridPython functions are loaded......')
else:
    raise Exception('ERROR(pRUN): gridPython package path, %s, does not exist.'%(GRIDPYTHON_PATH))
print(' ')

def pRUN(py_file,n_proc,machines,sched_options=None):
    """Launch a PythonMPI script on a grid environment with a scheduler.
    
    Usage:
    ------
    pRUN('py_code.py', n_proc, 'grid', 'scheduler options')
        Launch interactively on a suppored cluster system with the scheduler integration.
    
    pRUN('py_code.py', n_proc, 'grid&')
        Launch as a backgrounded job on a grid environment.
        
    py_file: a PythonMPI code name
    n_proc: number of PythonMPI processes to spawn
    machines: either a string or a list of machines
        'grid': dispatch the job to the default queue (interactive jobs)
        'grid&': backgrounded job to the default queue (entire job is running on the grid)
        []: running on the local machine
        ['machine_a','machine_b',...]: a list of machines to dispatch the job
    sched_options: additional scheduler options when using the scheduler [ToDo]

    Python version: Dr. Chansup Byun
    """
    
    # At this point, grid_config should be set.
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering pRUN')
        for p in sys.path:
            print(p)
        
    # Initialize the grid_config parameters
    grid.grid_config = grid_config_init()

    if sched_options:
        grid.grid_config['sched_options'] = sched_options

    grid.grid_config['LAUNCH_TIMING'] = False
    if LAUNCH_TIMING:
        grid.grid_config['LAUNCH_TIMING'] = LAUNCH_TIMING

    n_proc_req, machines, grid.grid_config = check_runtime( n_proc, machines, grid.grid_config )
    if DEBUG:
        print('After check_runtime: n_proc_req = %d'%(n_proc_req))
        print(grid.grid_config)

    if grid.grid_config['grid_job']:
        # Check allowance 
        cpu_type = grid.grid_config['cpu_type'] 

        # If a backgrounded triples mode job is launched with the environment variable PPYTHON_SRUN=yes,
        # do not check allowance for the job and the job will be submitted as a batch job using srun.
        chk_allowance = True
        if (os.getenv('PPYTHON_SRUN',default='no').lower() == 'yes'):
            grid.grid_config['srun'] = True
        else:
            grid.grid_config['srun'] = False
        if grid.grid_config['srun'] and grid.grid_config['EPPAC'] and (grid.grid_config['interactive']==0):
            chk_allowance = False

        status = 0
        if chk_allowance:
            status = check_allowance(n_proc_req,cpu_type)
        if DEBUG:
            print('pRUN: n_proc_req,cpu_type = %d, %s'%(n_proc_req,cpu_type))
            print('check_allowance status: %d'%(status))
    
    # For PC, use ;, For Mac & Linux, use :
    if OS.ispc:
        sep_path = ";"
    else:
        sep_path = ':'
        
    # Construct the PythonMPI search paths
    # For PC, use ;, For Mac & Linux, use :
    if OS.ispc:
        sep_path = ";"
    else:
        sep_path = ':'
        
    GRID_PATH = grid.grid_config['PPYTHON_PATH']+sep_path \
        +grid.grid_config['GRIDPYTHON_PATH']+sep_path \
        +grid.grid_config['PYTHONMPI_PATH']+sep_path \
        +grid.grid_config['LOCAL_PYTHONMPI_CONFIG_PATH']+sep_path \
        +grid.grid_config['DMAP_PATH']+sep_path \
        +grid.grid_config['DMAT_PATH']+sep_path \
        +grid.grid_config['CWD_PATH']
    os.environ["PYTHONMPI_PATH"] = GRID_PATH

    # Disable HDF5 file locking
    os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

    # Launch the script.
    print('Running: %s'%(py_file))

    # Clean up an old PythonMPI run
    if grid.grid_config['grid_job']:
        if DEBUG:
            print('. . . called grid_abort(grid.grid_config)')
        grid_abort(grid.grid_config)
    else:
        if DEBUG:
            print('. . . called grid_abort()')
        grid_abort()
    # wait for the filesystem update
    pyMPI_Sleep(1.0)
    pyMPI_Delete_all()
    # wait for the filesystem update
    pyMPI_Sleep(1.0)

    # Launch PythonMPI
    if DEBUG:
        print('grid_run called . . .')
    cmd = grid_run(py_file, n_proc_req, machines)

    if DEBUG:
        print('<-- Exiting pRUN')

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

import re
import os
import sys

# Set gridPython & PythonMPI search path and import it
GRIDPYTHON_HOME = os.getenv('GRIDPYTHON_HOME')
GRIDPYTHON_PATH = GRIDPYTHON_HOME+os.sep+'src'
if not os.path.exists(GRIDPYTHON_PATH):
    print('Need to set the environment variable, GRIDPYTHON_PATH')
    exit()
sys.path.append(GRIDPYTHON_PATH)

# Assuming PythonMPI is distributed with gridPython as shown below
PYTHONMPI_PATH = GRIDPYTHON_HOME+os.sep+'PythonMPI'+os.sep+'src'
sys.path.append(PYTHONMPI_PATH)

# Assuming local configuration is available from $HOME/pythonmpi directory.
HOME = os.getenv('HOME')
USER_PYTHONMPI_PATH = HOME+os.sep+'pythonmpi'
sys.path.append(USER_PYTHONMPI_PATH)

# PythonMPI path must be added first
if os.path.exists(PYTHONMPI_PATH):
    import checkOS as OS
    from PythonMPI import *
else:
    print('pRUN: PythonMPI package is not found at %s.'%(PYTHONMPI_PATH))
    exit()
    
if os.path.exists(GRIDPYTHON_PATH):
    import grid_config as grid
    from gridPython import *
else:
    print('pRUN: gridPython package is not found at %s.'%(GRIDPYTHON_PATH))
    exit()

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
    
    """
    
    # At this point, grid_config should be set.
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering pRUN')
        for p in sys.path:
            print(p)
        
    # Initialize the grid_config parameters
    grid.grid_config = grid_config_init()

    if DEBUG:
        print(grid.grid_config)

    # Check allowance 
    cpu_type = grid.grid_config['default_cpu_type'] 
    status = check_allowance(n_proc,cpu_type)
    if DEBUG:
        print('pRUN: n_proc,cpu_type = %d, %s'%(n_proc,cpu_type))
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
        
    GRID_PATH = grid.grid_config['GRIDPYTHON_PATH']+sep_path \
        +grid.grid_config['PYTHONMPI_PATH']+sep_path \
        +grid.grid_config['USER_PYTHONMPI_PATH']
    os.environ["PYTHONMPI_PATH"] = GRID_PATH

    # Disable HDF5 file locking
    os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

    # Launch the script.
    print('Running: %s'%(py_file))

    # Clearn up an old PythonMPI run
    MPI_Abort(grid.grid_config)
    # wait for the filesystem update
    pyMPI_Sleep(1.0)
    pyMPI_Delete_all()
    # wait for the filesystem update
    pyMPI_Sleep(1.0)

    # Launch PythonMPI
    if DEBUG:
        print('MPI_Run called . . .')
    cmd = MPI_Run(py_file, n_proc, machines)

    if DEBUG:
        print('<-- Exiting pRUN')

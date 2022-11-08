"""RUN.py

Example to run a PythonMPI code with pPython
To run, execute the following command.

    python RUN.py
"""

import os
import sys
import platform

# Specify whether using pPython installed on the grid or locally
GRID_PPYTHON = True  # True (grid installation)  or False(local  installation)

# PPYTHON_HOME environment variable should be set in order to find the pPython installation
system_name = platform.system()

if GRID_PPYTHON:
    # Use pPython installed on the grid
    # ToDo: update the path accordingly
    if system_name in ['Windows']:
        # For Windows OS environment, prefix with r to fix the unicodeunderscore codec issue
        GRID_MOUNT_PATH = r"Z:"
    elif system_name in ['Darwin']:
        # For Mac OS environment, the grid mount path includes the user name
        GRID_MOUNT_PATH = "/Volumes/ch21778"
    else:
        # For Linux OS environment, the grid mount path can be an arbitrary path
        GRID_MOUNT_PATH = "/home/gridsan/ch21778"
    PPYTHON_HOME = GRID_MOUNT_PATH + "/llgrid_beta/pPython/latest"
else:
    # Use pPython installed locally
    # ToDo: update the path accordingly
    if system_name in ['Windows']:
        # For Windows OS environment, prefix with r to fix the unicodeunderscore codec issue
        PPYTHON_HOME = r"C:\Users\CH21778\pPython\Ver-0.8.3"
    elif system_name in ['Darwin']:
        # For Mac OS environment
        PPYTHON_HOME = "/Users/ch21778/Documents/pPython/Ver-0.8.3"
    else:
        # For Linux OS environment
        PPYTHON_HOME = "/home//cbyun/projects/python/pPython/Ver-0.8.38"

os.environ["PPYTHON_HOME"] = PPYTHON_HOME

# Add Python search path for pPython main function
PPYTHON_PATH = PPYTHON_HOME+os.sep+"src"
sys.path.append(PPYTHON_PATH)

# Import PythonMPI launch funciton
from pRUN import *

# Disable HDF5 file locking (Lustre parallel filesystem on LLSC)
if GRID_PPYTHON:
    os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

# PythonMPI script filename
py_file = 'pRandomAccess.py'
# Define number of MPI processes
n_proc = 4

# Launch PythonMPI
# print('Running: %s via pRUN().'%(py_file))
if GRID_PPYTHON:
    pRUN( py_file, n_proc, 'grid' )
else:
    pRUN( py_file, n_proc, {} )


"""RUN.py

Example to run a PythonMPI code with pPython
To run, execute the following command.

    python RUN.py
"""

import os
import sys
import platform

"""
Customization for the user environment
"""
# Specify whether using pPython installed on the grid or locally
GRID_PPYTHON = False  # True (grid installation) or False(local installation)
USE_LATEST_VERSION = True
PPYTHON_VER = 'v0.9.1'

# PPYTHON_HOME environment variable should be set in order to find the pPython installation
system_name = platform.system()

if GRID_PPYTHON:
    # Use pPython installed on the grid
    # ToDo: update the GRID_MOUNT_PATH accordingly
    if system_name in ['Windows']:
        # For Windows OS environment, prefix with r to fix the unicodeunderscore codec issue
        GRID_MOUNT_PATH = r"Z:"
    elif system_name in ['Darwin']:
        # For Mac OS environment, the GRID_MOUNT_PATH includes the user name
        GRID_MOUNT_PATH = "/Volumes/ch21778"
    else:
        # For Linux OS environment, the GRID_MOUNT_PATH can be an arbitrary path
        GRID_MOUNT_PATH = "/home/gridsan/ch21778"
    QA_ON_GIT = os.getenv('QA_ON_GIT')
    if QA_ON_GIT:
        PPYTHON_HOME = GRID_MOUNT_PATH + "/devtools/git/pPython"
    else:
        PPYTHON_HOME = GRID_MOUNT_PATH + "/llgrid_beta/pPython/latest"
    print('RUN.py: PPYTHON_HOME = %s'%(PPYTHON_HOME))
else:
    # Use pPython installed locally
    # ToDo: update the GRID_MOUNT_PATH path accordingly
    if system_name in ['Windows']:
        # For Windows OS environment, prefix with r to fix the unicodeunderscore codec issue
        if USE_LATEST_VERSION:
            PPYTHON_HOME = r"C:\Users\CH21778\pPython\latest"
        else:
            PPYTHON_HOME = r"C:\Users\CH21778\pPython"+os.sep+PPYTHON_VER
    elif system_name in ['Darwin']:
        # For Mac OS environment
        if USE_LATEST_VERSION:
            PPYTHON_HOME = "/Users/ch21778/Documents/pPython/latest"
        else:
            PPYTHON_HOME = "/Users/ch21778/Documents/pPython/"+PPYTHON_VER
    else:
        # For Linux OS environment
        if USE_LATEST_VERSION:
            PPYTHON_HOME = "/home//cbyun/projects/python/pPython/latest"
        else:
            PPYTHON_HOME = "/home//cbyun/projects/python/pPython/"+PPYTHON_VER

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
py_file = 'pHPL.py'
# Define number of MPI processes
n_proc = 4

# Launch PythonMPI
# print('Running: %s via pRUN().'%(py_file))
if GRID_PPYTHON:
    pRUN( py_file, n_proc, 'grid' )
else:
    pRUN( py_file, n_proc, {} )


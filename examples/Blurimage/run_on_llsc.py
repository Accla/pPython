"""RUN.py

Example to run a PythonMPI code with pPython
To run, execute the following command.

    python RUN.py
"""

import os
import sys
import platform

# PPYTHON_HOME environment variable should be set in order to find the pPython installation
system_name = platform.system()
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
os.environ["PPYTHON_HOME"] = PPYTHON_HOME

# Add Python search path for pPython main function
PPYTHON_PATH = PPYTHON_HOME+os.sep+"src"
sys.path.append(PPYTHON_PATH)

# Import PythonMPI launch funciton
from pRUN import *

# Disable HDF5 file locking (Lustre parallel filesystem on LLSC)
os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

# PythonMPI script filename
py_file = 'pBlurimage.py'
# Define number of MPI processes
n_proc = 4

# Launch PythonMPI
# print('Running: %s via pRUN().'%(py_file))
# pRUN( py_file, n_proc, 'grid&' )
# pRUN( py_file, n_proc, 'grid-xeon-p8&','--exclusive' )
pRUN( py_file, n_proc, 'grid-xeon-e5')
# pRUN( py_file, n_proc, {} )


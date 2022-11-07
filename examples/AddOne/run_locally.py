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
    PPYTHON_HOME = r"C:\Users\CH21778\pPython\Ver-0.8.3"
elif system_name in ['Darwin']:
    # For Mac OS environment, the grid mount path includes the user name
    PPYTHON_HOME = "/Users/ch21778/Documents/pPython/Ver-0.8.3"
else:
    # For Linux OS environment, the grid mount path can be an arbitrary path
    PPYTHON_HOME = "/home/gridsan/ch2177/projects/python/pPython/Ver-0.8.38"

os.environ["PPYTHON_HOME"] = PPYTHON_HOME

PPYTHON_PATH = PPYTHON_HOME+os.sep+"src"
sys.path.append(PPYTHON_PATH)

# Local configuration setup
# LOCAL_PYTHONMPI_CONFIG_PATH = os.getenv('HOME')+os.sep+"pythonmpi"
# sys.path.append(LOCAL_PYTHONMPI_CONFIG_PATH)

# Import PythonMPI launch funciton
from pRUN import *

# Disable HDF5 file locking (Lustre parallel filesystem on LLSC)
# os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

# PythonMPI script filename
py_file = 'pAddOne.py'
# Define number of MPI processes
n_proc = 4

# Launch pPython
# print('Running: %s via pRUN().'%(py_file))
pRUN( py_file, n_proc, {} )


"""RUN.py

    Example to run a PythonMPI code with gridPython

    Python environemtn with the following packages:
        matplotlib
        glob
        h5py
        numpy
        pickle
        scipy
        time

    To run, execute the following command.
        python RUN.py

"""

import os
import sys

# Export the path to find gridPython & PythonMPI source code:
GRIDPYTHON_HOME = "/home/gridsan/ch21778/devtools/git/gridPython"
GRIDPYTHON_PATH = GRIDPYTHON_HOME+os.sep+"src"
os.environ["GRIDPYTHON_HOME"] = GRIDPYTHON_HOME
sys.path.append(GRIDPYTHON_PATH)

# Import PythonMPI launch funciton
from pRUN import *

# Disable HDF5 file locking (Lustre parallel filesystem on LLSC)
os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

# PythonMPI script filename
py_file = 'basic.py'
# Define number of MPI processes
n_proc = 4

# Launch PythonMPI
print('Running: %s via pRUN().'%(py_file))
pRUN( py_file, n_proc, 'grid&' )


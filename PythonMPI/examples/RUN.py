"""RUN.py

    Example to run a PythonMPI code

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

# Export the path to find PythonMPI source code:
PYTHONMPI_PATH = "/home/gridsan/ch21778/devtools/git/PythonMPI/src"
sys.path.append(PYTHONMPI_PATH)
# Add the current working directory to the system path
# so that any Python codes in the current working directory 
# can be called
CWD_PATH = os.getcwd()
sys.path.append(CWD_PATH)

# Import PythonMPI
from PythonMPI import *

# Disable HDF5 file locking
os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"
# Export PYTHONMPI_PATH so that MPI_Run() update the systme path
# for the MPI processes running remote hosts
os.environ["PYTHONMPI_PATH"] = PYTHONMPI_PATH+":"+CWD_PATH

# PythonMPI script filename
py_file = 'basic.py'

# Define number of MPI processes
n_proc = 4

# cpus = { 'c-5-8-1', 'c-5-8-2' };
cpus = {'a-20-11','a-20-12'}

# Launch the script.
print('Running: %s'%(py_file))

# Clearn up an old PythonMPI run
MPI_Abort()
pyMPI_Delete_all()
# wait for the filesystem update
pyMPI_Sleep(1.0)

# Launch PythonMPI
cmd = MPI_Run( py_file, n_proc, cpus )


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
HOME_PATH = os.getenv('HOME')
LLSC_PPYTHON_HOME = HOME_PATH+"/devtools/git/pPython/src/pPython"
LLSC_PPYTHON_SRC = LLSC_PPYTHON_HOME+'/src'
PYTHONMPI_PATH = LLSC_PPYTHON_HOME+"/PythonMPI/src"

sys.path.append(PYTHONMPI_PATH)
PPYTHON_CONF_PATH = HOME_PATH+"/ppython_conf"
sys.path.append(PPYTHON_CONF_PATH)
# Add the current working directory to the system path
# so that any Python codes in the current working directory 
# can be called
CWD_PATH = os.getcwd()
sys.path.append(CWD_PATH)

# Import PythonMPI
from MPI_Abort import *
from pyMPI_Delete_all import *
from pyMPI_Sleep import *
from MPI_Run import *

# Disable HDF5 file locking
os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"
# Export PYTHONMPI_PATH so that MPI_Run() update the systme path
# for the MPI processes running remote hosts
os.environ["PYTHONMPI_PATH"] = PYTHONMPI_PATH+":"+CWD_PATH

PYTHON_PATH = PYTHONMPI_PATH+':'+LLSC_PPYTHON_HOME+':'+LLSC_PPYTHON_SRC
os.environ["PYTHONPATH"] = PYTHON_PATH
print('PYTHONPATH: %s'%(PYTHON_PATH))

# PythonMPI script filename
py_file = 'blurimage.py'

# Define number of MPI processes
n_proc = 4

cpus = ['a-17-25.llgrid.ll.mit.edu','a-17-26.llgrid.ll.mit.edu']
# Launch the script.
print('Running: %s'%(py_file))

# Clearn up an old PythonMPI run
MPI_Abort()
pyMPI_Delete_all()
# wait for the filesystem update
pyMPI_Sleep(1.0)

# Launch PythonMPI
cmd = MPI_Run( py_file, n_proc, cpus )


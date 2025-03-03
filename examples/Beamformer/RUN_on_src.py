"""RUN.py

Example to run a pPython code with pPython source installation
To run, execute the following command.

    python RUN_on_src.py
"""

import os
import sys

"""
Customization for the user runtime environment
"""
HOME_PATH = os.getenv('HOME')
PPYTHON_HOME = HOME_PATH + "/devtools/git/pPython/src/pPython"
os.environ["PPYTHON_HOME"] = PPYTHON_HOME

# Add Python search path for pPython main function
PPYTHON_PATH = PPYTHON_HOME+os.sep+"src"
sys.path.append(PPYTHON_PATH)

#Update PYTHONPATH to direct to the pPython modules from the source location
PYTHONPATH=PPYTHON_HOME+os.sep+'PythonMPI'+os.sep+'src'
PYTHONPATH=PYTHONPATH+':'+PPYTHON_HOME+os.sep+'src'+os.sep+'map'
PYTHONPATH=PYTHONPATH+':'+PPYTHON_HOME+os.sep+'src'+os.sep+'dmat'
PYTHONPATH=PYTHONPATH+':'+PPYTHON_HOME+os.sep+'src'
PYTHONPATH=PYTHONPATH+':'+PPYTHON_HOME+os.sep+'sched'
PYTHONPATH=PYTHONPATH+':'+PPYTHON_HOME
os.environ["PYTHONMPI"]=PYTHONPATH
# print('PYTHONMPI=%s'%(PYTHONPATH))

# Import PythonMPI launch funciton
from pRUN import *

# Disable HDF5 file locking (Lustre parallel filesystem on LLSC)
os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

# PythonMPI script filename
py_file = 'pBeamformer.py'
# Define number of MPI processes
n_proc = 4
n_proc_triples = [4,2,24]

# Launch pPython
# print('Running: %s via pRUN().'%(py_file))
print('Running on grid ...')

run_locally = 0
if run_locally:
    # Running locally
    pRUN( py_file, n_proc, {})
else:
    # Running on a grid environment if configured properly
    # Use the triples mode job
    GRID_TARGET = 'grid-xeon-p8'
    pRUN( py_file, n_proc_triples, GRID_TARGET )



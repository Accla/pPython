import pyMPI_COMM_WORLD as pyMCW

"""Share Grid Python Environment Variables
"""
# Define MPI_COMM_WORLD dictionary if not defined.
try: comm
except NameError: comm = None
if comm is None:
        comm = pyMCW.MPI_COMM_WORLD



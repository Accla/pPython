"""pyMPI_COMM_WORLD - share MPI_COMM_WORLD among Python modules

    Import MPI_COMM_WORLD with Python pyMCW module
    (defined in PythonMPI.py and called in by MPI_Run())
    This is a work around to mimick MATLAB global variable, MPI_COMM_WORLD
    becauses Python global scope is not working consistently across multiple module files.
"""
# Define MPI_COMM_WORLD dictionary if not defined.
try: MPI_COMM_WORLD
except NameError: MPI_COMM_WORLD = None
if MPI_COMM_WORLD is None:
    MPI_COMM_WORLD = dict()


"""grid_config - share grid_config among Python modules

    Import grid_config with Python gc module
    (defined in PythonMPI.py and called in by MPI_Run())
    This is a work around to mimick MATLAB global variable, grid_config
    becauses Python global scope is not working consistently across multiple module files.
"""
# Define grid_config dictionary if not defined.
try: grid_config
except NameError: grid_config = None
if grid_config is None:
    grid_config = dict()


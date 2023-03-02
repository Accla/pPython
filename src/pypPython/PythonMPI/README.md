# PythonMPI

A project to port MatlabMPI to python environment. This module allows to parallelize python scripts so that it can be executed in parallel to process a large problem or to reduce the total execution time for a given problem.

In order to run PythonMPI, your python installation requires the following packages:
<pre>
        matplotlib
        glob
        h5py
        numpy
        pickle
        scipy
        time
</pre>
You will need to add the following  PythonMPI path to the Python system path so that PythonMPI sources can be called by PythonMPI code.
Also, PYTHONMPI_PATH environment variable should be exported so that MPI_Run() can update Python system search path for the Python processes launched on the remote hosts.
<br>
<pre>
PYTHONMPI_PATH = "/home/gridsan/ch21778/devtools/git/PythonMPI/src" 
sys.path.append(PYTHONMPI_PATH)
</pre>

If you are calling other Python modules from the current working directory outside of your main PythonMPI script, the current working directory path should be added to the Python system search path.
<br>
<pre>
CWD_PATH = os.getcwd()
sys.path.append(CWD_PATH)
</pre>
<br>
Export the PYTHONMPI_PATH environment variable so that MPI_Run() update the systme path for all MPI processes. You can add multiple paths by separating with the colon between the paths.
<br>
<pre>
os.environ["PYTHONMPI_PATH"] = PYTHONMPI_PATH+":"+CWD_PATH
</pre>
<br>
If you filesystem disables the file locking, you need to set the following environment variable in order to disable HDF5 file locking.
<br>
<pre>
os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"
</pre>
<br>
An example RUN.py script is available in the examples directory.



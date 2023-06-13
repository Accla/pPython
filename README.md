# pPython
pPython is a new LLSC capability that provides a parallel computing capability with good speed-up without sacrificing 
the ease of programming in Python. It will run on any combination of heterogeneous systems that support Python, 
including Windows, Linux, and MacOS operating systems.

In addition to running transparently on a single-node (e.g., a laptop), pPython provides a scheduler interface 
so that pPython can be executed in a massively parallel computing environment.

<br>
There are a few of requireemnts to use the pPython package
<br>
<li>
PythonMPI, which provides the minimal set of MPI functionalities in Python, is distributed with pPython at its installation directory. <br>
</li>
<li>
A local configuration files are required to customize the specific pPython runtime enivironment and they are installed at $HOME/ppython_conf directory.
</li>
<li>
For the grid environment, currently Slurm is the only scheduler supported by pPython for job dispatching and management and, depending on the cluster configuration, the local configuration files should be customized accordingly.
</li>
<br>
<br>
An example run script, RUN.py, is available in the example directory. 
<br>
<strong>Installation</strong>
The pPython package can be installed with the "pip install --user <pPYthon_package_name>" command.
In order to set up an interactive runtime environment on a local machine and launch pPython jobs to a grid environment,
the pPython package should be installed on both the local machine and the grid account in addition to mapping/mounting 
the home directory for the grid account on the local machine.

<strong>Running an example</strong>
The pPython examples distribued with the pPython source tarball file can be found in the dist directory from the git repository.
Once the pPython package is installed, an example can be executed by using the RUN.py script by typing
<li>
python RUN.py
</li>
from an example directory or it can be executed interactive by typing at the Python command prompt
<pre>
import pPyton
from pRUN import pRUN
pRUN('pMandelbrot.py',4,{})
</pre>
This will execute the parallel Mandelbrot example using 4 pPython processes locally.
<br>


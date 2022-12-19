# pPython

PythonMPI support with a grid environment so that jobs can be launched much easier
<br>
There are a couple of requireemnts to use the pPython package
<br>
<li>
It assumes that PythonMPI is distributed with pPython at its root directory. <br>
</li>
<li>
It is also assumes that a local configuration is available from $HOME/ppython_conf directory.
</li>
<br>
<br>
An example run script is available in the example directory. 
The following environment variables in the example run script need to be modified according to the user runtime environment.
This enables to run a pPython job either locally on a user desktop machine or on a grid environment.
GRID_PPYTHON: True (grid installation) or False(local installation) <br>
USE_LATEST_VERSION: True (use the latest version pointed by the latest symbolic link) or False (use the specific version defined by PPYTHON_VER) <br>
PPYTHON_VER: Define a specific version (such as v0.9.2) <br>
<br>
This will determine the PPYTHON_HOME environment variable.
<br>


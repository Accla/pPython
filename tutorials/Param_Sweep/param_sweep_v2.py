#
# Parameter sweep example: 
# Code section: 
#
# Extract the global and local properties for pPython process
# Print "My process ID (Pid or Rank)"
# Print "How many pPython processes are running (Np), Size"

# Define Map
# - How to distribute work load?

# File: param_sweep_v2.py

import pPython as GPC
from pPython.map import Dmap

# pPython MPI communicator.
comm = GPC.comm

# Get size and rank.
Np = GPC.Np
Pid = GPC.Pid

# Print rank.
print('Size: %d'%(Np))
print('My rank: %d'%(Pid))

# Define Map
pmap = Dmap([Np, 1], {}, range(Np), order='F')
print(pmap)

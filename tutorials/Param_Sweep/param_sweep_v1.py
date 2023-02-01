#
# Parameter sweep example: 
# Code section: 
#
# Extract the global and local properties for pPython process
# Print "My process ID (Pid or Rank)"
# Print "How many pPython processes are running (Np), Size"
# File: param_sweep_v1.py

import pPython as GPC

# pPython MPI communicator.
comm = GPC.comm

# Get size and rank.
Np = GPC.Np
Pid = GPC.Pid

# Print rank.
print('Size: %d'%(Np))
print('My rank: %d'%(Pid))
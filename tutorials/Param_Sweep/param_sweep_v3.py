#
# Parameter sweep example: 
# Code section: 
#
# Extract the global and local properties for pPython process
# Print "My process ID (Pid or Rank)"
# Print "How many pPython processes are running (Np), Size"
# Define Map
# - How to distribute work load?

# Create a distributed array (using the map)
# - How to find local portion of global indices?
# - How to find local portion of a distributed array (matrix)?

# File: param_sweep_v3.py

import pPython as GPC
from Dmap import *
from rand import *
from global_ind import *
from local import *

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

# Create a distributed matrix among Np processes (defined by pmap)
m = 16
n = 3
z = rand(m,n,map=pmap)

# Check the distributed z matrix
# Get the local portion of the global indices
my_i_global = global_ind(z, 0)[0]
print('Local portion of global indices in the first direction:')
print(my_i_global)

# Get the local portion of the distributed matrix
my_z = local(z)
print('Local portion of the distributed matrix')
print(my_z)

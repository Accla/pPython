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

# Do the computation independently
# - How to walk through the local portion of the work load?
# - How to save the result inot the distributed array (matrix)?

# File: param_sweep_v4.py

import pPython as GPC
from pPython.map import Dmap,rand
from pPython.dmat import global_ind,local,put_local

from sample_function import *

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
# print('Local portion of global indices in the first direction:')
# print(my_i_global)

# Get the local portion of the distributed matrix
my_z = local(z)
# print('Local portion of the distributed matrix')
# print(my_z)

# Loop over the local indices
for i_local in range(len(my_i_global)):
    # Determine the global index for this (local) iteration
    i_global = my_i_global[i_local]

    # Calculate another argument
    my_other_arg = 2.5 * i_global

    # call a function with the global index, and other arguments, and
    # store the result in a local row
    my_z[i_local,:] = sample_function(i_global, Pid, my_other_arg)


# print local results
print(' ')
print('Local result:')
print(my_z)

# Store the local portion of z into the distributed matrix z
z = put_local(z, my_z)
print('Updated local portion of global matric with the result on Pid = %d:'%(Pid))
print(local(z))


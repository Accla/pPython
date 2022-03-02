import numpy as np

from PythonMPI import *
from partition_1d import *

from sample_function import *
from agg_msg import *

# basic parameter sweep code
#
# Want to parallelize the for loop.
#
# Leader process Pid
leader = 0;

# Necessary setup for MPI processes
# Initialize MPI
MPI_Init()

# Create communicator. (pyMCW is imported in PythonMPI.py)
comm = pyMCW.MPI_COMM_WORLD;

# Get size and rank.
n_procs = MPI_Comm_size(comm)
my_rank = MPI_Comm_rank(comm)

# Print rank.
print('my_rank: %d'%(my_rank))

# Set data sizes.
m = 3   # number of output arguments
n = 16  # number of independent iterations

# Design data distribution among the MPI processes.
# (partition_1d is distributed with gridPython)
d_index,d_sizes = partition_1d(n,n_procs)
# print(d_index)
# print(d_sizes)
        
# Create z - data output matrix.
z = np.zeros((n, m),dtype=float)

# Get the local portion of the global indices
my_i_global = range(d_index[str(my_rank)]['beg'],d_index[str(my_rank)]['end']+1)

# Get the local portion of the distributed matrix
my_z = z[my_i_global,:]


# Loop over the local indices
i_local = 0
for i_global in my_i_global:
    # Determine the global index for this (local) iteration
    
    # Calculate another argument
    my_other_arg = 2.5 * i_global
    
    # call a function with the global index, and other arguments, and 
    # store the result in a local row
    my_z[i_local,:] = sample_function(i_global, my_rank, my_other_arg)

    # increase local index
    i_local += 1

# local results:
print('local results:')
print(my_z)

# Finally, aggregate all of the output onto the leader process
tag = 1004
z = agg_msg(z,my_z,d_index,leader,tag,comm)

# Finally, display the resulting matrix on the leader
if my_rank == leader:
    print('globally updated:')
    print(z)

# Finalize the pMATLAB program
print('SUCCESS');


"""test_param_sweep.py
    Test gridPython distributed array function, zeros()

    To run, start Pyhton and type:

        pRun('test_zeros.py',4,'grid')

    Output will be piped into two files:

        PythonMPI/test_zeros.0.out
        . . . 
        PythonMPI/test_zeros.3.out

    gridPython
    Dr. Chansup Byun
    MIT Lincoln Laboratory
    cbyun@ll.mit.edu
"""

from gridPython_all import *

from sample_function import *

# Initialize MPI
# MPI_Init()

# Create communicator.
# pyMCW is imported in PythonMPI.py
# comm = pyMCW.MPI_COMM_WORLD;
# GridPython as GPC in gridPython.py
comm = GPC.comm

# Get size and rank.
# Np = MPI_Comm_size(comm)
# Pid = MPI_Comm_rank(comm)
Np = GPC.comm_size
Pid = GPC.my_rank

# Print rank.
print('size: %d'%(Np))
print('my_rank: %d'%(Pid))

# Create a map
# 'b': block distribution, for details help('GridMap')
pmap = GridMap([Np,1],'b',range(Np))

# Create a distributed matrix on individual rank
m = 16
n = 3
z = zeros(m,n,dmap=pmap)

# Check the distributed z matrix
print('Local portion of global indices on Pid = %d:'%(Pid))
print(z.global_ind)
print('my local length:')
for i  in range(len(z.falls)):
    print_falls(z.falls[i])
print('my size:')
print(z.size)

# Get the local portion of the global indices
my_i_global = global_ind(z, 0)
print('Local portion of global indices in the first direction:')
print(my_i_global)

# Get the local portion of the distributed matrix
my_z = local(z)

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
print('Local result:')
print(my_z)

# Store the local portion of z into the distributed matrix z
z = put_local(z, my_z)
# print('Updated local portion of global matric with the result on Pid = %d:'%(Pid))
# print(z.local)

# To Do:
# Finally, aggregate all of the output onto the leader process
z_final = agg(z);
print('Final z_final on Pid = %d:'%(Pid))
print(z_final)


# Wait in order to check weather MPI message file is saved if uncommented line 42 above.
# pyMPI_Sleep(20)

# Finalize Matlab MPI.
print(' ')
print('SUCCESS')
print(' ')
print(' ')
# MPI_Finalize()

"""
 Copyright 2002 Massachusetts Institute of Technology
 
 Permission is herby granted, without payment, to copy, modify, display
 and distribute this software and its documentation, if any, for any
 purpose, provided that the above copyright notices and the following
 three paragraphs appear in all copies of this software.  Use of this
 software constitutes acceptance of these terms and conditions.

 IN NO EVENT SHALL MIT BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
 SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
 THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF MIT HAS BEEN ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
 
 MIT SPECIFICALLY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES INCLUDING,
 BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

 THIS SOFTWARE IS PROVIDED "AS IS," MIT HAS NO OBLIGATION TO PROVIDE
 MAINTENANCE, SUPPORT, UPDATE, ENHANCEMENTS, OR MODIFICATIONS.
"""

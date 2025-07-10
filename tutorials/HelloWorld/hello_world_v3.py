import pPython as GPC
from pPython.map import Dmap,rand
from pPython.dmat import local,global_ind,put_local,agg

# Just print 'Hello World!'
print('Hello World!')

# My pPython process ID (Pid or Rank)
Pid = GPC.Pid
print('My Pid = %d'%(Pid))

# How many pPython processes are running?
Np = GPC.Np
print('Total number of pPython processes (Np) = %d'%(Np))

# Create a distributed array
Nx = 3
Ny = 6
amap  = Dmap([1,Np], {}, range(Np))
Z = rand(Nx,Ny,map=amap)
myZ = local(Z)
print('My local portion of the distributed array, Z:')
print(myZ)

# Do some mathematical operation in parallel
# Get the local portion of the global indices
my_index = global_ind(Z, 1)
# Loop over the local indices
for index in range(len(my_index)):
    for j in range(Nx):
        myZ[j,index] = myZ[j,index] + 100.

# Store the local portion (myZ) of Z into the distributed matrix Z
Z = put_local(Z, myZ)

# Finally, aggregate all of the output onto the leader process
z_final = agg(Z);
print('Final z_final on Pid = %d:'%(Pid))
print(z_final)

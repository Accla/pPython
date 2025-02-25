import numpy as np
from timeit import default_timer as timer

# Import gridPython methods.
from Dmap import *
import pPython as GPC
from local import *
from print_falls import *
from rand import *
from zeros import *
from global_ind import *
from find import *


"""
    Implementation of the HPC Challenge Higher Performance Linpack
    benchmark which solve the equation Ax = b.
    To run in serial without distributed arrays, set         
      PARALLEL = 0
    At the Matlab prompt type
      pHPL
    To run in serial with distributed arrays, set         
      PARALLEL = 1
    At the Matlab prompt type
      pHPL
    To run in parallel with distributed arrays
    at the Matlab prompt type 
      eval(pRUN('pHPL',2,{}))
"""

#  MPI information
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# extract QA_PARALLEL environment variable
# Turn parallelism on or off.
QA_PARALLEL = os.getenv('QA_PARALLEL')
if QA_PARALLEL == '1':
    PARALLEL = 1
else:
    PARALLEL = 0

Amap = 1                                 # Serial map.
if PARALLEL:
    Amap = Dmap([Np,1],{},range(Np))    # Parallel map.

print('Np                                 = %d'%(Np))
print('Pid                                = %d'%(Pid))

print('-------')

# Create a distributed matrix on individual rank
z = rand(25,7,map=Amap)
print('Local portion of global matric: before')
print(local(z))

print('Local portion of global indices:')
print(global_ind(z))

# Test put_local()
if PARALLEL:
    temp_v = np.ones((z.local.shape))
else:
    temp_v = np.ones((z.shape))
#
[iis,jjs] = size(temp_v)
# Adjust local array
for il in range(0,iis,2):
    for jl in range(0,jjs,2):
        # print('il,jl = %d,%d'%(il,jl))
        temp_v[il][jl] = 0.
# update local array
z = put_local(z,temp_v)
# z = put_local(z,temp_v)

print('Local portion of global matric: after')
print(local(z))

[i,j] = find(z)
print('i')
print(i)
print('j')
print(j)

print(' ')
print(' ')
print(' ')
print('SUCCESS')
print(' ')
print(' ')
print(' ')
print(' ')


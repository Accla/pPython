import os

# import all
# from PythonMPI import *

# import only those called
import pPython as GPC
from Dmap import *
from ones import *
from zeros import *

# extract QA_PARALLEL environment variable
QA_PARALLEL = os.getenv('QA_PARALLEL')
if QA_PARALLEL == '1':
    PARALLEL = 1
else:
    PARALLEL = 0

#  MPI information
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# Print rank.
print('size: %d'%(Np))
print('Pid: %d'%(Pid))

# Create a map
Amap = 1
Bmap = 1
Cmap = 1
if PARALLEL:
    Amap = Dmap([1,Np],{},range(Np)) 
    Bmap = Dmap([1,Np],{},range(Np)) 
    Cmap = Dmap([Np,1],{},range(Np)) 

    if Amap == Bmap:
        print('This is correct. Amap is equal to Bmap')
    else:
        print('This is wrong. Both Amap and Bmap are the same.')

    if (Np>1):
        if (Amap == Cmap):
            print('This is wrong. Amap and Cmap should be different.')
        else:
            print('This is correct. Amap and Cmap are different.')
    else:
            print('This is correct. Amap and Cmap are the same.')
else:
    print('There is no difference among Amap, Bmap, and Cmap.')

# Create distributed arrays:
N = 10
A = zeros(N,N,map=Amap)
B = zeros(N,N,map=Bmap)
C = zeros(N,N,map=Cmap)

if PARALLEL:
    print('\nNow compare Dmap in the distributed array:\n')
    if A.map == B.map:
        print('This is correct. A is equal to B')
    else:
        print('This is incorrect. Both A and B are the same.')

    if (Np>1):
        if A.map == C.map:
            print('This is wrong. A and C should be different.')
        else:
            print('This is correct. A and C are different.')
    else:
            print('This is correct. Amap and Cmap are the same.')
else:
    print('There is no difference among Amap, Bmap, and Cmap.')

print(' ')
print(' ')
print(' ')
print('SUCCESS ')
print(' ')
print(' ')
print(' ')


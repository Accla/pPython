import os

# import all
# from PythonMPI import *

# import only those called
import pPython as GPC
from Dmap import *
from display import *

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

print('display(Amap)')
display(Amap)

print('display(Cmap)')
display(Cmap)

print(' ')
print(' ')
print(' ')
print('SUCCESS ')
print(' ')
print(' ')
print(' ')


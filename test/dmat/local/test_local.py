
from Dmap import *
from dcomplex import *
from rand import *

#  MPI information
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# PARAMETERS (OK to change)
# extract QA_PARALLEL environment variable
# Turn parallelism on or off.
QA_PARALLEL = os.getenv('QA_PARALLEL')
if QA_PARALLEL == '1':
    PARALLEL = 1
else:
    PARALLEL = 0

Ns = 90
Nb = 40
Nf = 100

Xmap = 1
if PARALLEL:
    Xmap = Dmap([1,1,Np],{},range(Np))

X = dcomplex(rand(Ns,Nb,Nf,map=Xmap),rand(Ns,Nb,Nf,map=Xmap))
Xlocal = local(X)

print('Xlocal.shape')
print(Xlocal.shape)
print(Xlocal)

print('')
print('SUCCESS')
print('')


######################################################
# Simple script that performs Y = X + 1.
# To run in serial without distributed arrays, set
#   PARALLEL = 0
# At the Matlab prompt type
#   pAddOne
# To run in serial with distributed arrays, set
#   PARALLEL = 1
# At the Matlab prompt type
#   pAddOne
# To run in parallel with distributed arrays
# at the Matlab prompt type
#   eval(pRUN('pAddOne',2,{}))
#   eval(pRUN('pAddOne',2,'grid'))
######################################################

# pPython class
import pPython as GPC
from Dmap import *

from zeros import *
from local import *
from put_local import *

# Create communicator.
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# Print rank.
print('size: %d'%(Np))
print('my_rank: %d'%(Pid))

# extract QA_PARALLEL environment variable
# Turn parallelism on or off.
QA_PARALLEL = os.getenv('QA_PARALLEL')
if QA_PARALLEL == '1':
    PARALLEL = 1  # Set control flag.
else:
    PARALLEL = 0


N = 100       # Set matrix size.
XYmap = 1     # Create serial map.

if PARALLEL:
    Np = GPC.Np
    XYmap = Dmap([Np, 1],{},range(Np))   # Create parallel map.

X = zeros(N,N,map=XYmap)     # Create distributed X.
Y = zeros(N,N,map=XYmap)     # Create distributed Y.
Xloc = local(X)          # Get local part of X.
Yloc = local(Y)          # Get local part of Y.
Yloc = Xloc + 1          # Add one to local part.
Y = put_local(Y,Yloc)    # Put back into Y.

print('')
print('')
print('SUCCESS')
print('')
print('')
print('')


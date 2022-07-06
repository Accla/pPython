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

N = 100       # Set matrix size.
PARALLEL = 1  # Set control flag.
XYmap = 1     # Create serial map.

if PARALLEL:
    Np = GPC.comm_size
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


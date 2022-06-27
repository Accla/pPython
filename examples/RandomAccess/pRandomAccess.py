import numpy as np
from timeit import default_timer as timer

# Import PythonMPI methods.
import pPython as GPC
from GridMap import *
from agg import *
from zeros import *
from global_ind import *
from global_block_range import *
from global_block_ranges import *
from uint64 import *

from RandomAccessStarts import *

"""
GUPS (Giga UPdates per Second) is a measurement that profiles the memory
architecture of a system and is a measure of performance similar to MFLOPS.
GUPS is calculated by identifying the number of memory locations that can be
randomly updated in one second, divided by 1 billion (1e9). The term
"randomly" means that there is little relationship between one address to be
updated and the next, except that they occur in the space of one half the
total system memory.  An update is a read-modify-write operation on a table
of 64-bit words.  An address is generated, the value at that address read from
memory, modified by an integer operation (add, and, or, xor) with a literal
value, and that new value is written back to memory.

Parameters:
* PARALLEL - Turn on distributed arrays.
* VALIDATE - Enable validation of results.
* Nup - Number of updates to the table.
* ErrorRate - Allowed error rate.
* lgN - Used to set size of table, where N = 2^lgN
* lgNb - Used to set block size of generating random references where Nb = 2^lgNb.

To run in serial without distributed arrays, set
    PARALLEL = 0
At the Python prompt type
    pRandomAccess
To run in serial with distributed arrays, set
    PARALLEL = 1
At the Python prompt type
    pRandomAccess
To run in parallel with distributed arrays
at the Python prompt type
    eval(pRUN('pRandomAccess',2,{}))
"""

"""
Uncomment if you want all numbers printed out in hex.
ToDo: Not sure how to handle this in Python yet)
"""
# format hex

PARALLEL = 1  # Turn distributed arrays on or off.
VALIDATE = 1  # Turn verification on or off.
ErrorRate = 0.01  # Set allowed error rate.

# Log size of main table (suggested: half of global memory).
#lgN = 27+log2(Np)   # Full memory.
#lgN = 20   # Performance.
lgN = 25   # Book
lgN = 18   # Debug.

# Since the main table size is large, updates are performed in blocks instead
# of one at a time.
# Set log block size.  The official HPC Challenge benchmark sets the block size
# to 1024, i.e. sets the lgNb to 10
lgNb = 10

# SETUP
N = 2**lgN  # Size of update table X.

# Number of updates to table.
# Must run either 4x number of table OR at least 1/4 time to run the Top500
# benchmark (~1000 seconds?)
#Nup = (4 * N)
#Nup = N/4
Nup = N/16
#Nup = N/2**(lgN-10-8)

Nb = 2**lgNb  # Size of update blocks.
Nblocks = int(Nup / Nb)  # Number of update blocks.

# Create mask that selects low bits we want to use for indexing large table X.
mask = uint64(N-1)

#  MPI information
comm = GPC.comm
Np = GPC.comm_size
Pid = GPC.my_rank

# Create maps.
Xmap = 1
if PARALLEL:
    Xmap = GridMap([1,Np],{},range(Np))  # Map for table.

tic = timer()
X = zeros(1,N,dmap=Xmap)  # Allocate main table.
Xloc = uint64(global_ind(X,1)) # Initialize local part indices.
Talloc = timer() - tic
print('Allocation Time (sec)              = %f'%(Talloc))

myX = global_block_range(X,1)  # Get local index range.
allX = global_block_ranges(X,1) # Get all index ranges.

print('Distributed table size             = 2^%d = %d words'%(lgN,N))
print('Distributed table size (bytes)     = %d'%(N*8))
print('Local table size (bytes)           = %d'%(Xloc.size*8))
print('Number of updates                  = %d'%(Nup))
print('Block size (should be 1024)        = %d'%(Nb))
print('Number of updates blocks           = %d'%(Nblocks))

# BEGIN BENCHMARK

# Distribute update block indices across processors.
myBLOCK = global_ind(zeros(1,Nblocks,dmap=Xmap),1)

# Create a block of starting locations in the random sequence.
ranStarts = RandomAccessStarts( (myBLOCK[0])*Nb + np.arange(Nb)*len(myBLOCK) )

# Synchronize start.
tic = timer()
sync = agg(zeros(1, Np, dmap=Xmap))
Tlaunch = timer() - tic
print('Launch Time (sec)                  = %f'%(Tlaunch))

# Cache VALIDATE flag.
tempVALIDATE = VALIDATE
VALIDATE = 0

# Run core of parallel RandomAccess benchmark, without validation
tic = timer()

# Execute pRandomAccessSpray script
# does it enherit all variables from the parent process?
exec(open("pRandomAccessTree.py").read())

Trun = timer() - tic
print('Run time (sec)                     = %f'%(Trun))

# Compute GUPS.
GUPS = Nup / Trun / 1.e9
print('Giga Updates Per Sec               = %f'%(GUPS))

#
# VALIDATION (in serial or "safe" mode; optional)

# Put VALIDATE flag back.
VALIDATE = tempVALIDATE

if VALIDATE:
    print('Validating results...')

    tic = timer()

    # Run core of parallel RandomAccess benchmark, with validation
    exec(open("pRandomAccessSpray.py").read())

    Xloc0 = uint64(global_ind(X,1));  # Compute errors.
    Nerrors = np.count_nonzero(np.not_equal(Xloc,Xloc0))

    Tvalidate = timer() - tic;
    print('Validate time (sec)                = %f'%(Tvalidate))

    # Aggregate data back on leader.
    Etable = zeros(1, Np, dmap=Xmap)
    Etable = put_local(Etable,Nerrors)
    EtableAll = agg(Etable)

    if (Pid == 0):
        # Total errors.
        erate = np.sum(EtableAll)/N
        print('Error rate                         = %f'%(erate))
        if (erate > ErrorRate):
            print('Validation Failed')
        else:
            print('Validation Passed')

print('')
print('')
print('')
print('SUCCESS')
print('')
print('')
print('')





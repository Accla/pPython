"""qa_uint64.py
    Test gridPython distributed array function, uint64()

    To run, start Pyhton and type:

        pRun('qa_uint64.py',4,'grid')

    Output will be piped into two files:

        PythonMPI/qa_uint64.0.out
        . . . 
        PythonMPI/qa_uint64.3.out

    PythonMPI
    Dr. Chansup Byun
    MIT Lincoln Laboratory
    cbyun@ll.mit.edu
"""
import os

# import all 
# from PythonMPI import *

# import only those called
import pPython as GPC
from Dmap import *
from uint64 import *
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
pmap = 1
if PARALLEL:
    pmap = Dmap([Np,1],'b',range(Np))

# Create a uint64 variable
print('Case 1: create a uint64 integer')
MOLY = uint64(7)
POLY = uint64(7)
print(POLY)
#error:why?  print('type(POLY): %s'%(type(POLY)))

HOLY = MOLY + POLY
print(HOLY)

print('Case 2: create a uint64 distributed array')
ran = zeros(1,8,dtype='uint64')
ran[:] = uint64(2)
print(ran)
print(ran[0,0])

print('Case 3: operate on an non-distributed array')
# create an input array of n
# myarg =  (myBLOCK(1)-1)*Nb + (0:(Nb-1))*length(myBLOCK);
myBLOCK = np.arange(16)
Nb = 2**10
n =  (myBLOCK[0])*Nb + np.arange(Nb)*len(myBLOCK)
BLOCKSIZE = len(n)
myu64 = uint64(n)


print('SUCCESS')
print(' ')
print(' ')
print(' ')


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

"""qa_sparse_dmat.py
    Test gridPython distributed array function, ones()

    To run, start Pyhton and type:

        pRun('qa_sparse_dmat.py',4,'grid')

    Output will be piped into two files:

        PythonMPI/qa_sparse_dmat.0.out
        . . . 
        PythonMPI/qa_sparse_dmat.3.out

    Dr. Chansup Byun
    MIT Lincoln Laboratory
    cbyun@ll.mit.edu
"""
import os
import numpy as np
from timeit import default_timer as timer

# Import gridPython methods.
# pPython class
import pPython as GPC
from Dmap import *
from local import *
from rand import *
from sparse import *

# extract QA_PARALLEL environment variable
QA_PARALLEL = os.getenv('QA_PARALLEL')
if QA_PARALLEL == '1':
    PARALLEL = 1
else:
    PARALLEL = 0

# Create communicator.
# pPython as GPC in gridPython.py
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# Print rank.
print('size: %d'%(Np))
print('Pid: %d'%(Pid))

# Create a random 2-D array
N = 16
N = 2*Np

Xmap = 1
if PARALLEL:
    Xmap = Dmap([1,Np],'b',range(Np))

# Case 1: gagg for a numpy array (reduction operation)
print('\n1. Random NxN DMAT array.')
myMat = rand(N,N,map=Xmap)
print('Before sparse:')

print('my local matrix:')
if PARALLEL:
    print(myMat.local)
   # str obj not callable error:  print(type(myMat.local))
else:
    print(myMat)
    # str obj not callable error: print('Type: %s'%(type(myMat[0])))

# Convert local matrix into sparse matrix format (csr)
newMat = sparse(myMat)

print('After sparse:')
if PARALLEL:
    if hasattr(newMat.local,'nnz'):
        print('newMat is in a sparse matrix format')
    print(newMat.local.toarray())
    print(newMat.local.nnz)
    # help(newMat.local)
    # print(type(newMat.local))
else:
    print(newMat)
    # print(type(newMat))


print(' ')
print(' ')
print('SUCCESS')
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

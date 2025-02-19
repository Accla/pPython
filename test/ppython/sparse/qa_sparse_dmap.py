"""qa_sparse_dmap.py
    Test gridPython distributed array function, ones()

    To run, start Pyhton and type:

        pRun('qa_sparse_dmap.py',4,'grid')

    Output will be piped into two files:

        PythonMPI/qa_sparse_dmap.0.out
        . . . 
        PythonMPI/qa_sparse_dmap.3.out

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
M = 16
# Note that, at least, 2 or more elements are needed on each local portion of the matrix
# Otherwise, the following error will happen
#
"""
Pid=2: Traceback (most recent call last):
Pid=2:   File "PythonMPI/PythonMPIdefs.py", line 12, in <module>
Pid=2:     pRUN_Parallel_wrapper('qa_sparse_dmap.py')
Pid=2:   File "/home/gridsan/CH21778/.local/lib/python3.8/site-packages/pPython/src/pRUN_Parallel_wrapper.py", line 80, in pRUN_Parallel_wrapper
Pid=2:     exec(open(py_file).read())
Pid=2:   File "<string>", line 70, in <module>
Pid=2:   File "/home/gridsan/CH21778/.local/lib/python3.8/site-packages/pPython/src/sparse.py", line 164, in sparse
Pid=2:     d.local = csr_matrix((s, (ii, jj)), shape=(local_size[0], local_size[1]), dtype=np.float64)
Pid=2:   File "/state/partition1/llgrid/pkg/anaconda/anaconda3-2022a/lib/python3.8/site-packages/scipy/sparse/compressed.py", line 54, in __init__
Pid=2:     other = self.__class__(coo_matrix(arg1, shape=shape,
Pid=2:   File "/state/partition1/llgrid/pkg/anaconda/anaconda3-2022a/lib/python3.8/site-packages/scipy/sparse/coo.py", line 196, in __init__
Pid=2:     self._check()
Pid=2:   File "/state/partition1/llgrid/pkg/anaconda/anaconda3-2022a/lib/python3.8/site-packages/scipy/sparse/coo.py", line 285, in _check
Pid=2:     raise ValueError('column index exceeds matrix dimensions')
Pid=2: ValueError: column index exceeds matrix dimensions
"""
#
N = 2*Np
# N = 8

print('M = %d, N = %d'%(M,N))

Xmap = 1
if PARALLEL:
    Xmap = Dmap([1,Np],'b',range(Np))

# Case 1: sparse(M,N,Xmap)
print('\n1. Sparse MxN DMAT matrix.')
oldMat = rand(M,N,map=Xmap)
myMat = sparse(oldMat)

if PARALLEL:
    if hasattr(myMat.local,'nnz'):
        print('myMat is in a sparse matrix format')
    print(myMat.local.toarray())
    print(myMat.local.nnz)

# Case 2: sparse([],[],[],M,N,NZMAX,Xmap)
print('\n2. Sparse MxN DMAT matrix with sparse([],[],[],M,N,NZMAX,Xmap).')
NZMAX=M*N
myMat = sparse([],[],[],M,N,NZMAX,map=Xmap)

if PARALLEL:
    if hasattr(myMat.local,'nnz'):
        print('myMat is in a sparse matrix format')
    print(myMat.local.toarray())
    print(myMat.local.nnz)

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

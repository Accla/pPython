"""qa_global_index_func.py
    Test gridPython distributed array function, global_index_func()

    To run, start Pyhton and type:

        pRun('qa_global_index_func.py',4,'grid')

    Output will be piped into two files:

        PythonMPI/qa_global_index_func.0.out
        . . . 
        PythonMPI/qa_global_index_func.3.out

    PythonMPI
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
from zeros import *
from global_ind import *
from global_block_ranges import *

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
M = 6
N = 16

Amap = 1
if PARALLEL:
    Amap = Dmap([1, Np],{},range(Np))

A = zeros(M,N,map=Amap)

print('Case 1: global_ind(A,1)[0]')
myBLOCK = global_ind(A,1)[0]
print('myBLOCK:')
print(myBLOCK)

for ib in myBLOCK:
    print('my global index position: %d'%(ib))

print('Case 2: global_block_ranges(A,1)[0]')
allX = global_block_ranges(A,1)[0] # Get all index ranges.
print('allX:')
print(allX)

print(' ')
print(' ')
print(' ')
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

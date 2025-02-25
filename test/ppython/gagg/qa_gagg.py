"""qa_ones.py
    Test gridPython distributed array function, ones()

    To run, start Pyhton and type:

        pRun('qa_ones.py',4,'grid')

    Output will be piped into two files:

        PythonMPI/qa_ones.0.out
        . . . 
        PythonMPI/qa_ones.3.out

    PythonMPI
    Dr. Chansup Byun
    MIT Lincoln Laboratory
    cbyun@ll.mit.edu
"""
import os
import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

from D4M.assoc import Assoc
# from pygraphblas import Matrix

# Import gridPython methods.
# pPython class
import pPython as GPC
from gagg import *

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
N = 3

# Case 1: gagg for a numpy array (reduction operation)
print('\n1. gagg for a numpy array (reduction operation)\n')
myMat = np.ones((N,N))
print('Before reduction:')
print(myMat)
newMat = gagg(myMat,0,'+')
print('After reduction:')
print(newMat)

# Case 2: gagg for an Associative variable (reduction operation)
print('\n2. gagg for an Associative variable (reduction operation)\n')
# Create an Associative variable
mypid = str(os.getpid())
myhost = os.uname()[1]
row = [myhost+',']
col = [mypid+',']
val = ['1']
myinfo = Assoc(row,col,val)
print('Before reduction:')
print(myinfo)
whole_info = gagg(myinfo,0,'+')
print('After reduction:')
print(whole_info)


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

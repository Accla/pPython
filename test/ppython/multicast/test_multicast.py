"""test_multicast.py
    Test pPython distributed array function, multicast()

    To run, start Pyhton and type:

        pRun('test_multicast.py',4,'grid')

    Output will be piped into two files:

        PythonMPI/test_multicast.0.out
        . . . 
        PythonMPI/test_multicast.3.out

    pPython
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
from multicast import *

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

# Case 1: multicast for a numpy array from the first process
print('\n1. multicast for a numpy array (source = 0, destination: the rest)\n')
if Pid == 0:
   myMat = np.ones((N,N))
else:
   myMat = np.zeros((N,N))
   
print('Before multicast() called.:')
print(myMat)

src = [0]
dst = list(range(1,Np))
newMat = multicast(src,dst,myMat)

print('After multicast() called.:')
print(newMat)


# Case 2: multicast for a numpy array from the last process
print('\n2. multicast for a numpy array (source = Np-1, destination: the rest)\n')
if Pid == Np-1:
   myMat = np.ones((N,N)) * 2.
else:
   myMat = np.zeros((N,N))
   
print('Before multicast() called.:')
print(myMat)

src = [Np-1]
dst = list(range(Np-1))
newMat = multicast(src,dst,myMat)

print('After multicast() called.:')
print(newMat)


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

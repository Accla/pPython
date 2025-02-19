"""test_agg.py
    Test pPython distributed array function, agg()

    To run, start Pyhton and type:

        pRun('test_agg.py',4,'grid')

    Output will be piped into two files:

        PythonMPI/test_agg.0.out
        . . . 
        PythonMPI/test_agg.3.out

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
from Dmap import *
from rand import *
from zeros import *
from display import *
from summation import *

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

Amap = 1
if PARALLEL:
    Nx = int(Np/2)
    Ny = 2
    Amap = Dmap([Nx,Ny],{},range(Np))

# Case 1: 
print('\nCase 1: aggregation of Dmap objects.\n')

X  = rand(N, 3,map=Amap)
print('Local X:')
print(local(X))
print(' ')
# Xglobal = agg(X)
# print(Xglobal)


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

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

# import all 
# from PythonMPI import *

# import only those called
import pPython as GPC
from Dmap import *
from ones import *
from pPython.dmat import global_ind

# extract QA_PARALLEL environment variable
QA_PARALLEL = os.getenv('QA_PARALLEL')
if QA_PARALLEL == '1':
    PARALLEL = 1
else:
    PARALLEL = 0

#  MPI information
comm = GPC.comm
print(comm)
Np = GPC.Np
Pid = GPC.Pid

# Print rank.
print('size: %d'%(Np))
print('Pid: %d'%(Pid))

# Create a map
pmap = 1
if PARALLEL:
    dist = {0:{'dist':'c'},1:{'dist':'b'}}
    pmap = Dmap([Np,1],dist,range(Np))
    # pmap = Dmap([Np,1],'c',range(Np))
    # pmap = Dmap([Np,1],'b',range(Np))

# Create a distributed matrix on individual rank
m = 25
n = 10
z = ones(m,n,map=pmap)

# Check the distributed z matrix
if PARALLEL:
    print('Local portion of global indices on Pid = %d:'%(Pid))
    print(z.global_ind)
print('Local portion of global matric on Pid = %d:'%(Pid))
print(local(z))

# Binary operation
y = z + 1

print('local portion of z after elementwise "add one" operation')
print(local(z))
print('local portion of the neww y after elementwise "add one" operation')
print(local(y))
print(global_ind(z,0))

# Finalize Matlab MPI.
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

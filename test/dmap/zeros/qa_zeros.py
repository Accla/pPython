"""qa_zeros.py
    Test gridPython distributed array function, zeros()

    To run, start Pyhton and type:

        pRun('qa_zeros.py',4,'grid')

    Output will be piped into two files:

        PythonMPI/qa_zeros.0.out
        . . . 
        PythonMPI/qa_zeros.3.out

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

# Create a distributed matrix on individual rank
m = 25
n = 10
z = zeros(m,n,map=pmap)

# Check the distributed z matrix
if PARALLEL:
    print('Local portion of global indices on Pid = %d:'%(Pid))
    print(z.global_ind)
print('Local portion of global matric on Pid = %d:'%(Pid))
print(local(z))
print('type(z): %s'%((z)))

y = z - 2
print('local portion of original distributed array, z, after deducting 2 elementwise.')
print(local(z))
print('local portion of new distributed array, y, after deducting 2 elementwise.')
print(local(y))

# non-disributed array
print('Case: non-distributed array with data type string')
m2 = zeros(2,8,dtype='uint64')

print('type(m2): %s'%((m2)))
print(m2)
print(m2[0][0])

# non-disributed array without datatype
print('Case: non-distributed array WITHOUT data type string') 
m3 = zeros(2,7)

print('type(m3): %s'%((m3)))
print(m3)
print(m3[0][0])

# non-disributed array without datatype
print('Case: a 1-D non-distributed array WITHOUT data type string')
m4 = zeros(7)
print('type(m4): %s'%((m4)))
print(m4)

# non-disributed array without datatype
print('Case: a 4-D non-distributed array WITHOUT data type string')
m5 = zeros(4,3,1,3)
print('type(m5): %s'%((m5)))
print('m5.shape')
print(m5.shape)
print('m5')
print(m5)

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

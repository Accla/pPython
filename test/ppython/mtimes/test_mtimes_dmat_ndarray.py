"""test_mtimes.py
    Test pPython distributed array function, mtimes()

    To run, start Pyhton and type:

        pRun('test_mtimes.py',4,'grid')

    Output will be piped into two files:

        PythonMPI/test_mtimes.0.out
        . . . 
        PythonMPI/test_mtimes.3.out

    pPython
    Dr. Chansup Byun
    MIT Lincoln Laboratory
    cbyun@ll.mit.edu
"""
import os
import numpy as np
from timeit import default_timer as timer
import pickle


# Import gridPython methods.
# pPython class
import pPython as GPC
from Dmap import *
from mtimes import *
from rand import *
from agg import *
from BcastMsg import *
# from dict_with_pickle import save_dict_to_pickle

DEBUG = 1

# extract QA_PARALLEL environment variable
QA_PARALLEL = os.getenv('QA_PARALLEL')
if QA_PARALLEL == '1':
    PARALLEL = 1
else:
    PARALLEL = 0

print('PARALLEL = %d'%(PARALLEL))
TMPDIR = os.getenv('TMPDIR')
print('TMPDIR = %s'%(TMPDIR))

# Create communicator.
# pPython as GPC in gridPython.py
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# Print rank.
print('size: %d'%(Np))
print('Pid: %d'%(Pid))

# Create a random 2-D Dmat array
Nx = 8
Ny = 8
# Nx = 3
# Ny = 3
Nx = 16
Ny = 16
Nm = 8

map_a = Dmap([Np,1],'b',range(Np))
map_b = 1

# Case 3: Dmat * ndarray 
print('Case 3: Dmat * ndarray ')

# Create B (ndarray) and broadcast to all processes
# B = rand(Nx,Ny,map=map_b)
if Pid == 0:
    B = np.random.rand(Nx,Ny)
    [B]= BcastMsg(0,1234,B)
else:
    B = np.zeros((Nx,Ny),dtype=float)
    [B]= BcastMsg(0,1234,B)

# print('B is type of %s' %(type(B)))
# print(B)


A = rand(Nx,Ny,map=map_a)

print(type(A))
print(type(B))
#
# For verification
#
global_A = agg(A)
global_B = agg(B)
global_C = np.matmul(global_A,global_B)

#
# Distributed matrix multiplication
C = mtimes(A,B)
dist_g_C = agg(C)

print(' ')
print(' ')
if Pid == 0:
    # save for debugging
    # matlab: save('global_matrices_dubug.mat','global_A','global_B','global_C','dist_g_C')

    # Check difference
    diff = global_C - dist_g_C
    diff_l2norm = np.linalg.norm(diff)
    print('L2 norm of difference: %f'%(diff_l2norm))
    if diff_l2norm < 1.e-6:
        print('SUCCESS')
    else:
        print('FAILED')
    if DEBUG:
        ga_pkl_file='global_arrays_debug.pkl'
        global_arrays = dict()
        global_arrays[0]=global_A
        global_arrays[1]=global_B
        global_arrays[2]=global_C
        global_arrays[3]=dist_g_C
        # save_dict_to_pickle(global_arrays, ga_pkl_file)
        with open(ga_pkl_file, 'wb') as handle:
            pickle.dump(global_arrays, handle, protocol=pickle.HIGHEST_PROTOCOL)

        print('--- DEBUG ---')
        print('A = ')
        print(global_A)
        print('B = ')
        print(global_B)
        print('C = np.matmul(A,B)')
        print(global_C)
        print('C = mtimes(A,B)')
        print(dist_g_C)
else:
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

import numpy as np

import pPython as GPC
from Dmat import *
from Dmap import *
from remap import *
from zeros import *
from size import *
from find import *
from multicast import *
from summation import *
from inmap import *

def mtimes(a,b):
    """Matrix multiply.
    C = MTIMES(A, B) or C = A (dot) B multiples two matrices together.
    Mtimes is an inner product matrix multiply and assumes that A is row mapped and B is column mapped.
    If B is row mapped, it is remapped in order to perform the matrix multiplication.
 
    For A row mapped, the function accepts B matrices that are double (not mapped),
    column mapped or row mapped.
    
    For a matrix A that is not mapped (doubles), B must be column mapped.
 
    WARNING: Overlaps have not been tested.  In fact, distributed matrix multiply was implemented 
    without a thought to overlap. This is a major TODO.
 
    Author:  Nadya Travinin
    Edited:  Edmund L. Wong (elwong@ll.mit.edu)
    Python version: Dr. Chansup Byun(cbyun@ll.mit.edu)
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering mtimes')

    # If one of the arguments is a scalar, do element-wise multiplication
    if (np.prod(size(a)) == 1) or (np.prod(size(b)) == 1):
        c = a * b
        return c
        if DEBUG:
            print('<-- Exiting mtimes with a scalar')
    
    # Check that both arguments are 2D
    if (len(a.shape) != 2) or (len(b.shape) != 2):
        raise Exception('ERROR (DMAT/MTIMES): Input arguments must be 2-D')
        # exit()

    res_distspec = dict()
    new_distspec = dict()
    if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
        # np.ndarray * np.ndarray
        c = np.matmul(a,b)
        if DEBUG:
            print('<-- Exiting mtimes, both are not a dmat matrix')
        return c

    elif isinstance(a, np.ndarray) and isinstance(b, Dmat):
        if DEBUG:
            print('--> Entering mtimes, a: ndarray, b: dmat matrix')
        # np.ndarray * dmat
        mapB = b.map
    
        # create sub-result matrices, each with a map equivalent to
        # one of map B's rows
        res_gridspec = [1, mapB.grid.shape[1]]
        res_distspec[0] = dict()
        res_distspec[0]['dist'] = 'b'
        res_distspec[1] = mapB.dist_spec[1]
                  
        my_idx = 0  
        res = dict() # store intermediate Dmat results     
        for i in range(mapB.grid.shape[0]):
            res_map = Dmap(res_gridspec, res_distspec, mapB.grid[i, :])
            res[i] = zeros(a.shape[0], size(b, 1)[0], map=res_map)
    
            # store which result matrix this processor will use
            if inmap(res_map, GPC.Pid):
                my_idx = i
    
        # map A's i-th column to the leftmost node in B's i-th row
        new_gridspec = [1, size(mapB.grid, 0)[0]]
        new_distspec[0] = dict()
        new_distspec[0]['dist'] = 'b'
        new_distspec[1] = mapB.dist_spec[0]
        new_proclist = np.transpose(mapB.grid[:, 0])

        if mapB.overlap:
            print('WARNING (@dmat/mtimes): TODO dmats with overlap may not work')
            new_mapA = Dmap(new_gridspec, new_distspec, new_proclist, mapB.overlap)
        else:
            new_mapA = Dmap(new_gridspec, new_distspec, new_proclist)
        if DEBUG:
            print('When A is a ndarray, new_mapA is ',end='')
            new_mapA.print()

        if DEBUG:
            print('mtimes: calling remap . . . ')
        a = remap(a, new_mapA)
        if DEBUG:
            print('mtimes: after remap, type of a is %s . . . '%(type(a)))
                  
        # find row/column in grid
        [myRow, myCol] = find(mapB.grid == GPC.Pid)
        if DEBUG:
            print('mtimes: after find, [myRow,myCol] = ')
            print(myRow)
            print(myCol)
            print('mapB.grid[myRow, 0] = %d'%(mapB.grid[myRow, 0]))
            print('mapB.grid[myRow, 1:] = ',end='')
            print(mapB.grid[myRow, 1:])
                  
        # send/receive data and do the multiplication
        res[my_idx].local = np.matmul(multicast(mapB.grid[myRow, 0], mapB.grid[myRow, 1:], a.local), b.local)

        # add back together sub-results to form resulting matrix (c)
        c = summation(zeros(size(a, 0)[0], size(b, 1)[0], map=mapB), res)
        if DEBUG:
            print('<-- Exiting mtimes, np.ndarry * dmat')
                  
    else:
                  
        # dmat * dmat OR dmat * double (is this a np.ndarray?)
        mapA = a.map
    
        # create sub-result matrices, each with a map equivalent to
        # one of map A's columns
        res_gridspec = [size(mapA.grid, 0)[0], 1]
        res_distspec[0] = mapA.dist_spec[0]
        res_distspec[1] = dict()
        res_distspec[1]['dist'] = 'b'

        if DEBUG:
            print('size(mapA.grid) = ',end='')
            print(size(mapA.grid))

        my_idx = 0
        res = dict() # store intermediate Dmat results     
        for i in range(size(mapA.grid, 1)[0]):
            res_map = Dmap(res_gridspec, res_distspec, mapA.grid[:,i])
            if DEBUG:
                print('res_map: ')
                res_map.print()

            res[i] = zeros(size(a, 0)[0], size(b, 1)[0], map=res_map)
            # store which result matrix this processor will use
            if inmap(res_map, GPC.Pid):
                my_idx = i
                if DEBUG:
                    print('Pid = %d found in res_map  my_idx = %d'%(GPC.Pid,i))
        # map B's ith row to the top node in A's ith column
        new_gridspec = [size(mapA.grid, 1)[0], 1]
        new_distspec[0] = mapA.dist_spec[1]
        new_distspec[1] = dict()
        new_distspec[1]['dist'] = 'b'
        #CB new_proclist = np.transpose(mapA.grid[0, :])
        new_proclist = mapA.grid[0, :]
        if mapA.overlap:
            print('Warning[@dmat/mtimes]: TODO dmats with overlap may not work')
            new_mapB = Dmap(new_gridspec, new_distspec, new_proclist, mapA.overlap)
        else:
            new_mapB = Dmap(new_gridspec, new_distspec, new_proclist)
        
        if DEBUG:
            print('new_mapB properties:')
            new_mapB.print()
            print('   Before b.loal = ')
            print(b.local)
            print('   n_dim_find error happened when calling remap: ')

        b = remap(b, new_mapB)
        if DEBUG:
            print('   After remap, a.loal = ')
            print(a.local)
            print('   After remap, b.loal = ')
            print(b.local)
    
        # find row/column in grid
        if DEBUG:
            print('mapA properties:')
            mapA.print()

        [myRow, myCol] = find(mapA.grid == GPC.Pid)
        if DEBUG:
            print('myRow & myCol that matches with GPC.Pid = %d'%(GPC.Pid))
            print('myRow:')
            print(myRow)
            print('myCol:')
            print(myCol)
            print('')
            print('A = ')
            print(a.local)
    
        # send/receive data and do the multiplication
        if DEBUG:
            print('   multicast source: ',end='')
            print(mapA.grid[0, myCol])
            print('   multicast destinations: ',end='')
            print(mapA.grid[1:, myCol])

        res[my_idx].local = np.matmul(a.local, multicast(mapA.grid[0, myCol], mapA.grid[1:, myCol], b.local))
        if DEBUG:
            print('After summation: res[my_idx].local')
            print(res[my_idx].local)
    
        # add back together sub-results to form resulting matrix (c)
        c = summation(zeros(size(a, 0)[0], size(b, 1)[0], map=mapA), res)
        if DEBUG:
            print('<-- Exiting mtimes, dmat * dmat OR dmat * np.ndarray')

    if DEBUG:
        print('After summation: c.local')
        print(c.local)
        print('<-- Exiting mtimes')

    return c
    
########################################################
# pMatlab: Parallel Matlab Toolbox
# Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
# Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
# MIT Lincoln Laboratory
########################################################
# Copyright (c) 2005, Massachusetts Institute of Technology All rights
# reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in
#        the documentation and/or other materials provided with the
#        distribution.
#      * Neither the name of the Massachusetts Institute of Technology nor
#        the names of its contributors may be used to endorse or promote
#        products derived from this software without specific prior written
#        permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


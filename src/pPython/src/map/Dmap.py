import sys
import numpy as np

import pyMPI_COMM_WORLD as pyMCW

class Dmap:
    """Define Map class. 

    MAP(GRID_SPEC, DIST_SPEC, PROC_LIST, overlap)
    GRID_SPEC - array of integers specifying how each dimension of a
            distributed object is broken up.
            For example is GRID_SPEC = [2 3], the first dimension is broken
            up between 2 processors and the second dimension is broken up
            between 3 processors. 
    DIST_SPEC - array of structures with two possible fields specifying 
            the distributed array distribution. Each entry in the array has to 
            have the DIST field defined. The DIST field can have the
            following values: 
                b = block
                c = cyclic
                bc = block-cyclic
            Additionally, if DIST == 'bc', the block size 'B_SIZE' must
            also be defined.
    PROC_LIST - array of processor ranks specifying on which ranks the
            object should be distributed. 
    
    Dmap object p contains:
    p.dim: number of dimensions of the the distributed object
    p.proc_list: the list of processors on which the object should bedistributed
    p.dist_spec: the distribution description for each dimension
    p.grid_spec: the distribution of processor grid (added with pPython)
    p.grid: p.dim-dimensional array of processors corresponding to how the
            object should be distributed
 
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    name = 'grid_map_class'
    
    def __init__(self,grid_spec=None,dist_spec=None,proc_list=None,overlap=None,**kwargs):
        """Init constructor."""
        
        DEBUG = 0
        if DEBUG:
            print('--> Entering Dmap.__init__()')
            print('grid_spec')
            print(grid_spec)
            print('proc_list')
            print(proc_list)

        if not bool(grid_spec):
            return
        #
        # Check ordering of processor grid
        order = 'C' # default order
        for key, value in kwargs.items():
            if key == 'order':
                order = value

        # set the comm as MPI_COMM_WORLD
        comm = pyMCW.MPI_COMM_WORLD

        dim = len(grid_spec); # dimension of the distributed object
        self.dim = dim
        self.grid_spec = grid_spec
        self.proc_list = proc_list
 
        if isinstance(overlap,type(None)):
            # MAP(GRID_SPEC, DIST_SPEC, PROC_LIST)
            # ensure that distribution is specified
            if not bool(dist_spec):
                # dist_spec is empty such as {} 
                # default distribution is block
                dist_spec = dict()
                for d in range(len(grid_spec)):
                    dist_spec[d] = dict()
                    dist_spec[d]['dist'] ='b'
            elif isinstance(dist_spec,str):
                if dist_spec == 'bc':
                    raise Exception('ERROR (Dmap): block-cyclic distribution also needs block size.')
                # 'b' for block & 'c' for cyclic distribution
                tmp_dist_spec = dist_spec
                dist_spec = dict()
                for d in range(len(grid_spec)):
                    dist_spec[d] = dict()
                    dist_spec[d]['dist'] = tmp_dist_spec
            elif any(map(lambda x: isinstance(x,dict),dist_spec.values())):
                # distribution spec is provided for all directions individually
                # dist_spec = {'0': {'dist': 'bc', 'b_size': 3}, '1': {'dist': 'b'}}
                if len(grid_spec) != len(dist_spec):
                    raise Exception('ERROR (Dmap): dimension does not match between grid_spec and dist_spec.')
            else:
                # dist_spec is provided as a dictionary form
                # dist_spec['dist'] = 'b' or 'c' or 'bc'
                # dist_spec['b_size'] = N where N is the block size
                #                       for block-cyclic distributions
                tmp_dist_spec = dist_spec
                dist_spec = dict()
                for d in range(len(grid_spec)):
                    dist_spec[d] = tmp_dist_spec
            # check for distribution spec
            for i in range(dim):
                # check that distributions defined are consistent with {'b', 'c', 'bc'}
                if (dist_spec[i]['dist'] != 'b') \
                and (dist_spec[i]['dist'] != 'c') \
                and (dist_spec[i]['dist'] != 'bc'):
                    raise Exception('ERROR (Dmap): %s is not a valid distribution'%(dist_spec[i]['dist']))
                else:
                    # check that block size is defined for block-cyclic distributions
                    if dist_spec[i]['dist'] == 'bc':
                        if (not 'b_size' in dist_spec[i]) or (dist_spec[i]['b_size'] < 1):
                            raise Exception('ERROR (Dmap): Block size must be specified for block-cyclic distibution')
            self.dist_spec = dist_spec
            
            # create the grid from the processor list
            p_list = np.array(proc_list)
            grid = np.zeros(np.prod(grid_spec),int)
            grid[:] = p_list[:]
            grid = grid.reshape(grid_spec,order=order)

            # check that the length of the processor list matches the size of
            # the grid
            gsize = grid.size
            if (len(proc_list) != gsize):
                raise Exception('ERROR (Dmap): Processor list does not match the size of the grid')
            else:
                grid.reshape(gsize)[:] = proc_list[:]
        
            if DEBUG:
                print('After grid.reshape(gsize)[:] = proc_list[:]')
                print(grid)
                print(proc_list)

            # if the maps are created within the scope of MPI_COMM_WORLD
            # then the processor list is checked against current
            # comm scope
            # find the number of processes allocated for the job
            if comm:
                if 'size' in comm:
                    n_procs = comm['size']
                    # check that the length of the processor list matches the number of
                    # processors requested
                    if (len(proc_list) > n_procs):
                        print('Dmap constructor: Processor list contains more processors '+\
                        'than number of processors requested.')
                else:
                    n_procs = None
            self.grid = grid
            self.overlap = None # no overlap specification

        else:
            # MAP(GRID_SPEC, DIST_SPEC, PROC_LIST, overlap)
            # ensure that distribution is specified
            if not bool(dist_spec):
                # dist_spec is empty such as {} 
                # default distribution is block
                dist_spec = dict()
                for d in range(len(grid_spec)):
                    dist_spec[d] = dict()
                    dist_spec[d]['dist'] ='b'
            elif isinstance(dist_spec,str):
                # if only one distribution is provided, then all dimensions are
                # distributed that way
                if dist_spec == 'b':
                    # 'b' for block distribution
                    tmp_dist_spec = dist_spec
                    dist_spec = dict()
                    for d in range(len(grid_spec)):
                        dist_spec[d] = dict()
                        dist_spec[d]['dist'] = tmp_dist_spec
                else:
                    raise Exception('ERROR (Dmap): Overlap is only supported for block distributions.')
            elif any(map(lambda x: isinstance(x,dict),dist_spec.values())):
                # distribution spec is provided for all directions individually
                # dist_spec = {0: {'dist': 'bc', 'b_size': 3}, 1: {'dist': 'b'}}
                if len(grid_spec) != len(dist_spec):
                    raise Exception('ERROR (Dmap): dimension does not match between grid_spec and dist_spec.')
                #
                # Can we use overlap only certain direction with this?
                #
            else:
                # dist_spec is provided as a dictionary form
                # dist_spec['dist'] = 'b'
                if dist_spec['dist'] != 'b':
                        raise Exception('ERROR (Dmap): Overlap is only supported for block distributions.')
                tmp_dist_spec = dist_spec
                dist_spec = dict()
                for d in range(len(grid_spec)):
                    dist_spec[d] = tmp_dist_spec
            # check for distribution  for all directions (dimensions)
            for i in range(dim):
                # check that distributions defined are consistent with {'b', 'c', 'bc'}
                if dist_spec[i]['dist'] != 'b':
                    raise Exception('ERROR (Dmap): Overlap is only supported for block distributions.')
            self.dist_spec = dist_spec
            
            # create the grid from the processor list
            grid = np.zeros(grid_spec,'int')

            # check that the length of the processor list matches the size of
            # the grid
            gsize = grid.size
            if (len(proc_list) != gsize):
                raise Exception('ERROR (Dmap): Processor list does not match the size of the grid')
            else:
                grid.reshape(gsize)[:] = proc_list[:]
            self.grid = grid
        
            if len(overlap) != self.dim:
                raise Exception('RROR (Dmap): Overlap must be specified for all of the dimensions of the map.')

            # if the maps are created within the scope of MPI_COMM_WORLD
            # then the processor list is checked against current
            # comm scope
            # find the number of processes allocated for the job
            if comm:
                if 'size' in comm:
                    n_procs = comm['size']
                    # check that the length of the processor list matches the number of
                    # processors requested
                    if (len(proc_list) > n_procs):
                        print('Dmap constructor: Processor list contains more processors '+\
                        'than number of processors requested.')
                else:
                    n_procs = None
            self.overlap = overlap

        if DEBUG:
            print('<-- Exiting Dmap.__init__()')

    def __eq__(self, other):
        # Check if both Dmap objects match with all their propreties
        if isinstance(other, Dmap):
            if (self.dim == other.dim) and (self.overlap == other.overlap) and (self.grid_spec == other.grid_spec) :
                if (self.grid == other.grid).all():
                    if (self.dist_spec == other.dist_spec):
                        if isinstance(self.proc_list,(list)):
                            if (self.proc_list == other.proc_list):
                                return False
                            else:
                                return False
                        else:
                            if (self.proc_list == other.proc_list).all() :
                                return True
                            else:
                                return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        return False
        
    def copy(self,old_map):
        """Copy the given map."""
        self.grid = old_map.grid
        self.grid_spec = old_map.grid_spec
        self.dist_spec = old_map.dist_spec
        self.proc_list = old_map.proc_list
        self.overlap = old_map.overlap
        return self

    def print(self):
        """Print the map."""
        print('Map Properties:')
        print('   Process grid (grid): %s'%(str(self.grid)))
        print('   Map distribution specificaiton (grid_spec): %s'%(str(self.grid_spec)))
        print('   Distribution type (dist_spec): %s'%(str(self.dist_spec)))
        print('   Process Pid list (proc_list): %s'%(str(self.proc_list)))
        print('   Overlap mapping (overlap): %s'%(str(self.overlap)))
        return

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

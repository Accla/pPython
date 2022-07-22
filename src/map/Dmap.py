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
 
    Author:   Nadya Travinin (pMatlab)
              Chansup Byun (pPython)
    """
    name = 'grid_map_class'
    
    def __init__(self,grid_spec=None,dist_spec=None,proc_list=None,overlap=None,**kwargs):
        """Init constructor."""
        
        DEBUG = 0
        if DEBUG:
            print('--> Entering Dmap.__init__()')
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
 
        if not overlap:
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
                    print('ERROR (Dmap): block-cyclic distribution also needs block size.')
                    exit()
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
                    print('ERROR (Dmap): dimension does not match between grid_spec and dist_spec.')
                    exit()
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
                    print('ERROR (Dmap): %s is not a valid distribution'%(dist_spec[i]['dist']))
                    exit()
                else:
                    # check that block size is defined for block-cyclic distributions
                    if dist_spec[i]['dist'] == 'bc':
                        if (not 'b_size' in dist_spec[i]) or (dist_spec[i]['b_size'] < 1):
                            print('ERROR (Dmap): Block size must be specified for block-cyclic distibution')
                            exit()
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
                print('ERROR (Dmap): Processor list does not match the size of the grid')
                exit()
            else:
                grid.reshape(gsize)[:] = proc_list[:]
        
            if DEBUG:
                print('After grid.reshape(gsize)[:] = proc_list[:]')
                print(grid)

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
                    print('ERROR (Dmap): Overlap is only supported for block distributions.')
                    exit()
            elif any(map(lambda x: isinstance(x,dict),dist_spec.values())):
                # distribution spec is provided for all directions individually
                # dist_spec = {0: {'dist': 'bc', 'b_size': 3}, 1: {'dist': 'b'}}
                if len(grid_spec) != len(dist_spec):
                    print('ERROR (Dmap): dimension does not match between grid_spec and dist_spec.')
                    exit()
                #
                # Can we use overlap only certain direction with this?
                #
            else:
                # dist_spec is provided as a dictionary form
                # dist_spec['dist'] = 'b'
                if dist_spec['dist'] != 'b':
                        print('ERROR (Dmap): Overlap is only supported for block distributions.')
                        exit()
                tmp_dist_spec = dist_spec
                dist_spec = dict()
                for d in range(len(grid_spec)):
                    dist_spec[d] = tmp_dist_spec
            # check for distribution  for all directions (dimensions)
            for i in range(dim):
                # check that distributions defined are consistent with {'b', 'c', 'bc'}
                if dist_spec[i]['dist'] != 'b':
                    print('ERROR (Dmap): Overlap is only supported for block distributions.')
                    exit()
            self.dist_spec = dist_spec
            
            # create the grid from the processor list
            grid = np.zeros(grid_spec,'int')

            # check that the length of the processor list matches the size of
            # the grid
            gsize = grid.size
            if (len(proc_list) != gsize):
                print('ERROR (Dmap): Processor list does not match the size of the grid')
                exit()
            else:
                grid.reshape(gsize)[:] = proc_list[:]
            self.grid = grid
        
            if len(overlap) != self.dim:
                print('RROR (Dmap): Overlap must be specified for all of the dimensions of the map.')
                exit()

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

        if isinstance(other, Dmap):
            if ((self.grid == other.grid).all()) and \
                (self.dim == other.dim) and \
                (self.dist_spec == other.dist_spec) and \
                (self.grid_spec == other.grid_spec) and \
                (self.proc_list == other.proc_list) and \
                (self.overlap == other.overlap):
                return True
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
        print('   Process grid: %s'%(str(self.grid)))
        print('   Map distribution specificaiton: %s'%(str(self.grid_spec)))
        print('   Distribution type: %s'%(str(self.dist_spec)))
        print('   Process Pid list: %s'%(str(self.proc_list)))
        print('   Overlap mapping: %s'%(str(self.overlap)))


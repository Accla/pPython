"""
Matlab structure (pMatlab map class) is best represented as dictionary in Python.
Thus Dmap class is redesigned as a dictionary class.
"""
from sys import getsizeof
import numpy as np

import pyMPI_COMM_WORLD as pyMCW

class Dmap(dict):
    """ Define Map class. 

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
            object should be distributed. (np.array type internally)
    
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
    dtype = 'Dmap'
    
    def __init__(self,grid_spec=None,dist_spec=None,proc_list=None,overlap=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Init constructor."""

        DEBUG = 0
        if DEBUG:
            print('--> Entering Dmap.__init__()')
            print('grid_spec')
            print(grid_spec)
            print('proc_list')
            print(type(proc_list))
            print(proc_list)

        self.nbytes = 0
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

        self['dim'] = len(grid_spec); # dimension of the distributed object
        self['grid_spec'] = grid_spec
        self['proc_list'] = np.array(proc_list)
        # workaround to be used with whosPy to be compatible with other data types
        self.shape = grid_spec
        
        if not isinstance(overlap,type(None)) and (len(overlap) != self['dim']):
            raise Exception('RROR (Dmap): Overlap must be specified for all of the dimensions of the map.')

        # MAP(GRID_SPEC, DIST_SPEC, PROC_LIST)
        # ensure that distribution is specified
        self['dist_spec'] = self._set_dist_spcc(dist_spec,overlap)
        self['overlap'] = overlap 

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

        # create the grid from the processor list
        p_list = np.array(proc_list)
        grid = np.zeros(np.prod(grid_spec),int)
        # check that the length of the processor list matches the size of
        # the grid
        gsize = grid.size
        if DEBUG:
            print('Before grid.reshape(gsize)[:] = proc_list[:]')
            print(grid)
            print(gsize)
            print(proc_list)
        if (len(proc_list) != gsize):
            raise Exception(('ERROR (Dmap): Processor list (size: %d) does not match the size (%d) of the grid'%(len(proc_list),gsize)))
        grid[:] = p_list[:]
        grid = grid.reshape(grid_spec,order=order)
        if DEBUG:
            print('After grid.reshape(gsize)[:] = proc_list[:]')
            print(grid)
            print(proc_list)
        self['grid'] = grid

        # Calculate the actual memory usage
        self.nbytes = getsizeof(self['dim'])+getsizeof(self['grid_spec'])+getsizeof(self.shape)+\
                getsizeof(self['proc_list'])+getsizeof(self['dist_spec'])+getsizeof(self['grid'])+\
                getsizeof(self['overlap'])+\
                64
        if DEBUG:
            print('<-- Exiting Dmap.__init__()')
        return

    def _set_dist_spcc(self, dist_spec, overlap):
        """ 
        Set the distribution specification
        """
        if not bool(dist_spec):
            # dist_spec is empty such as {} 
            # default distribution is block
            dist_spec = dict()
            for d in range(self['dim']):
                dist_spec[d] = dict()
                dist_spec[d]['dist'] ='b'
        elif isinstance(dist_spec,str):
            if isinstance(overlap,type(None)):
                if dist_spec == 'bc':
                    raise Exception('ERROR (Dmap): block-cyclic distribution also needs block size.')
            else:
                # if only one distribution is provided, then all dimensions are
                # distributed that way
                if dist_spec != 'b':
                    raise Exception('ERROR (Dmap): Overlap is only supported for block distributions.')                
            # 'b' for block & 'c' for cyclic distribution
            tmp_dist_spec = dist_spec
            dist_spec = dict()
            for d in range(self['dim']):
                dist_spec[d] = dict()
                dist_spec[d]['dist'] = tmp_dist_spec
        elif any(map(lambda x: isinstance(x,dict),dist_spec.values())):
            # distribution spec is provided for all directions individually as a dictionary variable
            # dist_spec = {'0': {'dist': 'bc', 'b_size': 3}, '1': {'dist': 'b'}}
            if self['dim'] != len(dist_spec):
                raise Exception('ERROR (Dmap): dimension does not match between grid_spec and dist_spec.')
        else:
            # dist_spec is provided as a dictionary form
            # dist_spec['dist'] = 'b' or 'c' or 'bc'
            # dist_spec['b_size'] = N where N is the block size
            #                       for block-cyclic distributions
            if not isinstance(overlap,type(None)):
                # in case of overlapped mapping
                if dist_spec['dist'] != 'b':
                    raise Exception('ERROR (Dmap): Overlap is only supported for block distributions.')
            tmp_dist_spec = dist_spec
            dist_spec = dict()
            for d in range(self['dim']):
                dist_spec[d] = tmp_dist_spec
                
        # check for distribution  for all directions (dimensions)
        # check that distributions defined are consistent with {'b', 'c', 'bc'}
        if isinstance(overlap,type(None)):
            for i in range(self['dim']):
                # Non-overlapped mapping
                if (dist_spec[i]['dist'] != 'b') \
                and (dist_spec[i]['dist'] != 'c') \
                and (dist_spec[i]['dist'] != 'bc'):
                    raise Exception('ERROR (Dmap): %s is not a valid distribution'%(dist_spec[i]['dist']))
                else:
                    # check that block size is defined for block-cyclic distributions
                    if dist_spec[i]['dist'] == 'bc':
                        if (not 'b_size' in dist_spec[i]) or (dist_spec[i]['b_size'] < 1):
                            raise Exception('ERROR (Dmap): Block size must be specified for block-cyclic distibution')
        else: 
            for i in range(self['dim']):
                # check that distributions defined are consistent with {'b', 'c', 'bc'}
                if dist_spec[i]['dist'] != 'b':
                    raise Exception('ERROR (Dmap): Overlap is only supported for block distributions.')
        return dist_spec


    def __eq__(self, other):
        DEBUG = 0
        # Check if both Dmap objects match with all their propreties
        if isinstance(other, Dmap):
            if (self['dim'] == other['dim']) and (self['overlap'] == other['overlap']) and (self['grid_spec'] == other['grid_spec']) :
                if (self['grid'] == other['grid']).all():
                    if (self['dist_spec'] == other['dist_spec']):
                        if DEBUG:
                            print(self['proc_list'])
                            print(type(self['proc_list']))
                            print(other['proc_list'])
                            print(type(other['proc_list']))
                        if (self['proc_list'] == other['proc_list']).all() :
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

    
    def subsref(self,s):
        """
        SUBSREF Subscripted reference.
        A.FIELD - allows the fields of a MAP objects to be referenced using
        the '.' notation (complies with structure behavior).
    
        This functionality might be deprecated from the final API, to limit
        control the user has of private members of the MAP object. SUBSREF
        might be replaced by getter functions.
    
        Author:  Nadya Travinin
        Edited:  Edmund L. Wong (elwong@ll.mit.edu)
        Python version: Dr. Chansup Byun
        """
        DEBUG = 0
        if DEBUG:
            print('--> Entering subsref for Dmap objects')
            print(a)
            print(s)
        
        """
        Note: Matlab is flexible to deal with whether s is a single structure or an array.
        In order to deal with that behavior in Python, coding becomes a little bit lengthy.
        s can be a single dictionary variable or a list of dictionary variables.
        
        In Python, the Matlab structure is converted to Pythion dictionary. 
        Listing the elements of the structure is provided by dictionary keys().
        """
    
        if isinstance(s,list):
            if s[0]['type']=='.': #subscripting type
                # switch s(1).subs
                if s[0]['subs']=='dim':
                    b = self.dim
                elif s[0]['subs']=='proc_list':
                    b = self.proc_list
                elif s[0]['subs']=='dist_spec':
                    b = self.dist_spec
                elif s[0]['subs']=='grid_spec':
                    # added for Python implementation
                    b = self.grid_spec
                elif s[0]['subs']=='grid':
                    b = self.grid
                elif s[0]['subs']=='overlap':
                    b = self.overlap
                else:
                    raise Exception('%s is not a field of Dmap.'%(s[0]['subs']))
            if DEBUG:
                print(b)
            # recursive call
            b = self.subsref(self,s[1:])
        else:
            if s['type']=='.': #subscripting type
                # switch s(1).subs
                if s['subs']=='dim':
                    b = self.dim
                elif s['subs']=='proc_list':
                    b = self.proc_list
                elif s['subs']=='dist_spec':
                    b = self.dist_spec
                elif s['subs']=='grid_spec':
                    # added for Python implementation
                    b = self.grid_spec
                elif s['subs']=='grid':
                    b = self.grid
                elif s['subs']=='overlap':
                    b = self.overlap
                else:
                    raise Exception('%s is not a field of Dmap.'%(s['subs']))
            else:
                raise Exception('%s is not a field of subset of map.'%(s['type']))

        if DEBUG:
            print('<-- Exiting subsref for Dmap objects')
        return b

    def copy(self):
        """Copy the given map'"""
        new_map = Dmap(self['grid_spec'],self['dist_spec'],self['proc_list'],self['overlap'])
        return new_map

    def show(self):
        """
        Show the map properties
        '"""        
        print('  Map object')
        print('      Dimension:  %d'%(self['dim']))
        print('      Grid specification: ',end='')
        print(self['grid_spec'])
        print('      Grid: ',end='')
        print(self['grid'])
        print('      Overlap: ',end='')
        print(self['overlap'])
        print('      Distribution: ')
        for i in range(self['dim']):
            print('         Dim %d: %s'%(i,self['dist_spec'][i]['dist']))
            
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


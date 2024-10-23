import numpy as np

import pPython as GPC
from Dmat import *
from size import *
from subsasgn_2D import *
from subsasgn_3D import *
from subsasgn_4D import *

def subsasgn_1D(a,s,b):
    """
    subsasgn_1D One dimensional subsasgn.
    
    S is of the following form [:], independent of the dimension of the
    distributed object dimension.
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering subsasgn_1D')

    # Instead of creating a copy of a, write directly to the memory
    # allocated for a in the caller's workspace
    # Not needed with Python: assignin('caller', inputname(1), [])
    
    if isinstance(b, (int,float,np.float64,np.float32,np.ndarray)): # RHS is a scalar or an array
        if s['subs'][0]==':':
            # A[:] = B
            if (len(size(b))==2) and (size(b)==[1,1]): 
                # b is a scalar
                # if (size(b)==[1 1])
                if inmap(a.map, GPC.Pid):
                    # assigment to a scalar
                    a.local[:] = b

            else:
                # b is a regular non distributed matrix
                # check that dimensions are the same and redistribute
                # according to a's map
                if (size(b) == a.shape): # dimensions are the same
                    if a.dim == 2: # 2-D
                        # Assuming global_ind is a tuple object of a range object or more
                        # Only works if there is no missing indices when multiple range objects are in the tuple
                        robj1 = []
                        for i in range(len(a.global_ind[0])):
                            robj1 += list(a.global_ind[0][i])
                        robj2 = []
                        for i in range(len(a.global_ind[1])):
                            robj2 += list(a.global_ind[1][i])
                        a.local[:,:] = b[robj1[0]:robj1[-1]+1,robj2[0]:robj2[-1]+1]
                    elif a.dim == 3: # 3-D
                        # Assuming global_ind is a tuple object of a range object or more
                        # Only works if there is no missing indices when multiple range objects are in the tuple
                        robj1 = []
                        for i in range(len(a.global_ind[0])):
                            robj1 += list(a.global_ind[0][i])
                        robj2 = []
                        for i in range(len(a.global_ind[1])):
                            robj2 += list(a.global_ind[1][i])
                        robj3 = []
                        for i in range(len(a.global_ind[2])):
                            robj3 += list(a.global_ind[2][i])
                        a.local[:,:] = b[robj1[0]:robj1[-1]+1,robj2[0]:robj2[-1]+1,robj3[0]:robj3[-1]+1]
                    elif a.dim == 4: # 4-D
                        # Assuming global_ind is a tuple object of a range object or more
                        # Only works if there is no missing indices when multiple range objects are in the tuple
                        robj1 = []
                        for i in range(len(a.global_ind[0])):
                            robj1 += list(a.global_ind[0][i])
                        robj2 = []
                        for i in range(len(a.global_ind[1])):
                            robj2 += list(a.global_ind[1][i])
                        robj3 = []
                        for i in range(len(a.global_ind[2])):
                            robj3 += list(a.global_ind[2][i])
                        robj4 = []
                        for i in range(len(a.global_ind[3])):
                            robj4 += list(a.global_ind[3][i])
                        a.local[:,:] = b[robj1[0]:robj1[-1]+1,robj2[0]:robj2[-1]+1,robj3[0]:robj3[-1]+1,robj4[0]:robj4[-1]+1]
                    else: # dimension > 4
                        raise Exception('DMAT/subsasgn_1D: Only up to 4 dimensional objects supported.')
                        # distributed object dimension
        else:
            raise Exception('unsupported indexing')

    # The following caused undefined Dmat error because its circular reference.
    # elif isinstance(b, Dmat):
    # elif hasattr(b, 'Dmat'):
    # elif hasattr(b, 'Dmap'):
    # elif isinstance(b, Dmat.Dmat):
    else:
        # RHS is a DMAT
        if isinstance(s['subs'][0], str):  # subscript is a CHAR
            if s['subs'][0] == ':': # subscript is a ':'
                if a.dim == 2: # 2-D
                    s['subs'][1] = ':'
                    a = subsasgn_2D(a,s,b)
                elif a.dim == 3: # 3-D
                    s['subs'][1] = ':'
                    s['subs'][2] = ':'
                    a = subsasgn_3D(a,s,b)
                elif a.dim == 4: # 4-D
                    s['subs'][1] = ':'
                    s['subs'][2] = ':'
                    s['subs'][3] = ':'
                    a = subsasgn_4D(a,s,b)
                else:
                    # >4-D
                    raise Exception('DMAT/subsasgn_1D: Only up to 4 dimensional objects supported.')
            else:
                # subscript is not ':'
                raise Exception('unsupported indexing')
                # subscript is not ':'
        else:
            # subscript is NOT a CHAR
            raise Exception('unsupported indexing')
            # subscript is NOT a CHAR

    # How to raise exception when RHS is not a DMAT or a DOUBLE?
    #   raise Exception('DMAT/subsasgn_1D: RHS must be a DOUBLE or DMAT.')

    if DEBUG:
        print('<-- Exiting subsasgn_1D')
    return a

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


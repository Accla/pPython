import numpy as np

from dcomplex import *
from size import *
from zeros import *

def remap(x, new_map):
    """
    REMAP Remaps a distributed array.
    
    REMAP(X, NEW_MAP) X is of class DMAT, NEW_MAP is of class MAP.
    Takes a distributed numerical array X and redistributes it according to
    the specified map NEW_MAP.
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering remap')

    s = size(x)
    if DEBUG:
        print('size(dmat): %s'%(str(s)))
    is_complex = 0
    if (np.iscomplex(local(x))).any():
        is_complex = 1

    if len(s) == 2: # 2D array, 2D map
        if is_complex:
            temp = dcomplex(zeros(s[0], s[1], map=new_map),zeros(s[0], s[1], map=new_map))
            temp[:,:] = x
            x = temp
        else:
            temp = zeros(s[0], s[1], map=new_map)
            if DEBUG:
                if isinstance(temp,Dmat):
                    print('local array shape of temp: %s'%(str(temp.local.shape)))
                    print('local array shape of x: %s'%(str(x.local.shape)))
                else:
                    print('local array shape of temp: %s'%(str(temp.shape)))
                    print('local array shape of x: %s'%(str(x.shape)))
            temp[:,:] = x
            x = temp
    elif len(s) == 3: #3 D array, 3D map
        temp = zeros(s[0], s[1], s[2], map=new_map)
        temp[:,:,:] = x
        x = temp
    elif len(s) == 4: # 4D array, 4D map
        temp = zeros(s[0], s[1], s[2], s[3], map=new_map)
        temp[:,:,:,:] = x
        x = temp
    else:
        raise Exception('ERROR (remap): REMAP can only be applied to arrays with 4 dimensions or less.')
    
    if DEBUG:
        print('<-- Exiting remap')
    return x

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

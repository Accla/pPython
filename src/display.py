import numpy as np
import sys

# pPython class
import pPython as GPC
from Dmat import *
from Dmap import *
from agg import *

def display(m):
    """
    DISPLAY(M) is called for the Map object or the distributed matrix object, M
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering display')
    
    if isinstance(m,Dmap):
        print('  Map object')
        print('      Dimension:  %d'%(m.dim))
        print('      Grid specification: ')
        print(m.grid_spec)
        print('      Grid: ')
        print(m.grid)
        print('      Overlap: ')
        print(m.overlap)
        print('      Distribution: ')
        for i in range(m.dim):
            print('      Dim %d: %s'%(i,m.dist_spec[i]['dist']))

    elif isinstance(m,Dmat):
        # ToDo: is there any better way to find the input variable name in Python?
        # Find all keys with same value
        keys = [k for k,v in sys._getframe(1).f_locals.items() if v == m]

        if DEBUG:
            print(keys)
        print('%s = '%(keys[0]))
        print('  Distributed matrix object')
        print(agg(m))

    if DEBUG:
        print('<-- Exiting display')

    return

########################################################
# pMatlab: Parallel Matlab Toolbox
# Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
# Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
# MIT Lincoln Laboratory
########################################################
# Copyright (c) 2023, Massachusetts Institute of Technology All rights
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

import numpy as np

from size import *
from zeros import *

def dcomplex(x,y):
    """Convert each local part of the DMATs, X & y to a new local portion of DMAT with a complex number, x.local + (y.local)j.
    If x & y are not a DMAT, it returns complex(x,y)
 
    Note: complex() is renamed as dcomplex to avoid naming conflicts

    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering dcomplex')

    if hasattr(x,'local') and hasattr(y,'local'):
        # DMAT objects
        if DEBUG:
            print('DMAT object')
        # if only works if x and y are equally sized and distributed DMAT
        if x.map == y.map:
            d = zeros(size(x),map=x.map,dtype=complex)
            d.local = np.vectorize(complex)(x.local,y.local)
        else:
            raise Exception('ERROR: Both DMAT objects have to be the same kind.')
        if DEBUG:
            print('dmat/dcomplex: return distributed array with its local array shape of %s'%(str(d.local.shape)))
    else:
        d = np.vectorize(complex)(x,y)
        if DEBUG:
            print('dmat/dcomplex: return non-distributed array shape of %s'%(str(d.shape)))
 
    if DEBUG:
        print('<-- Exiting dcomplex')
    return d

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

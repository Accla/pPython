import numpy as np

def size(d, dims=None):
    """Size of the distributed array.
    SIZE(D) returns the length of each dimension in distributed
    matrix D or an array
 
    SIZE(D, DIMS) returns the length of those dimensions specified
    in DIMS as a list object.
 
    Author:  Nadya Travinin
    Edited:  Edmund L. Wong (elwong@ll.mit.edu)
    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering size')

    # if no dimensions are specified, all are used
    if dims == None:
        # take care of non Dmat array
        if isinstance(d,np.ndarray):
            if len(d.shape) == 1:
                d = d.reshape(1,d.shape[0])
            dims = list(range(len(d.shape)))
        elif isinstance(d,(int, float)):
            # special treatment for a scalar
            dims = list(range(2))
        else:
            dims = list(range(d.dim))
    elif isinstance(dims,(int)):
        dims = [dims]
    
    # If there are no output arguments or 1 output argument,
    # return the size as an array
    s = []
    for i in dims:
        # take care of non Dmat array
        if isinstance(d,(int, float)):
            # special treatment for a scalar
            s.append(1)
        else:
            s.append(d.shape[i])
    
    if DEBUG:
        print(s)
        print('<-- Exiting size')
    return s

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


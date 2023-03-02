import numpy as np
from timeit import default_timer as timer

import pPython as GPC
from Dmat import *

from agg import *
from BcastMsg import *

def agg_all(d, leader=None):
    """
    AGG_ALL Conversion from a dmat to a double
    AGG_ALL(D) Converts a distributed array into a Python NumPy array object of type
        DOUBLE. Returns the entire matrix on all processors in the map of
        the distributed array.

    Hierarchical agg() aggregates the parts of a distributed matrix on the leader processor
     using an extended binary tree..
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering agg_all')

    if not isinstance(d,Dmat):
        return d

    Pid = GPC.Pid
    Np = GPC.Np
    comm = GPC.comm

    # Return immediately if Np = 1
    if Np == 1:
        mat = d.local
        return mat

    time_01 = timer()
    # Set the leader for aggregation
    if hasattr(GPC, 'leader'):
        # GPC has attribute, leader, defined.
        map_leader = GPC.leader
    if leader:
        map_leader = leader

    # collect the entire matrix on the leader
    whole_mat = agg(d,map_leader)
    
    # increment tag
    if hasattr(GPC, 'leader'):
        GPC.tag_num += 1
    else:
        GPC.tag_num = 0
    GPC.tag = 'tag-'+str(GPC.tag_num)

    # broadcast the entire matrix to all the other processes
    [mat] = BcastMsg(map_leader, GPC.tag, whole_mat)

    if DEBUG:
        time_02 = timer()
        print('Collection time for agg_all: %f (sec)'%(time_02-time_01))
        print('mat.shape')
        print(mat.shape)
        print('--> Exiting agg_all')
    return mat

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

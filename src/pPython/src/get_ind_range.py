def get_ind_range(a,s):
    """
    GET_IND_RANGE Creates index ranges from a dictionary S with fields:
    type -- string containing '()', '{}', or '.' specifying the subscript type.
    subs -- tuple of slice objects or [ToDo] string containing the actual subscripts.
     s = {'type':'()','subs':{0:(slice()), 1:':'}} 
     
    #obsolete: Return ind as a list object with index ranges of each dimension
    IND - a dictionary of length equal to the number of dimensions, where each
    entry specifies the global indices being referenced in that
    dimension.
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    ind = dict()
    if len(s['subs'])==2: # 2-D
        ind[0] = s['subs'][0]
        ind[1] = s['subs'][1]

    elif len(s['subs'])==3: # 3-D
        ind[0] = s['subs'][0]
        ind[1] = s['subs'][1]
        ind[2] = s['subs'][2]

    elif len(s['subs'])==4: # 4-D
        ind[0] = s['subs'][0]
        ind[1] = s['subs'][1]
        ind[2] = s['subs'][2]
        ind[3] = s['subs'][3]

    else:
        raise Exception('GET_IND_RANGE: Only up to 4 dimensional objects are supported.')
        
    return ind

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

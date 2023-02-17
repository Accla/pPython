def summation(sum, *argv):
    """
    SUMMATION  Takes a sum of several Dmat objects.
    SUM = SUMMATION(SUM, dmats{n})
    SUM = SUMMATION(SUM, dmat_1, ... dmat_n)
    
    This method takes the equivalent time of O(log2(n)) serial additions.
    
    Author: Edmund Wong (elwong@ll.mit.edu)
    Python version: Dr. Chansup Byun (cbyun@ll.mit.edu)
    """

    # Make inputs consistent regardless of which form is used
    #  i.e. res[n] will hold all the Dmats.
    nargin = len(argv)
    if nargin == 1:
        # single dictionary containing all Dmats
        res = argv[0]
    elif nargin > 1:
        # multiple Dmat arguments
        res = dict()
        for i in range(nargin):
            res[i] = argv[i]
    else:
        # no Dmat argument to sum
        raise Exception('Error (summation): no Dmats supplied.')

    # Addition pattern:
    #  1. res{1} += res{2}, ..., res{2i-1} += res{2i}, ...
    #  2. res{1} += res{3}, ..., res{4i-3} += res{4i-1}, ...
    #  3. res{1} += res{5}, ..., res{8i-7} += res{8i-3}, ...
    #  4. res{1} += res{9}, ..., res{16i-15} += res{16i-7}, ...
    #  ...
    #  n. res{1} += res{2^(n-1)}, ..., res{2^n(i-1)+1} +=
    #     res{2^(n-1)(2i-1)+1}, ...
    #
    # Invariant: At the end of round n:
    #
    #   res{(2^n)(i-1)+1} = summation(res{(2^n)(i-1)+1}, ..., res{(2^n)i})
    #
    # for i=1:ceil(len(res)/2^n)
    #
    # (someone might want to double-check that ) )
    gap = 1
    length = len(res)
    while gap < length:
        for i in range(0,length-gap,gap*2):
            res[i] = res[i] + res[i+gap]
        gap = gap*2

    sum[:, :] = res[0]
    
    return sum

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


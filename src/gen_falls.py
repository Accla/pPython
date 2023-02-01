from Falls import *

# Modified implemention to distribute elements across processors as evenly as possible.
#
def gen_falls(pf, pid):
    """Generates the local FALLS (FAmiLy of Line Segmentts) structure for processor, pid, from the given
    instance of PitFalls class.

    Usage:
    ------
    f = gen_falls(pf, pid)

    pf: insttance of the PitFalls class
    pid: process rank, starting from zero

    The following are the fields of each falls F:
    L: starting index of the first block
    R: ending index of the first block
    S: stride between successive L's
    N: number of equally spaced, equally sized blocks of elements
    LOCAL_LEN: local length of the data on the local processor
        NOTE: If dimensions are evenly divisible, LOCAL_LEN is
                always (R-L+1)*N
    COMPLETE_CYCLE: flag that indicates whether the processor has
                    incomplete cycles
    COMPLETE_BLOCK: flag that indicates whether the processor has
                    incomplete blocks

    Author: Nadya Travinin
    Python version: Dr. Chansup Byun

    References: Shankar Ramaswamy and Prithviraj Banerjee. Automatic Generation of Efficient Array
                Redistribution Routines for Distributed Memory Multicomputers. IEEE 1995.
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering gen_falls')

    # Create an empty Falls class.
    f = Falls()

    f.l = pf.l+pid*pf.d
    f.r = pf.r+pid*pf.d
    f.s = pf.s
    f.n = pf.n
    # additional info used to calculate global index in get_global_ind()
    f.dist = pf.dist

    # compute local length
    block_size = f.r-f.l+1 # block size
    if pf.rem_cycle == 0:
        f.local_len = f.n*block_size
        f.complete_cycle = True  # flag that signifies that the local data has no incomplete cycles
        f.complete_block = True  # flag that signifies that the local data has no incomplete blocks
        # (i.e. local indices can be computed directly from the falls info without
        # dealing with local length)
    else: # rem_cycle ~= 0
        # number of blocks in the incomplete cycle (both complete
        # and incomplete)
        num_blocks = math.ceil(pf.rem_cycle/block_size)
        # the length of incomplete block (if one exists)
        rem_block = pf.rem_cycle%block_size
        if DEBUG:
            print('num_blocks: %d'%(num_blocks))
            print('rem_block: %d'%(rem_block))

        if f.dist == 'b':
            if (pid)<pf.rem_cycle:
                # local processor does not have an incomplete cycle
                # and has no incomplete blocks
                f.local_len = (f.n)*block_size
                f.complete_cycle = True
                f.complete_block = True
            else:
                # local processor has an incomplete cycle with an
                # incomplete block
                f.local_len = (f.n)*block_size-1
                f.complete_cycle = False
                f.complete_block = False
                # adjustment for incomplete cycle & incomple block
                f.l = pf.l+pid*pf.d-(pid-pf.rem_cycle)
                f.r = pf.r+pid*pf.d-(pid-pf.rem_cycle)-1
                if DEBUG:
                    print('f.l & f.r changed (incomplete cycle, incomplete block): %d,%d'%(f.l,f.r))
        else:
            if (pid+1)<num_blocks:
                # local processor does not have an incomplete cycle
                # and has no incomplete blocks
                f.local_len = (f.n)*block_size
                f.complete_cycle = True
                f.complete_block = True
            elif (pid+1)>num_blocks:
                # local processor has one less block (incomplete cycle)
                # but no imcomplete blocks
                f.local_len = (f.n-1)*block_size
                f.complete_cycle = False
                f.complete_block = True
            elif (pid+1)==num_blocks:
                if rem_block==0:
                    # local processor has no incomplete cycles or blocks
                    f.local_len = f.n*block_size
                    f.complete_cycle = True
                    f.complete_block = True
                else:
                    # local processor has an incomplete cycle with an
                    # incomplete block
                    f.local_len = (f.n-1)*block_size+rem_block
                    f.complete_cycle = False
                    f.complete_block = False
    if DEBUG:
        print('<-- Exiting gen_falls')
    return f

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

from GridFalls import *

# Modified implemention to distribute elements across processors as evenly as possible.
#
def gen_falls(pf, pid):
    """Generates the local FALLS (FAmiLy of Line Segmentts) structure for processor, pid, from the given
    instance of GridPitFalls class.

    Usage:
    ------
    f = gen_falls(pf, pid)

    pf: insttance of the GridPitFalls class
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

    Original Author: Nadya Travinin (pMatlab)
    Author: Dr. Chansup Byun (pPython)

    References: Shankar Ramaswamy and Prithviraj Banerjee. Automatic Generation of Efficient Array
                Redistribution Routines for Distributed Memory Multicomputers. IEEE 1995.
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering gen_falls')

    # Create an empty GridFalls class.
    f = GridFalls()

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


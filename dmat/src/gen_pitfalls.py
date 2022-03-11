import math

class PitFalls:
    """Define empty PITFALLS class.
    """
    pass

def gen_pitfalls(np, dist_spec, dim_len, overlap=None):
    """Given the number of processors, distribution spec, and the length of the dimension,
    generates all the PITFALLS (Process Index Tagged FALLS) information.

    Usage:
    ------
    p = gen_pitfalls(np, dist_spec, dim_len[, overlap])

    np: number of processors along which the dimension is distributed
    dist_spec: distribution specification with two possible keys.
        The dist key is mandatory and could have the following values:
        'b' - block
        'c' - cyclic
        'bc' - block-cyclic
        if dist_spec['dist'] == 'bc', the block size 'b_size' must
        also be defined.
     dim_len: length of the dimension for which the PITFALLS is being
        created.

    Returns p:
    P is a single PITFALLS used to describe the distribution. P will
    have an extra field (p.rem_cycle) which will store the length of
    the incomplete cycle in the current distribution. This way 3
    PITFALLS will not be necessary to represent non-evenly divisible
    dimensions.
    P has the following fields:
        p.L: starting index of the first block on the first processor
        p.R: ending index of the first block on the first processor
        p.S: stride between successive L's
        p.N: number of equally spaced, equally sized blocks of elements
                per processor
        p.D: spacing between L's of successive processor FALLS
        p.P: number of processors
        p.REM_CYCLE: the length of the incomplete cycle.
            IMPORTANT: p.N includes the incomplete cycle if one exists, i.e. the
                PITFALLS calculation rounds up the length of the dimension and
                computes the PITFALLS information as if the dimension was
                evenly divisible by the cycle length.
        p.dist: distribution spec ('b', 'c', or 'bc'  )

    Original Author: Nadya Travinin (pMatlab)
    Author: Dr. Chansup Byun (gridPython)

    References: Shankar Ramaswamy and Prithviraj Banerjee. Automatic Generation of Efficient Array
        Redistribution Routines for Distributed Memory Multicomputers. IEEE 1995.

    """

    # Create an empty PitFalls class.
    p = PitFalls()
    p.overlap = overlap

    if not overlap:  # no overlap
        # store block size
        if dist_spec['dist'] == 'b':
            # ToDo: raise by 1 (ceil, pMatlab implementation) or not?
            b_size = math.ceil(dim_len/np)

        elif dist_spec['dist'] == 'c':
            b_size = 1
        elif dist_spec['dist'] == 'bc':
            b_size = dist_spec['b_size']

        # cycle length
        cycle_len = b_size*np
        # number of cycles - both complete and incomplete
        # ToDo: raise by 1 or not?
        num_cycles = math.ceil(dim_len/cycle_len)
        # length of incomplete cycle
        rem_cycle = dim_len%np
        # additional info used when calculating global index in get_global_ind()
        p.dist = dist_spec['dist']

        # create the PITFALLS data structure
        p.l = 1
        p.r = b_size


        # !!!THIS PRODUCES STRIDE>1 EVEN IF NUM_CYCLES==1...MAKE SURE THIS WORKS
        # !!!This might influence the intersection algorithm
        p.s = b_size*np

        p.n = num_cycles
        p.d = b_size
        p.p = np
        p.rem_cycle = rem_cycle

    else:  # overlap  (Need to verify, not yet tested)
        # store block size
        if dist_spec['dist'] == 'b':
            # ToDo: raise by 1 (ceil, pMatlab implementation) or not?
            b_size = math.ceil(dim_len/np)
        else:
            print('ERROR(gen_pitfalls): Overlap is only supported for block distributions.')

        # cycle length
        cycle_len = b_size*np+overlap
        # number of cycles - both complete and incomplete

        # ToDo: raise by 1 or not?
        num_cycles = math.ceil(dim_len/cycle_len)
        # length of incomplete cycle
        rem_cycle = dim_len%cycle_len

        # create the PITFALLS data structure
        p.l = 1
        p.r = b_size+overlap

        # !!!THIS PRODUCES STRIDE>1 EVEN IF NUM_CYCLES==1...MAKE SURE THIS WORKS
        # !!!This might influence the intersection algorithm
        p.s = b_size*np

        p.n = num_cycles
        p.d = b_size
        p.p = np
        p.rem_cycle = rem_cycle

    return p


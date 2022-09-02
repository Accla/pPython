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
        print('Error (summation): no Dmats supplied.')
        exit()

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


from LineSgmt import *

def ls_intersection(l1,l2):
    """
    LS_INTERSECTION Finds an intersection of two line segments.
    L1, L2, LI are line segment data structures that represent a block of
    elements in a single dimension. The line segment data structure, L, has
    the following fields:
    L.L - starting index of the block of elements
    L.R - ending index of the block of elements
    
    Returns an empty line segment object if no intersection
    
    Python version: Dr. Chansup Byun
    Author:   Nadya Travinin
    
    References: Shankar Ramaswamy and Prithviraj Banerjee. Automatic Generation of Efficient Array
                Redistribution Routines for Distributed Memory Multicomputers. IEEE 1995.

    """
    
    li = LineSgmt()
    
    li.l = max(l1.l, l2.l)
    li.r = min(l1.r, l2.r)
    
    if li.l>li.r:
        li = LineSgmt()
    
    return li


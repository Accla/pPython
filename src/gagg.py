from multipledispatch import dispatch
import numpy as np

from grid_gagg import *

@dispatch(object)
def gagg(m):
    """grid_gagg() wrapper method for imap = 1
    """
    dest = 0 # default destination
    ops = '+'
    plist = None
    return grid_gagg(m,dest,ops,plist)

@dispatch(object,int,str)
def gagg(m,dest,ops):
    """grid_gagg() wrapper method for imap = 1
    """
    plist = None
    return grid_gagg(m,dest,ops,plist)

@dispatch(object,int,str,list)
def gagg(m,dest,ops,plist):
    """grid_gagg() wrapper method for imap = 1
    """
    return grid_gagg(m,dest,ops,plist)


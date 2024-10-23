import numpy as np
from pPython.dmat import global_ind,local,put_local

def write_matrix(X,file):
    """Save a distributed matrix (2D) into a file
    """
    myJ = global_ind(X,1)  # Get local indices.
    Xlocal = local(X)        # Get local matrix.
    for j in range(len(myJ)):          # Loop over local indices.
        Xj = Xlocal[:,j]     #  Get a vector.
        filej = file+'.'+str(myJ[j])+ '.npz'  # Create filename.
        np.savez(filej, Xj=Xj)

def read_matrix(Y,file):
    """Read a distributed array (Matrix in 2-D)
    """
    myJ = global_ind(Y,1)        # Get local indices.
    Ylocal = local(Y)              # Create a local matrix.
    for j in range(len(myJ)):                # Loop over local indices.
        filej = file+'.'+str(myJ[j])+'.npz'  # Create filename.
        npzfile = np.load(filej) # Read data.
        Ylocal[:,j] = npzfile['Xj']
    Y = put_local(Y,Ylocal)        # Copy back to distributed matrix.
    return Y

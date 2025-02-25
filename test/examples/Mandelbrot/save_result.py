import numpy as np
from agg import *
def save_result(W,Pid,filename,ID):
    # Save an aggregated array, @
    np.save(filename+'_'+str(ID)+'.npy', W)    # .npy extension is added if not given
    #To load: W = np.load('filename_0.npy')



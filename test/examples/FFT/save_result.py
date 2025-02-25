import numpy as np
from agg import *
def save_result(X,Pid,ID):
    # Aggregate the results as a global array and save it.
    Xglobal = agg(X)
    if (Pid == 0):
        print('Xglobal')
        print(Xglobal.shape)
        np.save('test_Xglobal_'+str(ID)+'.npy', Xglobal)    # .npy extension is added if not given
        #To load: Xglobal = np.load('test3.npy')



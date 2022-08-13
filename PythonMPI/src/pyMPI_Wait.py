import os

from pyMPI_Sleep import *
from StopExecution import *

def pyMPI_Wait(funcname,filename,logical_state):
    """
    Wait until the given file reached the desired status
    funcname: calling function
    filename: name of the file to check
    logical_state: True: -> exits already
                   False -> not exist yet
    """

    # How much the pause time gets increased each iteration
    pause_rate = 0.03
    # Initial pause time
    pause_init = 0.3
    # max iteration
    max_iter = 100

    # Spin on the file until its desired status is reached.
    loop = 0;
    sum = 0;
    pause_time = pause_init
    while os.path.exists(filename) == logical_state :
        # Sleep statement allows cleaner profiling, but adds latency.
        sum += pause_time
        pyMPI_Sleep(pause_time);
        if loop > max_iter:
            print('%s: failed to find the %s file.'%(funcname,filename))
            print('Loop: %d, total wait time: %f, last pause interval: %f'%(loop,sum,pause_time))
            raise StopExecution
        loop = loop + 1
        pause_time += pause_time * pause_rate
    return

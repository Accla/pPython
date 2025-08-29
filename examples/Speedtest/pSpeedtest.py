"""
This script times SendMsg/RecvMsg for a variety of message sizes.
To run in parallel at the Matlab prompt type
    eval(pRUN('pSpeedtest',2,{}))
"""
import numpy as np
from timeit import default_timer as timer

# Import pPython class.
import pPython as GPC

# Import pPython methods.
from pPython.utils import SendMsg,RecvMsg

#  MPI information
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

Nmessage = 20  # Number of message sizes.
Ntrial = 4     # Trials per message size.

if(Np < 2):
    raise Exception('ERROR: too few processors (need at least 2)')

# Setting up a ring communication
source = (Pid - 1)%Np  # Set source.
dest =   (Pid + 1)%Np  # Set destination.

tag = 8  # Initial messge tag.
TotalTime = np.zeros((Ntrial,Nmessage))  # Timing matrix.

# Compute message sizes.
p = np.array(range(1,Nmessage+1))
messageSize = np.power(2,p)
ByteSize = 8*messageSize

for i_message in range(Nmessage):  # Loop over each message size.

    # Create message.
    sendData = np.zeros((1,messageSize[i_message])) + Pid

    for i_trial in range(Ntrial):

        tic = timer()                               # Start clock.
        SendMsg(dest,tag,sendData)                  # Send data.
        [recvData] = RecvMsg(source,tag)            # Receive data.
        TotalTime[i_trial,i_message] = timer()-tic  # Stop clock.

        # Check data.
        if (recvData != source).any():
            print('WARNING: incorrect data sent.')

        tag = (tag + 1)%32+1    # Increment message tag.

# Compute bandwidth.
MessageBytes = np.tile(ByteSize, (Ntrial, 1))
Bandwidth = np.divide(2*MessageBytes,TotalTime)

# Write data to a file.    
outfile = 'speedtest.'+str(Pid)+'.npz'
np.savez(outfile, ByteSize=ByteSize,TotalTime=TotalTime,MessageBytes=MessageBytes,Bandwidth=Bandwidth)

print('')
print('SUCCESS')
print('')


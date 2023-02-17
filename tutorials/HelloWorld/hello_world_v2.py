import pPython as GPC

# Just print 'Hello World!'
print('Hello World!')

# My pPython process ID (Pid or Rank)
Pid = GPC.Pid
print('My Pid = %d'%(Pid))

# How many pPython processes are running?
Np = GPC.Np
print('Total number of pPython processes (Np) = %d'%(Np))

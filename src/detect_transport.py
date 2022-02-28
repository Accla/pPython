import os

def detect_transport():
    """Detect the scheduler transport command. """
    sched_transport = 'ssh'
    if os.path.exists('/etc/llgrid.id'):
        # LLSC system 
        sched_transport = 'local'
        
    return sched_transport



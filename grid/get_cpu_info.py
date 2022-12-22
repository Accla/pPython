def get_cpu_info(cpu_type,cluster_name):
    """
    Set the max_cores and max_threads based on CPU and Node types

    max_slots: Maximum number of processes allowed to run normally 
             usually equivalent to number of physical cores, but not always
    max_cores: Maximum number of physical cores
    max_threads: Maximum number of hardware threads
  
    Python author: Dr. Chansup Byun
    """
    if (cpu_type == 'amd-epyc') or (cpu_type == 'amd-epyc,7702P'):
        max_slots = 64
        default_slots = 64
        max_cores = 64
        max_threads = 128
    elif (cpu_type == 'opteron') or (cpu_type == 'opteron,6274'): 
        max_slots = 32
        default_slots = 32
        max_cores = 32
        max_threads = 32
    elif (cpu_type == 'xeon-e5') or (cpu_type == 'xeon-e5,2683v3') or (cpu_type == 'xeon-e5,2680v4'):
        max_slots = 28
        default_slots = 28
        max_cores = 28
        max_threads = 56
    elif (cpu_type == 'xeon-g6') or (cpu_type == 'xeon-g6,6248'):
        max_slots = 40
        default_slots = 40
        max_cores = 40
        max_threads = 80
    elif (cpu_type == 'xeon-e5,2650'):
        # TX-E1 old nodes have 16 cores (2 sockets of 8 cores)
        max_slots = 16
        default_slots = 16
        max_cores = 16
        max_threads = 16
    elif (cpu_type == 'xeon-e7'): 
        max_slots = 2
        default_slots = 2
        max_cores = 2
        max_threads = 2
    elif (cpu_type == 'xeon64c') or (cpu_type == 'xeon64c,7210'): 
        max_slots = 64
        default_slots = 32
        max_cores = 64
        max_threads = 256
    elif (cpu_type == 'xeon-p8'): 
        max_slots = 48
        default_slots = 48
        max_cores = 48
        max_threads = 96
    else:
        print(' ')
        raise Exception('ERROR(get_cpu_info): CPU type, %s, is not available on %s'%(cpu_type,cluster_name))

    return max_slots,default_slots,max_cores,max_threads


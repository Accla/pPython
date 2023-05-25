#!/usr/bin/python
import numpy as np

def map_procs_to_cores(nppn, max_cores, ntpc, dist_type):
    #    
    # Generate physical threads list for taskset with the given number of prcesses per node
    # Distribute all the available physical threads to the given processes as evenly as possible
    # With oversubscription, all the overloaded processes follow the distribution done with nppn processes
    #    
    # Input:
    # nppn:              number of processes per node
    # max_cores:         max number of physical cores on the node
    # ntpc:              number of physical threads per core
    # dist_type:         determine how to distribute core id (block or cyclic)
    #                        1 = block, 2  = cyclic
    #                        cyclic_inc: default increment for cyclic distribution for two sockets
    #                        ToDo: cyclic_inc can be an input if there are more than two sockets per node
    cyclic_inc = 2;

    #    
    # Output:
    # cores_per_proc_list: a dictionary variable to hold physical core & thread ids for nppn processes
    #    
    # max_threads: max number of physical threads on the node
    max_threads = int(max_cores * ntpc)
    #    
    # Calculate the first core id position (starting from 0) of each group
    if nppn > max_cores:
        leaders = np.linspace(start = 0, stop = max_cores, num = max_cores+1).astype(int)
    else:
        leaders = np.linspace(start = 0, stop = max_cores, num = nppn+1).astype(int)

    # Generate all the physical threads list for the given number of processes
    cores_per_proc_list = dict()
    
    if nppn == 1:
        # if there is only one process on the node, use the original distribution
        dist_type = 1
        
    if dist_type == 1:
        # Processors are mapped by block  between sockets
        for i in range(nppn):
            # i starts from 0
            # print('For the process ID = %d\n' %(i))
            # Taka care of oversubscription when NPPN > max_cores
            ipos = i%max_cores
            # Process by each processor list with j1 being 1st element of the list
            # and j2 being the last element of the list in sequence plus one
            j1 = int(leaders[ipos])
            j2 = int(leaders[ipos+1])
            # print('start=%d end=%d\n'%(j1,j2))
            # 
            inum = []
            if ntpc == 1:
                # No physical thread, core = thread
                # Generate processor IDs in sequence between j1 and j2 (j2 not included)
                inum += list(np.arange(j1,j2).astype(str))
            elif ntpc == 2:
                # Each core has two physical threads, 1 core =  2 threads
                # Depending on the vendor, processord IDs are assigned differently (HP vs Dell)
                # For main core
                inum += list(np.arange(j1,j2).astype(str))
                # For 2nd physical thread
                inum += list(np.arange(j1+max_cores,j2+max_cores).astype(str))
            elif ntpc == 4:
                # Each core has four physical threads, 1 core =  4 threads
                # For main core
                inum += list(np.arange(j1,j2).astype(str))
                # For 2nd, 3rd, and 4th physical threads
                inum += list(np.arange(j1+max_cores,j2+max_cores).astype(str))
                inum += list(np.arange(j1+max_cores*2,j2+max_cores*2).astype(str))
                inum += list(np.arange(j1+max_cores*3,j2+max_cores*3).astype(str))

            else:
                print(' ')
                raise Exception('Error (map_proc_to_core): Number of physical threads per coe, %d, is not supported!'%(ntpc))
            #
            # Physical thread ID list assigned to the given process
            cores_per_proc_list[i]=inum
    elif dist_type == 2:
        # Processors are mapped cyclicly between sockets
        # For each loop, calculate mapping for two processes
        for i in range(0,nppn,2):
            # i starts from 0
            # print('For the process ID = %d\n' %(i))
            # Taka care of oversubscription when NPPN > max_cores
            ipos = i%max_cores
            # Process by pairs of processor lists with j1 being 1st element of the 1st  list
            # and j2 being the last element + 1 of the 2nd list
            j1 = int(leaders[ipos])
            j2 = int(leaders[ipos+cyclic_inc])
            # print('start=%d end=%d\n'%(j1,j2))
            inum1 = []
            inum2 = []
            if ntpc == 1:
                # No physical thread, core = thread
                # Generate processor IDs in sequence with cyclic_inc stride between j1 and j2 (j2 not included)
                # (j2 not included in the result from range function)
                # For main core (processed by pair of the processor IDs lists)
                inum1 += list(np.arange(j1,j2,cyclic_inc).astype(str))
                inum2 += list(np.arange(j1+1,j2,cyclic_inc).astype(str))
            elif ntpc == 2:
                # Each core has two physical thread, 1 core =  2 threads
                # Depending on the vendor, processord IDs are assigned differently (HP vs Dell)
                # For main core (processed by pair of the processor IDs lists)
                inum1 += list(np.arange(j1,j2,cyclic_inc).astype(str))
                inum2 += list(np.arange(j1+1,j2,cyclic_inc).astype(str))
                # For 2nd physical thread
                inum1 += list(np.arange(j1+max_cores,j2+max_cores,cyclic_inc).astype(str))
                inum2 += list(np.arange(j1+1+max_cores,j2+max_cores,cyclic_inc).astype(str))
            elif ntpc == 4:
                # Each core has four physical thread, 1 core =  4 threads
                # For main core (processed by pair of the processor IDs lists)
                inum1 += list(np.arange(j1,j2,cyclic_inc).astype(str))
                inum2 += list(np.arange(j1+1,j2,cyclic_inc).astype(str))
                # For 2nd, 3rd, and 4th physical threads
                inum1 += list(np.arange(j1+max_cores,j2+max_cores,cyclic_inc).astype(str))
                inum2 += list(np.arange(j1+1+max_cores,j2+max_cores,cyclic_inc).astype(str))
                inum1 += list(np.arange(j1+max_cores*2,j2+max_cores*2,cyclic_inc).astype(str))
                inum2 += list(np.arange(j1+1+max_cores*2,j2+max_cores*2,cyclic_inc).astype(str))
                inum1 += list(np.arange(j1+max_cores*3,j2+max_cores*3,cyclic_inc).astype(str))
                inum2 += list(np.arange(j1+1+max_cores*3,j2+max_cores*3,cyclic_inc).astype(str))
            else:
                print('')
                raise Exception('Error (map_procs_to_cores): Number of physical threads per coe, %d, is not supported!'%(ntpc))
            #
            # Physical thread ID list assigned to the given process
            cores_per_proc_list[i]=inum1
            if i < nppn-1:
                # Take care when nppn is an odd number
                cores_per_proc_list[i+1]=inum2

    return cores_per_proc_list


from grid_status import *

def grid_resource_policy(grid_config, n_proc, interactive):
    """Determine if there are enough resources to fit the requested job. 
    """
    
    #
    # Check the available resources (contact the scheduler)
    total_procs,unclaimed_procs,unclaimed_nodes,\
    cluster_name,grid_scheduler,grid_scheduler_ver \
    = grid_status(grid_config['default_cpu_type'])
    
    requested = n_proc - interactive
    if requested <= unclaimed_procs:
        if grid_config['nnode'] > unclaimed_nodes:
            # Triple mode jobs cannot be launched.
            print('!!! The triple-mode job launch can currently only offer a total of %d idle nodes.'\
            %(unclaimed_nodes))
            print('!!! Please submit your request with fewer nodes.')
            exit()
    else:
        # Not enough resources to fit my resource request currently.
        # Exit the process
        # More sophiscated resource policy implementation in gridMatlab ver.
        print('!!! The Grid can currently only offer a total of %d processors.'\
        %(total_procs))
        print('!!! Please submit your request with fewer cores.')
        exit()

    return requested,unclaimed_procs,unclaimed_nodes


from replace_token import *

def pyMPI_Dir_map(machine_db,path):
    """pyMPI_Dir_map  -  Takes care of pc/linux/mac/grid path translation for a given patth.
    
    Usage:
    ------
    dir_pc, dir_linux, dir_mac, dir_grid = pyMPI_Dir_map(machine_db,path)
    
    machine_db: machine database (dtype; dictionary)
    path:       directory path (dtype: string)
    dir_pc:     Winods OS directory path (dtype: string)
    dir_linux:  Linux OS directory path (dtype: string)
    dir_mac:    Mac OS directory path (dtype: string)
    dir_grid:   directory path on the grid (dtype: string)
    
    """

    DEBUG = 0

    # Default is to do nothing.
    dir_pc = path;
    dir_linux = path;
    dir_mac = path;
    dir_grid = path;

    # Check if a directory mapping has been defined.
    # If so, convert directory names.
    if 'local_dir_map' in machine_db:
        pc_base = machine_db['local_dir_map'][0]
        pc_n    = len(pc_base);
        linux_base = machine_db['local_dir_map'][1]
        linux_n    = len(linux_base);
        mac_base = machine_db['local_dir_map'][2]
        mac_n    = len(mac_base);
        grid_base = machine_db['local_dir_map'][3]
        grid_n    = len(grid_base);

        if path[0:pc_n].lower() == pc_base.lower():
            # Check if path has a pc base
            # Convert all other paths accordingly.
            # Swap bases for other path variables.
            dir_linux = linux_base + path[pc_n:]
            dir_mac = mac_base + path[pc_n:]
            dir_grid = grid_base + path[pc_n:]

            dir_linux = replace_token('\\','/',dir_linux)
            dir_mac = replace_token('\\','/',dir_mac)
            dir_grid = replace_token('\\','/',dir_grid)
            
        elif path[0:linux_n].lower() == linux_base.lower():
            # Check if path has a linux base
            # Convert all other paths accordingly.
            # Swap bases for other path variables.
            dir_pc = pc_base + path[linux_n:]
            dir_mac = mac_base + path[linux_n:]
            dir_grid = grid_base + path[linux_n:]

            dir_pc = replace_token('/','\\',dir_pc)
            
        elif path[0:mac_n].lower() == mac_base.lower():
            # Check if path has a mac base
            # Convert all other paths accordingly.
            # Swap bases for other path variables.
            dir_pc = pc_base + path[mac_n:]
            dir_linux = linux_base + path[mac_n:]
            dir_grid = grid_base + path[mac_n:]

            dir_pc = replace_token('/','\\',dir_pc)
            
        elif path[0:grid_n].lower() == grid_base.lower():
            # Check if path has a grid base
            # Convert all other paths accordingly.
            # Swap bases for other path variables.
            dir_pc = pc_base + path[grid_n:]
            dir_linux = linux_base + path[grid_n:]
            dir_mac = mac_base + path[grid_n:]

            dir_pc = replace_token('/','\\',dir_pc)
            
        else:
            print("ERROR(pyMPI_Dir_map): path, %s, does not match with any in machine_db['local_dir_map']"%(path))
            exit()

    return dir_pc, dir_linux, dir_mac, dir_grid

import os
import re

import checkOS as OS
from replace_token import *

def pyMPI_Dir_translate(machine_db,path):
    """pyMPI_Dir_translate  -  Takes care of pc/linux/mac/grid translation of current working directory.
    
    Usage:
    ------
    local_path = pyMPI_Dir_translate(machine_db,path)
    
    machine_db: machine database (dtype; dictionary)
    path:       input directory path (dtype: string)
    local_path: local directory path (dtype: string)
    """

    DEBUG = 0

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
    else:
        print('Error (pyMPI_Dir_translate): local directory map not defined in machine_db (local_dir_map)')
        exit()

    # Check which OS is compatiable with the given path
    if re.search(pc_base,path,re.IGNORECASE):
        n_base = pc_n
    elif re.search(linux_base,path,re.IGNORECASE):
        n_base = linux_n
    elif re.search(mac_base,path,re.IGNORECASE):
        n_base = mac_n
    elif re.search(grid_base,path,re.IGNORECASE):
        n_base = grid_n
    else:
        print('Error (pyMPI_Dir_translate): given path, %s, is not compatible with local directory map.')
        exit()

    if DEBUG:
        print('n_base = %d'%(n_base))
        
    # Swap bases.
    if os.path.exists('/etc/llgrid.id'):
        local_path = grid_base + path[n_base:]
        # in case, local_path has Windows separator in path
        local_path = replace_token("\\","/",local_path)
    else:
        if OS.ispc:
            local_path = pc_base + path[n_base:]
            # Replace '/' with '\\' if exists.
            local_path = replace_token("/","\\",local_path)
        elif OS.islinux:
            local_path = linux_base + path[n_base:]
            # Replace '\\' with '/' if exists.
            local_path = replace_token("\\","/",local_path)
        elif OS.ismac:
            local_path = mac_base + path[n_base:]
            # Replace '\\' with '/' if exists.
            local_path = replace_token("\\","/",local_path)

    if DEBUG:
        print('after replace: %s'%(dir_linux))

    return local_path


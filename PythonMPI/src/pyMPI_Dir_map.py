def pyMPI_Dir_map(machine_db,path):
    """pyMPI_Dir_map  -  Takes care of pc/linux/mac translation of current working directory.
    
    Usage:
    ------
    dir_pc, dir_linux, dir_mac = pyMPI_Dir_map(machine_db,path)
    
    machine_db: machine database (dtype; dictionary)
    path:       directory path (dtype: string)
    dir_pc:     Winods OS directory path (dtype: string)
    dir_linux:  Linux OS directory path (dtype: string)
    dir_max:    Mac OS directory path (dtype: string)
    
    """

    DEBUG = 0

    # Default is to do nothing.
    dir_pc = path;
    dir_linux = path;
    dir_mac = path;

    # Check if a directory mapping has been defined.
    # If so, convert directory names.
    if 'local_dir_map' in machine_db:
        pc_base = machine_db['local_dir_map'][0]
        pc_n    = len(pc_base);
        linux_base = machine_db['local_dir_map'][1]
        linux_n    = len(linux_base);
        mac_base = machine_db['local_dir_map'][2]
        mac_n    = len(mac_base);

        # Check if pc_dir has a linux base 
        # remove from string.
        if dir_pc[0:linux_n] == linux_base[0:linux_n]:
            # Swap bases.
            dir_pc = pc_base + dir_pc[linux_n:]

        # Replace '/' with '\'.
        dir_pc.replace('/','\\')

        # Check if mac_dir has a linux base 
        # remove from string.
        if dir_mac[0:linux_n] == linux_base[0:linux_n]:
            # Swap bases.
            dir_mac = mac_base + dir_mac[linux_n:]

        # Check if linux_dir has a pc base or a mac base
        # remove from string.
        if dir_linux[0:pc_n] == pc_base[0:pc_n]:
            # Swap bases.
            dir_linux = linux_base + dir_linux[pc_n:]
        elif dir_linux[0:mac_n] == mac_base[0:mac_n]:
            # Swap bases.
            dir_linux = linux_base + dir_linux[mac_n:]

        # Replace '\' with '/'.
        if DEBUG:
            print('befor replace: %s'%(dir_linux))
        old_str = "\\"
        new_str = "/"
        # replace() does not work for some reason
        # dir_linux.replace(old_str,new_str)
        # dir_mac.replace(old_str,new_str)
        new_path = ''
        for i, letter in enumerate(dir_linux):
            if letter == old_str:
                new_path = new_path+new_str
            else:
                new_path = new_path+letter
        dir_linux = new_path
        new_path = ''
        for i, letter in enumerate(dir_mac):
            if letter == old_str:
                new_path = new_path+new_str
            else:
                new_path = new_path+letter
        dir_mac = new_path
        if DEBUG:
            print('after replace: %s'%(dir_linux))

    return dir_pc, dir_linux, dir_mac

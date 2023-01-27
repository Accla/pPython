from replace_token import *

import checkOS as OS
import pyMPI_COMM_WORLD as pyMCW

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

    Note: machine_db can support multiple paths on the grid but only one path
          based on the user home directory path.  All other group shared directories
          should have symbolic links at $HOME.

    Python version: Dr. Chansup Byun
    """

    DEBUG = 0 
    if DEBUG: 
        print('--> Entering pyMPI_Dir_map')
        print('Current working directory path: %s'%(path))
        for ref_path in machine_db['local_dir_map']:
            print(ref_path)
        print('OS.islocal = %s'%(OS.islocal))

    # Default is to do nothing.
    dir_pc = path;
    dir_linux = path;
    dir_mac = path;
    dir_grid = path;
    dir_sgrp_1 = path;
    dir_sgrp_2 = path;
    dir_sgrp_3 = path;

    grid_job = False
    if 'grid_config' in pyMCW.MPI_COMM_WORLD:
        grid_job = pyMCW.MPI_COMM_WORLD['grid_config']['grid_job']

    if OS.islocal and (not grid_job):
        if DEBUG: 
            print('pyMPI_Dir_map: Skip checking directory path.')
            print('<-- Exiting pyMPI_Dir_map')
        return dir_pc, dir_linux, dir_mac, dir_grid
        

    # Check if a diresgrp_3_basectory mapping has been defined.
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
        sgrp_1_base = machine_db['local_dir_map'][4]
        sgrp_1_n    = len(sgrp_1_base);
        sgrp_2_base = machine_db['local_dir_map'][5]
        sgrp_2_n    = len(sgrp_2_base);
        sgrp_3_base = machine_db['local_dir_map'][6]
        sgrp_3_n    = len(sgrp_3_base);
        if DEBUG:
            print('sgrp_3_base: %s'%(sgrp_3_base))
            print('sgrp_3_n: %d'%(sgrp_3_n))

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
            
        elif path[0:sgrp_1_n].lower() == sgrp_1_base.lower():
            # Check if path has a shared group 1 base
            # Convert all other paths accordingly.
            # Swap bases for other path variables.
            #
            # shared group 1 path will be converted to dir_grid
            # 
            dir_pc = pc_base + path[sgrp_1_n:]
            dir_linux = linux_base + path[sgrp_1_n:]
            dir_mac = mac_base + path[sgrp_1_n:]
            dir_grid = grid_base + path[sgrp_1_n:]

            dir_pc = replace_token('/','\\',dir_pc)
            
        elif path[0:sgrp_2_n].lower() == sgrp_2_base.lower():
            # Check if path has a shared group 1 base
            # Convert all other paths accordingly.
            # Swap bases for other path variables.
            #
            # shared group 2 path will be converted to dir_grid
            # 
            dir_pc = pc_base + path[sgrp_2_n:]
            dir_linux = linux_base + path[sgrp_2_n:]
            dir_mac = mac_base + path[sgrp_2_n:]
            dir_grid = grid_base + path[sgrp_2_n:]

            dir_pc = replace_token('/','\\',dir_pc)
            
        elif path[0:sgrp_3_n].lower() == sgrp_3_base.lower():
            # user specified path on loacl machine when running locally
            dir_pc = sgrp_3_base
            dir_linux = sgrp_3_base
            dir_mac = sgrp_3_base
            dir_grid = sgrp_3_base

        else:
            raise Exception("ERROR(pyMPI_Dir_map): path, %s, does not match with any in machine_db['local_dir_map']"%(path))

    return dir_pc, dir_linux, dir_mac, dir_grid

########################################################
# MatlabMPI
# Dr. Jeremy Kepner
# MIT Lincoln Laboratory
# kepner@ll.mit.edu
########################################################
# Copyright 2002 Massachusetts Institute of Technology
#
# Permission is herby granted, without payment, to copy, modify, display
# and distribute this software and its documentation, if any, for any
# purpose, provided that the above copyright notices and the following
# three paragraphs appear in all copies of this software.  Use of this
# software constitutes acceptance of these terms and conditions.
#
# IN NO EVENT SHALL MIT BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
# SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
# THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF MIT HAS BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# MIT SPECIFICALLY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
#
# THIS SOFTWARE IS PROVIDED "AS IS," MIT HAS NO OBLIGATION TO PROVIDE
# MAINTENANCE, SUPPORT, UPDATE, ENHANCEMENTS, OR MODIFICATIONS.

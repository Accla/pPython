import os
import re

import checkOS as OS
import pyMPI_COMM_WORLD as pyMCW
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
    if DEBUG:
        print('--> Entering pyMPI_Dir_translate')
        for ref_path in machine_db['local_dir_map']:
            print(ref_path)

    grid_job = False
    if 'grid_config' in pyMCW.MPI_COMM_WORLD:
        grid_job = pyMCW.MPI_COMM_WORLD['grid_config']['grid_job']

    if OS.islocal and (not grid_job):
        # Running locally, local_path == path
        if DEBUG:
            print('pyMPI_Dir_translate: running locally, local_path == path')
            print('<-- Exiting pyMPI_Dir_translate')
        return path

    # Initialize the path check
    is_pc_path = 0
    is_linux_path = 0
    is_mac_path = 0
    is_grid_path = 0
    is_sgrp_1_path = 0
    is_sgrp_2_path = 0
    is_sgrp_3_path = 0

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
        sgrp_1_base = machine_db['local_dir_map'][4]
        sgrp_1_n    = len(sgrp_1_base);
        sgrp_2_base = machine_db['local_dir_map'][5]
        sgrp_2_n    = len(sgrp_2_base);
        sgrp_3_base = machine_db['local_dir_map'][6]
        sgrp_3_n    = len(sgrp_3_base);
    else:
        raise Exception('Error (pyMPI_Dir_translate): local directory map not defined in machine_db (local_dir_map)')

    # Check which OS is compatiable with the given path
    if re.search(pc_base,path,re.IGNORECASE):
        n_base = pc_n
        is_pc_path = 1
    elif re.search(linux_base,path,re.IGNORECASE):
        n_base = linux_n
        is_linux_path = 1
    elif re.search(mac_base,path,re.IGNORECASE):
        n_base = mac_n
        is_mac_path = 1
    elif re.search(grid_base,path,re.IGNORECASE):
        n_base = grid_n
        is_grid_path = 1
    elif re.search(sgrp_1_base,path,re.IGNORECASE):
        n_base = sgrp_1_n
        is_sgrp_1_path = 1
    elif re.search(sgrp_2_base,path,re.IGNORECASE):
        n_base = sgrp_2_n
        is_sgrp_2_path = 1
    elif re.search(sgrp_3_base,path,re.IGNORECASE):
        n_base = sgrp_3_n
        is_sgrp_3_path = 1
    else:
        raise Exception('Error (pyMPI_Dir_translate): given path, %s, is not compatible with local directory map.'%(path))

    if DEBUG:
        print('n_base = %d'%(n_base))
        
    # Swap bases.
    if os.path.exists('/etc/llgrid.id'):
        if is_grid_path:
            local_path = grid_base + path[n_base:]
        elif is_sgrp_1_path:
            local_path = sgrp_1_base + path[n_base:]
        elif is_sgrp_2_path:
            local_path = sgrp_2_base + path[n_base:]
        elif is_sgrp_3_path:
            local_path = sgrp_3_base + path[n_base:]
        elif is_linux_path:
            # if both linux and LLGrid share the same path
            local_path = linux_base + path[n_base:]
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
        print('after replace: %s'%(local_path))

    if DEBUG:
        print('<-- Exiting pyMPI_Dir_translate')
    return local_path

########################################################
# PythonMPI
# Dr. Jeremy Kepner & Dr. Chansup Byun
# MIT Lincoln Laboratory
# kepner@ll.mit.edu & cbyun@ll.mit.edu
########################################################
# Copyright 2023 Massachusetts Institute of Technology
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

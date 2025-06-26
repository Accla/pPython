from get_queue_cpu_table import *

def get_cpu_info(key_str,cluster_name):
    """
    Set the max_cores and max_threads based on CPU and Node types

    max_slots: Maximum number of processes allowed to run normally 
             usually equivalent to number of physical cores, but not always
    max_cores: Maximum number of physical cores
    max_threads: Maximum number of hardware threads
  
    Python author: Dr. Chansup Byun
    """

    PT, CT = get_queue_cpu_table()
    try:
        if key_str in CT.keys():
            # key string is indeed a CPU type name
            default_slots = CT[key_str]['default_slots']
            max_slots = CT[key_str]['max_slots']
            max_cores = CT[key_str]['max_cores']
            max_threads = CT[key_str]['max_threads']
        elif key_str in PT.keys():
            # key string is a partition name
            cpu_type = PT[key_str]['cpu_type']
            default_slots = CT[cpu_type]['default_slots']
            max_slots = CT[cpu_type]['max_slots']
            max_cores = CT[cpu_type]['max_cores']
            max_threads = CT[cpu_type]['max_threads']
        else:
            raise Exception('ERROR(get_cpu_info): the input key, %s, is neither a partition nor a CPU type name on %s'%(key_str,cluster_name))
    except:
        raise Exception('ERROR(get_cpu_info): CPU type, %s, is not available on %s'%(key_str,cluster_name))

    return max_slots,default_slots,max_cores,max_threads

########################################################
# gridMatlab
# Dr. Albert Reuther
# reuther@ll.mit.edu
# MIT Lincoln Laboratory
########################################################
# Copyright 2003-9 Massachusetts Institute of Technology
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

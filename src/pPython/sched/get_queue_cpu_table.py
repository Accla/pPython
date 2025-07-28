import os
import xml.etree.ElementTree as ET

def get_queue_cpu_table():
    '''
    Read in queue_cpu_table.xml file and
    convert xml data into Python dictionary variables
    '''

    # Check if queue_cpu_table.xml exists in ~/ppythjon_conf first
    HOME = os.environ['HOME']
    xml_file = os.path.join(HOME,'ppython_conf','queue_cpu_table.xml')
    if os.path.exists(xml_file):
        root = ET.parse(xml_file).getroot()
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        xml_file = os.path.join(dir_path,'queue_cpu_table.xml')
        root = ET.parse(xml_file).getroot()

    # debug
    print('Absolute path for queue_cpu_table.xml: %s'%(xml_file))

    PT = dict()
    for partition in root[0].findall('partition'):
        partition_name = partition.attrib['name']
        cpu_type = partition.find('cpu_type').text
        # print('Partition name = %s: \tCPU type = %s'%(partition_name,cpu_type))
        if partition_name not in PT:
            PT[partition_name] = dict()
        PT[partition_name]['cpu_type'] = cpu_type

    CT = dict()
    # print('CPU type \tMax. slots \tMax. cores \tMax. threads')
    for cpu_type in root[1].findall('cpu_type'):
        cpu_type_name = cpu_type.attrib['name']
        default_slots = cpu_type.find('default_slots').text
        max_slots = cpu_type.find('max_slots').text
        max_cores = cpu_type.find('max_cores').text
        max_threads = cpu_type.find('max_threads').text
        # print('%s \t%s \t\t%s \t\t%s'%(cpu_type_name,max_slots,max_cores,max_threads))
        # convert into a dictionary, CT
        if cpu_type_name not in CT:
            CT[cpu_type_name] = dict()
        CT[cpu_type_name]['default_slots'] = int(default_slots)
        CT[cpu_type_name]['max_slots'] = int(max_slots)
        CT[cpu_type_name]['max_cores'] = int(max_cores)
        CT[cpu_type_name]['max_threads'] = int(max_threads)

    return PT,CT
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


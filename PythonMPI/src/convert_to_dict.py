def convert_to_dict(input,host):
    """convert_to_dict - convert a list or a set into a dictionary variable
    
    Usage:
    output = convert_to_dict(input)
    
    input: a list or a set (dtype: list or set or dictionary)
    host:  local machine name (dtype: str)
    output: a dictionary variable (dtype: dictionary)
    
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering convert_to_dict')
        print(input)

    islocal = 0
    output = dict()
    if len(input) == 0:    # empty machines list, running locally
        output = {0:host}
        islocal = 1
        return output,islocal
    
    if type(input) == type(set()) or type(input) == type(list()):
        ii = 0
        for machine in input:
            output[ii] = machine
            ii = ii + 1
        return output,islocal
    elif type(input) == type(dict()):
        ii = 0
        for machine in input:
            output[ii] = machine
            ii = ii + 1
        return output,islocal
    else:
        raise Exception('Error in convert_to_dict(). Input is neither list nor set variable.')

    return

########################################################
# PythonMPI
# Dr. Chansup Byun
# MIT Lincoln Laboratory
# kepner@ll.mit.edu
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

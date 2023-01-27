import platform

"""checkOS - identify and set OS identification variables
    
    Windows OS:  ispc = 1
    Mac OS:   ismac = 1
    Linux OS: islinux = 1
    Either Linux or Mac: isunix = 1
    
"""
# Check if one of them is defined
try: ispc
except NameError: ispc = None
if ispc is None:
    isunix=0
    ismac=0
    islinux=0
    ispc=0
    # List of supported OS system names
    listMacSystem = ['Darwin']
    listLinuxSystem = ['Linux']
    listPCSystem = ['Windows']
    
    systemName = platform.system()
    if systemName in listMacSystem:
        ismac = 1
        isunix = 1
    elif systemName in listLinuxSystem:
        islinux = 1
        isunix = 1
    elif systemName in listPCSystem:
        ispc = 1
    else:
        raise Exception('Error in checking OS. Update OS names in _checkOS() with platform.system() output')

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

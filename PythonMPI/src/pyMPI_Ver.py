import pathlib

def pyMPI_Ver():
    """pyMPI_Ver - Return the current PythonMPI version.
    
    Usage:
    version = pyMPI_Ver()
    
    location: current location of the PythonMPI library (dtype: string)
    version:  PythonMPI version (dtype: string)
    
    """
    
    location = pathlib.Path().absolute()
    version = '0.2.0'
    
    print('PythonMPI version: %s'%(version))
    print('         Location: %s'%(location))
    
    return version

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

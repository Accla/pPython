def replace_token(old_str,new_str,old_path):
    """Replace an old token with the new token for a given path.
    Usage:
    ------

    new_path = replace_token(old_str,new_str,old_path)
    
    """
    # replace() does not work for some reason
    # dir_linux.replace(old_str,new_str)
    # dir_mac.replace(old_str,new_str)
    new_path = ''
    for i, letter in enumerate(old_path):
        if letter == old_str:
            new_path = new_path+new_str
        else:
            new_path = new_path+letter
    
    return new_path

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

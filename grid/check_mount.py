import platform
import re
import string

def check_mount(LL_FILE_SERVER):
    """Check all the mounted or mapped directory paths
    and determined whether LLGrid home directory is mounted or not.
    
    Usage:
    ------
    ismounted = checkMount('LL_FILE_SERVER_NAME')
    
    Author: Dr. Chansup Byun
    """
    
    ismounted = False
    ecmd = ExecShellCmd('')
    
    if platform.system() == 'Windows':
        """Workaroud implementation
        NOT WORKING: 
        process = Popen(['net','use'],stdout=PIPE, stderr=PIPE)        
        stdout, stderr = process.communicate()
        """
        for d in string.ascii_uppercase:
            cmdstr = 'net use '+d+':'
            ecmd.run(cmdstr)
            output = ecmd.get_output()
            if re.search(LL_FILE_SERVER,output,flags=re.IGNORECASE):
                ismounted = True
                break
    else:
        cmdstr = 'mount'
        ecmd.run(cmdstr)
        output = ecmd.get_output()
        for line in output.split('\n'):
            if re.search(LL_FILE_SERVER,line,flags=re.IGNORECASE):
                ismounted = True
                print('check_mount: LLGrid home directory is mounted.')
                break
                
    return ismounted

########################################################
# pPython: Parallel Python Programming Tool
# Dr. Jeremy Kepner and Dr. Chansup Byun
# (kepner@ll.mit.edu and cbyun@ll.mit.edu)
# MIT Lincoln Laboratory
########################################################
# Copyright (c) 2023, Massachusetts Institute of Technology All rights
# reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in
#        the documentation and/or other materials provided with the
#        distribution.
#      * Neither the name of the Massachusetts Institute of Technology nor
#        the names of its contributors may be used to endorse or promote
#        products derived from this software without specific prior written
#        permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

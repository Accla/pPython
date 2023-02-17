#
from subprocess import Popen
from subprocess import PIPE

class ExecShellCmd:
    """Execute a command on a local or a remote system and
    provide a method to extract the results if available.

    Author: Dr. Chansup Byun
    """

    name =''
    procObj= None
    def __init__(self,transport_cmd = ''):
        #Init constructor
        self.name = ''
        self.transport_cmd = transport_cmd

    def run(self, cmdstr, stdIn=None):
        """Execute the command and redirect the output to the PIPE. """
        if len(self.transport_cmd):
            cmdstr = self.transport_cmd+' '+cmdstr
        if stdIn :
            self.procObj = Popen(cmdstr, shell=True, stdin=stdIn, stdout=PIPE, stderr=PIPE)
        else:
            self.procObj = Popen(cmdstr, shell=True, stdout=PIPE, stderr=PIPE)
 
    def get_stdout(self):
        """Return the standard output stream. """
        return self.procObj.stdout

    def get_output(self):
        """Read from the standard output stream. """
        output = self.procObj.communicate()[0]
        # output = self.procObj.stdout.read()
        output = output.decode("utf-8")
        return output

    def print_output(self,hdr1=None):
        """Print the standard output stream and close it when done. """
        output = self.get_output()
        if hdr1:
            print(hdr1)
        if output:
            print(output)
        self.procObj.stdout.close()

    def get_stderr(self):
        """Read from the standard error stream. """
        errout = self.procObj.communicate()[1]
        errout = errout.decode("utf-8")
        return errout

    def close(self):
        """Close it when done. """
        self.procObj.stdout.close()

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

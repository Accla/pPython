#
from subprocess import Popen
from subprocess import PIPE

class ExecShellCmd:
    """Execute a command on a local or a remote system and
    provide a method to extract the results if available.
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


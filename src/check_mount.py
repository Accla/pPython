import platform
import re
import string

def check_mount(LL_FILE_SERVER):
    """Check all the mounted or mapped directory paths
    and determined whether LLGrid home directory is mounted or not.
    
    Usage:
    ------
    ismounted = checkMount('LL_FILE_SERVER_NAME')
    
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


from glob import glob
import mmap
import os
import sys

# Import PythonMPI
from MPI_Abort import *
from pyMPI_Delete_all import *
from pyMPI_Sleep import *
from MPI_Run import *

"""Test a PythonMPI example program

"""
def findString(strInput,fileList):
    # Number of files in the list
    n_files = len(fileList)
    # number of occurrences
    nfound = 0
    # list of files containing the string
    fileNames = []
    
    for i in range(n_files):
        # print('Opening %s'%(fileList[i]))
        with open(fileList[i]) as f:
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            if s.find(bytes(strInput,'utf-8')) != -1:
                # Found the string
                nfound = nfound + 1
                fileNames.append(fileList[i])
        # closing text file    
        f.close()
        
    return nfound,fileNames

def unit_test( py_file, n_proc, machines, time_limit, time_check ):
    # Launch the script.
    print('Running: %s'%(py_file))
    # print(os.sys.path)

    # Clearn up an old PythonMPI run
    MPI_Abort()
    pyMPI_Delete_all()
    # wait for the filesystem update
    pyMPI_Sleep(2.0)

    # Launch PythonMPI
    py_file_basename = py_file
    py_file = py_file+'.py'
    cmd = MPI_Run( py_file, n_proc, machines )

    # Determine how many times to do checks.
    n_check = round(time_limit / time_check)

    # Check status.
    searchStr = 'SUCCESS'
    # myfileStr = os.getcwd()+'/PythonMPI/'+py_file_basename+'*.out'
    myfileStr = '.'+os.sep+'PythonMPI'+os.sep+py_file_basename+'*.out'

    # wait for the output files to become visiable
    pyMPI_Sleep(time_check*2.)

    file_list = glob(myfileStr)
    loop = 0
    while(len(file_list) == 0):
        pyMPI_Sleep(1.0)
        file_list = glob(myfileStr)
        if (loop>10):
            raise Exception('Failed to find the output, %s'%(myfileStr))
        loop += 1
    # print(file_list)
    i_check = 1
    keep_checking = 1
    for i in range(n_check):
        # Flush buffers.
        # unix(' ');
        # Check to see how many are done.
        n_done,file_names = findString(searchStr,file_list)
        print('%d seconds, Completed: %d'%(int(time_check)*(i+1),n_done))
        if n_done == n_proc:
            status = 'SUCCESS'
            print('%s: SUCCESS'%(py_file))
            print(' ')
            # pyMPI_Delete_all()
            # pyMPI_Sleep(1.0)
            return status
        # wait for the next check
        pyMPI_Sleep(time_check)

    status = 'FAIL'
    print('%s: FAIL'%(py_file))
    print(' ')
    MPI_Abort()
    pyMPI_Delete_all
    pyMPI_Sleep(1.0)
    return status


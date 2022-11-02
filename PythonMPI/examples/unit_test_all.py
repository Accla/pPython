"""Script that calls all the unit tests.
    To run:
 
    (1) Make sure your settings in pyMPI_Comm_settings.py
        are correct for your system.
 
    (2) Make sure the machines listed in 'cpus' are
        are correct for your system
 
    (3) Launch the test with Python 3.x,  'python unit_test_all.py'
 
                            
    VERY VERY VERY IMPORTANT  
                            
    If the HOST is the first machine in your
    machines list, you must run it in the
    background, i.e.
    cpus = {'host&' 'machine2' ... }

    Change list of cpus to suit your environment.
    cpus = {'SLAVE&:pc'};
    cpus = {'SLAVE&:pc:C:\Documents and Settings\kepner\tmp'}

    Unix
    cpus = {'hagar&','buddy'};

    Change list of cpus to suit your environment.
    cpus = {'node-a&:/gigabit/node-a/kepner' ...
         'node-b:/gigabit/node-b/kepner' ...
         'node-c:/gigabit/node-c/kepner' ...
         'node-d:/gigabit/node-d/kepner' ...
         'node-e:/gigabit/node-e/kepner' ...
         'node-f:/gigabit/node-f/kepner' ...
         'node-g:/gigabit/node-g/kepner' ...
         'node-h:/gigabit/node-h/kepner'};
"""

import os
import sys

#
# Modify the following variables according to your runtime environment
#
# Machines list (dtype: list)
cpus = ['a-15-0.llgrid.ll.mit.edu','a-15-1.llgrid.ll.mit.edu']
# Export the path to find PythonMPI source code:
# For Linux OS
HOME_PATH="/home/gridsan/ch21778"
# For Windows OS
HOME_PATH="Z:"
LLSC_PYTHONMPI_PATH = HOME_PATH+os.sep+"devtools"+os.sep+"git"+os.sep+"PythonMPI"+os.sep+"src"
# Export the path to modify PythonMPI settings for an individual user
LOCAL_PYTHONMPI_CONFIG_PATH = HOME_PATH+os.sep+"pythonmpi"

# Add the current working directory to the system path
# so that any Python codes in the current working directory
# can be called
CWD_PATH = os.getcwd()

sys.path.append(LLSC_PYTHONMPI_PATH)
sys.path.append(LOCAL_PYTHONMPI_CONFIG_PATH)
sys.path.append(CWD_PATH)

from unit_test import *
import checkOS as OS

# For PC, use ;, For Mac & Linux, use :
if OS.ispc:
    sep_path = ";"
else:
    sep_path = ':'
PYTHONMPI_PATH = LLSC_PYTHONMPI_PATH+sep_path+LOCAL_PYTHONMPI_CONFIG_PATH+sep_path+CWD_PATH
os.environ["PYTHONMPI_PATH"] = PYTHONMPI_PATH

# Disable HDF5 file locking
os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

# Set initial status.
all_status = 'SUCCESS';

# Unit test all the scripts.

status = unit_test('basic', 4, cpus, 200, 20)
if status == 'FAIL':
    all_status = 'FAIL';

status = unit_test('xbasic', 4, cpus, 200, 20)
if status == 'FAIL':
    all_status = 'FAIL';

status = unit_test('broadcast', 4, cpus, 200, 20)
if status == 'FAIL':
    all_status = 'FAIL';

status = unit_test('basic_app', 4, cpus, 200, 20)
if status == 'FAIL':
    all_status = 'FAIL';

status = unit_test('basic_app2', 4, cpus, 200, 20)
if status == 'FAIL':
    all_status = 'FAIL';

status = unit_test('basic_app3', 4, cpus, 200, 20)
if status == 'FAIL':
    all_status = 'FAIL';

status = unit_test('basic_app4', 4, cpus, 200, 20)
if status == 'FAIL':
    all_status = 'FAIL';

status = unit_test('basic_app5', 4, cpus, 200, 20)
if status == 'FAIL':
    all_status = 'FAIL';

status = unit_test('basic_app6', 4, cpus, 200, 20)
if status == 'FAIL':
    all_status = 'FAIL';

status = unit_test('probe', 2, cpus, 200, 20)
if status == 'FAIL':
    all_status = 'FAIL';

status = unit_test('speedtest', 2, cpus, 200, 20)
if status == 'FAIL':
    all_status = 'FAIL';

status = unit_test('blurimage', 4, cpus, 200, 20)
if status == 'FAIL':
    all_status = 'FAIL';

print('All tests: %s'%(all_status))


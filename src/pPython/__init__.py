"""
    Add system search paths for all the pPython files
    and define initial parameters necessary for pPython.
"""
import os
import sys

base_dir_path = os.path.dirname(os.path.abspath(__file__))
os.environ['PPYTHON_HOME'] = base_dir_path

sys.path.append(base_dir_path+os.sep+'src')
sys.path.append(base_dir_path+os.sep+'src'+os.sep+'map')
sys.path.append(base_dir_path+os.sep+'src'+os.sep+'dmat')
sys.path.append(base_dir_path+os.sep+'grid')
sys.path.append(base_dir_path+os.sep+'PythonMPI'+os.sep+'src')


"""
pPython initialization.

Adds system search paths for all pPython files and defines the initial
parameters necessary for pPython.
"""

import os
import sys

DEBUG = 0

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

# Set pPython HOME path environment
BASE_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
os.environ['PPYTHON_HOME'] = BASE_DIR_PATH

# Set pPython runtime paths
_SUBDIRS = [
    ('src',),
    ('src', 'map'),
    ('src', 'dmat'),
    ('sched',),
    ('PythonMPI', 'src'),
]
for subdir in _SUBDIRS:
    sys.path.append(os.path.join(BASE_DIR_PATH, *subdir))

# --------------------------------------------------------------------------
# MPI environment
# --------------------------------------------------------------------------

# Share pPython environment variables
import pyMPI_COMM_WORLD as pyMCW  # noqa: E402  (sys.path set above)

# Define MPI_COMM_WORLD dictionary if not defined
comm = globals().get('comm')
if comm is None:
    comm = pyMCW.MPI_COMM_WORLD
    if not isinstance(comm, dict):
        comm = {'rank': 0}

Np = globals().get('Np', 1)
Pid = globals().get('Pid', 0)

# --------------------------------------------------------------------------
# GPU setup
# --------------------------------------------------------------------------

# Check GPU availability based on CUDA_VISIBLE_DEVICES
cuda_visible_devices = os.getenv('CUDA_VISIBLE_DEVICES', '')
use_gpu = cuda_visible_devices != ''

gpu_device = None
if use_gpu:
    import cupy as cp  # noqa: E402
    # Only a single GPU is visible to the process due to GPU binding,
    # and Pid is always 0 at this stage, so this effectively selects
    # the (single) visible device.
    gpu_device = cp.cuda.Device(Pid % cp.cuda.runtime.getDeviceCount())

if DEBUG:
    print(f'pPython **init**: use_gpu = {use_gpu}')
    print(f'pPython **init**: CUDA_VISIBLE_DEVICES = {cuda_visible_devices}')
    print('pPython:')
    print(f'sys.path: {sys.path}')
    print(f'comm: {comm}')
    print(f'Np = {Np}, Pid = {Pid}')
    print(f'gpu_device: {gpu_device}')

########################################################
# pPython: Parallel Python Programming Tool
# Python extension: Dr. Chansup Byun (cbyun@ll.mit.edu)
# Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
# Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
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


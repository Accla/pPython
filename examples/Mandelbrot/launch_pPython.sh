#!/bin/bash

source /etc/profile
#
# Currently using LLSC provided Python environment.
# Replace with your own Python environment if needed.
module load conda/Python-ML-2025b-pytorch

# Display the job submission command 
export PPYTHON_DEBUG=YES

# Uncomment the following 2 lines to enable GPU resources
# export GPU=1
# export PPYTHON_GPU_BINDING=yes
#
# Uncomment the following 2 lines to use TF32 with CuPy for GPU 
# export CUPY_TF32=1
# export CUPY_ACCELERATORS=cub,cutensor

# Use the default partition (xeon-p8 48 core compute nodes)
python -c "import pPython; from pRUN import pRUN; pRUN('pMandelbrot.py',[1,1,48],'grid&'); exit()"


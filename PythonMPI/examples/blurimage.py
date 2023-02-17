"""blurimage.py
    This script implements a basic image convolution
    across multiple processors.
    To run, start Matlab and type:

        MPI_Run('blurimage',2,{})

    Or, to run a different machine type:

        MPI_Run('blurimage',2,{'machine1' 'machine2'})

    Output will be piped into to

        PythonMPI/blurimage.0.out
        PythonMPI/blurimage.1.out
        ...

    Auxilary files: synch_start.py,conv2.py

    PythonMPI
    Dr. Chansup Byun
    MatlabMPI
    Dr. Jeremy Kepner
    MIT Lincoln Laboratoy
    {cbyun,kepner}@ll.mit.edu
"""

import numpy as np
from time import time

from PythonMPI import *
from conv2 import *
from synch_start import *

# Initialize MPI
MPI_Init()

# Create communicator. (pyMCW is imported in PythonMPI.py)
comm = pyMCW.MPI_COMM_WORLD

# Modify common directory from default for better performance.
# (Use only when all MPI processes are on the same node)
# comm = pyMPI_Comm_dir(comm,'/tmp')

# Get size and rank.
comm_size = MPI_Comm_size(comm)
my_rank = MPI_Comm_rank(comm)

# Print rank.
print('my_rank: %d'%(my_rank))

# Do a synchronized start.
starter_rank = 0
# delay in Seconds
delay = 30
synch_start(comm,starter_rank,delay)

# Set image size (use powers of 2).
n_image_x = 2**17
n_image_x = 2**2
n_image_x = 2**(10+1)*comm_size

n_image_y = 2**10

# Number of points to put in each sub-image.
n_point = 100

# Set filter size (use powers of 2).
n_filter_x = 2**5
n_filter_y = 2**5

# Set the number of times to filter.
n_trial = 2

# Computer number of operations.
total_ops = 2*n_trial*n_filter_x*n_filter_y*n_image_x*n_image_y

if (n_image_x%comm_size):
    raise Exception('ERROR: processors need to evenly divide image')

# Set who is source and who is destination.
left = my_rank - 1
if (left < 0):
  left = comm_size - 1

right = my_rank + 1
if (right >= comm_size):
  right = 0

# Create a unique tag id for this message (very important in Python MPI!).
tag = 1

# Create timing matrices.
# start_time = np.zeros(n_trial)
# end_time = start_time

# Get a zero clock.
zero_clock = time()

# Compute sub_images for each processor.
n_sub_image_x = n_image_x/comm_size
n_sub_image_y = n_image_y

# Create starting image and working images..
sub_image0 = np.power(np.random.rand(int(n_sub_image_x),int(n_sub_image_y)),10)
sub_image = sub_image0
work_image = np.zeros([int(n_sub_image_x+n_filter_x),int(n_sub_image_y+n_filter_y)])


# Create kernel.
x_shape = np.power(np.sin(np.pi*np.arange(n_filter_x)/(n_filter_x-1)),2)
y_shape = np.power(np.sin(np.pi*np.arange(n_filter_y)/(n_filter_y-1)),2)
kernel = x_shape.reshape(-1,1)*y_shape

# Create box indices. 
# Note that starting index is 0
lboxw = np.array(np.int32([0,n_filter_x/2,0,n_sub_image_y]))
cboxw = np.array(np.int32([n_filter_x/2,n_filter_x/2+n_sub_image_x,0,n_sub_image_y]))
rboxw = np.array(np.int32([n_filter_x/2+n_sub_image_x,n_sub_image_x+n_filter_x,0,n_sub_image_y]))

lboxi = np.array(np.int32([0,n_filter_x/2,0,n_sub_image_y]))
rboxi = np.array(np.int32([n_sub_image_x-n_filter_x/2,n_sub_image_x,0,n_sub_image_y]))


# Set start time.
start_time = time()


# Loop over each trial.
for i_trial in range(n_trial):
    # i_trial start from zero to n_trial-1 in Python

    # Copy center sub_image into work_image.
    # Note that the range operator (:) does not include the last one in python.
    work_image[cboxw[0]:cboxw[1],cboxw[2]:cboxw[3]] = sub_image

    if (comm_size > 1):
        # Create message tag.
        ltag = 2*i_trial
        rtag = 2*i_trial+1

        # Send left sub-image.
        l_sub_image = sub_image[lboxi[0]:lboxi[1],lboxi[2]:lboxi[3]]
        MPI_Send(  left, ltag, comm, l_sub_image )

        # Receive right padding.
        [r_pad] = MPI_Recv( right, ltag, comm )
        work_image[rboxw[0]:rboxw[1],rboxw[2]:rboxw[3]] = r_pad

        # Send right sub-image.
        r_sub_image = sub_image[rboxi[0]:rboxi[1],rboxi[2]:rboxi[3]]
        MPI_Send( right, rtag, comm, r_sub_image )

        # Receive left padding.
        [l_pad] = MPI_Recv( left, rtag, comm )
        work_image[lboxw[0]:lboxw[1],lboxw[2]:lboxw[3]] = l_pad

    # Compute convolution.
    work_image = conv2(work_image,kernel,'same')

    # Extract sub_image.
    sub_image = work_image[cboxw[0]:cboxw[1],cboxw[2]:cboxw[3]]

# Get end time for the this message.
end_time = time()

# Print the results.
total_time = end_time - start_time

# Print compute performance.
# total_ops
gigaflops = total_ops / total_time / 1.e9
print('GigaFlops:  %f'%(gigaflops))


# Write data to a file.
outfile = 'blurimage.'+str(my_rank)+'.pkl'
with open(outfile,'wb') as f:
    pickle.dump([start_time,end_time,total_time,kernel], f)

# Finalize Matlab MPI.
print('SUCCESS')
MPI_Finalize()

"""
 Copyright 2002 Massachusetts Institute of Technology
 
 Permission is herby granted, without payment, to copy, modify, display
 and distribute this software and its documentation, if any, for any
 purpose, provided that the above copyright notices and the following
 three paragraphs appear in all copies of this software.  Use of this
 software constitutes acceptance of these terms and conditions.

 IN NO EVENT SHALL MIT BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
 SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
 THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF MIT HAS BEEN ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
 
 MIT SPECIFICALLY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES INCLUDING,
 BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

 THIS SOFTWARE IS PROVIDED "AS IS," MIT HAS NO OBLIGATION TO PROVIDE
 MAINTENANCE, SUPPORT, UPDATE, ENHANCEMENTS, OR MODIFICATIONS.
"""

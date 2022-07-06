########################################################
# Serial version adapted to Octave
########################################################

import numpy as np
from scipy.signal import convolve
from timeit import default_timer as timer
import matplotlib.pyplot as plt

from zeros import *
from global_ind import *

UseGraphics = 1

# Check answer with an identical serial calculation.
CHECK = 0  # Can be 1 or 0.  OK to change.

# Scale image by number of cpus size (use powers of 2).
n_image_x = 2**10
n_image_y = 2**10

# Number of points to put in each sub-image.
n_point = 100

# Set filter size (use powers of 2).
n_filter_x = 2**5
n_filter_y = 2**5

# Create maps
mapImOv = 1

# Set the number of times to filter.
n_trial = 2

# Compute number of operations.
total_ops = 2.*n_trial*n_filter_x*n_filter_y*n_image_x*n_image_y 

# Create timing matrices.
start_time = np.zeros(n_trial) 
end_time = np.zeros(n_trial) 

# Get a zero clock.
zero_clock = timer()

# Create starting image and working images..
if (CHECK):
    im = np.zeros(n_image_x,n_image_y)

# Create a distributed matrix on individual rank
imOv = zeros(n_image_x,n_image_y,map=mapImOv) 

# Get local indices.
[myI,myJ] = global_ind(imOv) 

# Assign values to image.
# Add one to compensate the starting index, zero
# myI = myI + 1
# myJ = myJ + 1
imOv = (np.array([myI])+1).T * np.ones([len(myJ)]) + np.ones((1,len(myI))).T * (np.array([myJ])+1)

if (CHECK):
    im = (np.array([list(range(int(n_image_x)))])+1).T  * np.ones((1,n_image_y)) + \
    np.ones((1,n_image_x)).T * (np.array([list(range(int(n_image_y)))])+1)

# Create kernel.
# x_shape = sin(pi.*(0:(n_filter_x-1))./(n_filter_x-1)).^2 
# y_shape = sin(pi.*(0:(n_filter_y-1))./(n_filter_y-1)).^2 
# kernel = (x_shape.')*y_shape 
kernel = np.ones((n_filter_x,n_filter_y))/(n_filter_x*n_filter_y) 

# Set start time.
start_time = timer() 

# Loop over each trial.
for i_trial in range(n_trial):

    imOv[0:-n_filter_x+1,0:-n_filter_y+1] = convolve(imOv,kernel,'valid')

    if (CHECK):
        im[0:-n_filter_x+1,0:-n_filter_y+1] = convolve(im,kernel,'valid')

# Compare results
if (CHECK):
    max_difference = max(max(abs(local(imOv) - im[myI[0]:myI[-1],myJ[0]:myJ[-1]])))
    # imagesc(local(imOv) - im(myI,myJ))

# Get end time for the this message.
end_time = timer() 

# Print the results.
total_time = end_time - start_time

if UseGraphics:
    # Show output in a figure
    plt.imshow(imOv, origin = 'lower',  extent = [0, 10, 0, 10])
    plt.savefig('imOv_serial.png')

# Print compute performance.
# total_ops 
gigaflops = total_ops / total_time / 1.e9 
print('GigaFlops: %f'%(gigaflops))

# Don't exist if we are the host.
print('SUCCESS') 



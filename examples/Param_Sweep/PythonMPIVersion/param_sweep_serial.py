import numpy as np

from sample_function import *

"""Basic parameter sweep code (serial)"""

# Set data sizes.
m = 3   #  number of output arguments
n = 16  #  number of independent iterations

# Create z data output matrix.
z = np.zeros((n, m), dtype=float);

# Loop over the local indices	
for ii in range(n):
    # Calculate another argument
    my_other_arg = 2.5 * ii

    # call a function with the index, and other arguments, and 
    # store the result in a row
    z[ii, :] = sample_function(ii, 0, my_other_arg)

# Finalize the program
print('SUCCESS')

# Finally, display the resulting matrix on the leader
print(z)

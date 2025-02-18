import numpy as np

def reference_frame(n,a,b):
    """
    input:
    n: image size
    a:
    b:
    
    output:
    refFrame: A reference frame of size, nxn
    """
    
    DEBUG = 1
    if DEBUG: 
        print('--> Entering reference_frame')
        
    # Create axis.
    x_axis = np.linspace(-1,1,n)
    y_axis = np.linspace(-1,1,n)
    nx = len(x_axis)
    
    # Create x and y.
    [x,y] = np.meshgrid(x_axis,y_axis,indexing='xy')
    rt2 = 2.**0.5
    
    # Create Reference frame.
    # refFrame = (y > x - rt2*a).any() and (y < x + rt2*a).any() and (y < rt2*b - x).any() and (y > -rt2*b - x).any()
    ref1 = (y > x - rt2*a)
    ref2 = (y < x + rt2*a)
    ref3 = (y < rt2*b - x)
    ref4 = (y > -rt2*b - x)
    refFrame = np.logical_and.reduce((ref1, ref2, ref3, ref4))
    # Add some noise (shouldn't add noise).
    # Extracting integer from tuple, b: *b       
    refFrame = refFrame + 0.1*(np.random.rand(*(refFrame.shape)) - 0.5)       
                      
    if DEBUG: 
        print('reference_frame: generated reference frame of size, %s'%(str(refFrame.shape)))
        print('<-- Exiting reference_frame')

    return refFrame          


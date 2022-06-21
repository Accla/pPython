from math import ceil,pi
from scipy.signal import convolve

from zeros import *

from imdown import *

def zoom_frames(refFrame,scaleFactor,blurSigma):
    """
    ZOOMFRAMES:  Zooms in on a reference frame.
    Usage: zoomedFrames =zoom_frames(refFrame,scaleFactor,blurSigma)
    
    Input parameters are as follows:
    refFrames  = reference image.
    scaleFactor= vector of zoome scale factors.
    blurSigma  = standard deviation of blur kernel (in pixels)
    
    Output variables are as follows:
    zoomeFrames = 3D array of output images.
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering zoom_frames')
    
    # Linear dimension of cropping window  (pixels)
    windowSize = size(refFrame)
    windowSize = windowSize[0]
    
    # Allocate output frames.
    zoomedFrames = zeros(windowSize,windowSize,len(scaleFactor))
    if DEBUG:
        print('len(scaleFactor)')
        print(len(scaleFactor))
        print('zoomedFrames.shape')
        print(zoomedFrames.shape)
    
    # Estimate frames at selected ranges.
    for i in range(len(scaleFactor)):
    
        # Generate point spread function.
        # Pre-selected to be 5-sigma.
        nelem = ceil(scaleFactor[i]*(5*blurSigma))
        if nelem%2 == 0:
            # Make odd.
            nelem = nelem+1

        # Create gaussian kernel.
        x = np.arange(nelem).reshape(1,nelem) - (nelem-1)/2
        o = np.ones((1,nelem))
        r2 = (np.dot(x.T , o)**2 + np.dot(o.T , x)**2)
        h = (1/np.sqrt(2*pi*blurSigma))*np.exp(r2/blurSigma**2)
    
        # Calculate blurred image (at requested range).
        blurFrame = convolve(h,refFrame,mode='full', method='auto')
        if DEBUG and (i==0):
            print('refFrame')
            print(refFrame)
            print('blurFrame')
            print(blurFrame)
    
        # Simulate sampled image at requested range.

        zoomedFrames[:,:,i] = imdown(blurFrame,windowSize,scaleFactor[i])
    
    if DEBUG:
        print('<-- Exiting zoom_frames')
    
    return zoomedFrames


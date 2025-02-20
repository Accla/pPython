from math import ceil,pi
from scipy.signal import convolve
import warnings
import sys

import numpy as np
from scipy.interpolate import interp2d, RegularGridInterpolator

from size import *
from zeros import *

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

    # Supress overflow warning in np.exp()
    warnings.filterwarnings('ignore')

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
        factor = int(scaleFactor[i])
        nelem = ceil(scaleFactor[i]*(5*blurSigma))
        if nelem%2 == 0:
            # Make odd.
            nelem = nelem+1

        # Create gaussian kernel.
        x = np.arange(nelem).reshape(1,nelem) - (nelem-1)/2
        o = np.ones((1,nelem))
        if DEBUG:
            print('... Loop index: %d, Nelem = %d'%(i,nelem))
            filename = 'r2-nelem-'+str(nelem)+'.npy'
        r2 = (np.dot(x.T , o)**2 + np.dot(o.T , x)**2)
        if DEBUG:
            filename = 'r2-nelem-'+str(nelem)+'.npy'
            exp_arg = r2/blurSigma**2
            np.save(filename,exp_arg)
        try:
            h = (1/np.sqrt(2*pi*blurSigma))*np.exp(r2/blurSigma**2)
        except OverflowError as err:
            print('Overflow occur at loop index: %d'%(i))
            if DEBUG:
                print('blurSigma')
                print(blurSigma)
                print('r2')
                print(r2)
    
        # Calculate blurred image (at requested range).
        blurFrame = convolve(h,refFrame,mode='full', method='auto')
        if DEBUG and (i==0):
            print('refFrame')
            print(refFrame)
            print('blurFrame')
            print(blurFrame)
    
        # Simulate sampled image at requested range.
        if DEBUG:
            print('sys.path = ',end=''); print(sys.path)
        zoomedFrames[:,:,i] = imdown(blurFrame,windowSize,scaleFactor[i])
    
    if DEBUG:
        print('<-- Exiting zoom_frames')
    
    return zoomedFrames


def imdown(I,res,alpha):
    """
    # IMDOWN Resamples a grayscale image.
    #    DOWNIMG = IMDOWN(I,R,A) Resamples the input
    #    image I using bilinear interpolation using a sampling
    #    lattice with R point samples at A times the original
    #    sample spacing.  Extrapolated values are set to zero.
    """

    #MATLAB: Vq = interp2(V,Xq,Yq) assumes X=1:N and Y=1:M where [M,N]=SIZE(V).
    #Python:
    [npix,npiy] = size(I)
    X = np.array(range(1,npix+1))
    Y = np.array(range(1,npiy+1))
    # deprecated
    # f  = interp2d(X, Y, I.astype(float), kind='linear')
    interp = RegularGridInterpolator((X, Y), I.astype(float), bounds_error=False, fill_value=None)
   
    # Create the down-sampling lattice.
    x = alpha*(np.array(range(1,res+1))-((res+1)/2))+((res+1)/2)+(npix-res)/2
    y = alpha*(np.array(range(1,res+1))-((res+1)/2))+((res+1)/2)+(npix-res)/2
    [XI,YI] = np.meshgrid(x,y,indexing='xy')

    # Down-sample the input grayscale image.
    # downimg = interp2(im2double(I),XI,YI,'bilinear')
    # downimg = interp2(double(I),XI,YI,'bilinear')
    # downimg = interp2(double(I),XI,YI,'linear')
    # Interpret at the mesh points
    downimg = interp((XI, YI))
    downimg[np.argwhere(np.isnan(downimg))] = 0
 
    return downimg


"""
This includes the basic utilities and helper functions for pre-processing the EEG data"""

import numpy
from numpy import fft as fft



def apply_hamming_window(data, samples):
    window=numpy.hamming(samples)
    data=data*window
    return data

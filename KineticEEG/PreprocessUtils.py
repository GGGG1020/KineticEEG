"""
This includes the basic utilities and helper functions for pre-processing the EEG data"""

import numpy
from numpy import fft as fft
import math
def apply_hamming_window(data, samples):
    window=numpy.hamming(samples)
    data=data*window
    return data
def get_magnitude(complex_num):
    magnitude=math.sqrt(complex_num.real*complex_num.real+complex_num.imag*complex_num.imag)
    return magnitude


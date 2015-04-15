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
def basic_window(data):
    lendata=len(data)
    g=lendata/128
    x=numpy.linspace(0,g,lendata)
    A=numpy.sin(numpy.pi*x/g)*numpy.sin(numpy.pi*x/g)
    data=A.T*data
    return data
    

	

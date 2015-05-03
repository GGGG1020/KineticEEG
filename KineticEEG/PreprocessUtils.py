"""
This includes the basic utilities and helper functions for pre-processing the EEG data"""

import numpy
from numpy import fft as fft
import math
import scipy.signal
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
def butter_highpass_filter(data, cutoff, samplingfreq, order):
    nyq=0.5*samplingfreq
    norm_cutoff=cutoff/nyq
    b,a = scipy.signal.butter(order, norm_cutoff,'highpass')
    filtereddat=scipy.signal.lfilter(b,a,data)
    return filtereddat
def get_alpha_beta_pow(data):
	"""Do NOT use:This is experimental!"""
    fftedddat=fft.fft(data)
    maggedfft=abs(fftedddat)
    powedfft=numpy.square(maggedfft)
    
    
def bin_power(X,Band,Fs):
    C = fft.fft(X)
    #C = abs(C)
    newc=list()
    for i in C:
        newc.append(i*i.conjugate())
    C=numpy.array(newc)
    
    #numpy.square(C)
    Power =numpy.zeros(len(Band)-1);
    for Freq_Index in range(0,len(Band)-1):
            Freq = float(Band[Freq_Index])										
            Next_Freq = float(Band[Freq_Index+1])
            Power[Freq_Index] = sum(C[numpy.floor(Freq/Fs*len(X)):numpy.floor(Next_Freq/Fs*len(X))])
    Power_Ratio = Power/sum(Power)
    return Power, Power_Ratio	


	

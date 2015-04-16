import PreprocessUtils
import math
import numpy
""""
Specification for DataProcessor
------------------------------

The arrays taken in are of the following format:

[AF3, F7, F3, FC5, T7, P7, O1,O2,P8,T8, FC6, F4,AF4]

The array for the each contains the uV data."""

class DataProcessor:
    """This does all the data processing in it's stages:
    High Pass Filter(0.16Hz.)->Windowing Function->FFT->Convert to Power for Bands"""
    def __init__(self, arrays

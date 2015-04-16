import PreprocessUtils
import math
import numpy



class DataProcessor:
    """This does all the data processing in it's stages:
    High Pass Filter(0.16Hz.)->Windowing Function->FFT->Convert to Power for Bands"""

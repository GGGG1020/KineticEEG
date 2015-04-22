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
    def __init__(self, arrays):
        self.data_dict={"AF3":arrays[0], "F7":arrays[1],"F3":arrays[2],"FC5":arrays[3],"T7":arrays[4],"P7":arrays[5],"O1":arrays[6],"O2":arrays[7],"P8":arrays[8],"T8":arrays[9],"FC6":arrays[10],"F4":arrays[11],"AF4":arrays[12]}
    def do_high_pass(self):
        for item in self.data_dict.keys():
            self.data_dict[item]=PreprocessUtils.butter_highpass_filter(self.data_dict[item],0.16,128,5)
    def do_hanning_wndow(self):
        for item in self.data_dict.keys():
            self.data_dict[item]=PreprocessUtils.do_basic_window(self.data_dict[item])
    def do_bin_power(self):
        for item in self.data_dict.keys():
            self.data_dict[item]=PreprocessUtils.bin_power(self.data_dict[item], [1,4,7,13,30], 128)

            
        
        
        

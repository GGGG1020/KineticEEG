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
    sensors=['AF3','F7','F3', 'FC5', 'T7', 'P7', 'O1', 'O2','P8', 'T8', 'FC6', 'F4','F8', 'AF4']
    def __init__(self):
        self.data_dict=dict()
    def do_high_pass(self):
        for item in self.data_dict.keys():
            self.data_dict[item]=PreprocessUtils.butter_highpass_filter(self.data_dict[item],0.16,128,5)
    def do_hanning_wndow(self):
        for item in self.data_dict.keys():
            self.data_dict[item]=PreprocessUtils.basic_window(self.data_dict[item])
    def do_bin_power(self):
        for item in self.data_dict.keys():
            self.data_dict[item]=PreprocessUtils.bin_power(self.data_dict[item], [1,4,7,13,30], 128)
    def update_data(self, dictofdat):
        self.data_dict.clear()
        self.data_dict=dictofdat            
        
        
        

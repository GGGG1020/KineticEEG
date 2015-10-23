"""Plot Utility:
This program helps plot fft values"""

import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/KineticEEG")
import CSVProc
import matplotlib.pyplot as plt

class FFTPlot:
    def __init__(self, csvextract):
        a=CSVProc(csvextract)
        important=a.get_with_settings(["F3", "F4", "FC5", "FC6"], ["Mu"])

    def plot
        
        

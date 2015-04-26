import matplotlib
import os.path
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/Tools")
import CSV_Extractor
import Preprocessers
import PreprocessUtils
"""CSV_Viewer
Written by Gaurav Ghosal as a tool for KineticEEG
______________________________
This is a commandline program to help view and fft the csv files"""
"""USAGE:
_______________________
python CSV_Viewer.py path_to_csv.csv step ymin ymax

DESCRIPTION OF ARGUMENTS
___________________________
path_to_csv is the path to the csv that you want to display

step is the number of elapsed samples between ffts()

ymin is the minimum y value on the graph

ymax is the maximum y value on the graph"""
def animated_barplot(file,step):
    # http://www.scipy.org/Cookbook/Matplotlib/Animations
    a=CSV_Extractor.CSVExtractor(file)
    b=a.get_data_from_sensor("FC5", 8192)
    chunk0=0
    chunk1=1024
    rects = plt.bar(range(1), 0,  align = 'center')
    for i in range(4096):
        dat=b[chunk0:chunk1]
        r=PreprocessUtils.butter_highpass_filter(dat,0.16,128,5)
        c=PreprocessUtils.basic_window(r)
        er=PreprocessUtils.bin_power(c, [1,4,7,13,30], 128)
        for rect in rects:
            print(er[1][0])
            rect.set_height(er[1][0])
        chunk0+=step
        chunk1+=step
        fig.canvas.draw()
file=sys.argv[1]
if not os.path.exists(file):
    print("""CSV_Viewer
Written by Gaurav Ghosal as a tool for KineticEEG
______________________________
This is a commandline program to help view and fft the csv files""")
    print("""USAGE:
_______________________
python CSV_Viewer.py path_to_csv.csv step ymin ymax

DESCRIPTION OF ARGUMENTS
___________________________
path_to_csv is the path to the csv that you want to display

step is the number of elapsed samples between ffts()

ymin is the minimum y value on the graph

ymax is the maximum y value on the graph""")
    exit()
step=int(sys.argv[2])
ymin=int(sys.argv[3])
ymax=int(sys.argv[4])
print(sys.argv[1])
fig = plt.figure()
plt.xlim(0,9)
plt.ylim(ymin, ymax)
win = fig.canvas.manager.window
plt.ion()
win.after(100, lambda:animated_barplot(file,step))
plt.show()



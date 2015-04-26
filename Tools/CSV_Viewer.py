import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/Tools")
import CSV_Extractor
import Preprocessers
import PreprocessUtils
"""This is a command line app to view fft"""
def animated_barplot(file):
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
        chunk0+=1
        chunk1+=1
        fig.canvas.draw()
file=sys.argv[1]
print(sys.argv[1])
fig = plt.figure()
plt.xlim(0,9)
plt.ylim(0, 2)
win = fig.canvas.manager.window
plt.ion()
win.after(100, lambda:animated_barplot(file))
plt.show()


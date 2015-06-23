import matplotlib
import os.path
import time
#matplotlib.use('TKAgg')
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
def animated_barplot(file,step,how_muc,size):
    # http://www.scipy.org/Cookbook/Matplotlib/Animations
    print("l")
    a=CSV_Extractor.CSVExtractor(file)
    b=a.get_data_from_sensor("FC5", how_much)
    chunk0=0
    chunk1=size
    print("G")
    rects = plt.bar(range(1), 0,  align = 'center')
    rect1=plt.bar(2, 0,  align = 'center')
    rect2=plt.bar(3, 0,  align = 'center')
    rect3=plt.bar(4, 0,  align = 'center')
    print(len(b)/128)
    for i in range(int(len(b)/step)):
        dat=b[chunk0:chunk1]
        r=PreprocessUtils.butter_highpass_filter(dat,0.16,128,5)
        c=PreprocessUtils.basic_window(r)
        #print((len(c),i))
        er=PreprocessUtils.bin_power(c, [1,4,7,13,30], 128)
        j.append(er[1][0])
        for rect in rects:
            #print(er[1][0])
            rect.set_height(er[1][0])
        for rect in rect1:
            rect.set_height(er[1][1])
        for rect in rect2:
            rect.set_height(er[1][2])
        for rect in rect3:
            rect.set_height(er[1][3])
        chunk0+=step
        chunk1+=step
        fig.canvas.draw()
        time.sleep(0.0625)

def rollingbarplot(file, step, size,sensor):
    a=CSV_Extractor.CSVExtractor(file)
    proc=Preprocessers.DataProcessor()
    temproc=Preprocessers.DataProcessor()
    rects = plt.bar(range(1), 0,  align = 'center')
    rect1=plt.bar(2, 0,  align = 'center')
    rect2=plt.bar(3, 0,  align = 'center')
    rect3=plt.bar(4, 0,  align = 'center')
    tree={'F3': [], 'FC5': [], 'T7': [], 'F7': [], 'P7': [], 'P8': [], 'AF4': [], 'O2': [], 'O1': [], 'T8': [], 'AF3': [], 'FC6': [], 'F4': [], 'F8': []}
    step=False
    binnedstuff=dict()
    while not len(tree["F3"])==size:
        for i in a.sensor2column:
            fed=a.get128more(i)
            fed={i:fed}
            PreprocessUtils.
            temproc.update_data(fed)
            temproc.do_high_pass()
            fed=temproc.data_dict
            tree[i]+=fed
    while True:
        if len(tree[0])==size:
                #Now it is time to actually do the calculations
            proc.update_data(tree)
            proc.do_hann_wndow()
            proc.do_bin_power()
            binnedstuff=proc.data_dict
            interestingbinnedstuff=proc.data_dict[sensor][1]
        else:break
        for rect in rects:
            #print(er[1][0])
            rect.set_height(interestingbinnedstuff[0])
        for rect in rect1:
            rect.set_height(interestingbinnedstuff[1])
        for rect in rect2:
            rect.set_height(interestingbinnedstuff[2])
        for rect in rect3:
            rect.set_height(interestingbinnedstuff[3])
        for i in tree:
            del tree[i][0:16]            
        time.sleep(16/128)
        for i in tree:
            tree[i]+=a.get16more(i)
            
            
            
        
   
            
#run 8 times per second            
            

file=sys.argv[1]
if not os.path.exists(file):
    print("""CSV_Viewer
Written by Gaurav Ghosal as a tool for KineticEEG
______________________________
This is a commandline program to help view and fft the csv files""")
    print("""USAGE:
______________________
python CSV_Viewer.py path_to_csv.csv step ymin ymax tofetch
DESCRIPTION OF ARGUMENTS
___________________________
path_to_csv is the path to the csv that you want to display
step is the number of elapsed samples between ffts()
ymin is the minimum y value on the graph
ymax is the maximum y value on the graph
tofetch is how much data to get
size is size of fft""")
    exit()
step=int(sys.argv[2])
ymin=int(sys.argv[3])
ymax=int(sys.argv[4])
how_much=int(sys.argv[5])
size=int(sys.argv[6])
sensor=str(sys.argv[7])
print(sys.argv[1])
fig = plt.figure()
plt.xlim(0,9)
plt.ylim(ymin, ymax)
win = fig.canvas.manager.window
plt.ion()
j=list()
print("Hi")
#Program isn't making it here
win.after(0, lambda:rollingbarplot(file,step,size, sensor))

plt.show()


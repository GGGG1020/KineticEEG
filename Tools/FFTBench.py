#better plotter.py
import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/KineticEEG","C:/Users/Gaurav/Documents/GitHub/KineticEEG/Tools")
import PreprocessUtils
#matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy
import CSV_Extractor
#Cleaner, better version
FFT_SIZE=1024
STEP_SIZE=16
def bplot(file, sensor):
    a=CSV_Extractor.CSV_Extractor(file)
    rects = plt.bar(range(1), 0,  align = 'center')
    rect1=plt.bar(2, 0,  align = 'center')
    rect2=plt.bar(3, 0,  align = 'center')
    rect3=plt.bar(4, 0,  align = 'center')
    tree=list()
    while not len(tree)==FFT_SIZE:
       stuff=a.get128more(sensor)
       stuff=PreprocessUtils.highpass(stuff)
       tree+=stuff
       time.sleep(1)
    while True:
        win32=numpy.hanning(1024)
        stuff1=win32*tree
        stuff2=PreprocessUtils.bin_power(stuff1, [1,4,7,13,30], 128)
        
        
        
        
    
    
       
       
        

import time
import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/Tools")
import PreprocessUtils
#matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy
import CSV_Extractor
#Cleaner, better version
FFT_SIZE=1024
STEP_SIZE=16
FFT_SENSOR="FC5"
def bplot(file, sensor, rects1, a, fig):
    
    tree=list()
    while not len(tree)==FFT_SIZE:
       stuff=a.get128more(sensor)
       tree+=stuff
       time.sleep(1)
    while True:
        artree=PreprocessUtils.highpass(tree)
        win32=numpy.hanning(1024)
        artree=numpy.array(artree)
        stuff1=win32*artree
        stuff2=PreprocessUtils.bin_power(stuff1, [1,4,7,13,30], 128)
        stuff4=abs(20*numpy.log(stuff2))
        stuff5=tuple(stuff4[0])
        print(stuff5)        #print(stuff5)
        counter=int()
##        for i in rects1:
##            #print("Getting here?")
##            i.set_height(stuff5[counter])
##            counter+=1
##        fig.canvas.draw()
        del tree[0:16]
        more16=a.get16more(sensor)
        tree+=more16
        time.sleep(0.125/2)
        
file="C:/Users/Gaurav/Documents/CSV/Done/Zander -1-12.02.15.13.18.23.CSV"        
fig, ax=plt.subplots()
rects1=ax.bar([0,1,2,3], (0,0,0,0),1)
plt.ylim(105, 112)
plt.ion()
win=fig.canvas.manager
a=CSV_Extractor.CSVExtractor(file)
plt.show()
bplot(file,FFT_SENSOR, rects1, a, fig)
        
        
    
    
       
       
        

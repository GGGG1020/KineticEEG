import time
import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/Tools")
import PreprocessUtils
import matplotlib.pyplot as plt
import numpy
import CSV_Extractor
import time
FILE="C:/Users/Gaurav/Documents/CSV/Done/Zander -1-12.02.15.13.18.23.CSV"   
FFT_SIZE=1024
STEP_SIZE=16
FFT_SENSOR="FC5"
def bplot(file, sensor, a):
    #file2w=open("C:/Users/Gaurav/Desktop/fc51-fft.txt", "w")
    goodlist=list()
    tree=list()
    counter=float()
    retlist=list()
    while not len(tree)==FFT_SIZE:
       print("s")
       stuff=a.get128more(sensor)
       tree+=stuff
       #time.sleep(1)
       counter+=1
    while True:
        try:
            inittime=time.time()
            artree=PreprocessUtils.highpass(tree)
            win32=numpy.hanning(1024)
            artree=numpy.array(artree)
            stuff1=win32*artree
            stuff2=PreprocessUtils.bin_power(stuff1, [1,4,7,13,30], 128)
            stuff4=abs(20*numpy.log(stuff2))
            stuff5=tuple(stuff4[0])
            retlist.append(stuff5)   
            goodlist.append(stuff5)
            del tree[0:16]
            more16=a.get16more(sensor)
            tree+=more16
            #time.sleep((0.125-(time.time()-inittime)))
            counter+=(0.125)
        except:
            return retlist
a=CSV_Extractor.CSVExtractor(FILE)
finlist=bplot(FILE,FFT_SENSOR,  a)
        
        
    
    
       
       
        

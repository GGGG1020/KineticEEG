import time
import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/Tools")
import PreprocessUtils
import matplotlib.pyplot as plt
import numpy
import CSV_Extractor
import time
FILE="C:/Users/Gaurav/Documents/CSV/Done/Alex C.-1-24.02.15.10.20.39.CSV"   
FFT_SIZE=512
STEP_SIZE=16
FFT_SENSOR="FC5"
class CSVProc:
    def __init__(self, extract):
        """Extract is a CSV_Extractor.CSVExtractor object"""
        self.data_tree=dict()
        self.sensors= ['F3', 'O2', 'O1', 'F8', 'F4', 'FC6', 'AF3', 'P7', 'P8', 'FC5', 'T8', 'AF4', 'F7', 'T7']
        for i in self.sensors:
            self.data_tree[i]=self.__proc(i, extract)
    def get_with_settings(self, sensors=['F3', 'O2', 'O1', 'F8', 'F4', 'FC6', 'AF3', 'P7', 'P8', 'FC5', 'T8', 'AF4', 'F7', 'T7'], bands=["Delta", "Theta", "Mu", "Beta"]):
        """Allows maximum control over data"""
        buildlist=dict()
        word2list={"delta":0, "theta":1, "mu":2, "beta":3}
        indices1=list(map(str.lower, bands))
        indices=list()
        for l in indices1:
            indices.append(word2list[l])
        for i in sensors:
            buildlist[i]={}
            for j in indices:
                buildlist[i][j]=[w[j] for w in self.data_tree[i]]
        return buildlist
    def __proc(self, sensor, a):
        """Utility function to do the heavy lifting"""
        goodlist=list()
        tree=list()
        counter=float()
        retlist=list()
        while not len(tree)==FFT_SIZE:
           stuff=a.get128more(sensor)
           tree+=stuff
           #time.sleep(1)
           counter+=1
        while True:
            try:
                inittime=time.time()
                artree=PreprocessUtils.highpass(tree)
                win32=numpy.hanning(512)
                artree=numpy.array(artree)
                stuff1=win32*artree
                stuff2=PreprocessUtils.bin_power(stuff1, [1,4,8,12,30], 128)
                stuff4=abs(20*numpy.log(stuff2))
                stuff5=tuple(stuff4[0])
                retlist.append(stuff5)   
                goodlist.append(stuff5)
                ##print(len(tree))
                del tree[0:16]
                more16=a.get16more(sensor)
                tree+=more16
                #time.sleep((0.125-(time.time()-inittime)))
                counter+=(0.125)
            except:
                return retlist

       

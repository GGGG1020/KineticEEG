#trainer for  csv files
import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/Tools")
import CSV_Extractor
import PreprocessUtils
import numpy
import time
class CSV_Trainer:
    """This trains with CSV"""
    def __init__(self, file):
        ##self.fileobj=open(file, mode='r')
        self.file_name=str(file)
        self.csvextract=CSV_Extractor.CSVExtractor(self.file_name)
        self.SENSORS_OF_INTEREST=["FC5","F3","F4","FC6"]
        self.rawspecdict=dict()
        self.proc_specdict=dict()
    def preprocess(self, dictth,dictt1):
        for i in dictth.keys():
            nowconsd=dictth[i]
            tree=PreprocessUtils.highpass(nowconsd)
            tree1=numpy.hanning(1024)*tree
            stuff2=PreprocessUtils.bin_power(tree1, [1,4,7,13,30], 128)
            stuff4=abs(20*numpy.log(stuff2))
            stuff5=tuple(stuff4[0])
            dictt1[i].append(stuff5[0])
        return dictt1            
    def train_action(self, action,time1):
        """time1 and time2 seconds"""
        assert action=='kick',action=='arm'
        startpos=time1*128
        endpos=startpos+1024
        dictt1=dict()
        for i in self.SENSORS_OF_INTEREST:
            dictt1[i]=list()
        while True:
            for x in self.SENSORS_OF_INTEREST:
                self.rawspecdict[x]=self.csvextract.get_with_constraints(x, startpos, endpos)
            dictt1=self.preprocess(self.rawspecdict, dictt1)
            startpos+=16; endpos+=16
        return dictt1
            
            
        
            
        
        
        
        
        
        
    
        
        

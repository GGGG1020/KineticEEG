#trainer for  csv files
import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/Tools")
import CSV_Extractor
import PreprocessUtils
import operator
import CSVProc
import numpy
import time
class CSV_Trainer:
    """This trains with CSV"""
    def __init__(self, file,trainfile):
        ##self.fileobj=open(file, mode='r')
        self.file_name=str(file)
        self.csvextract=CSV_Extractor.CSVExtractor(self.file_name)
        self.SENSORS_OF_INTEREST=["FC5","F3","F4","FC6"]
        self.maindict=dict()
        self.trainfileobj=open(trainfile, "a+")
        for i in self.SENSORS_OF_INTEREST:
            self.maindict[i]=CSVProc.Proc(self.file_name, i, self.csvextract)
        self.rawspecdict=dict()
        self.proc_specdict=dict()
    def getlist(self, sensor,secs, secs1):
        return self.maindict[sensor][(secs-8)*8:(secs1-8)*8]
    def train_nuetral(self, secs):
        for i in self.SENSORS_OF_INTEREST: 
            data=self.getlist(i, secs, secs+2)
            dataspec=map(operator.itemgetter(0),data)
            self.dataspec=list(dataspec)
            self.avg=sum(self.dataspec)/len(self.dataspec)
            teblist=self.dataspec[0:10]
            strstowrite=[str(i)+"\n" for i in teblist]
            strstowrite.insert(0, str(("#,"+i+","+"NULL"+','+"10"+"\n")))
            for r in strstowrite:
                self.trainfileobj.write(r)
                #print(r)
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
            
            
        
            
        
        
        
        
        
        
    
        
        

#trainer for  csv files
import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/Tools")
import CSV_Extractor
import PreprocessUtils
import numpy

class CSV_Trainer:
    """This trains with CSV"""
    SENSORS_OF_INTEREST=["FC5","F3","F4","FC6"]
    def __init__(self, file):
        ##self.fileobj=open(file, mode='r')
        self.file_name=str(file)
        self.csvextract=CSV_Extractor.CSVExtractor(self.file_name)
        self.rawspecdict=dict()
        self.proc_specdict=dict()
    def preprocess(self, dictth):
        dictt1=dict()
        for i in dictth.keys():
            nowconsd=dictth[i]
            tree=PreprocessUtils.highpass(nowconsd)
            tree1=numpy.hanning(1024)*tree
            stuff2=PreprocessUtils.bin_power(stuff1, [1,4,7,13,30], 128)
            stuff4=abs(20*numpy.log(stuff2))
            stuff5=tuple(stuff4[0])
            dictt1[i]=[stuff5]
        return dictt1
            
            
    def train_action(self, action,time1, time2):
        """time1 and time2 seconds"""
        assert action=='kick',action=='arm'
        startpos,endpos=time1*128, time2*128
        for x in SENSORS_OF_INTEREST:
            self.rawspecdict[x]=self.csv_extract.get_with_constraint(x, startpos, endpos)
        
            
        
        
        
        
        
        
    
        
        

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
        for i in dictth.keys():
            
            
    def train_action(self, action,time1, time2):
        """time1 and time2 seconds"""
        assert action=='kick',action=='arm'
        startpos,endpos=time1*128, time2*128
        for x in SENSORS_OF_INTEREST:
            self.rawspecdict[x]=self.csv_extract.get_with_constraint(x, startpos, endpos)
            
        
        
        
        
        
        
    
        
        

"CSVClassifier.py"
import sys
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/Tools")
import CSV_Extractor
import Preprocessers
import ClassifyUtils
import Detector
import socket
import pickle
class Classifier:
    def __init__(self):
        self.detector=Detector.AverageBasedDetector(5)
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('127.0.0.1',4097))
        self.diff_data=dict({"FC5":[], "FC6":[], "F3":[], "F4":[]})
        self.socket.listen(1)
        self.newsock,useless=self.socket.accept()
    def __getdirection(self, listy):
        iir_tc=0.98
        background=signal[0]
        hp=list()
        hp.append(0)
        for i in range(1, len(signal)):
            signal[i]=float(signal[i])
            background=(iir_tc*background)+(1-iir_tc)*signal[i]
            hp.append(signal[i]-background)
    def mainloop(self):
        data=self.newsock.recv(4096)
        self.data=pickle.loads(data)
        for i in ["FC5", "FC6", "F3", "F4"]:
            self.diff_data[i]=self.__getdirection(self.data[i])
        
            
    
        
        
        
        

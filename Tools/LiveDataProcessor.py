import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/KineticEEG")
#import CSVProc
import PreprocessUtils
import subprocess
import socket
import pickle 
import time
import Detector
import Preprocessers
class LiveDataProcessor:
    """For Training Purposes only"""
    def __init__(self, fftsize):
        #self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket.bind(('127.0.0.1', 4096))
        self.fftsize=fftsize
        self.goodlist=dict({'F3': [], 'FC5': [], 'T7': [], 'F7': [], 'P7': [], 'P8': [], 'AF4': [], 'O2': [], 'O1': [], 'T8': [], 'AF3': [], 'FC6': [], 'F4': [], 'F8': []})
        self.firstlist=dict()
        self.subprocess_args=["python", "C:/Users/Gaurav/Documents/GitHub/KineticEEG/Tools/EmotivDataGetter.py"]
        #self.subprocess=subprocess.Popen(self.subprocess_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    def mainloop(self):
        self.subprocess=subprocess.Popen(self.subprocess_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        self.socket.listen(1)
        self.carryover=dict()
        self.finaldict=dict()
        #self.newsocket, ip=self.socket.accept()
        data=b''
        tmpdata=b''
        done=False
        self.firstlist=pickle.loads(data)
        for i in self.firstlist.keys():
            artree=PreprocessUtils.highpass(self.firstlist[i])
            win32=numpy.hanning(512)
            artree=numpy.array(artree)
            stuff1=win32*artree
            stuff2=PreprocessUtils.bin_power(stuff1, [1,4,8,12,30], 128)
            stuff4=abs(20*numpy.log(stuff2))
            stuff5=tuple(stuff4[0])
            goodlist[i].append(stuff5)
        done=True
        while(self.subprocess.poll()==None):
            data=b''
            while (1):
                tmpdata=self.newsocket.recv(4096)
                if tmpdata is not None:
                    data=data+tmpdata
                else:
                    break
            if data==b'':
                return 
            self.carryover=pickle.loads(data)
            for i in self.carryover.keys():
                self.firstlist[i].append(self.carryover[i])
                del self.firstlist[i][0:16]
            for i in self.firstlist.key():
                artree=PreprocessUtils.highpass(self.firstlist[i])
                win32=numpy.hanning(512)
                artree=numpy.array(artree)
                stuff1=win32*artree
                stuff2=PreprocessUtils.bin_power(stuff1, [1,4,8,12,30], 128)
                stuff4=abs(20*numpy.log(stuff2))
                stuff5=tuple(stuff4[0])
                retlist.append(stuff5)   
                goodlist[i].append(stuff5)
class LiveDataProcessorWithDetector:
    """For actual usage"""
    def __init__(self, fftsize:int):
        #self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket.bind(('127.0.0.1', 4096))
        self.processor=Preprocessers.DataProcessor()
        self.fftsize=fftsize
        self.goodlist=dict({'F3': [], 'FC5': [], 'T7': [], 'F7': [], 'P7': [], 'P8': [], 'AF4': [], 'O2': [], 'O1': [], 'T8': [], 'AF3': [], 'FC6': [], 'F4': [], 'F8': []})
        self.firstlist=dict()
        self.subprocess_args=["python", "C:/Users/Gaurav/Documents/GitHub/KineticEEG/Tools/EmotivDataGetter.py"]
        self.detector=Detector.AverageBasedDetector(4)
        #self.subprocess=subprocess.Popen(self.subprocess_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    def makebinpower(self,firstlist:dict):
        for i in firstlist.key():
            artree=PreprocessUtils.highpass(self.firstlist[i])
            win32=numpy.hanning(512)
            artree=numpy.array(artree)
            stuff1=win32*artree
            stuff2=PreprocessUtils.bin_power(stuff1, [1,4,8,12,30], 128)
            stuff4=abs(20*numpy.log(stuff2))
            stuff5=tuple(stuff4[0])
            retlist.append(stuff5)   
            #goodlist.append(stuff5)
        return retlist
    def mainloop(self):
        self.subprocess=subprocess.Popen(self.subprocess_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        self.socket.listen(1)
        self.carryover=dict()
        self.finaldict=dict()
        #self.newsocket, ip=self.socket.accept()
        data=b''
        tmpdata=b''
        done=False
        self.firstlist=pickle.loads(data)
        for i in self.firstlist.keys():
            artree=PreprocessUtils.highpass(self.firstlist[i])
            win32=numpy.hanning(512)
            artree=numpy.array(artree)
            stuff1=win32*artree
            stuff2=PreprocessUtils.bin_power(stuff1, [1,4,8,12,30], 128)
            stuff4=abs(20*numpy.log(stuff2))
            stuff5=tuple(stuff4[0])
            goodlist[i].append(stuff5)
        done=True
        while(self.subprocess.poll()==None):
            data=b''
            while (1):
                tmpdata=self.newsocket.recv(4096)
                if tmpdata is not None:
                    data=data+tmpdata
                else:
                    break
            if data==b'':
                return 
            self.carryover=pickle.loads(data)
            for i in self.carryover.keys():
                self.firstlist[i].append(self.carryover[i])
                del self.firstlist[i][0:16]
            for i in self.firstlist.key():
                artree=PreprocessUtils.highpass(self.firstlist[i])
                win32=numpy.hanning(512)
                artree=numpy.array(artree)
                stuff1=win32*artree
                stuff2=PreprocessUtils.bin_power(stuff1, [1,4,8,12,30], 128)
                stuff4=abs(20*numpy.log(stuff2))
                stuff5=tuple(stuff4[0])
                retlist.append(stuff5)   
                goodlist[i].append(stuff5)
            self.detector.update(goodlist)
            if self.detector.detect():
                #Let me think about it for a second here.....
                
                
                
        
            
  
                
            

        
             
            
                
            
        
        

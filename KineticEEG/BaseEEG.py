import ctypes
import sys
import os
import tkinter
import multiprocessing 
from ctypes import *
import PreprocessUtils
import numpy
from numpy import *
import time
from ctypes.util import find_library
os.chdir("C:/Program Files (x86)/Emotiv Research Edition SDK v2.0.0.20/dll/32 bit/")
libEDK = cdll.LoadLibrary("edk.dll")
def run_data_getter_processer(q):
    j=EmotivDataGetter()
    j.scan_loop(q)
    j.cleanup()
    
class EmotivDataGetter:
    ED_COUNTER = 0
    ED_INTERPOLATED=1
    ED_RAW_CQ=2
    ED_AF3=3
    ED_F7=4
    ED_F3=5
    ED_FC5=6
    ED_T7=7
    ED_P7=8
    ED_O1=9
    ED_O2=10
    ED_P8=11
    ED_T8=12
    ED_FC6=13
    ED_F4=14
    ED_F8=15
    ED_AF4=16
    ED_GYROX=17
    ED_GYROY=18
    ED_TIMESTAMP=19
    ED_ES_TIMESTAMP=20
    ED_FUNC_ID=21
    ED_FUNC_VALUE=22
    ED_MARKER=23
    ED_SYNC_SIGNAL=24
    def __init__(self):
            #q.put("Hi")
            self.targetChannelList = [EmotivDataGetter.ED_COUNTER,EmotivDataGetter.ED_AF3, EmotivDataGetter.ED_F7,EmotivDataGetter.ED_F3, EmotivDataGetter.ED_FC5, EmotivDataGetter.ED_T7,
                                      EmotivDataGetter.ED_P7, EmotivDataGetter.ED_O1, EmotivDataGetter.ED_O2, EmotivDataGetter.ED_P8,EmotivDataGetter.ED_T8,EmotivDataGetter.ED_FC6, EmotivDataGetter.ED_F4,
                                      EmotivDataGetter.ED_F8,EmotivDataGetter.ED_AF4, EmotivDataGetter.ED_GYROX, EmotivDataGetter.ED_GYROY, EmotivDataGetter.ED_TIMESTAMP, EmotivDataGetter.ED_FUNC_ID,
                                   EmotivDataGetter.ED_FUNC_VALUE, EmotivDataGetter.ED_MARKER, EmotivDataGetter.ED_SYNC_SIGNAL]
            self.targetChannelList = [EmotivDataGetter.ED_AF3, EmotivDataGetter.ED_F7,EmotivDataGetter.ED_F3, EmotivDataGetter.ED_FC5, EmotivDataGetter.ED_T7,
                                      EmotivDataGetter.ED_P7, EmotivDataGetter.ED_O1, EmotivDataGetter.ED_O2, EmotivDataGetter.ED_P8,EmotivDataGetter.ED_T8,EmotivDataGetter.ED_FC6, EmotivDataGetter.ED_F4,
                                      EmotivDataGetter.ED_F8,EmotivDataGetter.ED_AF4]
            self.header = ['COUNTER','AF3','F7','F3', 'FC5', 'T7', 'P7', 'O1', 'O2','P8', 'T8', 'FC6', 'F4','F8', 'AF4','GYROX', 'GYROY', 'TIMESTAMP','FUNC_ID', 'FUNC_VALUE', 'MARKER', 'SYNC_SIGNAL']
            self.sens=['AF3','F7','F3', 'FC5', 'T7', 'P7', 'O1', 'O2','P8', 'T8', 'FC6', 'F4','F8', 'AF4']
            self.eEvent=libEDK.EE_EmoEngineEventCreate()
            self.eState= libEDK.EE_EmoStateCreate()
            #print("Hi")
            self.userID =c_uint(0)
            self.nSamples=c_uint(0)
            self.nSam= c_uint(0)
            self.nSamplesTaken  = pointer(self.nSamples)
            self.dct1={}
            for i in self.sens:
                self.dct1[i]=[]
            self.da= zeros(128,double)
            self.data= pointer(c_double(0))
            self.user= pointer(self.userID)
            self.composerPort= c_uint(1726)
            self.secs= c_float(1)
            self.datarate= c_uint(0)
            self.readytocollect  = False
            self.option= c_int(0)
            self.state= c_int(0)
            libEDK.EE_EngineConnect(b"Emotiv Systems-5")
            self.hData = libEDK.EE_DataCreate()
            libEDK.EE_DataSetBufferSizeInSec(4)
            #q.put("Connected")
            
    def scan_example(self,q):
        x=int()
        while True:
            q.put(x)
            x+=1
            time.sleep(8/128)
    def test_parallel_withq(self,q):
        first_iter=bool(True)
        try:
            while True :
                for i in self.sens:
                    self.dct1[i]=[]
                state = libEDK.EE_EngineGetNextEvent(self.eEvent)
                if state == 0:
                    eventType = libEDK.EE_EmoEngineEventGetType(self.eEvent)
                    libEDK.EE_EmoEngineEventGetUserId(self.eEvent, self.user)
                    if eventType == 16: #libEDK.EE_Event_enum.EE_UserAdded:
                        libEDK.EE_DataAcquisitionEnable(self.userID,True)
                        self.readytocollect = True
                if self.readytocollect==True:    
                    libEDK.EE_DataUpdateHandle(0, self.hData)
                    libEDK.EE_DataGetNumberOfSample(self.hData,self.nSamplesTaken)
                    if first_iter:
                        if self.nSamplesTaken[0] == 512:
                            self.nSam=self.nSamplesTaken[0]
                            arr=(ctypes.c_double*self.nSamplesTaken[0])()
                            ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))                      
                            data = array('d')
                            useless=list(self.targetChannelList.keys())
                            for sampleIdx in range(self.nSamplesTaken[0]): 
                                for i in self.targetChannelList:
                                    libEDK.EE_DataGet(hData,useless.index(i),byref(arr), nSam)
                                    self.dct1[i].append(arr[sampleIdx])
                            q.put(self.dct1)
                            first_iter=False
                    else:
                        if self.nSamplesTaken==16:
                            self.nSam=self.nSamplesTaken[0]
                            arr=(ctypes.c_double*self.nSamplesTaken[0])()
                            ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))                  
                            data = array('d')
                            for sampleIdx in range(self.nSamplesTaken[0]): 
                                for i in self.sens: 
                                    libEDK.EE_DataGet(hData,i,byref(arr), nSam)
                                    self.dct1[i].append(arr[sampleIdx])
                            q.put(self.dct1)
        except:
            q.put("die")
            self.cleanup()
    def scan_loop(self,q):
        first_iter=bool(True)
        for i in self.sens:
            self.dct1[i]=[]
        try:
            while True :
                state = libEDK.EE_EngineGetNextEvent(self.eEvent)
                if state == 0:
                    eventType = libEDK.EE_EmoEngineEventGetType(self.eEvent)
                    libEDK.EE_EmoEngineEventGetUserId(self.eEvent, self.user)
                    if eventType == 16: #libEDK.EE_Event_enum.EE_UserAdded:
                        libEDK.EE_DataAcquisitionEnable(self.userID,True)
                        self.readytocollect = True
                if self.readytocollect==True:
                    #print("ready")
                    if first_iter:
                        #print("Now", time.time())
                        while not self.nSamplesTaken[0]>=512:
                            libEDK.EE_DataUpdateHandle(0, self.hData)
                            libEDK.EE_DataGetNumberOfSample(self.hData,self.nSamplesTaken)
                          #  print(self.nSamplesTaken[0])
                            time.sleep(float(512.0-self.nSamplesTaken[0])/128.0)
                            libEDK.EE_DataUpdateHandle(0, self.hData)
                            libEDK.EE_DataGetNumberOfSample(self.hData,self.nSamplesTaken)
                        #print(self.nSamplesTaken[0], time.time())
                        if self.nSamplesTaken[0]==512:
                            self.nSam=self.nSamplesTaken[0]
                            arr=(c_double*512)()
                            libEDK.EE_DataGetNumberOfSample(self.hData,self.nSamplesTaken)
                            ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))                      
                            data = array('d')
                            useless=list(self.sens)
                            for sampleIdx in range(self.nSamplesTaken[0]): 
                                for i in self.sens:
                                    libEDK.EE_DataGet(self.hData,useless.index(i),byref(arr), self.nSam)
                                    self.dct1[i].append(arr[sampleIdx])
                                if len(self.dct1["FC5"])==512:
                                    q.send(self.dct1)
                                   # eefe=open("C:/Users/Gaurav/Desktop/gatherside.txt", "w")
                                    #eefe.write(str(self.dct1))
                                    #eefe.close()
                                    first_iter=False
                                    for i in self.sens:
                                        self.dct1[i]=[]
                    count=0
                    while True:
                      #print(time.time())
                      ##time.sleep(0.025*0.75)
                      libEDK.EE_DataUpdateHandle(0, self.hData)
                      libEDK.EE_DataGetNumberOfSample(self.hData, self.nSamplesTaken)
                      #print(self.nSamplesTaken[0], time.time())
                      #while not self.nSamplesTaken[0]==16:
                          #libEDK.EE_DataUpdateHandle(0, self.hData)
                         # libEDK.EE_DataGetNumberOfSample(self.hData, self.nSamplesTaken)
                       #   print(self.nSamplesTaken[0])
                      if self.nSamplesTaken[0]!=0:
                           # libEDK.EE_DataUpdateHandle(0, self.hData)
                            self.nSam=self.nSamplesTaken[0]
                            arr=(c_double*self.nSamplesTaken[0])()
                            ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))                  
                            data = array('d')
                            useless=list(self.sens)
                            for sampleIdx in range(self.nSamplesTaken[0]): 
                                for i in self.sens: 
                                    libEDK.EE_DataGet(self.hData,useless.index(i),byref(arr), self.nSam)
                                    #print("jo", len(self.dct1["FC5"]))
                                    self.dct1[i].append(arr[sampleIdx])
                                count+=1
                                if count==16:
                                    q.send(self.dct1)
                                    #q.put(len(self.dct1["FC5"]))
                                    
                                    #eefe=open("C:/Users/Gaurav/Desktop/gatherside.txt", "a")
                                    #eefe.write("\n")
                                    #eefe.write("\n")
                                    #eefe.write(str(len(self.dct1["FC5"])))
                                    #eefe.write("\n")
                                    #eefe.write(str(self.dct1))
                                    #eefe.close()
                                    #print("Hi", time.time())
                                    for i in self.sens:
                                        count=0
                                        self.dct1[i]=[]
                            
        except:
            
            self.cleanup()
            q.close()
            raise
        
                
    def cleanup(self):
        libEDK.EE_DataFree(self.hData)
        libEDK.EE_EngineDisconnect()
        libEDK.EE_EmoStateFree(self.eState)
        libEDK.EE_EmoEngineEventFree(self.eEvent)
def exec_proc(q,putq,samps):
    t=EEG_Processer()
    try:
        t.mainloop(q, putq, samps)
    except:
        a=open("C:/Users/Gaurav/Desktop/errors.txt", "w")
        a.write("ERROR")
        
        a.close()
        a=open("C:/Users/Gaurav/Desktop/errors.txt", "w")
        
        sys.stderr=a
        raise
        
class EEG_Processer:
    def __init__(self):
        self.sensors= ['F3', 'O2', 'O1', 'F8', 'F4', 'FC6', 'AF3', 'P7', 'P8', 'FC5', 'T8', 'AF4', 'F7', 'T7']
    def mainloop_example(self, q, q2, st):
        while True:
            j=q.get()
            q2.put(j)
    def mainloop(self, q,q2,st):
        j={'F3':[], 'O2':[], 'O1':[], 'F8':[], 'F4':[], 'FC6':[], 'AF3':[], 'P7':[], 'P8':[], 'FC5':[], 'T8':[], 'AF4':[], 'F7':[], 'T7':[]}
        b={}
        #q2.put("Hi")
        firstdat=q.recv()
        #fileh=open("C:/Users/Gaurav/Desktop/Testlogs.txt", "w")
        #fileh.write(str(firstdat))
        #fileh.close()
        #q2.put('Hi')
        if type(firstdat)==str:q2.put(firstdat)
        #if firstdat=="j":q2.put("j")
        for i in self.sensors:
            current=firstdat[i]
            b[i]=current
            artree=PreprocessUtils.highpass(current)
            win32=numpy.hanning(512)
            artree=numpy.array(artree)
            stuff1=win32*artree
            stuff2=PreprocessUtils.bin_power(stuff1, [1,4,8,12,30], 128)
            stuff4=abs(20*numpy.log(stuff2))
            stuff5=tuple(stuff4[0])
            j[i].append(stuff5)
            time.sleep(16/128)
        q2.send(j)
        while True:
            
            secondat=q.recv()
            #q2.send("recieved one")
            #fileh=open("C:/Users/Gaurav/Desktop/Testlogs.txt", "w")
            #fileh.write(str(secondat))
            #fileh.close()
            #q2.put('Hi')
            if type(secondat)==str:q2.put(secondat)
            #if str(secondat)=="die": q2.put("die");break
            for i in self.sensors:
                current=b[i]
                del current[0:16]
                current+=secondat[i]
                #q2.put(len(current))
                b[i]=current
                artree=PreprocessUtils.highpass(current)
                #q2.send("Highpass")
                win32=numpy.hanning(512)
                artree=numpy.array(artree)
                stuff1=win32*artree
                stuff2=PreprocessUtils.bin_power(stuff1, [1,4,8,12,30], 128)
                stuff4=abs(20*numpy.log(stuff2))
                stuff5=tuple(stuff4[0])
                j[i].append(stuff5)
                time.sleep(16/128)
            #if len(j["FC5"])==st:
            q2.send(j)
            for i in j.keys():
                j[i]=[]

    
if __name__=='__main__':
    a=EmotivDataGetter()
    a.test_non_parallel()
        
                        
    

    

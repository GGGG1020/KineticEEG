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
os.chdir("C:/Program Files (x86)/Emotiv Research Edition SDK v2.0.0.20/Applications")
libEDK = cdll.LoadLibrary("edk.dll")
def run_data_getter_processer(q):
    j=EmotivDataGetter()
    j.scan_loop(q)
    j.cleanup()
class EmotivDataGetter:
    ED_COUNTER = 0 #Definitions(From Emotiv EDK header and docs)
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
            self.targetChannelList = [EmotivDataGetter.ED_COUNTER,EmotivDataGetter.ED_INTERPOLATED,
                                        EmotivDataGetter.ED_RAW_CQ,EmotivDataGetter.ED_AF3, EmotivDataGetter.ED_F7,EmotivDataGetter.ED_F3, EmotivDataGetter.ED_FC5, EmotivDataGetter.ED_T7,
                                    EmotivDataGetter.ED_P7, EmotivDataGetter.ED_O1, EmotivDataGetter.ED_O2, EmotivDataGetter.ED_P8,EmotivDataGetter.ED_T8,EmotivDataGetter.ED_FC6, EmotivDataGetter.ED_F4,
                                   EmotivDataGetter.ED_F8,EmotivDataGetter.ED_AF4, EmotivDataGetter.ED_GYROX, EmotivDataGetter.ED_GYROY, EmotivDataGetter.ED_TIMESTAMP, EmotivDataGetter.ED_FUNC_ID,
                                   EmotivDataGetter.ED_FUNC_VALUE, EmotivDataGetter.ED_MARKER, EmotivDataGetter.ED_SYNC_SIGNAL] #to order and interpret the data
##            self.targetChannelList = [EmotivDataGetter.ED_AF3, EmotivDataGetter.ED_F7,EmotivDataGetter.ED_F3, EmotivDataGetter.ED_FC5, EmotivDataGetter.ED_T7,
##                                      EmotivDataGetter.ED_P7, EmotivDataGetter.ED_O1, EmotivDataGetter.ED_O2, EmotivDataGetter.ED_P8,EmotivDataGetter.ED_T8,EmotivDataGetter.ED_FC6, EmotivDataGetter.ED_F4,
##                                      EmotivDataGetter.ED_F8,EmotivDataGetter.ED_AF4]
            self.header = ['COUNTER','AF3','F7','F3', 'FC5', 'T7', 'P7', 'O1', 'O2','P8', 'T8', 'FC6', 'F4','F8', 'AF4','GYROX', 'GYROY', 'TIMESTAMP','FUNC_ID', 'FUNC_VALUE', 'MARKER', 'SYNC_SIGNAL']
            self.sens=['c','int', 'cq', 'AF3','F7','F3', 'FC5', 'T7', 'P7', 'O1', 'O2','P8', 'T8', 'FC6', 'F4','F8', 'AF4']#sensor list
            self.eEvent=libEDK.EE_EmoEngineEventCreate()#Allocate memory for event and states
            self.eState= libEDK.EE_EmoStateCreate()
            #print("Hi")
            self.userID =c_uint(0)#User id int
            self.nSamples=c_uint(0)#number of samples int.
            self.nSam= c_uint(0)#
            self.nSamplesTaken  = pointer(self.nSamples)#Track the number of samples taken
            self.dct1={}#Create a dictionary to hold data
            for i in self.sens:
                self.dct1[i]=[]#initialize it with slots and spaces.
####Constants needed for aquisition###
            self.da= zeros(128,double)
            
            self.data= pointer(c_double(0))
            self.user= pointer(self.userID)
            self.composerPort= c_uint(1726)
            self.secs= c_float(1)
            self.datarate= c_uint(0)
            self.readytocollect  = False
            self.option= c_int(0)
            self.state= c_int(0)
#####Begin Connection Process####
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
        first_iter=bool(True)#Is this the first run of the interface?Constants must be initialized
        try:#Provide error handling
            while True :#infinite loop(escape through KeyBoardInterrupt)
                for i in self.sens:#Clear the dictionary.
                    self.dct1[i]=[]
                state = libEDK.EE_EngineGetNextEvent(self.eEvent)#Get the next event from the Emotiv API
                if state == 0:#If there is data to collect
                    eventType = libEDK.EE_EmoEngineEventGetType(self.eEvent)#Type of event
                    libEDK.EE_EmoEngineEventGetUserId(self.eEvent, self.user)#Acess user id.
                    if eventType == 16: #libEDK.EE_Event_enum.EE_UserAdded:
                        libEDK.EE_DataAcquisitionEnable(self.userID,True)#Enable data aquisition
                        self.readytocollect = True#Set flag to ready
                if self.readytocollect==True:    
                    libEDK.EE_DataUpdateHandle(0, self.hData)#Provide variable
                    libEDK.EE_DataGetNumberOfSample(self.hData,self.nSamplesTaken)#get number of samples
                    if first_iter:#initialize variables...
                        if self.nSamplesTaken[0] != 0:#Check that some samples have been taken
                            self.nSam=self.nSamplesTaken[0]
                            arr=(ctypes.c_double*self.nSamplesTaken[0])()#Allocate memory
                            ctypes.cast(arr, ctypes.POINTER(ctypes.c_double)) #I don't know what this does but Emotiv does it.....                     
                            data = array('d')
                            useless=list(self.targetChannelList.keys())
                            for sampleIdx in range(self.nSamplesTaken[0]): #For each sample taken.
                                for i in self.targetChannelList:#For each channel present
                                    libEDK.EE_DataGet(hData,useless.index(i),byref(arr), nSam)#Get the data of that sample(retrieve it)
                                    self.dct1[i].append(arr[sampleIdx])#append the piece of data to the data store.
                                if len(self.dct1["F3"])==512:#Check if there are 512 samples stored already
                                    q.put(self.dct1)#Place the dictionary on the IPC socket
                                    first_iter=False
                    else:    #Else case-After the first sample, step at 16.
                        if self.nSamplesTaken==16:
                            self.nSam=self.nSamplesTaken[0]
                            arr=(ctypes.c_double*self.nSamplesTaken[0])()#Same thing, see above.
                            ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))                  
                            data = array('d')
                            for sampleIdx in range(self.nSamplesTaken[0]): 
                                for i in self.sens: 
                                    libEDK.EE_DataGet(hData,i,byref(arr), nSam)
                                    self.dct1[i].append(arr[sampleIdx])
                                if len(self.dct1["F3"])==512:
                                    q.put(self.dct1)
                                    first_iter=False
                
        except:
            q.put("die")
            self.cleanup()
    def scan_loop(self,q):
        ###See above for the commentary on a previous, but semantically identical piece of code####
        first_iter=bool(True)
        for i in self.sens:
            self.dct1[i]=[]
        try:
            while True :
                state = libEDK.EE_EngineGetNextEvent(self.eEvent)
                if state == 0:
                    eventType = libEDK.EE_EmoEngineEventGetType(self.eEvent)
                    libEDK.EE_EmoEngineEventGetUserId(self.eEvent, self.user)
                    if eventType == 16:
                        libEDK.EE_DataAcquisitionEnable(self.userID,True)
                        self.readytocollect = True
                if self.readytocollect==True:
                    if first_iter:
                        while not self.nSamplesTaken[0]>=512:
                            libEDK.EE_DataUpdateHandle(0, self.hData)
                            libEDK.EE_DataGetNumberOfSample(self.hData,self.nSamplesTaken)
                            time.sleep(float(512.0-self.nSamplesTaken[0])/128.0)
                            libEDK.EE_DataUpdateHandle(0, self.hData)
                            libEDK.EE_DataGetNumberOfSample(self.hData,self.nSamplesTaken)
                        if self.nSamplesTaken[0]==512:
                            self.nSam=self.nSamplesTaken[0]
                            arr=(c_double*512)()
                            libEDK.EE_DataGetNumberOfSample(self.hData,self.nSamplesTaken)
                            ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))                      
                            data = array('d')
                            useless=list(self.sens)
                            for sampleIdx in range(self.nSamplesTaken[0]): 
                                for i in range(3, 17):
                                    libEDK.EE_DataGet(self.hData,i,byref(arr), self.nSam)
                                    self.dct1[self.sens[i]].append(arr[sampleIdx])
                                if len(self.dct1["FC5"])==512:
                                    q.send(self.dct1)
                                    first_iter=False
                                    for i in self.sens:
                                        self.dct1[i]=[]
                    count=0
                    while True:
                      imi=time.time()
                     
                      libEDK.EE_DataUpdateHandle(0, self.hData)
                      libEDK.EE_DataGetNumberOfSample(self.hData, self.nSamplesTaken)
                      if self.nSamplesTaken[0]!=0:
                            self.nSam=self.nSamplesTaken[0]
                            arr=(c_double*self.nSamplesTaken[0])()
                            ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))                  
                            data = array('d')
                            useless=list(self.sens)
                            time.sleep(0.125-(time.time()-imi))#Get the timing right!
                            for sampleIdx in range(self.nSamplesTaken[0]): 
                                for i in self.sens: 
                                    libEDK.EE_DataGet(self.hData,useless.index(i),byref(arr), self.nSam)
                                    #print("jo", len(self.dct1["FC5"]))
                                    self.dct1[i].append(arr[sampleIdx])
                                count+=1
                                if count==16:
                                    q.send(self.dct1)
                                    for i in self.sens:
                                        count=0
                                        self.dct1[i]=[]
                            
        except:
            
            self.cleanup()
            q.close()
            raise
        
    def scan_loop1(self,q):
        first_iter=bool(True)
        for i in self.sens:
            self.dct1[i]=[]
        try:
            while True :
                state = libEDK.EE_EngineGetNextEvent(self.eEvent)
                if state == 0:
                    eventType = libEDK.EE_EmoEngineEventGetType(self.eEvent)
                    libEDK.EE_EmoEngineEventGetUserId(self.eEvent, self.user)
                    if eventType == 16: #
                        libEDK.EE_DataAcquisitionEnable(self.userID,True)
                        self.readytocollect = True
                if self.readytocollect==True:
                    if first_iter:
                        libEDK.EE_DataGetNumberOfSample(self.hData,self.nSamplesTaken)
                        if self.nSamplesTaken[0]!=0:
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
                                    first_iter=False
                                    for i in self.sens:
                                        self.dct1[i]=[]
                    count=0
                    while True:
                      libEDK.EE_DataUpdateHandle(0, self.hData)
                      libEDK.EE_DataGetNumberOfSample(self.hData, self.nSamplesTaken)
                      if self.nSamplesTaken[0]!=0:
                            self.nSam=self.nSamplesTaken[0]
                            arr=(c_double*self.nSamplesTaken[0])()
                            ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))                  
                            data = array('d')
                            useless=list(self.sens)
                            for sampleIdx in range(self.nSamplesTaken[0]): 
                                for i in self.sens: 
                                    libEDK.EE_DataGet(self.hData,useless.index(i),byref(arr), self.nSam)
                                    self.dct1[i].append(arr[sampleIdx])
                                count+=1
                                if count==16:
                                    q.send(self.dct1)
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
            current=firstdat[i]#Captre data in a variable
            b[i]=current#store it in the dictionary(for intermediate)
            artree=PreprocessUtils.highpass(current)#Common Average Referenced High-Pass Filter
            win32=numpy.hanning(512)#Hanning window
            artree=numpy.array(artree)#put it in an array
            stuff1=win32*artree#apply hanning window
            stuff2=PreprocessUtils.bin_power(stuff1, [1,4,8,12,30], 128)#Do a fast fourier transform 
            stuff4=abs(20*numpy.log(stuff2))#Convert to dB.
            stuff5=tuple(stuff4[0])#place into a tuple.
            j[i].append(stuff5)#Append this to the package 
            #time.sleep(16/128)
        q2.send(j)#Place on an interprocess communication pipe
        while True:#Enter infinite loop of processing 
            
            secondat=q.recv()#Recieve package of data
            if type(secondat)==str:q2.put(secondat)#Propogate the SIG_TERM
            #if str(secondat)=="die": q2.put("die");break
####**See lines 302-314 for commentary of this section**####
            for i in self.sensors:#iterate over each sensor
                current=b[i]
                del current[0:16]
                current+=secondat[i]
                b[i]=current
                artree=PreprocessUtils.highpass(current)
                win32=numpy.hanning(512)
                artree=numpy.array(artree)
                stuff1=win32*artree
                stuff2=PreprocessUtils.bin_power(stuff1, [1,4,8,12,30], 128)
                stuff4=abs(20*numpy.log(stuff2))
                stuff5=tuple(stuff4[0])
                j[i].append(stuff5)
            q2.send(j)
            for i in j.keys():
                j[i]=[]
__version__=1.0
__author__="Gaurav Ghosal"        
                        
    

    

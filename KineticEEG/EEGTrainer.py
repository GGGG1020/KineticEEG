import sys
import os
import tkinter
import multiprocessing 
from ctypes import *
import atexit
import PreprocessUtils
from numpy import *
import time
from ctypes.util import find_library
os.chdir("C:/Program Files (x86)/Emotiv Research Edition SDK v2.0.0.20/dll/32 bit/")
libEDK = cdll.LoadLibrary("edk.dll")
def run_data_getter_processer(q):
    q.put("hi")
    j=EmotivDataGetter()
    q.put("j")
    j.scan_example(q)
    #j.cleanup()
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
            libEDK.EE_DataSetBufferSizeInSec(self.secs)
    def scan_example(self,q):
        x=int()
        while True:
            q.put(x)
            x+=1
            time.sleep(16/128)
    def scan_loop(self,q):
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
                                for i in self.targetChannelList: 
                                    libEDK.EE_DataGet(hData,i,byref(arr), nSam)
                                    self.dct1[i].append(arr[sampleIdx])
                            q.put(self.dct1)
                time.sleep(0.2)
        except:
            q.put("die")
            self.cleanup()
                
    def cleanup(self):
        libEDK.EE_DataFree(self.hData)
        libEDK.EE_EngineDisconnect()
        libEDK.EE_EmoStateFree(self.eState)
        libEDK.EE_EmoEngineEventFree(self.eEvent)
def exec_proc(q,putq,samps):
    t=EEG_Processer()
    putq.put("made it here")
    t.mainloop_example(q,putq, samps)
    
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
        firstdat=q.get()
        if firstdat=="j":q2.put("j")
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
        while not q.empty():
            secondat=q.get()
            if str(secondat)=="die": q2.put("die");break
            for i in self.sensors:
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
                time.sleep(16/128)
            if len(j[0])==1:
                q.put(j) 
if __name__=='__main__':
    try:
        main_q=multiprocessing.Queue()
        second_q=multiprocessing.Queue()
        main_proc=multiprocessing.Process(target=run_data_getter_processer, args=(main_q,))
        main_proc.start()
        print(main_proc.pid)
        proc_proc=multiprocessing.Process(target=exec_proc, args=(main_q, second_q,16))
        proc_proc.start()
        print(proc_proc.pid)
        while main_proc.is_alive():
            print(second_q.get())
    except KeyboardInterrupt:
        main_proc.terminate()
        proc_proc.terminate()
            
    
        
                                      
        
    
    

    

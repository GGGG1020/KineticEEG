import numpy
import numpy.polynomial as poly
import ClassifyUtils
import multiprocessing
import BaseEEG
import statistics
import ctypes
import itertools
import kFoldCrossValidation2
import statistics
import time
import pickle








class MultiLiveTrainingDataGatherer:
     def __init__(self, process1,process2,q,dumpto, qevents,k):
        self.getter=process1
        self.q=q
        self.events=qevents
        self.k=k
        self.processer=process2
     def car(self,data_dict):
         pp=numpy.matrix([data_dict[j] for j in data_dict])
         count=0
         for j in pp.T:
             avg=statistics.mean(numpy.array(j).flatten())
             for p in data_dict:
                 data_dict[p][count]-=avg
             count+=1
     def runApp(self):
        self.getter.start()
        getpid=self.getter.pid
        procget=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(getpid))
        kernel.SetPriorityClass(procget, 0x0100)
        self.processer.start()
        procpid=self.processer.pid
        procproc=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(procpid))
        kernel.SetPriorityClass(procproc, 0x0100)
        sampslist=dict()
        data_dict=dict()
        count=0
        for i in self.events:
            sampslist[i]=[]
        for k in range(self.k):
            for i in self.events:
                data_dict[i]={"F3":[], "F4":[], "FC5":[], "FC6":[]}
            for tp in data_dict:
                print(tp)
                first=bool(True)
                try:
                    while self.getter.is_alive():
                        data=self.q.recv()
                        if first:
                            data=self.q.recv()
                            first=False
                        for i in data_dict[tp]:
                            data_dict[tp][i].append(data[i][0][2])
                        if len(data_dict[tp]["F3"])==32:
                            for i in data_dict[tp]:
                                del data_dict[tp][i][0]
                            raise KeyboardInterrupt    
                        print(time.asctime())
                except:
                    for i in range(32):
                         self.q.recv()
                    if not count==3:
                        continue
            count=0
            for pl in data_dict:
                sampslist[pl].append(Sample(pl, data_dict[pl]))
                print("j")
            print("Train Done")
        self.getter.terminate()
        self.processer.terminate()
        for j in sampslist:
            for p in sampslist[j]:
                print(p.data)
                self.car(p.data)
                print(p.data)
        fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "wb")
        fileobj.write(pickle.dumps(sampslist))
        fileobj.close()

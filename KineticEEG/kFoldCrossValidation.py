#kFoldCrossValidation.py
import sys
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/Tools")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG")
import CSV_Proc
import SLICERZ
import statistics
import PolyFitClassifier
import BaseEEG
import multiprocessing
import math
import random
import time
import ctypes
import pickle
kernel=ctypes.windll.kernel32
class Sample:
    def __init__(self, label, data):
        self.data=data
        self.label=label
class kFoldCrossValidationGatherer:
     def __init__(self, process1,process2,q,dumpto,times,labels=["arm", "kick", "neutral"]):
        self.getter=process1
        self.q=q
        self.times=times
        self.collection={}
        for i in labels:self.collection.update({i:[]})
        self.events=labels
        self.labels=labels
        self.processer=process2
     def runApp(self):
        self.getter.start()
        getpid=self.getter.pid
        procget=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(getpid))
        kernel.SetPriorityClass(procget, 0x0100)
        self.processer.start()
        procpid=self.processer.pid
        procproc=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(procpid))
        kernel.SetPriorityClass(procproc, 0x0100)
        data_dict=dict()
        for i in range(self.times):
            for p in self.events:
                data_dict[p]={"F3":[], "F4":[], "T7":[], "T8":[]}
            
            for tp in data_dict:
                
                print(tp)
                #time.sleep(1)
                first=bool(True)
                
                try:
                    while self.getter.is_alive():
                        #print(data_dict)
                        #print(data_dict[tp])
                        data=self.q.recv()
                        if first:
                            
                            #print(tp)
                            #time.sleep(1)
                            data=self.q.recv()
                            first=False
                        for j in data_dict[tp]:
                            data_dict[tp][j].append(data[j][0][2])
                        if len(data_dict[tp]["F3"])==24:
                            for p in data_dict[tp]:
                                del data_dict[tp][p][0]
                            #print(self.livedataclass.test_classifiers_ret(data_dict))
                            raise KeyboardInterrupt
                        
                            
                        print(time.asctime())
                     #a#   self.system_up_time+=16/128
                except:
                    #print(e)
                    for l in data_dict:
                        self.collection[l].append(Sample(l,data_dict[i]))
                    for po in range(32):
                         self.q.recv()
                    print("Train Done")
                    
                   # raise

        self.getter.terminate()
        self.processer.terminate()
        fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Gaurav1.kineegxval", "wb")
        fileobj.write(pickle.dumps(self.collection))
        fileobj.close()
class NonConformingInterface(Exception):
    pass
class kFoldCrossValidationRunner2:
    def __init__(self, k, classify, actions=["arm", "kick", "neutral"], parsefunc=None):
        self.fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Gaurav1.kineegxval", "rb")
        self.dat=pickle.loads(self.fileobj.read())
        for i in self.dat:
            for j in range(len(self.dat[i])):
                for t in self.dat[i][j]:
                    if t.data==self.dat[self.dat[i][j].index(j)+1].data:
                        del self.dat[i][j][self.dat[self.dat[i][j].index(j)+1]]
            
                                 
        self.k=k
        self.classify=classify
        test=classify(2)
        
        self.actions=actions
        if not hasattr(test, "train") or not hasattr(test, "classify"):
            raise NonConformingInterface("Not proper classifier")
    def run2(self):
        classlist={}
        reslist=list()
        errors=[]
        unpacked=list()
        for b in self.actions:
            unpacked+=self.dat[b]
            #print(unpacked)
        for i in range(self.k):
            classlist={}
            right=0
            total=0
            temp=self.classify(15)
            traindict={}
            #for i  in self.actions:
                #traindict[i]=random.sample(self.dat[i], 1)[0].data
            random.shuffle(unpacked)
            ransam=unpacked[0]
                    
            temp.train({"arm":self.dat["arm"][0].data,"kick":self.dat["kick"][0].data,"neutral":self.dat["neutral"][0].data})
                #print(ransam)
                #traindict[i]=ransam
            #temp.train(traindict)
            #classlist[j]=temp
            count=0
            for p in unpacked:

                #print("Hi")
                #rint("Hi")
                #print(p.data)
                #res=[tuple((ki, classlist[ki].classify(p.data))) for ki in classlist]
                #if temp.classify(p.data)[0]==p.label:
                    
                    #right+=1
                #elif not p.label=='neutral':errors.append(p.label)
                #print(res, p.label)
                #if not p.label=="neutral":
                
                count+=1
                #print(right, total
                print(temp.classify(p.data), p.label)
                if temp.classify(p.data)[0]==p.label:
                
                    right+=1
                total+=1
                reslist.append(right/total)
            return [statistics.mean(reslist),errors]
    def run(self):
        classlist={}
        reslist=list()
        errors=[]
        unpacked=list()
        for b in self.actions:
            unpacked+=self.dat[b]
            #print(unpacked)
        for i in range(self.k):
            classlist={}
            right=0
            total=0
            self.temp=self.classify(17)
            traindict={}
            #for i  in self.actions:
                #traindict[i]=random.sample(self.dat[i], 1)[0].data
            random.shuffle(unpacked)
            ransam=unpacked[0]
            #del unpacked[0]
                #print(ransam)
                #traindict[i]=ransam
            #temp.train(traindict)
            #classlist[j]=temp
            count=0
            for p in unpacked:
                if not count==0:
                    
                    self.temp.train({p.label:p.data})
                    
                #print("Hi")
                #rint("Hi")
                #print(p.data)
                #res=[tuple((ki, classlist[ki].classify(p.data))) for ki in classlist]
                #if temp.classify(p.data)[0]==p.label:
                    
                    #right+=1
                #elif not p.label=='neutral':errors.append(p.label)
                #print(res, p.label)
                #if not p.label=="neutral":
                
                count+=1
                #print(right, total
            print(self.temp.classify(ransam.data), ransam.label)
            if self.temp.classify(ransam.data)[0]==ransam.label:
                
                right+=1
            total+=1
            reslist.append(right/total)
        return [len(list(filter(lambda x:x==1, reslist))),errors]
class kFoldCrossValidationRunner:
    def __init__(self, k, classify, actions=["arm", "kick", "neutral"], parsefunc=None):
        self.fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Gaurav1.kineegxval", "rb")
        self.dat=pickle.loads(self.fileobj.read())
        self.k=k
        self.classify=classify
        test=classify()
        
        self.actions=actions
        if not hasattr(test, "train") or not hasattr(test, "classify"):
            raise NonConformingInterface("Not proper classifier")      
    def run(self):
        classlist={}
        reslist=list()
        errors=[]
        unpacked=list()
        for b in self.actions:
            unpacked+=self.dat[b]
            print(unpacked)
        for i in range(self.k):
            classlist={}
            right=0
            total=0
            for j in self.actions:
                temp=self.classify()
                ransam=random.sample(self.dat[j], 1)[0].data
                #print(ransam)
                temp.train(ransam)
                classlist[j]=temp
            for p in unpacked:
                #print("Hi")
                #print(p.data)
                res=[tuple((ki, classlist[ki].classify(p.data))) for ki in classlist]
                if max(res, key =lambda x: x[1])[0]==p.label and not p.label=="neutral" and max(res, key =lambda x: x[1])[1]>=0.79:
                    
                    right+=1
                elif not p.label=='neutral':errors.append(p.label)
                #print(res, p.label)
                if not p.label=="neutral":
                    total+=1
                #print(right, total)
            reslist.append(right/total)
        return [reslist,errors]
    def run2(self):
        classlist={}
        reslist=list()
        errors=[]
        unpacked=list()
        for b in self.actions:
            unpacked+=self.dat[b]
            print(unpacked)
        for t in range(self.k):
            classlist={}
            right=0
            total=0
            random.shuffle(unpacked)
            usey=unpacked[0]
            del unpacked[0]
            dely={}

            curvy={}
            for i in self.actions:
                dely[i]=list(filter(lambda x: x.label==i, unpacked))
                curvy[i]={"F3":[], "F4":[], "T7":[], "T8":[]}
            
            for i in dely:
                for j in ["F3", "F4", "T7", "T8"]:
                    for q in range(len(dely[i][0].data[j])):
                        curvy[i][j].append(statistics.mean([m.data[j][q] for m in dely[i]]))
                    
                
            
            #for j in unpacked:
            
            for j in dely:
            #ransam=random.sample(self.dat[j], 1)[0].data
                #print(ransam)
                temp=self.classify()
                temp.train(curvy[j])
            
                classlist[j]=temp
            #for p in unpacked:
                #print("Hi")
                #print(p.data)
            res=[tuple((ki, classlist[ki].classify(usey.data))) for ki in classlist]
            if max(res, key =lambda x: x[1])[0]==usey.label:
                    
                    right+=1
                #elif not p.label=='neutral':errors.append(p.label)
                #print(res, p.label)
                #if not p.label=="neutral":
            print(usey.label, res)
            total+=1
                #print(right, total)
            reslist.append(right/total)
        return [len(list(filter(lambda x:x==1.0, reslist))),errors]
def DataGather():
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    myApp=kFoldCrossValidationGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "wb"),6)
    myApp.runApp()                
if __name__=='__main__':
    #DataGather()
    listy=[]
    for i in range(1):
        valrunner=kFoldCrossValidationRunner2(100, PolyFitClassifier.PolyBasedClassifier)
        listy.append(valrunner.run())
    print(statistics.mean(listy))
    
                
                
                
            
            
            
            
            
            
            
            
            
            
        

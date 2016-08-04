#CrossValidation.py
import sys
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/Tools")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG")
import CSV_Proc
import SLICERZ
import statistics
import math
class Sample:
    def __init__(self, label, data):
        self.data=data
        self.label=label
class CrossValGatherer:
     def __init__(self, process1,process2,q,dumpto, qevents, labels=["arm", "kick", "neutral"], times):
        self.getter=process1
        self.q=q
        self.times=times
        self.collection={}
        for i in labels:self.collection.update({i:[]})
        self.events=qevents
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
        for i in self.times:
            for i in self.events:
                data_dict[i]={"F3":[], "F4":[], "T7":[], "T8":[]}
            
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
                        for i in data_dict[tp]:
                            data_dict[tp][i].append(data[i][0][2])
                        if len(data_dict[tp]["F3"])==24:
                            for i in data_dict[tp]:
                                del data_dict[tp][i][0]
                            #print(self.livedataclass.test_classifiers_ret(data_dict))
                            raise KeyboardInterrupt
                        
                            
                        print(time.asctime())
                     #a#   self.system_up_time+=16/128
                except:
                    for i in range(32):
                         self.q.recv()
                    print("Train Done")
                    
                   # raise
        for i in data_dict:
            self.collection[i].append(Sample(data_dict[i], i))
        self.getter.terminate()
        self.processer.terminate()
        fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Gaurav1.kineegxval", "wb")
        fileobj.write(pickle.dumps(self.collection))
        fileobj.close()
class NonConformingInterface(Exception):
    pass

class kFoldCrossValidationRunner:
    def __init__(self, filename, k, classify, actions=["arm", "kick", "neutral"], parsefunc=None):
        self.fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Gaurav1.kineegxval", "rb")
        self.dat=pickle.loads(self.fileobj.read())
        self.k=k
        test=classify()
        self.actions=actions
        if not hasattr(test, "train") or not hasattr(test, "run"):
            raise NonConformingInterface("Not proper classifier")      
    def run(self):
        classlist={}
        reslist=list()
        unpacked=list()
        for b in self.actions:
            unpacked+=self.dat[b]
        for i in range(self.k):
            right=0
            total=0
            for j in self.actions:
                temp=classify()
                temp.train(random.sample(self.dat[j], 1)[0])
                classlist[j]=temp
            for p in unpacked:
                res=[tuple((ki, classlist[ki].classify(p.data))) for ki in classlist]
                if max(res, key =lambda x: x[1])[1]>=0.79 and max(res, key =lambda x: x[1])[0]==p.label:
                    right+=1
                total+=1
            reslist.append(right/total)
        
        
                    
                    
                
                
                
                
                
                
            
            
            
            
            
            
            
            
            
            
        

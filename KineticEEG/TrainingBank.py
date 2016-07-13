import pickle
import BaseEEG
import multiprocessing
import ClassifyUtils, statistics
import ctypes
import time
kernel=ctypes.windll.kernel32
def modded_euclidean(inst1, inst2):
    return ClassifyUtils.euclideandistance(inst1, inst2[1], len(inst1))
def MultiRunApp():
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    #print("Start")
    myApp=MultiLiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "rb"))
    #myApp=LiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "wb"))
    myApp.runAppSubprocessed()
def MultiDataGather():
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    #myApp=LiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "rb"))
    myApp=MultiLiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "wb"),["kick", "arm","neutral"],2)
    #print("Move")
    myApp.runApp()    
##def MultiDataGather():
##    q,q1=multiprocessing.Pipe()
##    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
##    q2, q3=multiprocessing.Pipe()
##    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
##    #myApp=LiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "rb"))
##    myApp=MultiLiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "wb"),["kick", "arm","neutral"])
##    #print("Move")
##    myApp.runApp()
class MultiLiveClassifierApplication:
    def __init__(self, process1, process2, q,  profile,subprocessed=True):
        self.getter=process1
        self.processer=process2
        self.profile=profile
        self.q=q
        self.tbank=pickle.loads(self.profile.read())
        self.classs=kNearest(self.tbank, modded_euclidean, False, 1)
       # self.dict_data=pickle.loads(profile.read())
        self.classifiers=dict()
##        if subprocessed:
##             dubs=[]
##             for i in self.dict_data:
##                  dubs.append(tuple((i, self.dict_data[i])))
##             self.classq, q=multiprocessing.Pipe()
##             self.classproc=multiprocessing.Process(target=setup_classifers, args=(q, dubs,))     
##        for i in self.dict_data:
##            curr_class=SLICERZ.LiveRunClassifier()
##            curr_class.run_train(self.dict_data[i])
##            self.classifiers[i]=curr_class
##        self.processer=process2
##        self.thresh,self.d=self.calculate_thresh()
##        print("#####THRESHOLD="+str(self.thresh))
        self.system_up_time=0
    def calculate_thresh(self):
          thresh_select=list()
          for i in self.dict_data:
               for j in self.classifiers:
                    if not j==i:
                         thresh_select.append(self.classifiers[j].test_classifiers_ret(self.dict_data[i]))
          return (max(thresh_select), sorted(thresh_select)[-1]-sorted(thresh_select)[-2])
    def normalized(self, tt):
        return statistics.mean(tt)#*(1-statistics.stdev(tt))

    def runAppSubprocessed(self):
        self.getter.start()
        getpid=self.getter.pid
        procget=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(getpid))
        kernel.SetPriorityClass(procget, 0x0100)
##        self.classproc.start()
##        classpid=self.getter.pid
##        proclass=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(classpid))
##        kernel.SetPriorityClass(proclass, 0x0100)
        self.processer.start()
        procpid=self.processer.pid
        procproc=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(procpid))
        data_dict=dict({"F3":[], "F4":[], "T7":[], "T8":[]})
        print("Enter Loop")
        countr=0
        try:
            while self.getter.is_alive():
                data=self.q.recv()
                #print(data)
                for i in data_dict:
                    data_dict[i].append(data[i][0][2])
                countr=countr+1
                if len(data_dict["F3"])==64:                   #print("In Detector")
                    for i in data_dict:
                        del data_dict[i][0]
                    if (countr%1)==0:
                        print("in class")
                        assembled=data_dict["F3"]+data_dict["F4"]+data_dict["T7"]+data_dict["T8"]
                        #print (len(res1))
                        #print(res)
                        res=self.classs.get_classify_for_next_point(assembled)
                        #kNearest(a, modded_euclidean, False, 2)
                        #if max(res, key=lambda x:x[1])[1]>=0.825 and not max(res, key=lambda x:x[1])[0]=="neutral" and (sorted(res, key=lambda x:x[1])[-1][1]-sorted(res, key=lambda x:x[1])[-2][1])>self.d:
                        print(res)
                        countr+=1
                    #countr=0
                    #print(data_dict)
                    
                #print(time.time())
                self.system_up_time+=16/128
        except:
            self.getter.terminate()
            #self.classproc.terminate()
            self.processer.terminate()
            raise

    def runApp(self):
        self.getter.start()
        getpid=self.getter.pid
        procget=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(getpid))
        kernel.SetPriorityClass(procget, 0x0100)
        self.processer.start()
        procpid=self.processer.pid
        procproc=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(procpid))
        kernel.SetPriorityClass(procproc, 0x0100)
        data_dict=dict({"F3":[], "F4":[], "T7":[], "T8":[]})
        countr=0
        try:
            while self.getter.is_alive():
                data=self.q.recv()
                #print(data)
                for i in data_dict:
                    data_dict[i].append(data[i][0][2])
                countr=countr+1
                if len(data_dict["F3"])==16:
                    #print("In Detector")
                    for i in data_dict:
                        del data_dict[i][0]
                    #if (countr%4)==0:
                    res=[(tr, self.classifiers[tr].test_classifiers_ret(data_dict)) for tr in self.classifiers]
                    #p=multiprocessing.Pool()
                    
                   # res=map(classify_func,res)
                    #print(list(res))
                    res1=list(res)
                    print (len(res1))
                    if max(res, key=lambda x:x[1])[1]>=0.85 and not max(res, key=lambda x:x[1])[0]=="neutral":
                         print(str(max(res, key=lambda x:x[1])[0])+str(max(res, key=lambda x:x[1])))
                    #countr=0
                    #print(data_dict)
                    
                print(time.time())
                self.system_up_time+=16/128
        except:
            self.getter.terminate()
            self.processer.terminate()
            raise
def MultiDataGather():
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    #myApp=LiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "rb"))
    myApp=MultiLiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "wb"),["kick", "arm","neutral"],20)
    #print("Move")
    myApp.runApp()
class MultiLiveTrainingDataGatherer:
     def __init__(self, process1,process2,q,dumpto, qevents, training_sets):
        self.getter=process1
        self.q=q
        self.events=qevents
        self.processer=process2
        self.TBank=TrainingBank()
        self.numtrains=training_sets
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
        self.events=self.events*self.numtrains
        data_dict={"F3":[], "F4":[], "T7":[], "T8":[]}
        for tp in self.events:
            data_dict={"F3":[], "F4":[], "T7":[], "T8":[]}
            
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
                    for i in data_dict:
                        data_dict[i].append(data[i][0][2])
                    if len(data_dict["F3"])==64:
                        for i in data_dict[tp]:
                            del data_dict[tp][i][0]
                        #print(self.livedataclass.test_classifiers_ret(data_dict))
                        raise KeyboardInterrupt
                    
                        
                    print(time.asctime())
                 #a#   self.system_up_time+=16/128
            except Exception as e:
                print(e)
                self.TBank.add_to_bank(tp, data_dict["F3"]+data_dict["F4"]+data_dict["T7"]+data_dict["T8"])
                for i in range(32):
                     self.q.recv()
                print("Train Done")
                
               # raise
        self.getter.terminate()
        self.processer.terminate()
        fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "wb")
        fileobj.write(pickle.dumps(self.TBank))
        fileobj.close()
        


        
class TrainingBank:
    def __init__(self, data_dict=None):
        """Data_dict is list of tuples like so:
              [('arm', {data_dict})]"""
        self.data_dict=data_dict or []
    @classmethod    
    def fromfile(cls, filename):
        f=open(filename, "rb")
        lst_of_dct=pickle.loads(f.read())
        return cls(data_dict=dct)
    def add_to_bank(self,action, data):
        self.data_dict.append(tuple((action, data)))
    def get_data_iter(self):
        return self.data_dict
    def filter_action(self, action):
        training_list=list()
        for i in self.data_dict:
            if i[0]==action:
                training_list.append(i)
        return training_list
class kNearest:
    """Distance function should be a function capable of taking in whatever data type the trainingbank consists of. No type checking is implemented.(Trainingbanktuple[0] should= movement type)"""
    def __init__(self, TBank, distancefunction:callable, high, k):
        self.TBank=TBank
        self.high=high
        self.distance_function=distancefunction
        self.k=k
    def get_classify_for_next_point(self, dpoint):
        sortd=sorted(self.TBank.get_data_iter(),key=lambda x:self.distance_function(dpoint, x), reverse=self.high)
        a=list()
        for i in range(self.k):
            a.append(sortd[i][0])
        try:
            j=statistics.mode(a)
        except statistics.StatisticsError:
            j="Neutral"
        return j

if __name__=='__main__':
    #MultiDataGather()
    MultiRunApp()
##    a=TrainingBank()
##    a.add_to_bank("Arm", [1,2,3,4])
##    a.add_to_bank("Kick", [1,3,5,7])
##    a. add_to_bank("neutral", [1,2,2,-1])
##    a.add_to_bank("Arm", [1,2,3,3.5])
##    a.add_to_bank('Kick', [1,3.5, 5,7])
##    a. add_to_bank("neutral", [1,2,2,-2])
##    #s=pickle.dumps(a)
##    #p=pickle.loads(s)
##    def modded_euclidean(inst1, inst2):
##        return ClassifyUtils.euclideandistance(inst1, inst2[1], len(inst1))
##    b=kNearest(a, modded_euclidean, False, 2)
##    print(b.get_classify_for_next_point([1,2,4,5]))
        
            
        
        
        
        
        
        
    
                
        
        

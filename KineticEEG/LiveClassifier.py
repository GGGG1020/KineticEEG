###Marker.py
import BaseEEG
import multiprocessing
import tkinter
import ctypes
import time
import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/")
import SLICERZ
import pickle
kernel=ctypes.windll.kernel32
##
##class GUIBuild:
##    def __init__(self):
##        self.a=tkinter.Tk()
##        self.a.title("EmoSoft")
##        self.a.geometry("500x500")
##        self.button1=tkinter.Button(self.a, text="Train", command=DataGather)
##        self.button1.pack()
##        self.button2=tkinter.Button(self.a, text="Launch Main", command=RunApp)
##        self.button2.pack()
class MultiLiveTrainingDataGatherer:
     def __init__(self, process1,process2,q,dumpto, qevents):
        self.getter=process1
        self.q=q
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
                    if len(data_dict[tp]["F3"])==32:
                        for i in data_dict[tp]:
                            del data_dict[tp][i][0]
                        #print(self.livedataclass.test_classifiers_ret(data_dict))
                        raise KeyboardInterrupt
                    
                        
                    print(time.asctime())
                 #a#   self.system_up_time+=16/128
            except:
                print("Train Done")
                
               # raise
        self.getter.terminate()
        self.processer.terminate()
        fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "wb")
        fileobj.write(pickle.dumps(data_dict))
        fileobj.close()
        
class LiveTrainingDataGatherer:
    def __init__(self, process1,process2,q,dumpto):
        self.getter=process1
        self.q=q
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
        data_dict=dict({"F3":[], "F4":[], "T7":[], "T8":[]})
            
        print("Move1")
        first=bool(True)
        try:
            while self.getter.is_alive():
                data=self.q.recv()
                if first:
                    
                    print("Move")
                    time.sleep(0)
                    data=self.q.recv()
                    first=False
                for i in data_dict:
                    data_dict[i].append(data[i][0][2])
                if len(data_dict["F3"])==24:
                    for i in data_dict:
                        del data_dict[i][0]
                    #print(self.livedataclass.test_classifiers_ret(data_dict))
                    raise KeyboardInterrupt
                    
                print(time.asctime())
             #a#   self.system_up_time+=16/128
        except:
            self.getter.terminate()
            self.processer.terminate()
            fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "wb")
            fileobj.write(pickle.dumps(data_dict))
            fileobj.close()
            print("Train Done")
class LiveClassifierApplication:
    def __init__(self, process1, process2, q,  profile):
        self.getter=process1
        self.profile=profile
        self.q=q
        self.livedataclass=SLICERZ.LiveRunClassifier()
        self.livedataclass.run_train(pickle.loads(self.profile.read()))
        self.processer=process2
        self.system_up_time=0
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
        try:
            while self.getter.is_alive():
                data=self.q.recv()
                #print(data)
                for i in data_dict:
                    data_dict[i].append(data[i][0][2])
                if len(data_dict["F3"])==24:
                    for i in data_dict:
                        del data_dict[i][0]
                    jj=self.livedataclass.test_classifiers_ret(data_dict)
                    if jj>=0.85:
                        print("You moved")
                        print(jj)
                    #print(data_dict)
                    
                print(time.time())
                self.system_up_time+=16/128
        except:
            self.getter.terminate()
            self.processer.terminate()
            raise
def classify_func(arg):
     return (arg[0], arg[1].test_classifiers_ret(arg[2]))
def setup_classifers(q,doubles):
     a=MultiClassifier(doubles,q)
     a.RunSystem()
     
class MultiClassifier:
     def __init__(self, doubles,q):
          self.classifiers=dict()
          self.q=q
          for i in doubles:
               curr=SLICERZ.LiveRunClassifier()
               curr.run_train(i[1])
               self.classifiers[i[0]]=curr
     def RunSystem(self):
          while True:
               curr=self.q.recv()
               results_vec=[]
               for i in self.classifiers:
                    results_vec.append(tuple((i, self.classifiers[i].test_classifiers_ret(curr))))
               self.q.send(results_vec)
               
               
               
          
class MultiLiveClassifierApplication:
    def __init__(self, process1, process2, q,  profile,subprocessed=True):
        self.getter=process1
        self.profile=profile
        self.q=q
        self.dict_data=pickle.loads(profile.read())
        self.classifiers=dict()
        if subprocessed:
             dubs=[]
             for i in self.dict_data:
                  dubs.append(tuple((i, self.dict_data[i])))
             self.classq, q=multiprocessing.Pipe()
             self.classproc=multiprocessing.Process(target=setup_classifers, args=(q, dubs,))     
        for i in self.dict_data:
            curr_class=SLICERZ.LiveRunClassifier()
            curr_class.run_train(self.dict_data[i])
            self.classifiers[i]=curr_class
        self.processer=process2
        self.system_up_time=0

    def runAppSubprocessed(self):
        self.getter.start()
        getpid=self.getter.pid
        procget=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(getpid))
        kernel.SetPriorityClass(procget, 0x0100)
        self.classproc.start()
        classpid=self.getter.pid
        proclass=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(classpid))
        kernel.SetPriorityClass(proclass, 0x0100)
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
                if len(data_dict["F3"])==32:
                    #print("In Detector")
                    for i in data_dict:
                        del data_dict[i][0]
                    if (countr%4)==0:
                         self.classq.send(data_dict)
                         res=self.classq.recv()
                         #p=multiprocessing.Pool()
                         
                        # res=map(classify_func,res)
                         #print(list(res))
                         res1=list(res)
                         print (len(res1))
                         if max(res, key=lambda x:x[1])[1]>=0.85 and not max(res, key=lambda x:x[1])[0]=="neutral":
                              print(str(max(res, key=lambda x:x[1])[0])+str(max(res, key=lambda x:x[1])))
                         countr+=1
                    #countr=0
                    #print(data_dict)
                    
                print(time.time())
                self.system_up_time+=16/128
        except:
            self.getter.terminate()
            self.classproc.terminate()
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
def DataGather():
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    #myApp=LiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "rb"))
    myApp=LiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "wb"))
    print("Move")
    myApp.runApp()
def RunApp():    
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    print("Start")
    myApp=LiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "rb"))
    #myApp=LiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "wb"))
    myApp.runApp()
def MultiDataGather():
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    #myApp=LiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "rb"))
    myApp=MultiLiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "wb"),["kick", "arm","neutral"])
    #print("Move")
    myApp.runApp()
def MultiRunApp():
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    #print("Start")
    myApp=MultiLiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "rb"))
    #myApp=LiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "wb"))
    myApp.runAppSubprocessed()
if __name__=='__main__':
##    q,q1=multiprocessing.Pipe()
##    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
##    q2, q3=multiprocessing.Pipe()
##    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
##    #myApp=LiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "rb"))
##    myApp=LiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "wb"))
##    myApp.runApp()
     try:
         MultiDataGather()
         MultiRunApp()
     except Exception as e:
          print(e)
          input()
    #a=GUIBuild()
    
    
                      

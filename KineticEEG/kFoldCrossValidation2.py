import sys
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/Tools")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG")
import CSV_Proc
import SLICERZ
import numpy
import statistics
import Polyfit222
import BaseEEG
import CrossCorrelationAlgorithm
import matplotlib.pyplot as plt
import multiprocessing
import math
import random
import time
import ctypes
import DTWKNN
import pickle
import DTWAlg
import csv
FILENAME="C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr"
kernel=ctypes.windll.kernel32   
class ErrorDetectionAlgorithm:
    def __init__(self, classifier, averages_matrix): 
        self.classifier=classifier
    def predict_error(self, sm):
        result=self.classifier.smart_algo(sm)
        result[2]
        
        
        
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
        count=0
        for i in range(self.times):
            for p in self.events:
                data_dict[p]={"F3":[], "F4":[], "FC5":[], "FC6":[]}
            
            for tp in data_dict:
                
                print(tp)
                #time.sleep(1)
                first=bool(True)
                count+=1
                
                try:
                    while self.getter.is_alive():
                        data=self.q.recv()
                        if first:
                            data=self.q.recv()
                            first=False
                        for j in data_dict[tp]:
                            data_dict[tp][j].append(data[j][0][2])
                        if len(data_dict[tp]["F3"])==24:
                            for p in data_dict[tp]:
                                del data_dict[tp][p][0]
                            raise KeyboardInterrupt
                        
                            
                        print(time.asctime())
                     #a#   self.system_up_time+=16/128
                except:
                    for po in range(32):
                         self.q.recv()
                    if not count==3:
                        continue
                    #print(e)
            print(data_dict)
            count=0
            for l in data_dict:
                self.collection[l].append(Sample(l,data_dict[l]))
                print("J")

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
    def __init__(self, k, classify,degree, filename,parsefunc=None):
        self.fileobj=open(filename, "rb")
        self.dat=pickle.loads(self.fileobj.read())
        self.actions=["arm", "kick","neutral"]
        self.deg=degree         
        self.k=k
        self.classify=classify
        test=classify(2)
        self.actions=['arm', 'kick',"neutral"]
    def highpass(self,signal):
        iir_tc=0.98
        background=signal[0]
        hp=list()
        hp.append(0)
        for i in range(1, len(signal)):
            signal[i]=float(signal[i])
            background=(iir_tc*background)+(1-iir_tc)*signal[i]
            hp.append(signal[i]-background)
        return hp
    def car(self,data_dict):
         pp=numpy.matrix([data_dict[j] for j in data_dict])
         count=0
         for j in pp.T:
             avg=statistics.mean(numpy.array(j).flatten())
             for p in data_dict:
                 data_dict[p][count]-=avg
             count+=1
         return data_dict
    def run2(self):
        classlist={}
        reslist=list()
        errors=[]
        unpacked=list()
        for b in self.actions:
            unpacked+=self.dat[b]
        for i in range(self.k):
            classlist={}
            right=0
            total=0
            temp=self.classify(12,4)
            traindict={}
            random.shuffle(unpacked)
            ransam=unpacked[0]
            temp.train({"arm":self.dat["arm"][0].data,"kick":self.dat["kick"][0].data,"neutral":self.dat["neutral"][0].data})
            count=0
            for p in unpacked:
                count+=1
                if temp.smart_algo(p.data).lower()==p.label:
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
            #print("k1")
            unpacked=list()
            for b in self.actions:
                unpacked+=self.dat[b]
            classlist={}
            right=0
            total=0
            self.temp=self.classify(self.deg,4)
            traindict={}
            random.shuffle(unpacked)
            ransam=unpacked[0]
            deff={"arm":[], "kick":[], "neutral":[]}
            for i in unpacked:
                if not i==unpacked[0]:
                    if i.label=='arm':
                        deff['arm'].append(i)
                    elif i.label=='kick':
                        deff['kick'].append(i)
                    elif i.label=='neutral':
                        deff['neutral'].append(i)
            for i in deff:
                if len(deff[i])==6:
                    del deff[i][0]
            count=0
            self.temp.train(deff)
            randat=ransam.data
            labs=[]
            for i in self.temp.classify(randat):
                labs.append(i[0])
            try:guess=statistics.mode(labs)
            except:guess="neutral"
            if guess==ransam.label:
                right+=1
            total+=1
            reslist.append(right/total)
        return [len(list(filter(lambda x:x==1, reslist))),errors]
    def test_for_error_system(self):
        classlist={}
        final_results=list()
        reslist=list()
        errors=[]
        right=0
        pol1=[]
        kfoldtraindata=self.run_for_errors()
        pol2=[]
        wrong2=list()
        right2=list()
        for i in range(self.k):
            unpacked=list()
            for b in self.actions:
                unpacked+=self.dat[b]
            classlist={} 
            total=0
            self.temp=self.classify(self.deg)
            traindict={}
            random.shuffle(unpacked)
            ransam=unpacked[0]
            todelete=[]
            for i in self.actions:
                if not ransam.label==i:
                    todelete.append(i)
            ccc=0  
            del unpacked[0]
            count=0
            for p in unpacked:
                if True:                    
                    self.temp.train({p.label:p.data})
                count+=1
            eroor=Polyfit222.ErrorDetectionAlgorithm(self.temp, kfoldtraindata)
            guess=self.temp.smart_algo(ransam.data)
            if guess[0][0]==ransam.label and eroor.classify(ransam.data)=='right':
                pol1.append(guess[1])
                right2.append(guess[2])
                final_results.append(tuple((guess[1], guess[2], "right")))
                right+=1
            elif not guess[0][0]==ransam.label and eroor.classify(ransam.data)=='wrong':
                pol2.append(guess[1])
                wrong2.append(guess[2])
                final_results.append(tuple((guess[1], guess[2], "wrong")))
                right+=1
                pass
            else: pass
            total+=1
            reslist.append(right/total)
        print(right)
    def run_for_errors(self):
        classlist={}
        final_results=list()
        reslist=list()
        errors=[]
        pol1=[]
        pol2=[]
        wrong2=list()
        right2=list()
        for i in range(self.k):
            unpacked=list()
            for b in self.actions:
                unpacked+=self.dat[b]
            classlist={}
            right=0
            total=0
            self.temp=self.classify(self.deg)
            traindict={}
            random.shuffle(unpacked)
            ransam=unpacked[0]
            todelete=[]
            for i in self.actions:
                if not ransam.label==i:
                    todelete.append(i)
            ccc=0  
            del unpacked[0]
            count=0
            for p in unpacked:
                if True:
                    self.temp.train({p.label:p.data})
                count+=1
            guess=self.temp.smart_algo(ransam.data)
            if guess[0][0]==ransam.label:
                print(ransam.label, guess)
                pol1.append(guess[1])
                right2.append(guess[2])
                final_results.append(tuple((guess[1], guess[2], "right")))
                right+=1
            else:
                pol2.append(guess[1])
                wrong2.append(guess[2])
                final_results.append(tuple((guess[1], guess[2], "wrong")))
            total+=1
            
            reslist.append(right/total)
        return final_results
    def run4(self):
        classlist={}
        final_results=list()
        reslist=list()
        errors=[]
        pol1=[]
        right=0
        pol2=[]
        wrong2=list()
        dt3file=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "rb")
        dt3dat=pickle.loads(dt3file.read())
        right2=list()
        for i in range(self.k):
            unpacked=list()
            for b in self.actions:
                unpacked+=self.dat[b]
            classlist={}
            total=0
            self.temp=self.classify(self.deg)
            traindict={}
            random.shuffle(unpacked)
            ransam=unpacked[0]
            unpacked2=list()
            neutral_store=list()
            del unpacked[0]
            count=0
            for p in unpacked:
                if True:                  
                    self.temp.train({p.label:p.data})
                count+=1
            guess=self.temp.smart_algo_with_neutral(ransam.data)
            if guess[0][0]==ransam.label:
                right+=1
            else:
                pass
            total+=1
        return right
    def run1data(self):
        reslist=list()
        unpacked=list()
        for b in self.actions:
            unpacked+=self.dat[b] #Make list for easy popping
        for i in range(18):#18 times
            testsam=unpacked.pop(0)#Pop
            self.temp=self.classify(self.deg)#Initalize classifier.
            exclude=list()
            #print(testsam.data)
            #print(unpacked)
##            for r in ['arm', 'kick', 'neutral']:
##                if not r==testsam.label:
##                    count=0
##                    for de in unpacked:
##                        #int(de)
##                        if de.label==r:
##                            break
##                        count+=1
##                    #unpacked.pop(count)
##                    exclude.append(count)
##            #print(exclude)
            count2=0          
            for p in unpacked:
                if not count2 in exclude:
                    self.temp.train({p.label:p.data})     #Go through and train the classifier
                count2+=1
            
            guess=self.temp.smart_algo(testsam.data) #Retrieve prediciton
            print(guess, testsam.label)
            if guess[0][0]==testsam.label:
                reslist.append(1) #Test if it is correct
            unpacked.append(testsam)#reappppend item to end of list
        return [sum(reslist)]
    def run1(self):
        reslist=list()
        errors=[]
        pol1=[]
        wrong2=[]
        pol2=[]
        right2=list()
        for i in range(self.k): #For number of times which the loop should occur.
            unpacked=list() #List containing all of the Samples
            for b in self.actions:
                unpacked+=self.dat[b] #Take the samples out of bins.
            self.temp=self.classify(self.deg) #initialize classifier.
            traindict={}
            random.shuffle(unpacked) #Shuffle the list randomly.
            ransam=unpacked[0]#Pop the first item off the list.
            todelete=[]
            for i in self.actions:
                if not ransam.label==i:
                    todelete.append(i)
            ccc=0  
            del unpacked[0]#Delete the first element
            for p in unpacked:
                if True:
                    self.temp.train({p.label:p.data}) #train the classifier with the unused data
            guess=self.temp.smart_algo(ransam.data)#Take the guess of the classifier.
            if guess[0][0]==ransam.label:#Check whether it matches.
                reslist.append(1)
            
        return [sum(reslist), errors]

class kFoldCrossValidationRunner:
    def __init__(self, k, classify,i):
        self.fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "rb")
        self.dat=pickle.loads(self.fileobj.read())
        self.k=k
        self.actions=["arm", "kick", "neutral"]
        self.classify=classify
        test=classify(12)
        self.deg=i
        
#        self.actions=actions
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
        print(type(self.actions))
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
                curvy[i]={"F3":[], "F4":[], "FC5":[], "FC6":[]}
            
            for i in dely:
                for j in ["F3", "F4", "FC5", "FC6"]:
                    for q in range(len(dely[i][0].data[j])):
                        curvy[i][j].append(statistics.mean([m.data[j][q] for m in dely[i]]))
                    
                
            
            #for j in unpacked:
            
            for j in dely:
            #ransam=random.sample(self.dat[j], 1)[0].data
                #print(ransam)
                temp=self.classify(self.deg)
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
    myApp=kFoldCrossValidationGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/nice", "wb"),12)
    myApp.runApp()                
if __name__=='__main__':
    #DataGather()
    print("KineticEEG kFoldCrossValidation2 Simulator")
    listy=[]
    res=[]
    for i in range(40):
        valrunner=kFoldCrossValidationRunner2(1, CrossCorrelationAlgorithm.CrossCorrelationClassifier, i, FILENAME)
        pl=valrunner.run1data()
        #valrunner.test_for_error_system()
        print(pl)
        um=0
    
        for p in listy:
            um+=p[0]

        res.append([i,pl])
    for i in res:
        print([i[0], i[1][0]])
        #outputWriter.writerow([i[0], i[1][0]])

   # outputFile.close()
    plt.plot([tt[1][0] for tt in res])
    plt.show()
    
##    listy=[]
##    for i in range(100):
##        valrunner=kFoldCrossValidationRunner2(2, PolyFitClassifier.PolyBasedClassifier,17)
##        listy.append(valrunner.run())
    
    
##    listy=[]       
##    for i in range(100):
##        valrunner=kFoldCrossValidationRunner(2, SLICERZ.UniformInterfaceLiveRunClassifier)
##        listy.append(valrunner.run2())
##    um=0
##    
##    for i in listy:
##        um+=i[0]
##
##    print(um/200)
	

    
                
                
                
            
            
            
            
            
            
            
            
            
            
        

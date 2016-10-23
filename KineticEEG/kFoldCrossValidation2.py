import sys
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/Tools")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG")
import CSV_Proc
import SLICERZ
import statistics
import Polyfit222 as PolyFitClassifier
import BaseEEG
import matplotlib.pyplot as plt
import multiprocessing
import math
import random
import time
import ctypes
import pickle
import csv
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
    def __init__(self, k, classify,degree,actions=["arm", "kick", "neutral"], parsefunc=None):
        self.fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "rb")
        self.dat=pickle.loads(self.fileobj.read())
        #print(self.dat['kick'])
        for i in self.dat:
            for j in self.dat[i]:
                pass
                #del j.data['FC5']
                #del j.data['FC6']
                #del j.data["F4"]
                #del j.data["F3"]
        #for i in self.dat:
            #for j in self.dat[i]:
               # print(j.data.keys())
                #print(j.data.keys())
        self.deg=degree
        ##for i in self.dat:
            ##for j in range(len(self.dat[i])):
                ##for t in self.dat[i][j]:
                    ##if t.data==self.dat[self.dat[i][j].index(j)+1].data:
                        ##del self.dat[i][j][self.dat[self.dat[i][j].index(j)+1]]
            
                                 
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
            temp=self.classify(6)
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
                #print(temp.classify(p.data), p.label)
                if temp.classify(p.data).lower()==p.label:
                
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
            self.temp=self.classify(self.deg)
            traindict={}
            #for i  in self.actions:
                #traindict[i]=random.sample(self.dat[i], 1)[0].data
            
            random.shuffle(unpacked)
            #print(len(unpacked))
            ransam=unpacked[0]
            #del unpacked[0]
                #print(ransam)
                #traindict[i]=ransam
            #temp.train(traindict)
            #classlist[j]=temp
            deff={"arm":[], "kick":[], "neutral":[]}
            for i in unpacked:
                if not i==unpacked[0]:
                    if i.label=='arm':
                        deff['arm'].append(i)
                        #print("Cool")
                    elif i.label=='kick':
                        deff['kick'].append(i)
                    elif i.label=='neutral':
                        deff['neutral'].append(i)
            #print("Hello")
            count=0

##                    print(len(p.data["F3"]))
##                    for i in p.data["F3"]:
##                             curr_avg=[]
##                             for j in p.data:
##                                 dat[j]=[]
##                             for j in p.data:
##                                 
##                                 curr_avg.append(p.data[j][i])
##                                 
##                             subtract=statistics.mean(curr_avg)
##                             for j in p.data:
##                                 dat[j].append(p.data[j][i]-subtract)
                  
                    
                #print("Hi")
                #rint("Hi")
                #print(p.data)
                #res=[tuple((ki, classlist[ki].classify(p.data))) for ki in classlist]
                #if temp.classify(p.data)[0]==p.label:
                    
                    #right+=1
                #elif not p.label=='neutral':errors.append(p.label)
                #print(res, p.label)
                #if not p.label=="neutral":
                

                #print(right, tota
            self.temp.train(deff)
            randat=ransam.data
##            for i in range( len(ransam.data["F3"])):
##                             curr_avg=[]
##                             for j in ransam.data:
##                                 randat[j]=[]
##                             for j in ransam.data:
##                                 curr_avg.append(ransam.data[j][i])
##                             subtract=statistics.mean(curr_avg)
##                             for j in ransam.data:
##                                 randat[j].append(ransam.data[j][i]-subtract)
            #print(self.temp.classify(randat), ransam.label)
            labs=[]
            for i in self.temp.classify(randat):
                labs.append(i[0])
            try:guess=statistics.mode(labs)
            except:guess=labs[0]
            if guess==ransam.label:
                
                right+=1
            total+=1
            reslist.append(right/total)
        return [len(list(filter(lambda x:x==1, reslist))),errors]
    def run1(self):
        classlist={}
        reslist=list()
        errors=[]
        unpacked=list()
        for b in self.actions:
            unpacked+=self.dat[b]
            #print(unpacked)
        for i in range(self.k):
            print("Hi")
            classlist={}
            right=0
            total=0
            self.temp=self.classify(self.deg)
            traindict={}
            #for i  in self.actions:
                #traindict[i]=random.sample(self.dat[i], 1)[0].data
            random.shuffle(unpacked)
            ransam=unpacked[0]
            todelete=[]
            for i in self.actions:
                if not ransam.label==i:
                    todelete.append(i)
            ccc=0
            
##            while len(todelete>0):
##                ccc=0
##                for i in unpacked:
##                    if i.label in todelete:
##                        del unpacked[ccc]
##                        del todelete[todelete.index(i.label)]
##                        break
##                    else:
##                        ccc+=1
##
            #print("neutral", sum(i.data=='neutral' for i in unpacked))
            #print("arm", sum(i.data=='arm' for i in unpacked))
            #print("neutral", sum(i.data=='neutral' for i in unpacked))
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
            #print(self.temp.classify(ransam.data), ransam.label)
            if self.temp.classify(ransam.data)[0].lower()==ransam.label:
                
                right+=1
            total+=1
            reslist.append(right/total)
        return [len(list(filter(lambda x:x==1, reslist))),errors]
class kFoldCrossValidationRunner2:
    def __init__(self, k, classify,degree, parsefunc=None):
        self.fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "rb")
        self.dat=pickle.loads(self.fileobj.read())
        self.actions=["arm", "kick", "neutral"]
        #print(self.dat['kick'])
        for i in self.dat:
            for j in self.dat[i]:
                pass
                #del j.data['FC5']
                #del j.data['FC6']
                #del j.data["F4"]5
                #del j.data["F3"]
        #for i in self.dat:
            #for j in self.dat[i]:
               # print(j.data.keys())
                #print(j.data.keys())
        self.deg=degree
        ##for i in self.dat:
            ##for j in range(len(self.dat[i])):
                ##for t in self.dat[i][j]:
                    ##if t.data==self.dat[self.dat[i][j].index(j)+1].data:
                        ##del self.dat[i][j][self.dat[self.dat[i][j].index(j)+1]]
            
                                 
        self.k=k
        self.classify=classify
        test=classify(2)
        
        self.actions=['arm', 'kick', 'neutral']
        #if not hasattr(test, "train") or not hasattr(test, "classify"):
            #raise NonConformingInterface("Not proper classifier")
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
            temp=self.classify(12,4)
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
                #print(temp.classify(p.data), p.label)
                if temp.classify(p.data).lower()==p.label:
                
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
            #for i  in self.actions:
                #traindict[i]=random.sample(self.dat[i], 1)[0].data
            
            random.shuffle(unpacked)
            #print(len(unpacked))
            ransam=unpacked[0]
            #del unpacked[0]
                #print(ransam)
                #traindict[i]=ransam
            #temp.train(traindict)
            #classlist[j]=temp
            deff={"arm":[], "kick":[], "neutral":[]}
            for i in unpacked:
                if not i==unpacked[0]:
                    if i.label=='arm':
                        deff['arm'].append(i)
                        #print("j.data", i.data)
                    elif i.label=='kick':
                        deff['kick'].append(i)
                    elif i.label=='neutral':
                        deff['neutral'].append(i)
            for i in deff:
                if len(deff[i])==6:
                    del deff[i][0]
            #print("Hello")
            count=0

##                    print(len(p.data["F3"]))
##                    for i in p.data["F3"]:
##                             curr_avg=[]
##                             for j in p.data:
##                                 dat[j]=[]
##                             for j in p.data:
##                                 
##                                 curr_avg.append(p.data[j][i])
##                                 
##                             subtract=statistics.mean(curr_avg)
##                             for j in p.data:
##                                 dat[j].append(p.data[j][i]-subtract)
                  
                    
                #print("Hi")
                #rint("Hi")
                #print(p.data)
                #res=[tuple((ki, classlist[ki].classify(p.data))) for ki in classlist]
                #if temp.classify(p.data)[0]==p.label:
                    
                    #right+=1
                #elif not p.label=='neutral':errors.append(p.label)
                #print(res, p.label)
                #if not p.label=="neutral":
                

                #print(right, tota

            self.temp.train(deff)

            randat=ransam.data
##            for i in range( len(ransam.data["F3"])):
##                             curr_avg=[]
##                             for j in ransam.data:
##                                 randat[j]=[]
##                             for j in ransam.data:
##                                 curr_avg.append(ransam.data[j][i])
##                             subtract=statistics.mean(curr_avg)
##                             for j in ransam.data:
##                                 randat[j].append(ransam.data[j][i]-subtract)
            #print(self.temp.classify(randat), ransam.label)
            labs=[]
            #print(self.temp.classify(randat))
            for i in self.temp.classify(randat):
                labs.append(i[0])
            try:guess=statistics.mode(labs)
            except:guess="neutral"
            if guess==ransam.label:
                
                right+=1
            total+=1
            reslist.append(right/total)
        return [len(list(filter(lambda x:x==1, reslist))),errors]
    def run1(self):
        classlist={}
        reslist=list()
        errors=[]
        pol1=[]
        pol2=[]
        for i in range(self.k):
            unpacked=list()
            for b in self.actions:
                unpacked+=self.dat[b]
            #print(unpacked)
            classlist={}
            right=0
            total=0
            self.temp=self.classify(self.deg)
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
            todelete=[]
            for i in self.actions:
                if not ransam.label==i:
                    todelete.append(i)
            ccc=0
            del unpacked[0]
            while len(todelete)>0:
                ccc=0
                for i in unpacked:
                    if i.label in todelete:
                        del unpacked[ccc]
                        del todelete[todelete.index(i.label)]
                        break
                    else:
                        ccc+=1
                
##
            
            #print("neutral", sum(i.label=='neutral' for i in unpacked))
            #print("arm", sum(i.label=='arm' for i in unpacked))
            #print("kick", sum(i.label=='kick' for i in unpacked))
            count=0
            for p in unpacked:
                if True:
                    #print(p)
                    
                    self.temp.train({p.label:p.data})
##            for j in self.temp.mat:
##                for i in self.temp.mat[j]:
##                    print(len(self.temp.mat[j][i]))
                    
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
            #print(self.temp.classify(ransam.data), ransam.label)
            #print(self.temp.classify(ransam.data))
            #self.temp.find_most_clustered([])
            guess=self.temp.find_most_clustered(ransam.data)[0][0] 
            if guess==ransam.label:
                #pol1.append(self.temp.classify_old(ransam.data)[0][1])
                #print("Right")
                right+=1
            else:
                #pol2.append(self.temp.classify_old(ransam.data)[0][1])
                pass
            total+=1
            
            reslist.append(right/total)
        #print("Right"+str(statistics.mean(pol1)))
        #print("Wrong"+str(statistics.mean(pol2)))
        return [len(list(filter(lambda x:x==1, reslist))),errors]

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
    outputFile = open('C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/CrossValx{0}.csv'.format(time.asctime().replace(":", " ")), 'w', newline='')
    outputWriter = csv.writer(outputFile)
    listy=[]
    res=[]
    for i in range(1,21):
        valrunner=kFoldCrossValidationRunner2(100, PolyFitClassifier.PolyBasedClassifier, i)
        pl=valrunner.run1()
        print(pl)
        um=0
    
        for p in listy:
            um+=p[0]

        res.append([i,pl])
    for i in res:
        print([i[0], i[1][0]])
        outputWriter.writerow([i[0], i[1][0]])

    outputFile.close()
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
	

    
                
                
                
            
            
            
            
            
            
            
            
            
            
        

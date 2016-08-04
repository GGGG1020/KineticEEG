###Marker.py
import BaseEEG,numpy
import tkinter 
import math
import multiprocessing
import tkinter
import ctypes
import time
import statistics
import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/")
import SLICERZ
import pickle
kernel=ctypes.windll.kernel32
import PyWinMouse
a=PyWinMouse.Mouse()
def highpass(signal):
    iir_tc=0.98
    background=signal[0]
    hp=list()
    hp.append(0)
    for i in range(1, len(signal)):
        signal[i]=float(signal[i])
        background=(iir_tc*background)+(1-iir_tc)*signal[i]
        hp.append(signal[i]-background)
    return hp
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
                for i in range(32):
                     self.q.recv()
                print("Train Done")
                
               # raise
        self.getter.terminate()
        self.processer.terminate()
        fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "wb")
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
                if len(data_dict["F3"])==16:
                    for i in data_dict:
                        del data_dict[i][0]
                    #print(self.livedataclass.test_classifiers_ret(data_dict))
                    raise KeyboardInterrupt
                    
                print(time.asctime())
             #a#   self.system_up_time+=16/128
        except:
            self.getter.terminate()
            self.processer.terminate()
            fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "wb")
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
                if len(data_dict["F3"])==64:
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
        self.thresh,self.d=self.calculate_thresh()
        print("#####THRESHOLD="+str(self.thresh))
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
    def runAppSubprocessedDiffAlgo(self):
        self.getter.start()
        getpid=self.getter.pid
        procget=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(getpid))
        kernel.SetPriorityClass(procget, 0x0100)
        self.classproc.start()
        classpid=self.getter.pid
        self.thresh=0.79
        proclass=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(classpid))
        kernel.SetPriorityClass(proclass, 0x0100)
        self.processer.start()
        procpid=self.processer.pid
        procproc=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(procpid))
        kernel.SetPriorityClass(procproc, 0x0100)
        data_dict=dict({"F3":[], "F4":[], "T7":[], "T8":[]})
        countr=0
        switch_countr=0
        switch=False
        average_q={"kick":[self.thresh], "arm":[self.thresh], "neutral":[self.thresh]}
        running_q={"kick":[], "arm":[], "neutral":[]}
        print("Enter Loop")
        try:
            while self.getter.is_alive():
                data=self.q.recv()
                #print(data)
                for i in data_dict:
                    data_dict[i].append(data[i][0][2])
                countr=countr+1
                if len(data_dict["F3"])==32:                  #print("In Detector")
                    for i in data_dict:
                        del data_dict[i][0]
                    if (countr%4)==0:
                         self.classq.send(data_dict)
                         res=self.classq.recv()
                         print("recv...")
                         #p=multiprocessing.Pool()
                         #a.move_mouse(a.get_mouse_pos()[0], a.get_mouse_pos()[1]+2)
                        # res=map(classify_func,res)
                         #print(list(res))
                         res1=list(res)
                         #print (len(res1))
                         #print(res)
                         for i in res:
                              average_q[i[0]].append(i[1])
                              #print("Here1")
                              if len(running_q[i[0]])==3:
                                   #print("Hi")
                                   del running_q[i[0]][0]
                              running_q[i[0]].append(i[1])
                         final_list=list()
                         if len(running_q["arm"])<3:continue
                         for i in running_q:
                             #print(running_q[i])
                             curr_avg=numpy.average(running_q[i], weights=[1,4,9])
                             if curr_avg>self.thresh:
                                 final_list.append(tuple((i, curr_avg)))
                                 
                         
##                         final_list=list()
##                         for i in average_q:
##                              
##                              #print("Here3")
##                              if not highpass(running_q[i])[-1] in curr_ar and highpass(running_q[i])[-1]>curr_ar.miny:
##                                   final_list.append(tuple((i,highpass(running_q[i])[-1])))
                         if len(final_list)==0:
                              #print("Here4")
                              continue
                         if not switch_countr==3 and switch==True:
                             switch_countr+=1
                             continue
                         if switch_countr==3 and switch ==True:
                            switch_countr=0
                            switch=False
                            continue
                         if len(final_list)==1:
                              percent=final_list[0][1]
                              #print("Here5")
                              #percent=abs(percent-statistics.mean(average_q[final_list[0][0]]))
                              percent=abs(percent-self.thresh)
                              #print(str(max(res, key=lambda x:x[1])[0])+str(sorted(res, key=lambda x:x[1])[-1][1]-sorted(res, key=lambda x:x[1])[-2][1])+str("\n"))
                              if max(res, key=lambda x:x[1])[0]=="kick":
                                   switch=True
                                   a.move_mouse(a.get_mouse_pos()[0], int(a.get_mouse_pos()[1]+(abs(percent*100*60))))
                                   print("Kick"+str(percent))
                              else:
                                    switch=True
                                    print("arm"+str(percent))
                                    a.move_mouse(a.get_mouse_pos()[0], int(a.get_mouse_pos()[1]-(abs(percent*100*60))))
                         else:
                              maxy=max(final_list, key=lambda x:x[1])
                              percent=final_list[0][1]
                              percent=abs(percent-self.thresh)
                              #percent=abs(float(maxy[1])-float(statistics.mean(float(average_q[maxy[0]]))))
                              if maxy[0]=="kick":
                                   switch=True
                                   print("kick"+str(percent))
                                   a.move_mouse(a.get_mouse_pos()[0], int(a.get_mouse_pos()[1]+(abs(percent*100*60))))
                              else:
                                  switch=True
                                  print("arm"+str(percent))
                                  a.move_mouse(a.get_mouse_pos()[0], int(a.get_mouse_pos()[1]-(abs(percent*100*60))))
                         
                              #if max(res, key=lambda x:x[1])[1]>=0.825 and not max(res, key=lambda x:x[1])[0]=="neutral" and (sorted(res, key=lambda x:x[1])[-1][1]-sorted(res, key=lambda x:x[1])[-2][1])>self.d:

                                   
                                   
                         countr+=1
                    #countr=0
                    #print(data_dict)
                    
                #print(time.time())
                self.system_up_time+=16/128
        except:
            self.getter.terminate()
            self.classproc.terminate()
            self.processer.terminate()
            raise

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
        switch_countr=0
        switch=False
        average_q={"kick":[self.thresh], "arm":[self.thresh], "neutral":[self.thresh]}
        running_q={"kick":[], "arm":[], "neutral":[]}
        print("Enter Loop")
        try:
            while self.getter.is_alive():
                data=self.q.recv()
                #print(data)
                for i in data_dict:
                    data_dict[i].append(data[i][0][2])
                countr=countr+1
                if len(data_dict["F3"])==32:                   #print("In Detector")
                    for i in data_dict:
                        del data_dict[i][0]
                    if (countr%4)==0:
                         self.classq.send(data_dict)
                         res=self.classq.recv()
                         #p=multiprocessing.Pool()
                         #a.move_mouse(a.get_mouse_pos()[0], a.get_mouse_pos()[1]+2)
                        # res=map(classify_func,res)
                         #print(list(res))
                         res1=list(res)
                         #print (len(res1))
                         #print(res)
                         for i in res:
                              average_q[i[0]].append(i[1])
                              #print("Here1")
                              if len(running_q[i[0]])==3:
                                   #print("Hi")
                                   del running_q[i[0]][0]
                              running_q[i[0]].append(i[1])
                         #print("Here2")
                         final_list=list()
                         for i in average_q:
                              if len(average_q[i])<=1:
                                   curr_ar=SLICERZ.Area(highpass(average_q[i])[-1], 0)
                              else:
                                   curr_ar=SLICERZ.Area(highpass(average_q[i])[-1], 1*statistics.stdev(highpass(average_q[i])))
                              #print("Here3")
                              if not highpass(running_q[i])[-1] in curr_ar and highpass(running_q[i])[-1]>curr_ar.miny:
                                   final_list.append(tuple((i,highpass(running_q[i])[-1])))
                         if len(final_list)==0:
                              #print("Here4")
                              continue
                         if not switch_countr==3 and switch==True:
                             switch_countr+=1
                             continue
                         if switch_countr==3 and switch ==True:
                            switch_countr=0
                            switch=False
                            continue
                         if len(final_list)==1:
                              percent=final_list[0][1]
                              #print("Here5")
                              #percent=abs(percent-statistics.mean(average_q[final_list[0][0]]))
                              percent=abs(percent-highpass(average_q[final_list[0][0]])[-1])
                              #print(str(max(res, key=lambda x:x[1])[0])+str(sorted(res, key=lambda x:x[1])[-1][1]-sorted(res, key=lambda x:x[1])[-2][1])+str("\n"))
                              if max(res, key=lambda x:x[1])[0]=="kick":
                                   switch=True
                                   a.move_mouse(a.get_mouse_pos()[0], int(a.get_mouse_pos()[1]+(abs(percent*100*60))))
                                   print("Kick"+str(percent))
                              else:
                                    switch=True
                                    print("arm"+str(percent))
                                    a.move_mouse(a.get_mouse_pos()[0], int(a.get_mouse_pos()[1]-(abs(percent*100*60))))
                         else:
                              maxy=max(final_list, key=lambda x:x[1])
                              percent=final_list[0][1]
                              percent=abs(percent-highpass(average_q[final_list[0][0]])[-1])
                              #percent=abs(float(maxy[1])-float(statistics.mean(float(average_q[maxy[0]]))))
                              if maxy[0]=="kick":
                                   switch=True
                                   print("kick"+str(percent))
                                   a.move_mouse(a.get_mouse_pos()[0], int(a.get_mouse_pos()[1]+(abs(percent*100*60))))
                              else:
                                  switch=True
                                  print("arm"+str(percent))
                                  a.move_mouse(a.get_mouse_pos()[0], int(a.get_mouse_pos()[1]-(abs(percent*100*60))))
                         
                              #if max(res, key=lambda x:x[1])[1]>=0.825 and not max(res, key=lambda x:x[1])[0]=="neutral" and (sorted(res, key=lambda x:x[1])[-1][1]-sorted(res, key=lambda x:x[1])[-2][1])>self.d:

                                   
                                   
                         countr+=1
                    #countr=0
                    #print(data_dict)
                    
                #print(time.time())
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
                if len(data_dict["F3"])==64:
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
    myApp=LiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "wb"))
    print("Move")
    myApp.runApp()
def RunApp():    
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    print("Start")
    myApp=LiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "rb"))
    #myApp=LiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "wb"))
    myApp.runApp()
def MultiDataGather():
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    #myApp=LiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "rb"))
    myApp=MultiLiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "wb"),["kick", "arm","neutral"])
    #print("Move")
    myApp.runApp()
def MultiRunApp():
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    #print("Start")
    myApp=MultiLiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "rb"))
    #myApp=LiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "wb"))
    myApp.runAppSubprocessedDiffAlgo()
class GUIBuild:
    def __init__(self):
        self.a=tkinter.Tk()
        self.a.title("EmoSoft")
        self.a.geometry("500x500")
        self.button1=tkinter.Button(self.a, text="Train", command=MultiDataGather)
        self.button1.pack()
        self.button2=tkinter.Button(self.a, text="Launch Main", command=lambda:self.execute)
        self.button2.pack()
    def execute(self):
        self.a.destroy()
        MultiRunApp()
        
if __name__=='__main__':
##    q,q1=multiprocessing.Pipe()
##    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
##    q2, q3=multiprocessing.Pipe()
##    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
##    #myApp=LiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "rb"))
##    myApp=LiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.dat", "wb"))
##    myApp.runApp()
##    GUIBuild()
     try:
         if ctypes.windll.user32.MessageBoxA(0, "Use old training?", "KineticEEG Training System", 0x00000004)==6:
              MultiDataGather()
         print("Start Session")
         MultiRunApp()
     except Exception as e:
          print(e)
          input()
    #a=GUIBuild()
    
    
                      

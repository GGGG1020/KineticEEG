###Marker.py
import BaseEEG
import multiprocessing
import tkinter
import time
class MarkerApplication:
    def __init__(self, process1, process2, q, dumpto):
        self.getter=process1
        self.q=q
        self.processer=process2
        assert hasattr(dumpto, "write")
        self.print=dumpto.write
        self.closedump=dumpto.close
        self.markers=list()
        self.system_up_time=0
    def writelines(self,line):
        for d in line:
            if d is not None:
                self.print(str(d)+', ')
    def registerMarker(self, marker, delay):
        self.markers.append(tuple((marker, self.system_up_time+delay)))
    def checkMarkerStatus(self):
        for i in self.markers:
            if self.system_up_time==i[1]:
                del self.markers[self.markers.index(i)]
                return i
        
            elif (abs(self.system_up_time-i[1])<=5):
                print('Please {0} in {1}'.format(i, (self.system_up_time-i[1])))
    def runApp(self):
        self.getter.start()
        print(self.getter.pid)
        self.processer.start()
        print(self.processer.pid)
        try:
            while self.getter.is_alive():
                #print("Entered Loop")
                data=self.q.recv()
                if type(data)==str:print(data)
                #print("Got data"+str(len(data)))
                #print("Data"+str(data))
                if not type(data)==str:print([len(data[i]) for i in data])
                print(self.processer.is_alive())
                #print(data)
                self.system_up_time+=16/128
                ms=self.checkMarkerStatus()
                #print(self.system_up_time)
##                for i in data:
##                    i.append(ms)
##                self.writelines(data) 
        except:
            self.getter.terminate()
            #self.processer.terminate()
            self.closedump()
            raise
if __name__=='__main__':
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    myApp=MarkerApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/gauravArm.csv", "w"))
    myApp.registerMarker("kick", 60)
    myApp.registerMarker("Arm", 120)
    print("registered")
    myApp.runApp()
    
                      

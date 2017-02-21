#Placement Detector.py
import ClassifyUtils
import statistics
import math
import pickle
from Polyfit222 import Sample
import numpy.polynomial as poly
class PlacementDetector:
    def __init__(self, trainbank):
        self.trainbank=[]
        count=0
        for i in trainbank:
            for p in i['neutral']:
                    for t in p.data:
                        p.data[t]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(p.data[t]))), p.data[t], 7)).coef
            self.trainbank+=i['neutral']
            count+=1
            print(i)
            
        print(len(self.trainbank))
        print(count)
    def placement_check(self, signal):
        ty=list()
        #print("TYPE SIGNAL:", type(signal))
        for i in signal.data:
            signal.data[i]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(signal.data[i]))), signal.data[i], 7)).coef
        print(len(self.trainbank))
        for i in self.trainbank:
            ty.append(ClassifyUtils.euclideandistance(i.data["FC5"]+i.data["FC6"]+i.data["F3"]+i.data['F4'], signal.data["FC5"]+signal.data["FC6"]+signal.data["F3"]+signal.data['F4'],
                                                      min(len(i.data["FC5"]+i.data["FC6"]+i.data["F3"]+i.data['F4']),len(signal.data["FC5"]+signal.data["FC6"]+signal.data["F3"]+signal.data['F4']) ))
)
        print(math.floor(ty.index(min(ty))/6))
        print(ty)
        return statistics.mean(ty)
if __name__=='__main__':
    f1=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Favorites/Trainingdata (8).kineegtr", "rb")
    f2=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Favorites/Trainingdata (9).kineegtr", "rb")
    f3=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles//Favorites/Trainingdata (2).kineegtr", "rb")
    f4=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Favorites/Trainingdata (3).kineegtr", "rb")
    b=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Favorites/Trainingdata (2).kineegtr", "rb")
    a=PlacementDetector([pickle.loads(f1.read()), pickle.loads(f2.read()), pickle.loads(f3.read()), pickle.loads(f4.read())])
    statbin=list()
    stor=pickle.loads(b.read())['neutral']
    print(len(stor))
    for j in stor:
        print(j)
        statbin.append(a.placement_check(j))
    print(statistics.mean(statbin))
    print(statistics.stdev(statbin))

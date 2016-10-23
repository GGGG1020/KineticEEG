#Autocluster.py
import sys
import statistics
import Polyfit222 as PolyFitClassifier
import BaseEEG
import matplotlib.pyplot as plt
import statistics
import itertools
import numpy.polynomial as poly
import ClassifyUtils
def euclideandistance(inst1, inst2, leng):
    d=0
    for i in range(leng):
        d+=(inst1[i]-float(inst2[i]))/inst2[i]
    return d/leng
class AutoCluster:
    def __init__(self, dataset):
        self.new_data={}
        for i in ['arm', 'kick', 'neutral']:
            avg=list()
            for j in (itertools.combinations(dataset[i],2)):
                avg.append(euclideandistance(j[0].data, j[1].data, len(j[0].data)))
            avg1=statistics.mean(avg)
            print("Average", avg1)
            st=statistics.stdev(avg)
            print("STDEV", st)
            count=0
            for m in dataset[i]:
                localavg=list()
                for j in dataset[i]:
                    if not m==j:
                        avg.append(euclideandistance(m.data, j.data, len(j.data)))
                if statistics.mean(avg)>(avg1+st):
                    print("removing..", i)
                    del dataset[i][count]
                else:
                    count+=1
        
        print(dataset)
        for i in dataset:
            print(len(dataset[i]))
    def tooclose():
        for i in itertools.combinations(['arm', 'kick', 'neutral'],2):
             avg=list()
             for j in listy[i[0]]:
                 for k in listy[i[1]]:
                     avg.append(ClassifyUtils.euclideandistance(j.data, k.data, len(j.data)))
             print(str(i[0]+"v."+i[1])+str(sum(avg)/len(avg)))
             for j in kkkkkkkk
class AutoCluster2:
    def __init__(self, dataset):
        self.new_data={}
        for i in ['arm', 'kick', 'neutral']:
            avg=list()
            for j in (itertools.combinations(dataset[i],2)):
                map1={}
                for l in j[0]:
                    map1[l]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(j[0][l]))), j[0][l], self.deg))
                for l in j[1]:
                    map2[l]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(j[1][l]))), j[1][l], self.deg))
                
                
            avg1=statistics.mean(avg)
            print("Average", avg1)
            st=statistics.stdev(avg)
            print("STDEV", st)
            count=0
            for m in dataset[i]:
                localavg=list()
                for j in dataset[i]:
                    if not m==j:
                        avg.append(ClassifyUtils.euclideandistance(m.data, j.data, len(j.data)))
                if statistics.mean(avg)>(avg1+st):
                    print("removing..", i)
                    del dataset[i][count]
                else:
                    count+=1
        
        print(dataset)
        for i in dataset:
            print(len(dataset[i]))
class PolyBasedClassifier:
    def __init__(self,degree):
        self.mat={}
        self.deg=degree
        self.actions=['arm', 'kick', 'neutral']
        for i in self.actions:self.mat.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
    def train(self, data):
        #for i in data:
        for i in data:
            #print("Check 1")
            for j in data[i]:
                #print(j)
                #print("Check 2")
                #print(data[i][j])
                self.mat[i][j].append(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[i][j]))), data[i][j], self.deg)))
                #print("Check3")
        #print("Trained")
        
    def classify(self, data):
        mat2={}
        for i in data:
                mat2[i]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[i]))), data[i], self.deg))
        output=self.k_nn(mat2)
        return output
    def k_nn(self, data):
        pp=[]
        avg=[]
        count=0
        for i in self.mat:
            total=0
            for m in self.mat[i]:
                count=0
                for j in self.mat[i][m]:
                    total+=ClassifyUtils.euclideandistance(j.coef, data[m].coef, self.deg)
                    count+=1
                    #avg.append(ClassifyUtils.euclideandistance(j.coef, data[m].coef, self.deg))
            #print(count)
            pp.append(tuple((i, total)))
            avg=[]
        return pp        
if __name__=='__main__':
    f=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "rb")
    import pickle
    from Polyfit222 import Sample
    a=pickle.loads(f.read())
    deg=5
    
##    for i in a:
##        print(i, ":")
##        for p in a[i]:
            
    for i in a:
        for j in a[i]:
            j.data=list(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(j.data['F3']))),j.data["F3"], deg)).coef)+list(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(j.data['F4']))),j.data["F4"], deg)).coef)+list(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(j.data['FC5']))), j.data["FC5"], deg)).coef)+list(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(j.data['FC6']))),j.data["FC6"], deg)).coef)
            #j.data=list(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(j.data["FC5"]))),j.data["FC5"], deg).coef))))+list(poly.polynomial.Polynomial(poly.polynomial.polyfit(len(j.data["FC6"]),j.data["FC6"], deg).coef))+list(poly.polynomial.Polynomial(poly.polynomial.polyfit(len(j.data["F3"]),j.data["F3"], deg).coef))+list(poly.polynomial.Polynomial(poly.polynomial.polyfit(len(j.data["F4"]),j.data["F4"], deg).coef))
    for i in a:
        for j in a[i]:
            print(i, j.data)
    tt=AutoCluster(a)
    
    
        

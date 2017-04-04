#Neutral or Movement Classifier


import pickle
import sys
import numpy
import numpy.polynomial as poly
from Polyfit222 import Sample
import statistics
import ClassifyUtils
import Polyfit222
from itertools import chain
import random
import itertools
import BaseEEG
import matplotlib.pyplot as plt
FILENAME="C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Favorites/KineticEEGProgamFiles/Favorites/Trainingdata (13).kineegtr"


class PolyBasedClassifier:
    def __init__(self,degree, actions=["arm", "kick", "neutral"]):
        self.mat={}
        self.deg=degree
        self.actions=actions
        for i in actions:self.mat.update({i:[]})
        for i in self.actions:self.mat.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
    def train(self, data):
    
        for i in data:
            for j in data[i]:
                self.mat[i][j].append(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[i][j]))), data[i][j], self.deg)))
                #print(self.mat)
                #self.mat[i][j].append(data[i][j])

        #print(self.mat)
                
    def classify(self, data):
        mat2={}
        for i in data:
                mat2[i]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[i]))), data[i], self.deg))
                #mat2[i]=data[i]
        output=self.k_nn_old(mat2)
        num=abs(sorted(output, key=lambda x:x[1])[0][1]-sorted(output, key=lambda x:x[1])[1][1])
        return [min(output, key=lambda x:x[1]), num]
    def smart_algo(self, data):
    
        matp={"F3":[], "F4":[], "FC5":[], "FC6":[]}
        mat2={}
        #for i in self.actions:mat2.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
        throttle={}
        rule={}
        for i in self.actions:
            #print(i)
            
            for j in self.mat[i]:
                #print(mat[i][j])
                initlist=[]
                for p in itertools.combinations(self.mat[i][j], 2):
                    #print(str(i+"v"+j))
                    initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[1].coef)))
                #print(str(i+"v"+j))
                matp[j].append(statistics.mean(initlist))
            #for b in matp:
            #print(len(self.mat['kick']['FC5']))
            minst=min(matp, key=lambda x:statistics.mean(matp[x]))
            #print(minst)
            matr=numpy.matrix([i.coef for i in self.mat[i][minst]])
            final=list()
            #rule[minst]=[]
            for j in matr.T:
                #print(j)
                final.append(statistics.mean(numpy.array(j).flatten()))
                #print(Final")
            rule[i]={minst:final}
        for p in data:
            mat2[p]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[p]))), data[p], self.deg))
        for d in rule:
            #print(d)
            for tt in rule[d]:
                sum1=0
                #for ppp in rule[d][tt]:
                sum1+=ClassifyUtils.euclideandistance(mat2[tt].coef, rule[d][tt],len(rule[d][tt]))
                    
                throttle[d]=(sum1/1)
                
    
        return [[min(throttle, key=lambda x:throttle[x])], throttle[min(throttle, key=lambda x:throttle[x])]-throttle[sorted(throttle, key=lambda x:throttle[x])[1]],throttle[min(throttle, key=lambda x:throttle[x])] ]
        
            
                
            
            
            

    def k_nn_old(self, data):
        pp=[]
        totallist=[]
        for i in self.mat:
            total=0
            for m in self.mat[i]:
                totallist.clear()
                #print(self.mat[i][m])
                for j in list(sorted(self.mat[i][m], key=lambda x:ClassifyUtils.euclideandistance(x.coef, data[m].coef, self.deg+1))):
                    totallist.append(ClassifyUtils.euclideandistance(j.coef, data[m].coef, self.deg+1))
                #totallist.append(0)
                if 0 in totallist:print("OOps")
                totallist=list(filter(lambda x: (x>=(statistics.mean(totallist)-3*statistics.stdev(totallist)) and x<=(statistics.mean(totallist)+3*statistics.stdev(totallist))), totallist))
                
                
                total+=sum(totallist)
            pp.append(tuple((i, total)))
        return pp
    def k_nn(self, data):
        pp=[]
        #print(len(self.mat['arm']['F3']),"Mat")
        for i in self.mat:
            
            for m in self.mat[i]:
                pp.append((i,m.euclidean_distance_between(data)))
               
        return pp
    
def kfold(deg):
    fat=open(FILENAME, "rb")
    dat=pickle.loads(fat.read())
    #print(dat)
    dat2={"Move":list(dat['arm']+dat['kick']), 'neutral':dat['neutral']}
    #print(dat2)
    upacked=list()
    for i in dat2['Move']:
        if i.label in ['arm', 'kick']:
            i.label="Move"
    for i in ["Move",'neutral']:
        for j in dat2[i]:
            upacked.append(j)
    random.shuffle(upacked)
    ransam=upacked[0]
    del upacked[0]
    cla=PolyBasedClassifier(10, actions=['Move', 'neutral'])
    for i in upacked:
        cla.train({i.label:i.data})
    if cla.smart_algo(ransam.data)[0][0]==ransam.label:
        #print(cla.smart_algo(ransam.data)[0],ransam.label)
        return 1
    else:
        #print(cla.smart_algo(ransam.data),ransam.label)
        return 0
        
    
    
for deg in range(21):
    indx=0
    for i in range(100):
        indx+=kfold(deg)
    print(indx)

import numpy
import numpy.polynomial as poly
import ClassifyUtils
import multiprocessing
import BaseEEG
import statistics
import ctypes
import itertools
import kFoldCrossValidation2
import statistics
import time
import pickle
kernel=ctypes.windll.kernel32
class Sample:
    def __init__(self, label, data):
        self.data=data
        self.label=label
    def euclidean_distance_between(self, other):
        tote=0
        for i in self.data:
            tote+=ClassifyUtils.euclideandistance(self.data[i].coef, other.data[i].coef, len(self.data[i].coef))
        return tote
class ErrorDetectionAlgorithm:
    """This is a k-Nearest Neighbor Classifier to find the erronous classifications made"""
    def __init__(self, classifier, kfoldresults):
        '''kfoldresults is a tuple containing the different fields ending in class (CORRECT/INCORRECT)'''
        self.classifier=classifier
        self.kfoldresults=kfoldresults
    def classify(self, sample):
        results=self.classifier.smart_algo(sample)
        results=results[1:3]
        self.results=[]
        for i in self.kfoldresults:
            self.results.append([ClassifyUtils.euclideandistance(i[0:2], results,2), i[-1]])
        self.results=sorted(self.results, key=lambda x:x[0])
        listy=list()
        for i in self.results[0:10]:
            if not i[0]==0:
                listy.append(i[-1])
        try:
            guess=statistics.mode(listy)
        except:
            guess='tie'
        return guess
def RunErrorDetectionApp(file, deg):
    crossval=kFoldCrossValidation2.kFoldCrossValidationRunner2(100,PolyBasedClassifier, deg)
    output=crossval.run_for_errors()
    jk=ErrorDetectionAlgorithm(crossval.temp, output)
class PolyBasedClassifier:
    def __init__(self,degree, actions=["arm", "kick", "neutral"]):
        self.mat={} #self.mat will contain the data for each action, for each variable.
        self.deg=degree #Degree of fit
        self.actions=actions #List of actions.
        for i in actions:self.mat.update({i:[]})
        for i in self.actions:self.mat.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})#Set up data structure per action, per sensor
    def train(self, data):
        for i in data: #i will equal the current action 
            for j in data[i]:#j is the current sensor 
                self.mat[i][j].append(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[i][j]))), data[i][j], self.deg))) #Supply the data for a polynomial fit(seconds vs EEG Mu wave power)
    
    def train2(self, data):
        for i in data: #i will equal the current action 
            for j in data[i]:#j is the current sensor 
                self.mat[i][j].append(data[i][j]) #Supply the data for a polynomial fit(seconds vs EEG Mu wave power)
    
    def classify(self, data):
        mat2={}
        for i in data:
                mat2[i]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[i]))), data[i], self.deg))
                #mat2[i]=data[i]
        output=self.k_nn_old(mat2)
        num=abs(sorted(output, key=lambda x:x[1])[0][1]-sorted(output, key=lambda x:x[1])[1][1])
        return [min(output, key=lambda x:x[1]), num]
    def cross_classify(self, data, rule_vectors):
        results=dict()
        for i in rule_vectors:
            for j in i:
                results[i]=(i,ClassifyUtils.euclideandistance(data[j].coef, rule[i][j],len(rule[i][j])))
        return min(results, key=lambda x: results[x][1])
    def smart_algo_2(self, data):
        matp={"F3":[], "F4":[], "FC5":[], "FC6":[]} #Data structrure for the incoming data(Multiple pieces of data not needed)
        mat2={}#dictionary
        #for i in self.actions:mat2.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
        throttle={}
        rule={}
        boundarypoints={"arm":{}, 'kick':{}}
        for i in ['arm', 'kick']:
            for j in self.mat[i]:
                initlist=[]
                for p in itertools.combinations(self.mat[i][j], 2):
                    initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[1].coef)))
                boundarypoints[i][j]=initlist
                matp[j].append(statistics.mean(initlist))
        for i in ['arm', 'kick','neutral']:
            minst=min(matp, key=lambda x:statistics.mean(matp[x]))
            matr=numpy.matrix([i.coef for i in self.mat[i][minst]])
            final=list()
            for j in matr.T:
                final.append(statistics.mean(numpy.array(j).flatten()))
            rule[i]={minst:final}
        for p in data:
            mat2[p]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[p]))), data[p], self.deg))
        for d in ['arm', 'kick']:
            for tt in rule[d]:
                sum1=0
                sum1+=ClassifyUtils.euclideandistance(mat2[tt].coef, rule[d][tt],len(rule[d][tt]))
                throttle[d]=(sum1/1)
        if throttle[min(throttle, key=lambda x:throttle[x])]>(numpy.percentile(boundarypoints[min(throttle, key=lambda x:throttle[x])][minst],95)+(2*statistics.stdev(boundarypoints[min(throttle, key=lambda x:throttle[x])][minst]))):
            return [["neutral"]]
        return [[min(throttle, key=lambda x:throttle[x])], throttle[min(throttle, key=lambda x:throttle[x])]-throttle[sorted(throttle, key=lambda x:throttle[x])[1]],throttle[min(throttle, key=lambda x:throttle[x])]]
        
    def smart_algo_knearest(self, data):    
        matp={"F3":[], "F4":[], "FC5":[], "FC6":[]}#Data structrure for the incoming data(Multiple pieces of data not needed)
        mat2={}
        #for i in self.actions:mat2.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
        throttle={}
        rule={}
        for i in ['arm', 'kick', "neutral"]:#Associative rule mining phase
            for j in self.mat[i]:# for sensor in action(j is the current sensor)
                initlist=[]#initlist is a list which one will append the distances alculated to.This is done for statistical purposes
                for p in itertools.combinations(self.mat[i][j], 2):#For the 6 choose two combinations of two polynomial object ifor a given movement, sensor
                    initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[1].coef)))#Append the euclidean distance between the two .
                matp[j].append(statistics.mean(initlist))#Append the mean of all of the distances for this sensor.
        for i in ['arm', 'kick','neutral']:#Going through each action
            minst=min(matp, key=lambda x:statistics.mean(matp[x]))# Find the most clustered sensor by finding the minimum average distance over the three actions.
            matr=numpy.matrix([p.coef for p in self.mat[i][minst]])#Creation of a numpy matrix 
            final=list()#List to contain rules.
            finalfinal=list
            #for j in matr.T: #Transposition of the matrix
                #final.append(statistics.median(numpy.array(j).flatten()))#Flatten the row and average it in order to create the rule vector.
            #finalfinal=(min(matr, key=lambda x:ClassifyUtils.euclideandistance(x.tolist()[0], final, len(final))))
            rule[i]={minst:matr}
        for p in data: #Exit Training phase, begin work on live data.
            mat2[p]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[p]))), data[p], self.deg))#Featurize(find the polynomial fit of) the data
        
        for d in rule: #Classification phase-Iterate over actions
            for tt in rule[d]: #Iterate over sensor(ONly one sensor, no true iteration)
                sum1=0#Assign variable
                count=0
                for q in rule[d][tt]:
                    sum1+=ClassifyUtils.euclideandistance(mat2[tt].coef, q.tolist()[0],len(q.tolist()[0]))#Add the Euclidean Distance between sample and rule
                    count+=1
                throttle[d]=(sum1/count)#append information to dictionary
        return [[min(throttle, key=lambda x:throttle[x])],
                throttle[min(throttle, key=lambda x:throttle[x])]-throttle[sorted(throttle, key=lambda x:throttle[x])[1]],throttle[min(throttle, key=lambda x:throttle[x])] ] #Return classification.
    def smart_algo(self, data):    
        matp={"F3":[], "F4":[], "FC5":[], "FC6":[]}#Data structrure for the incoming data(Multiple pieces of data not needed)
        mat2={}
        #for i in self.actions:mat2.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
        throttle={}
        rule={}
        for i in ['arm', 'kick', "neutral"]:#Associative rule mining phase
            for j in self.mat[i]:# for sensor in action(j is the current sensor)
                initlist=[]#initlist is a list which one will append the distances alculated to.This is done for statistical purposes
                for p in itertools.combinations(self.mat[i][j], 2):#For the 6 choose two combinations of two polynomial object ifor a given movement, sensor
                    initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[1].coef)))#Append the euclidean distance between the two .
                matp[j].append(statistics.mean(initlist))#Append the mean of all of the distances for this sensor.
        for i in ['arm', 'kick','neutral']:#Going through each action
            minst=min(matp, key=lambda x:statistics.mean(matp[x]))# Find the most clustered sensor by finding the minimum average distance over the three actions.
            matr=numpy.matrix([p.coef for p in self.mat[i][minst]])#Creation of a numpy matrix 
            final=list()#List to contain rules.
            finalfinal=list
            for j in matr.T: #Transposition of the matrix
                final.append(statistics.median(numpy.array(j).flatten()))#Flatten the row and average it in order to create the rule vector.
            finalfinal=(min(matr, key=lambda x:ClassifyUtils.euclideandistance(x.tolist()[0], final, len(final))))
            rule[i]={minst:finalfinal.tolist()[0]}
        for p in data: #Exit Training phase, begin work on live data.
            mat2[p]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[p]))), data[p], self.deg))#Featurize(find the polynomial fit of) the data
        for d in rule: #Classification phase-Iterate over actions
            for tt in rule[d]: #Iterate over sensor(ONly one sensor, no true iteration)
                sum1=0#Assign variable
                #for ppp in rule[d][tt]:
                sum1+=ClassifyUtils.euclideandistance(mat2[tt].coef, rule[d][tt],len(rule[d][tt]))#Add the Euclidean Distance between sample and rule
                throttle[d]=(sum1/1)#append information to dictionary
        return [[min(throttle, key=lambda x:throttle[x])],
                throttle[min(throttle, key=lambda x:throttle[x])]-throttle[sorted(throttle, key=lambda x:throttle[x])[1]],throttle[min(throttle, key=lambda x:throttle[x])] ] #Return classification.
    def smart_algo_neutral(self, data):
        matp={"F3":[], "F4":[], "FC5":[], "FC6":[]}
        mat2={}
        throttle={}
        min_sensor=list()
        rule={}
        for i in ['arm', 'kick']:
            for j in self.mat[i]:
                initlist=[]
                for p in itertools.combinations(self.mat[i][j], 2):
                    initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[1].coef)))
                matp[j].append(statistics.mean(initlist))
            minst=min(matp, key=lambda x:statistics.mean(matp[x]))
            min_sensor.append(minst)
            matp={"F3":[], "F4":[], "FC5":[], "FC6":[]}
            matr=numpy.matrix([t.coef for t in self.mat[i][minst]])
            final=list()
            for j in matr.T:
                final.append(statistics.mean(numpy.array(j).flatten()))
            rule[i]={minst:final}
        for i in ['neutral']:
            subdict=dict()
            for j in list(set(min_sensor)):
                matr=numpy.matrix([t.coef for t in self.mat[i][j]])
                final=list()
                for q in matr.T:
                    final.append(statistics.mean(numpy.array(q).flatten()))
                subdict[j]=final
            rule[i]=subdict
        for p in data:
            mat2[p]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[p]))), data[p], self.deg))
        for d in ['arm', 'kick']:
            sum1=0
            for tt in rule[d]:
                sum1+=ClassifyUtils.euclideandistance(mat2[tt].coef, rule[d][tt],len(rule[d][tt]))
                throttle[d]=(sum1/1)
        for d in ['neutral']:
            minlist=list()
            for tt in rule[d]:
                minlist.append(ClassifyUtils.euclideandistance(mat2[tt].coef, rule[d][tt],len(rule[d][tt])))
            throttle[d]=max(minlist)
        return [[min(throttle, key=lambda x:throttle[x])], throttle[min(throttle, key=lambda x:throttle[x])]-throttle[sorted(throttle, key=lambda x:throttle[x])[1]],throttle[min(throttle, key=lambda x:throttle[x])] ]
    def k_nn_old(self, data):
        pp=[]
        totallist=[]
        for i in self.mat:
            total=0
            for m in self.mat[i]:
                totallist.clear()
                for j in list(sorted(self.mat[i][m], key=lambda x:ClassifyUtils.euclideandistance(x.coef, data[m].coef, self.deg+1))):
                    totallist.append(ClassifyUtils.euclideandistance(j.coef, data[m].coef, self.deg+1))
                if 0 in totallist:print("OOps")
                totallist=list(filter(lambda x: (x>=(statistics.mean(totallist)-3*statistics.stdev(totallist)) and x<=(statistics.mean(totallist)+3*statistics.stdev(totallist))), totallist))
                total+=sum(totallist)
            pp.append(tuple((i, total)))
        return pp
    def k_nn(self, data):
        pp=[]
        for i in self.mat:
            for m in self.mat[i]:
                pp.append((i,m.euclidean_distance_between(data)))
        return pp
##class CrossCorrelationClassifier:
##    def __init__(self,degree, actions=["arm", "kick", "neutral"]):
##        self.mat={} #self.mat will contain the data for each action, for each variable.
##        self.deg=degree #Degree of fit
##        self.actions=actions #List of actions.
##        for i in actions:self.mat.update({i:[]})
##        for i in self.actions:self.mat.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})#Set up data structure per action, per sensor
##    def train(self, data):
##        for i in data: #i will equal the current action 
##            for j in data[i]:#j is the current sensor 
##                self.mat[i][j].append(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[i][j]))), data[i][j], self.deg))) #Supply the data for a polynomial fit(seconds vs EEG Mu wave power)
##    
##    def train2(self, data):
##        for i in data: #i will equal the current action 
##            for j in data[i]:#j is the current sensor 
##                self.mat[i][j].append(data[i][j]) #Supply the data for a polynomial fit(seconds vs EEG Mu wave power)
##    
##    def classify(self, data):
##        mat2={}
##        for i in data:
##                mat2[i]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[i]))), data[i], self.deg))
##                #mat2[i]=data[i]
##        output=self.k_nn_old(mat2)
##        num=abs(sorted(output, key=lambda x:x[1])[0][1]-sorted(output, key=lambda x:x[1])[1][1])
##        return [min(output, key=lambda x:x[1]), num]
##    def cross_classify(self, data, rule_vectors):
##        results=dict()
##        for i in rule_vectors:
##            for j in i:
##                results[i]=(i,ClassifyUtils.euclideandistance(data[j].coef, rule[i][j],len(rule[i][j])))
##        return min(results, key=lambda x: results[x][1])
##    def smart_algo_2(self, data):
##        matp={"F3":[], "F4":[], "FC5":[], "FC6":[]} #Data structrure for the incoming data(Multiple pieces of data not needed)
##        mat2={}#dictionary
##        #for i in self.actions:mat2.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
##        throttle={}
##        rule={}
##        boundarypoints={"arm":{}, 'kick':{}}
##        for i in ['arm', 'kick']:
##            for j in self.mat[i]:
##                initlist=[]
##                for p in itertools.combinations(self.mat[i][j], 2):
##                    initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[1].coef)))
##                boundarypoints[i][j]=initlist
##                matp[j].append(statistics.mean(initlist))
##        for i in ['arm', 'kick','neutral']:
##            minst=min(matp, key=lambda x:statistics.mean(matp[x]))
##            matr=numpy.matrix([i.coef for i in self.mat[i][minst]])
##            final=list()
##            for j in matr.T:
##                final.append(statistics.mean(numpy.array(j).flatten()))
##            rule[i]={minst:final}
##        for p in data:
##            mat2[p]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[p]))), data[p], self.deg))
##        for d in ['arm', 'kick']:
##            for tt in rule[d]:
##                sum1=0
##                sum1+=ClassifyUtils.euclideandistance(mat2[tt].coef, rule[d][tt],len(rule[d][tt]))
##                throttle[d]=(sum1/1)
##        if throttle[min(throttle, key=lambda x:throttle[x])]>(numpy.percentile(boundarypoints[min(throttle, key=lambda x:throttle[x])][minst],95)+(2*statistics.stdev(boundarypoints[min(throttle, key=lambda x:throttle[x])][minst]))):
##            return [["neutral"]]
##        return [[min(throttle, key=lambda x:throttle[x])], throttle[min(throttle, key=lambda x:throttle[x])]-throttle[sorted(throttle, key=lambda x:throttle[x])[1]],throttle[min(throttle, key=lambda x:throttle[x])] ]
##        
##            
##    def classification_algorithm(self, data):
##        for i in self.mat:
##            for j in self.mat[i]:
##                pass
##
##                        
##                
##                
##                
##    def smart_algo_knearest(self, data):    
##        matp={"F3":[], "F4":[], "FC5":[], "FC6":[]}#Data structrure for the incoming data(Multiple pieces of data not needed)
##        mat2={}
##        #for i in self.actions:mat2.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
##        throttle={}
##                
##        rule={}
##        for i in ['arm', 'kick', "neutral"]:#Associative rule mining phase
##            for j in self.mat[i]:# for sensor in action(j is the current sensor)
##                initlist=[]#initlist is a list which one will append the distances alculated to.This is done for statistical purposes
##                for p in itertools.combinations(self.mat[i][j], 2):#For the 6 choose two combinations of two polynomial object ifor a given movement, sensor
##                    initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[1].coef)))#Append the euclidean distance between the two .
##                matp[j].append(statistics.mean(initlist))#Append the mean of all of the distances for this sensor.
##        for i in ['arm', 'kick','neutral']:#Going through each action
##            minst=min(matp, key=lambda x:statistics.mean(matp[x]))# Find the most clustered sensor by finding the minimum average distance over the three actions.
##            matr=numpy.matrix([p.coef for p in self.mat[i][minst]])#Creation of a numpy matrix 
##            final=list()#List to contain rules.
##            finalfinal=list
##            #for j in matr.T: #Transposition of the matrix
##                #final.append(statistics.median(numpy.array(j).flatten()))#Flatten the row and average it in order to create the rule vector.
##            #finalfinal=(min(matr, key=lambda x:ClassifyUtils.euclideandistance(x.tolist()[0], final, len(final))))
##            rule[i]={minst:matr}
##        for p in data: #Exit Training phase, begin work on live data.
##            mat2[p]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[p]))), data[p], self.deg))#Featurize(find the polynomial fit of) the data
##        
##        for d in rule: #Classification phase-Iterate over actions
##            for tt in rule[d]: #Iterate over sensor(ONly one sensor, no true iteration)
##                sum1=0#Assign variable
##                count=0
##                for q in rule[d][tt]:
##                    sum1+=ClassifyUtils.euclideandistance(mat2[tt].coef, q.tolist()[0],len(q.tolist()[0]))#Add the Euclidean Distance between sample and rule
##                    count+=1
##                throttle[d]=(sum1/count)#append information to dictionary
##        return [[min(throttle, key=lambda x:throttle[x])],
##                throttle[min(throttle, key=lambda x:throttle[x])]-throttle[sorted(throttle, key=lambda x:throttle[x])[1]],throttle[min(throttle, key=lambda x:throttle[x])] ] #Return classification.
##    def smart_algo(self, data):    
##        matp={"F3":[], "F4":[], "FC5":[], "FC6":[]}#Data structrure for the incoming data(Multiple pieces of data not needed)
##        mat2={}
##        #for i in self.actions:mat2.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
##        throttle={}
##        rule={}
##        for i in ['arm', 'kick', "neutral"]:#Associative rule mining phase
##            for j in self.mat[i]:# for sensor in action(j is the current sensor)
##                initlist=[]#initlist is a list which one will append the distances alculated to.This is done for statistical purposes
##                for p in itertools.combinations(self.mat[i][j], 2):#For the 6 choose two combinations of two polynomial object ifor a given movement, sensor
##                    initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[1].coef)))#Append the euclidean distance between the two .
##                matp[j].append(statistics.mean(initlist))#Append the mean of all of the distances for this sensor.
##        for i in ['arm', 'kick','neutral']:#Going through each action
##            minst=min(matp, key=lambda x:statistics.mean(matp[x]))# Find the most clustered sensor by finding the minimum average distance over the three actions.
##            matr=numpy.matrix([p.coef for p in self.mat[i][minst]])#Creation of a numpy matrix 
##            final=list()#List to contain rules.
##            finalfinal=list
##            for j in matr.T: #Transposition of the matrix
##                final.append(statistics.median(numpy.array(j).flatten()))#Flatten the row and average it in order to create the rule vector.
##            finalfinal=(min(matr, key=lambda x:ClassifyUtils.euclideandistance(x.tolist()[0], final, len(final))))
##            rule[i]={minst:finalfinal.tolist()[0]}
##        #for p in data: #Exit Training phase, begin work on live data.
##            #mat2[p]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[p]))), data[p], self.deg))#Featurize(find the polynomial fit of) the data
##        for d in rule: #Classification phase-Iterate over actions
##            for tt in rule[d]: #Iterate over sensor(ONly one sensor, no true iteration)
##                sum1=0
##                sum1+=ClassifyUtils.euclideandistance(mat2[tt].coef, rule[d][tt],len(rule[d][tt]))#Add the Euclidean Distance between sample and rule
##                throttle[d]=(sum1/1)#append information to dictionary
##        return [[min(throttle, key=lambda x:throttle[x])],
##                throttle[min(throttle, key=lambda x:throttle[x])]-throttle[sorted(throttle, key=lambda x:throttle[x])[1]],throttle[min(throttle, key=lambda x:throttle[x])] ] #Return classification.
##      def smart_algo(self, data):    
##        matp={"F3":[], "F4":[], "FC5":[], "FC6":[]}#Data structrure for the incoming data(Multiple pieces of data not needed)
##        mat2={}
##        #for i in self.actions:mat2.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
##        throttle={}
##        rule={}
##        for i in ['arm', 'kick', "neutral"]:#Associative rule mining phase
##            for j in self.mat[i]:# for sensor in action(j is the current sensor)
##                initlist=[]#initlist is a list which one will append the distances alculated to.This is done for statistical purposes
##                for p in itertools.combinations(self.mat[i][j], 2):#For the 6 choose two combinations of two polynomial object ifor a given movement, sensor
##                    initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[1].coef)))#Append the euclidean distance between the two .
##                matp[j].append(statistics.mean(initlist))#Append the mean of all of the distances for this sensor.
##        for i in ['arm', 'kick','neutral']:#Going through each action
##            minst=min(matp, key=lambda x:statistics.mean(matp[x]))# Find the most clustered sensor by finding the minimum average distance over the three actions.
##            matr=numpy.matrix([p.coef for p in self.mat[i][minst]])#Creation of a numpy matrix 
##            final=list()#List to contain rules.
##            finalfinal=list
##            for j in matr.T: #Transposition of the matrix
##                final.append(statistics.median(numpy.array(j).flatten()))#Flatten the row and average it in order to create the rule vector.
##            finalfinal=(min(matr, key=lambda x:ClassifyUtils.euclideandistance(x.tolist()[0], final, len(final))))
##            rule[i]={minst:finalfinal.tolist()[0]}
##        for p in data: #Exit Training phase, begin work on live data.
##            mat2[p]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[p]))), data[p], self.deg))#Featurize(find the polynomial fit of) the data
##        for d in rule: #Classification phase-Iterate over actions
##            for tt in rule[d]: #Iterate over sensor(ONly one sensor, no true iteration)
##                sum1=0#Assign variable
##                #for ppp in rule[d][tt]:
##                sum1+=ClassifyUtils.euclideandistance(mat2[tt].coef, rule[d][tt],len(rule[d][tt]))#Add the Euclidean Distance between sample and rule
##                throttle[d]=(sum1/1)#append information to dictionary
##        return [[min(throttle, key=lambda x:throttle[x])],
##                throttle[min(throttle, key=lambda x:throttle[x])]-throttle[sorted(throttle, key=lambda x:throttle[x])[1]],throttle[min(throttle, key=lambda x:throttle[x])] ] #Return classification.
##    def smart_algo_neutral(self, data):
##        matp={"F3":[], "F4":[], "FC5":[], "FC6":[]}
##        mat2={}
##        throttle={}
##        min_sensor=list()
##        rule={}
##        for i in ['arm', 'kick']:
##            for j in self.mat[i]:
##                initlist=[]
##                for p in itertools.combinations(self.mat[i][j], 2):
##                    initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[1].coef)))
##                matp[j].append(statistics.mean(initlist))
##            minst=min(matp, key=lambda x:statistics.mean(matp[x]))
##            min_sensor.append(minst)
##            matp={"F3":[], "F4":[], "FC5":[], "FC6":[]}
##            matr=numpy.matrix([t.coef for t in self.mat[i][minst]])
##            final=list()
##            for j in matr.T:
##                final.append(statistics.mean(numpy.array(j).flatten()))
##            rule[i]={minst:final}
##        for i in ['neutral']:
##            subdict=dict()
##            for j in list(set(min_sensor)):
##                matr=numpy.matrix([t.coef for t in self.mat[i][j]])
##                final=list()
##                for q in matr.T:
##                    final.append(statistics.mean(numpy.array(q).flatten()))
##                subdict[j]=final
##            rule[i]=subdict
##        for p in data:
##            mat2[p]=poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(data[p]))), data[p], self.deg))
##        for d in ['arm', 'kick']:
##            sum1=0
##            for tt in rule[d]:
##                sum1+=ClassifyUtils.euclideandistance(mat2[tt].coef, rule[d][tt],len(rule[d][tt]))
##                throttle[d]=(sum1/1)
##        for d in ['neutral']:
##            minlist=list()
##            for tt in rule[d]:
##                minlist.append(ClassifyUtils.euclideandistance(mat2[tt].coef, rule[d][tt],len(rule[d][tt])))
##            throttle[d]=max(minlist)
##        return [[min(throttle, key=lambda x:throttle[x])], throttle[min(throttle, key=lambda x:throttle[x])]-throttle[sorted(throttle, key=lambda x:throttle[x])[1]],throttle[min(throttle, key=lambda x:throttle[x])] ]
##    def k_nn_old(self, data):
##        pp=[]
##        totallist=[]
##        for i in self.mat:
##            total=0
##            for m in self.mat[i]:
##                totallist.clear()
##                for j in list(sorted(self.mat[i][m], key=lambda x:ClassifyUtils.euclideandistance(x.coef, data[m].coef, self.deg+1))):
##                    totallist.append(ClassifyUtils.euclideandistance(j.coef, data[m].coef, self.deg+1))
##                if 0 in totallist:print("OOps")
##                totallist=list(filter(lambda x: (x>=(statistics.mean(totallist)-3*statistics.stdev(totallist)) and x<=(statistics.mean(totallist)+3*statistics.stdev(totallist))), totallist))
##                total+=sum(totallist)
##            pp.append(tuple((i, total)))
##        return pp
##    def k_nn(self, data):
##        pp=[]
##        for i in self.mat:
##            for m in self.mat[i]:
##                pp.append((i,m.euclidean_distance_between(data)))
##        return pp
class MultiLiveClassifierApplication:
    def __init__(self, process1, process2, q,  profile,subprocessed=False):
        self.getter=process1
        self.profile=profile
        self.q=q
        self.dict_data=pickle.loads(profile.read())
        self.classifiers=dict()
        unpacked=list()
        for b in self.dict_data:
            unpacked+=self.dict_data[b]
        self.classif=PolyBasedClassifier(12)
        self.processer=process2
        for j in unpacked:
            self.classif.train({j.label: j.data})
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
    def car(self,data_dict):
         pp=numpy.matrix([data_dict[j] for j in data_dict])
         #print(pp)
         count=0
         for j in pp.T:
             avg=statistics.mean(numpy.array(j).flatten())
             for p in data_dict:
                 #print(data_dict[p][count])
                 data_dict[p][count]-=avg
             count+=1
         return data_dict
    def runAppSubprocessedDiffAlgo(self):
        self.getter.start()
        getpid=self.getter.pid
        procget=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(getpid))
        kernel.SetPriorityClass(procget, 0x0100)
        #self.classproc.start()
        classpid=self.getter.pid
        self.thresh=0.825
        proclass=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(classpid))
        kernel.SetPriorityClass(proclass, 0x0100)
        self.processer.start()
        procpid=self.processer.pid
        procproc=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(procpid))
        kernel.SetPriorityClass(procproc, 0x0100)
        data_dict=dict({"F3":[], "F4":[], "FC5":[], "FC6":[]})
        countr=0
        switch_countr=0
        switch=False
        average_q={"kick":[self.thresh], "arm":[self.thresh], "neutral":[self.thresh]}
        running_q={"kick":[], "arm":[], "neutral":[]}
        print("Enter Loop")
        runloop=[]
        try:
            print("in")
            while self.getter.is_alive():
                data=self.q.recv()
                #print(data)
                for i in data_dict:
                    data_dict[i].append(data[i][0][2])
                countr=countr+1
                if len(data_dict["F3"])==32:                   
                     print(self.classif.smart_algo(self.car(data_dict))[0][0])
                     for i in data_dict:
                        del data_dict[i][0:32]
        except:
            self.getter.terminate()
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
        data_dict=dict({"F3":[], "F4":[], "FC5":[], "FC6":[]})
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
                if len(data_dict["F3"])==32:                
                    for i in data_dict:
                        del data_dict[i][0]
                    if (countr%4)==0:
                         self.classq.send(data_dict)
                         res=self.classq.recv()
                         res1=list(res)
                         for i in res:
                              average_q[i[0]].append(i[1])
                              if len(running_q[i[0]])==3:
                                   del running_q[i[0]][0]
                              running_q[i[0]].append(i[1])
                         final_list=list()
                         for i in average_q:
                              if len(average_q[i])<=1:
                                   curr_ar=SLICERZ.Area(highpass(average_q[i])[-1], 0)
                              else:
                                   curr_ar=SLICERZ.Area(highpass(average_q[i])[-1], 1*statistics.stdev(highpass(average_q[i])))
                              if not highpass(running_q[i])[-1] in curr_ar and highpass(running_q[i])[-1]>curr_ar.miny:
                                   final_list.append(tuple((i,highpass(running_q[i])[-1])))
                         if len(final_list)==0:
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
                              percent=abs(percent-highpass(average_q[final_list[0][0]])[-1])
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
                              if maxy[0]=="kick":
                                   switch=True
                                   print("kick"+str(percent))
                                   a.move_mouse(a.get_mouse_pos()[0], int(a.get_mouse_pos()[1]+(abs(percent*100*60))))
                              else:
                                  switch=True
                                  print("arm"+str(percent))
                                  a.move_mouse(a.get_mouse_pos()[0], int(a.get_mouse_pos()[1]-(abs(percent*100*60))))
                         countr+=1
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
        data_dict=dict({"F3":[], "F4":[], "FC5":[], "FC6":[]})
        countr=0
        try:
            while self.getter.is_alive():
                data=self.q.recv()
                for i in data_dict:
                    data_dict[i].append(data[i][0][2])
                countr=countr+1
                if len(data_dict["F3"])==32:
                    for i in data_dict:
                        del data_dict[i][0]
                print(time.time())
                self.system_up_time+=16/128
        except:
            self.getter.terminate()
            self.processer.terminate()
            raise
    
class MultiLiveTrainingDataGatherer:
     def __init__(self, process1,process2,q,dumpto, qevents,k):
        self.getter=process1
        self.q=q
        self.events=qevents
        self.k=k
        self.processer=process2
     def car(self,data_dict):
         pp=numpy.matrix([data_dict[j] for j in data_dict])
         count=0
         for j in pp.T:
             avg=statistics.mean(numpy.array(j).flatten())
             for p in data_dict:
                 data_dict[p][count]-=avg
             count+=1
     def runApp(self):
        self.getter.start()
        getpid=self.getter.pid
        procget=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(getpid))
        kernel.SetPriorityClass(procget, 0x0100)
        self.processer.start()
        procpid=self.processer.pid
        procproc=kernel.OpenProcess(ctypes.c_uint(0x0200|0x0400), ctypes.c_bool(False), ctypes.c_uint(procpid))
        kernel.SetPriorityClass(procproc, 0x0100)
        sampslist=dict()
        data_dict=dict()
        count=0
        for i in self.events:
            sampslist[i]=[]
        for k in range(self.k):
            for i in self.events:
                data_dict[i]={"F3":[], "F4":[], "FC5":[], "FC6":[]}
            for tp in data_dict:
                print(tp)
                first=bool(True)
                try:
                    while self.getter.is_alive():
                        data=self.q.recv()
                        if first:
                            data=self.q.recv()
                            first=False
                        for i in data_dict[tp]:
                            data_dict[tp][i].append(data[i][0][2])
                        if len(data_dict[tp]["F3"])==32:
                            for i in data_dict[tp]:
                                del data_dict[tp][i][0]
                            raise KeyboardInterrupt    
                        print(time.asctime())
                except:
                    for i in range(32):
                         self.q.recv()
                    if not count==3:
                        continue
            count=0
            for pl in data_dict:
                sampslist[pl].append(Sample(pl, data_dict[pl]))
                print("j")
            print("Train Done")
        self.getter.terminate()
        self.processer.terminate()
        for j in sampslist:
            for p in sampslist[j]:
                print(p.data)
                self.car(p.data)
                print(p.data)
        fileobj=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "wb")
        fileobj.write(pickle.dumps(sampslist))
        fileobj.close()
def MultiDataGather():
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    myApp=MultiLiveTrainingDataGatherer(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "wb"),["kick", "arm","neutral"],6)
    myApp.runApp()
def MultiRunApp():
    q,q1=multiprocessing.Pipe()
    getter=multiprocessing.Process(target=BaseEEG.run_data_getter_processer, args=(q1,))
    q2, q3=multiprocessing.Pipe()
    processor=multiprocessing.Process(target=BaseEEG.exec_proc, args=(q, q2, 1))
    myApp=MultiLiveClassifierApplication(getter, processor, q3, open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "rb"))
    myApp.runAppSubprocessedDiffAlgo()
if __name__=='__main__':
    #MultiDataGather()
    MultiRunApp()
    pass

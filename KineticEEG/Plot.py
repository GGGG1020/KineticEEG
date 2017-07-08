#Plots.py

import matplotlib.pyplot
import pickle
import numpy
import itertools
import ClassifyUtils
import DBA
import statistics
import numpy.polynomial as poly
#from Polyfit222 import Sample
import matplotlib.pyplot as plt
import fastdtw
import numpy
class Sample:
    def __init__(self, label, data):
        self.data=data
        self.label=label
    def euclidean_distance_between(self, other):
        tote=0
        for i in self.data:
            tote+=ClassifyUtils.euclideandistance(self.data[i].coef, other.data[i].coef, len(self.data[i].coef))
        return tote
#Load files
def average_distance_from_rulevector(filename, deg):
    fileobj=open(filename, "rb")
    results=dict()
    dat=pickle.loads(fileobj.read())
    labels=list()
    data=list()
    actions=["arm", "kick",'neutral']
    data_to_plot=[]
    distance_data=dict()
    for i in actions:
        distance_data[i]=[]
    labels=[]
    rule=dict()
    average_clustering={"F3":[], "F4":[], "FC5":[], "FC6":[]}
    mat=dict()
    for i in actions:results.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
    for i in actions:mat.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
    for b in actions:
        for c in dat[b]:
            #for j in c.data:
                for p in c.data:
                    mat[b][p].append(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(c.data[p]))), c.data[p], deg)))
                    
    #print(len(mat['kick']['F3']))
    for i in ['arm', 'kick', 'neutral']:
        for q in mat[i]:
            initlist=[]
            for p in itertools.combinations(mat[i][q], 2):
                print(p)
                initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[0].coef)))
            average_clustering[q].append(statistics.mean(initlist))
    for i in ['arm', 'kick', 'neutral']:
        #print(average_clustering)
        minimum_sensor=min(average_clustering, key=lambda x:statistics.mean(average_clustering[x]))
        #print(minimum_sensor)
        matr=numpy.matrix([p.coef for p in mat[i][minimum_sensor]])
        finalrule=list()
        for j in matr.T:
            finalrule.append(statistics.mean(numpy.array(j).flatten()))
        rule[i]={minimum_sensor:finalrule}
    for action_to_test in ['arm', 'kick', 'neutral']:
        
        for sample in mat[action_to_test][list(rule[action_to_test].keys())[0]]:
            #print(sample)
            #print("Action to test", rule[action_to_test])
            labels.append(action_to_test)
            #data.append(ClassifyUtils.euclideandistance(rule[action_to_test][list(rule[action_to_test].keys())[0]], sample.coef, len(sample.coef)))
            distance_data[action_to_test].append(ClassifyUtils.euclideandistance(rule[action_to_test][list(rule[action_to_test].keys())[0]], sample.coef, len(sample.coef)))
            
    ##Make the Plot
    plt.suptitle("Distance to Rule Vector from Samples")
    fig=plt.figure(1, figsize=(20,6))
    ax=fig.add_subplot(111)
    for i in ['arm', 'kick', 'neutral']:
        data.append([distance_data[i]])
    print(len(data))
    bp=ax.boxplot(data, labels=['arm', 'kick', 'neutral'])
    fig.show()
    
    
            
            
        
def normalized_cross_correlation(sig1,sig2):
	numerator=0
	for i in range(len(sig1)):
		numerator+=((sig1[i]-statistics.mean(sig1))*(sig2[i]-statistics.mean(sig2)))
	sig2denominator=0
	sig1denom=0
	for j in range(len(sig1)):
		sig2denominator+=pow(sig2[j], 2)
		sig1denom+=pow(sig1[j], 2)
	denominator=pow(sig2denominator, 0.5)*pow(sig1denom, 0.5)
	return numerator/denominator 
                
        
        
        
def run_clusteringplot(filename,deg):
    fileobj=open(filename, "rb")
    results=dict()
    dat=pickle.loads(fileobj.read())
    actions=["arm", "kick",'neutral']
    data_to_plot=[]
    labels=[]
    mat=dict()
    for i in actions:results.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
    for i in actions:mat.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
    for b in actions:
        for c in dat[b]:
            #for j in c.data:
                for p in c.data:
                    mat[b][p].append(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(c.data[p]))), c.data[p], deg)))
    for i in actions:
        #print(i)
        for j in mat[i]:
            #print(j)
            initlist=[]
            for p in itertools.combinations(mat[i][j], 2):
                initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[1].coef)))

            data_to_plot.append(initlist)
            labels.append(i+j)
    plt.suptitle(filename.split("/")[-1]+" "+"Average Clustering of Data")
    fig=plt.figure(1, figsize=(20,6))
    ax=fig.add_subplot(111)
    bp=ax.boxplot(data_to_plot, labels=labels)
    fig.show()
def run_data_plot(filename):
    fileobj=open(filename, "rb")
    results=dict()
    min_dict={"arm":{}, "kick":{}, "neutral":{}}
    main_dict={"arm":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "kick":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "neutral":{"F3":[], "F4":[], "FC5":[], "FC6":[]}}
    dat=pickle.loads(fileobj.read())
    fg=plt.figure(1)
    meanlist={"arm":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "kick":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "neutral":{"F3":[], "F4":[], "FC5":[], "FC6":[]}}
    std_dict={"arm":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "kick":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "neutral":{"F3":[], "F4":[], "FC5":[], "FC6":[]}}
    for i in dat:
        for p in dat[i]:
            for d in p.data:
                main_dict[i][d].append(p.data[d])
                #print(len(p.data[d]))
                
    
    for i in main_dict:
        for j in main_dict[i]:
            #plt.figure()
            #fig, ax=plt.subplots()
            for t in main_dict[i][j]:
                #plt.plot(t)
                pass
            #ax.plot(meanlist[i][sens], label="Mean")
            #legend = ax.legend(loc='upper center', shadow=True)
                
            
            #plt.suptitle(i+j)
   
            average_matrix=numpy.matrix([t for t in main_dict[i][j]])
            final_list=list()#Average all the signals
            std=list()#Hold the standard deviations of all the signals.
            
            for pro in average_matrix.T:
                #print(i.flatten().tolist())
                final_list.append(statistics.mean(pro.tolist()[0]))
                #std.append(abs(statistics.stdev(pro.tolist()[0])/statistics.mean(pro.tolist()[0])))
                pass
            for psq1,psq2 in itertools.combinations(average_matrix,2):
                std.append((fastdtw.dtw(sum(psq1.tolist(),[]), sum(psq2.tolist(), []))[0]))#/abs(statistics.mean([statistics.mean(sum(psq1.tolist(),[])), statistics.mean(sum(psq2.tolist(), []))])))
            print(std)
            meanlist[i][j]=final_list
            #print(i+j, str(str(statistics.mean(std))+"+/-"+str(statistics.stdev(std))))
            std_dict[i][j]=statistics.mean(std)

                
    #plt.draw()i=
    for i in std_dict:
        #print(std_dict[i])
        #print(max(std_dict[i], key=lambda x:std_dict[i][x]))
        sens=min(std_dict[i], key=lambda x:std_dict[i][x])
        #print("I:",i)
        plt.figure()
        fig,  ax=plt.subplots()
        for pvnrt in main_dict[i][sens]:
            plt.plot(pvnrt)
            #print("VNRT",pvnrt)
        #tseries=[numpy.array(i) for i in main_dict[i][sens]]
        #print(tseries)
        #dba=DBA.DBA(30)
        #dba_avg=dba.compute_average(tseries)
        ax.plot(meanlist[i][sens], label="Mean")
        legend = ax.legend(loc='upper center', shadow=True)
                
            
        plt.suptitle(i+j)
        #print(i)
        min_dict[i][sens]=meanlist[i][sens]
        #print(numpy.polyfit(range(0, len(meanlist[i][sens])), meanlist[i][sens], 1))

    plt.draw()
    
    for d in dat:
        for q in dat[d]:
            selector={}
            for mint in min_dict:
                for sensor in min_dict[mint]:
                    #print("Average", statistics.mean(q.data[sensor]))
                    #print("Average", statistics.mean(min_dict[mint][sensor]))
                    selector[mint]=(fastdtw.dtw(q.data[sensor], min_dict[mint][sensor])[0])#/abs(statistics.mean([float(statistics.mean(q.data[sensor])), float(statistics.mean(min_dict[mint][sensor]))]))
                    #print(sensor, mint)
                    print(numpy.polyfit(range(0, len(q.data[sensor])), q.data[sensor], 1), sensor)
            print(d, min(selector, key=lambda x:selector[x]))
            
        
                           
        #pt=numpy.polyfit(range(0, len(meanlist[i][sens])), meanlist[i][sens], 4)
        #print(i+sens, pt)
    plt.show()
def normalized_cross_correlation(sig1,sig2):
	numerator=0
	for i in range(len(sig1)):
		numerator+=(sig1[i])*(sig2[i])
	sig2denominator=0
	sig1denom=0
	for j in range(len(sig1)):
		sig2denominator+=pow(sig1[j]-statistics.mean(sig1), 2)
		sig1denom+=pow(sig2[j]-statistics.mean(sig2), 2)
	denominator=pow(sig2denominator, 0.5)*pow(sig1denom, 0.5)
	return numerator/denominator 
        
        


if __name__=='__main__':
    run_data_plot("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Favorites/Trainingdata (16).kineegtr")
    #run_data_plot("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr")

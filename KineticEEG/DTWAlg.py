###Dynamic Time Warping
import matplotlib.pyplot
import pickle
import numpy
import itertools
import ClassifyUtils
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


def normalized_cross_correlation(sig1,sig2):
	numerator=0
	for i in range(len(sig1)):
		numerator+=((sig1[i])*(sig2[i]))
	sig2denominator=0
	sig1denom=0
	for j in range(len(sig1)):
		sig2denominator+=pow(sig2[j], 2)
		sig1denom+=pow(sig1[j], 2)
	denominator=pow(sig2denominator, 0.5)*pow(sig1denom, 0.5)
	return numerator/denominator 
def normalized_cross_correlation(sig1,sig2):
	numerator=0
	for i in range(len(sig1)):
		numerator+=(sig1[i])*(sig2[i])
	sig2denominator=0
	sig1denom=0
	for j in range(len(sig1)):
		sig2denominator+=pow((sig2[j]), 2)
		sig1denom+=pow((sig1[j]), 2)
	denominator=pow(sig2denominator, 0.5)*pow(sig1denom, 0.5)
	return numerator/denominator         
        

class CrossCorrelationClassifier:
    def __init__(self,degree, actions=['arm', 'kick', 'neutral']):
        self.actions=actions
        self.mat=dict()
        for i in self.actions:self.mat.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
    def train(self,data):
        for pvnrt in data:
            for q in data[pvnrt]:
                self.mat[pvnrt][q].append(data[pvnrt][q])
    def classify(self, data):
        meanlist={"arm":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "kick":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "neutral":{"F3":[], "F4":[], "FC5":[], "FC6":[]}}
        std_dict={"arm":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "kick":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "neutral":{"F3":[], "F4":[], "FC5":[], "FC6":[]}}
        min_dict={"arm":{}, "kick":{}, "neutral":{}}
        by_sensor={"F3":[], "F4":[], 'FC5':[], "FC6":[]}
        main_dict={"arm":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "kick":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "neutral":{"F3":[], "F4":[], "FC5":[], "FC6":[]}}
        print("Working")
        for p in self.mat:
            for j in self.mat[p]:
                average_matrix=numpy.matrix([t for t in self.mat[p][j]])
                final_list=list()#Average all the signals
                std=list()#Hold the standard deviations of all the signals.
            
                for pro in average_matrix.T:
                    #print(i.flatten().tolist())
                    final_list.append(statistics.mean(pro.tolist()[0]))
                    #std.append(abs(statistics.stdev(pro.tolist()[0])/statistics.median(pro.tolist()[0])))
                for psq1,psq2 in itertools.combinations(average_matrix,2):
                    std.append(fastdtw.dtw(sum(psq1.tolist(),[]), sum(psq2.tolist(), []))[0])#/abs(statistics.mean([statistics.mean(sum(psq1.tolist(),[])), statistics.mean(sum(psq2.tolist(), []))])))
                meanlist[p][j]=final_list
                #print(i+j, str(str(statistics.mean(std))+"+/-"+str(statistics.stdev(std))))
                std_dict[p][j]=statistics.mean(std)
                print(statistics.mean(std))
        for qrt in self.mat:
                for pst in self.mat[qrt]:
                        for j in self.mat[qrt][pst]:
                                by_sensor[pst].append(Sample(qrt,j))

        for i in std_dict:
            sens=min(std_dict[i], key=lambda x:std_dict[i][x])
            min_dict[i][sens]=meanlist[i][sens]
            #print(numpy.polyfit(range(0, len(meanlist[i][sens])), meanlist[i][sens], 1))        
        for q in data: 
            #print(q)
            selector={}
            for mint in min_dict:
                for sensor in min_dict[mint]:
                
                    selector[mint]=fastdtw.dtw(data[q], min_dict[mint][sensor])[0]#/(abs(statistics.mean([float(statistics.mean(data[q])), float(statistics.mean(min_dict[mint][sensor]))])))
                    #pred=max(by_sensor[sensor], key=lambda x:normalized_cross_correlation(data[q], x.data))
                    #print(sensor, mint)
                    #print(numpy.polyfit(range(0, len(q.data[sensor])), q.data[sensor], 1), sensor)]
        print(selector)
        return [[min(selector, key=lambda x:selector[x])]]
        print(min(selector, key=lambda x:selector[x]))
        #return [[pred.label]]

    def smart_algo(self, data):
        return self.classify(data)
                
                            

                    
            
                    
        


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
            average_matrix=numpy.matrix([t for t in main_dict[i][j]])
            final_list=list()#Average all the signals
            std=list()#Hold the standard deviations of all the signals.
            
            for pro in average_matrix.T:
                #print(i.flatten().tolist())
                final_list.append(statistics.median(pro.tolist()[0]))
                #std.append(abs(statistics.stdev(pro.tolist()[0])/statistics.median(pro.tolist()[0])))
            for psq1,psq2 in itertools.combinations(average_matrix,2):
                std.append(normalized_cross_correlation(sum(psq1.tolist(),[]), sum(psq2.tolist(), [])))
            meanlist[i][j]=final_list
            #print(i+j, str(str(statistics.mean(std))+"+/-"+str(statistics.stdev(std))))
            std_dict[i][j]=statistics.mean(std)

                

    for i in std_dict:
        #print(std_dict[i])
        #print(max(std_dict[i], key=lambda x:std_dict[i][x]))
        sens=max(std_dict[i], key=lambda x:std_dict[i][x])
        #print(sens)
        plt.figure()
        fig,  ax=plt.subplots()
        for pvnrt in main_dict[i][sens]:
            plt.plot(pvnrt)
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
                    recordlist=list()
                    for example in maindict[mint][sensor]:
                        recordlist.append(normalized_cross_correlation(q.data[sensor], example))
                    selector[mint]=statistics.median(recordlist)#normalized_cross_correlation(q.data[sensor], min_dict[mint][sensor])
                    #print(sensor, mint)
                    #print(numpy.polyfit(range(0, len(q.data[sensor])), q.data[sensor], 1), sensor)
            print(d, min(selector, key=lambda x:selector[x]))
            
        
                           
        #pt=numpy.polyfit(range(0, len(meanlist[i][sens])), meanlist[i][sens], 4)
        #print(i+sens, pt)
    plt.show()

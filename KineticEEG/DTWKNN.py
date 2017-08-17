####DTAKNN
####Uses dynamic time warping

import ClassifyUtils
import fastdtw
import numpy
import statistics
import itertools

class Sample:
    def __init__(self, label, data):
        self.data=data
        self.label=label
    def euclidean_distance_between(self, other):
        tote=0
        for i in self.data:
            tote+=ClassifyUtils.euclideandistance(self.data[i].coef, other.data[i].coef, len(self.data[i].coef))
        return tote

class DTW_kNN:
    def __init__(self, k):
        self.k=k
        #self.actions=actions
        self.trset=list()
    def train(self, dictionary)->None:
        for i in dictionary:
            self.trset.append(Sample(i, dictionary[i]))
    def classify(self, data:dict)->str:
        results=dict()
        q=data
        min_dict={"arm":{}, "kick":{}, "neutral":{}}
        main_dict={"arm":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "kick":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "neutral":{"F3":[], "F4":[], "FC5":[], "FC6":[]}}
        meanlist={"arm":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "kick":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "neutral":{"F3":[], "F4":[], "FC5":[], "FC6":[]}}
        std_dict={"arm":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "kick":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "neutral":{"F3":[], "F4":[], "FC5":[], "FC6":[]}}
        for i in self.trset:
            for d in i.data:
                #print(d)
                main_dict[i.label][d].append(i.data[d])
        for i in main_dict:
            for j in main_dict[i]:
                average_matrix=numpy.matrix([t for t in main_dict[i][j]])
                final_list=list()#Average all the signals
                std=list()#Hold the standard deviations of all the signals.
                for pro in average_matrix.T:
                    final_list.append(statistics.mean(pro.tolist()[0]))
                    #std.append(abs(statistics.stdev(pro.tolist()[0])/statistics.mean(pro.tolist()[0])))
                    pass
                for psq1,psq2 in itertools.combinations(average_matrix,2):
                    std.append((fastdtw.dtw(sum(psq1.tolist(),[]), sum(psq2.tolist(), []))[0]))#/abs(statistics.mean([statistics.mean(sum(psq1.tolist(),[])), statistics.mean(sum(psq2.tolist(), []))])))
                #print(std)
                meanlist[i][j]=final_list
                std_dict[i][j]=statistics.mean(std)
        for i in std_dict:
            sens=min(std_dict[i], key=lambda x:std_dict[i][x])
            #print(sens)
            min_dict[i][sens]=meanlist[i][sens]
        selector={}
        for mint in min_dict:
            for sensor in min_dict[mint]:
                selector[mint]=(fastdtw.dtw(q[sensor], min_dict[mint][sensor])[0])#/abs(statistics.mean([float(statistics.mean(q.data[sensor])), float(statistics.mean(min_dict[mint][sensor]))]))
                #print(numpy.polyfit(range(0, len(q.data[sensor])), q.data[sensor], 0), sensor)
                    
            #print(d, min(selector, key=lambda x:selector[x]))
            
        return min(selector, key=lambda x:selector[x])
    def smart_algo(self, data):
        return self.classify(data)
                            
            
        
        

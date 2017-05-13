#Plots.py

import matplotlib.pyplot
import pickle
import numpy
import itertools
import ClassifyUtils
import statistics
import numpy.polynomial as poly
#from Polyfit222 import Sample
import matplotlib.pyplot as plt

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


if __name__=='__main__':
    run_clusteringplot("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Favorites/Trainingdata (17).kineegtr",12)

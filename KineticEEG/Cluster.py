import matplotlib.pyplot
import pickle
import numpy
import itertools
import ClassifyUtils
import statistics
import numpy.polynomial as poly
from Polyfit222 import Sample
deg=8
filename="C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr"
fileobj=open(filename, "rb")
results=dict()
dat=pickle.loads(fileobj.read())
actions=["arm", "kick",'neutral']
mat=dict()
for i in actions:results.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
for i in actions:mat.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
for b in actions:
    for c in dat[b]:
        #for j in c.data:
            for p in c.data:
                mat[b][p].append(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(c.data[p]))), c.data[p], deg)))
for i in actions:
    print(i)
    for j in mat[i]:
        print(j)
        initlist=[]
        for p in itertools.combinations(mat[i][j], 2):
            initlist.append(ClassifyUtils.euclideandistance(p[0].coef, p[1].coef, len(p[1].coef)))

        print(statistics.mean(initlist), statistics.stdev(initlist))
##import numpy as np
##import matplotlib.pyplot as plt
##
##N = 3
##f3_means = [results[i]["F3"] for i in actions]
##print(f3_means)
##f3_means=tuple(f3_means)
##
##f4_means = [results[i]["F4"] for i in actions]
##print(f4_means)
##f4_means=tuple(f4_means)
##
##fc5_means = [results[i]["FC5"] for i in actions]
##print(fc5_means)
##fc5_means=tuple(fc5_means)
##
##fc6_means = [results[i]["FC6"] for i in actions]
##print(fc6_means)
##fc6_means=tuple(fc6_means)
##
##
##ind = np.arange(N)  # the x locations for the groups
##width = 0.25       # the width of the bars
##
##fig, ax = plt.subplots()
##rects1 = ax.bar(ind, f3_means, width, color='r')
##
##rects2 = ax.bar((1*ind) + width, f4_means, width, color='y')
##
##rects3 = ax.bar((1*ind) + (2*width), fc5_means, width, color='b')
##rects4 = ax.bar((1*ind) + (3*width), fc6_means, width, color='g')
### add some text for labels, title and axes ticks
##ax.set_ylabel('Scores')
##ax.set_title('Scores by group and gender')
##ax.set_xticks((1*ind) + (5*width)/2)
##ax.set_xticklabels(('Arm', 'Kick', 'Neutral'))
##
##ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ('F3', "F4","FC5", "FC6"))
##
####
####def autolabel(rects):
####    """
####    Attach a text label above each bar displaying its height
####    """
####    for rect in rects:
####        height = rect.get_height()
####        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
####                '%d' % int(height),
####                ha='center', va='bottom')
####
####autolabel(rects1)
####autolabel(rects2)
##
##plt.show()

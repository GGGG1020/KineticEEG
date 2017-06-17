#Analysis.py

import matplotlib.pyplot
import pickle
import numpy
import itertools
import ClassifyUtils
import statistics
import numpy.polynomial as poly
#from Polyfit222 import Sample
import matplotlib.pyplot as plt
from Polyfit222 import Sample
import numpy
import tkinter
from tkinter import filedialog

####Load file


def normalized_cross_correlation(sig1,sig2):
	numerator=0
	for i in range(len(sig1)):
		numerator+=((sig1[i]-statistics.mean(sig1))*(sig2[i]-statistics.mean(sig2)))
	sig2denominator=0
	sig1denom=0
	for j in range(len(sig1)):
		sig2denominator+=pow((sig2[j]-statistics.mean(sig2)), 2)
		sig1denom+=pow((sig2[j]-statistics.mean(sig2)), 2)
	denominator=pow(sig2denominator, 0.5)*pow(sig1denom, 0.5)
	return numerator/denominator 
jk=filedialog.askopenfile(initialdir="C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/")
name=jk.name
jk.close()
f=open(jk.name, "rb")
results=dict()
min_dict={"arm":{}, "kick":{}, "neutral":{}}
main_dict={"arm":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "kick":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "neutral":{"F3":[], "F4":[], "FC5":[], "FC6":[]}}
dat=pickle.loads(f.read())
f.close()
fg=plt.figure(1)
meanlist={"arm":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "kick":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "neutral":{"F3":[], "F4":[], "FC5":[], "FC6":[]}}
std_dict={"arm":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "kick":{"F3":[], "F4":[], "FC5":[], "FC6":[]}, "neutral":{"F3":[], "F4":[], "FC5":[], "FC6":[]}}
for i in dat:
    for p in dat[i]:
        for d in p.data:
            main_dict[i][d].append(p.data[d])
print("Average Pairwise Cross-Correlation Value")
for i in main_dict:
    for p in main_dict[i]:
        listofcrosscorr=list()
        for q,r in itertools.combinations(main_dict[i][p],2):
            #print(i,p)
            listofcrosscorr.append(normalized_cross_correlation(q,r))
        print(statistics.mean(listofcrosscorr), i+p) 
print("Cross Correlation Value Between Two Sensors")
for i,k in itertools.combinations(['arm', 'kick', 'neutral'], 2):
    for s1 in ['FC5', "F3", "F4", "FC6"]:
        reclist=list()
        for q1 in main_dict[i][s1]:
            for q2 in main_dict[k][s1]:
                reclist.append(normalized_cross_correlation(q1,q2))
        print(statistics.mean(reclist), (i+s1)+" "+(k+s1))
    
            
                



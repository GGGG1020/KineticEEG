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
import fastdtw
from tkinter import filedialog

####Load file


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
print("Average Pairwise Time-Warp Value")
for i in main_dict:
    for p in main_dict[i]:
        listofcrosscorr=list()
        for q,r in itertools.combinations(main_dict[i][p],2):
            #print(i,p)
            listofcrosscorr.append((fastdtw.dtw(q,r)[0])/statistics.mean([statistics.mean(q),statistics.mean(r)]))
            #print(listofcrosscorr)
        print(statistics.mean(listofcrosscorr), i+p) 
print("Timewarp Value Between Two Sensors")
for i,k in itertools.combinations(['arm', 'kick', 'neutral'], 2):
    for s1 in ['FC5', "F3", "F4", "FC6"]:
        reclist=list()
        for q1 in main_dict[i][s1]:
            for q2 in main_dict[k][s1]:
                reclist.append(abs((fastdtw.dtw(q1,q2)[0])/statistics.mean([statistics.mean(q1),statistics.mean(q2)])))
                #print(reclist)
        print(statistics.mean(reclist), (i+s1)+" "+(k+s1))

                



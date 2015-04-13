"""This file contains many nessecary utilities for the classification alogrithm"""
import math

def euclideandistance(inst1, inst2, leng):
    d=0
    for i in range(leng):
        d+=pow((inst1[i]-inst2[i]),2)
    return math.sqrt(d)
def list_d(inst1, inst2, leng):
    d_list=list()
    for i in range(leng):
        d_list.append(int(abs(inst1[i]-inst2[i])))
    return d_list
def load_trainingdata(file):
    """The training data file will look like this:\
    TRAINING.dat
    Fc4, 3.39, 1.00,1.89,0.00, arm
    The dictionary returned will look like this:
    trainingdat={"FC4":[[3.39, 1.00,1.89,0.00, "arm"],[6.34,0.879,1.23,0.10, "kick"]]}"""
    f=open(file, "r")
    trainingdat=dict()
    for i in f.readlines():
        i=i.split()
        senor=i.pop(0)
        trainingdat[sensor].append(i)
        
    return trainingdat

        

###Grapher.py



import matplotlib.pyplot as plt
import pickle
from Polyfit222 import Sample

f=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "rb")
am=pickle.loads(f.read())
print(am)
for j in am:
    for t in j:
        pass

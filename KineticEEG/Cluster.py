import matplotlib.pyplot
import pickle
import numpy
import itertools
import ClassifyUtils
import statistics
import numpy.polynomial as poly
from Polyfit222 import Sample
deg=4
filename="C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Favorites/KineticEEGProgamFiles/Favorites/Trainingdata (12).kineegtr"
fileobj=open(filename, "rb")
dat=pickle.loads(fileobj.read())
actions=["arm", "kick",'neutral']
mat=dict()
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

        print(statistics.mean(initlist), i, j)
    



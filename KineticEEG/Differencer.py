import itertools
import pickle
import sys
sys.path.append('C:/Users/Gaurav/Desktop/')
import ClassifyUtils
import numpy
from Polyfit222 import Sample
import numpy.polynomial as poly
import statistics
import matplotlib.pyplot as plt
import sys
sys.path.append("C:/Users/Gaurav/Desktop")
import Polyfit222
def make_unique(original_list):
    unique_list = []
    [unique_list.append(obj) for obj in original_list if obj not in unique_list]
    return unique_list

def combine_between_two_lists(l1, l2):
	results=[]
	ab=itertools.permutations(l2, len(l2))
	for i in ab:
		counter=0
		for j in i:
			results.append((l1[counter], j))
			counter+=1
	return results
def find_trouble(listy, sensor, ref):pass
def difference(listy,sensor):
    avg=list()
    res=[]
    #print(listy[ref][sensor])
    for ref in ['arm', 'kick', 'neutral']:
        for i in (itertools.combinations(listy[ref][sensor], 2)):
            avg.append(ClassifyUtils.euclideandistance(i[0], i[1], len(i[0])))
        print(str(ref+"v."+ref)+str(sum(avg)/len(avg)))
        print(statistics.stdev(avg))
    for i in itertools.combinations(['arm', 'kick', 'neutral'],2):
            avglist=list()
            for j in make_unique(combine_between_two_lists(listy[i[0]][sensor], listy[i[1]][sensor])):
                avglist.append(ClassifyUtils.euclideandistance(j[0], j[1], len(j[0])))
            print(str(i[0]+"v."+i[1])+str(sum(avglist)/len(avglist)))
            print(statistics.stdev(avglist))
def difference2(listy):
    for i in ['arm', 'kick', 'neutral']:
        avg=list()
        for j in (itertools.combinations(listy[i],2)):
            avg.append(ClassifyUtils.euclideandistance(j[0].data, j[1].data, len(j[0].data)))
        print(str(i+"v."+i)+str(sum(avg)/len(avg)))
    for i in itertools.combinations(['arm', 'kick', 'neutral'],2):
         avg=list()
         for j in listy[i[0]]:
             for k in listy[i[1]]:
                 avg.append(ClassifyUtils.euclideandistance(j.data, k.data, len(j.data)))
         print(str(i[0]+"v."+i[1])+str(sum(avg)/len(avg)))
                 
     
##        for i in itertools.combinations(['arm', 'kick', 'neutral'],2):
##            avglist=list()
##            for j in make_unique(combine_between_two_lists(listy[i[0]], listy[i[1]])):
##                avglist.append(ClassifyUtils.euclideandistance(j[0], j[1], len(j[0])))
##            print(str(i[0]+"v."+i[1])+str(sum(avglist)/len(avglist)))
##            print(statistics.stdev(avglist))
##        
    
if __name__=='__main__':
    f=open("C:/Users/Gaurav/Desktop/KineticEEGProgamFiles/Trainingdata.kineegtr", "rb")
    pol=f.read()
    dd=pickle.loads(pol)
    deg=18
    data=dd
    actions=['arm', 'kick', 'neutral']
    mat={}
    print(data)
    for i in actions:mat.update({i:{"F3":[], "F4":[], "FC5":[], "FC6":[]}})
    for i in data:
        for j in data[i]:
            print(j)
            #j.data['FC5']=[0]
            #j.data['FC6']=[0]
            #j.data["F4"]=[0]
            #j.data["F3"]=[0]
    matp={"F3":[], "F4":[], "FC5":[], "FC6":[]}
    for i in data:
    #print("Check 1")
        for j in data[i]:
            for q in j.data:
        #print(j)
        #print("Check 2")
        #print(data[i][j])
                if not j.data[q]:
                    mat[i][q]=[]
                else:
                    mat[i][q].append(list(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(j.data[q]))), j.data[q], deg)).coef))

    for i in ['arm', 'kick', 'neutral']:

        print(i)
        
        for j in mat[i]:
            #print(mat[i][j])
            initlist=[]
            for p in itertools.combinations(mat[i][j], 2):
                #print(str(i+"v"+j))
                initlist.append(ClassifyUtils.euclideandistance(p[0], p[1], len(p[1])))
            #print(str(i+"v"+j))
            matp[j].append(statistics.mean(initlist))
        #for b in matp:
        minst=min(matp, key=lambda x:statistics.mean(matp[x]))
        
            
    
##    for i in matp:
##        for q in matp[i]:
##            print(i, statistics.mean(matp[i]))
##            mat[i][q].append(j.data[q])
##    for i in ['arm', 'kick','neutral']:
##        for j in mat[i]:
##            plt.text(3,2,str(i)+str(j))
##            for ll in mat[i][j]:
##                plt.plot(ll)
##            plt.figure()
##    plt.show()
        

        #print("Check3")
    # Most predictive term analysis
    indx=0
    for i in dd:
        for j in dd[i]:
            j.data=[list(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(j.data['FC5']))),j.data["FC5"], deg)).coef)[indx]]+[list(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(j.data['F4']))),j.data["F4"], deg)).coef)[indx]]+[list(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(j.data['FC5']))), j.data["FC5"], deg)).coef)[indx]]+[list(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(j.data['FC6']))),j.data["FC6"], deg)).coef)[indx]]
            print(j.data)
            #j.data=[statistics.stdev(j.data["F3"]),statistics.stdev(j.data["F4"]),statistics.stdev(j.data["FC5"]),statistics.stdev(j.data["FC6"])]
    
    difference2(dd)
    #print(dd)
##    for j in dd:
##        #print(j)
##        count=0
##        for i in dd[j]:
##            #print(i)
##            li=[]
##            for q in dd[j][i]:
##                #print(q)
##                li.append(list(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(q))), q, 12)).coef))
##           dd del dd[j][i]
##            dd[j][i]=li
##    

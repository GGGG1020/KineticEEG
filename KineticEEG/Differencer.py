import itertools
import pickle
import ClassifyUtils
import numpy
import numpy.polynomial as poly

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

def difference(listy,sensor):
    avg=list()
    #print(listy[ref][sensor])
    for ref in ['arm', 'kick', 'neutral']:
        for i in (itertools.combinations(listy[ref][sensor], 2)):
            avg.append(ClassifyUtils.euclideandistance(i[0], i[1], len(i[0])))
        print(str(ref+"v."+ref)+str(sum(avg)/len(avg)))
    for i in itertools.combinations(['arm', 'kick', 'neutral'],2):
            avglist=list()
            for j in make_unique(combine_between_two_lists(listy[i[0]][sensor], listy[i[1]][sensor])):
                avglist.append(ClassifyUtils.euclideandistance(j[0], j[1], len(j[0])))
            print(str(i[0]+"v."+i[1])+str(sum(avglist)/len(avglist)))
if __name__=='__main__':
    f=open("C:/Users/Gaurav/Desktop/nicesortedfile.dat", "rb")
    pol=f.read()
    dd=pickle.loads(pol)
    #print(dd)
    for j in dd:
        #print(j)
        count=0
        for i in dd[j]:
            #print(i)
            li=[]
            for q in dd[j][i]:
                #print(q)
                li.append(list(poly.polynomial.Polynomial(poly.polynomial.polyfit(list(range(len(q))), q, 6)).coef))
            del dd[j][i]
            dd[j][i]=li
            
    for i in ["F3", "F4", "FC5", "FC6"]:
        print("####"+i)
        difference(dd, i)

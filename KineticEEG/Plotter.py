import matplotlib.pyplot as plt
import sys
import pickle
#plt.ion()

file=sys.argv[1]
f=open(file, "rb")
dict1=pickle.loads(f.read())

for i in dict1:
    for t in dict1[i]:
        plt.plot(dict1[i][t], label=i+" "+t)
plt.legend(loc='best')

plt.show()

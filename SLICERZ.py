import statistics
import math
import matplotlib.pyplot as plt
class Slope:
    def __init__(self, location, dire):
        self.loc=location
        self.dire=dire
    def __repr__(self):
        return "Slope @ "+str(self.loc)+" "+str(self.dire)
class TempFeature:
    def __init__(self, location,data:list):
        self.location=location
    def __repr__(self):
        return "Feature @ "+str(self.location)
class Feature:
    def __init__(self,location,lo):
        self.loc=location
        self.lo=lo
      #  self.dire=direction
    def __repr__(self):
        return "Feature @ "+str(self.loc)+" with shape"+str(self.lo)
class Classifier:
    def __init__(self):
        self.train1=[]
    def train(self, data):
        self.finder=FeatureFinder()
        deftolerance=self.finder.train(data)
        tree=self.finder.scan_data(data)
        print(tree)
        self.outline=DataOutline(tree, data)
        self.outline.scan()
    def classify(self, data):
       return self.outline.runit(data)
class ClassifierTester:
    def __init__(self):
        self.dat=[90.37764633360645, 91.014555470066, 91.721352379002,
                     92.42960343758679, 93.1270701625897, 93.83838282891722,
                     94.61756769951398, 95.62545876818837, 96.7447585417242,
                     97.7838836655262, 98.66583077945143, 99.35386506293614,
                     99.82108980552063, 100.0453546435296, 100.02926641061357,
                     99.88353380337247, 99.65276313158463, 99.20857016079242, 98.5202096519103, 97.58587741736116,
                     96.41784563807974, 95.04112717584547,
                     93.50302041301316, 91.884516870911, 90.31773467696574]
        self.dat1=[90.37764633360645, 91.014555470066, 91.721352379002,
                     93.42960343758679, 92.1270701625897, 93.83838282891722,
                     94.61756769951398, 95.62545876818837, 96.7447585417242,
                     97.7838836655262, 97.66583077945143, 99.35386506293614,
                     100.82108980552063, 100.0453546435296, 101.02926641061357,
                     99.88353380337247, 99.65276313158463, 98.20857016079242, 97.5202096519103, 97.58587741736116,
                     95.41784563807974, 95.04112717584547,
                     93.50302041301316, 92.884516870911, 90.31773467696574]
        self.classif=Classifier()
        plt.ion()
        plt.plot(self.dat)
        plt.plot(self.dat1)
    def run(self):
        self.classif.train(self.dat)
        print(self.classif.classify(self.dat1))
    
        
        
class DataOutline:
    def __init__(self,download,data):
        self.listy=[]
        self.outline=[]
        self.download=download
        print(self.download)
        self.data=data
        for i in range(len(download)-1):
            self.listy.append(data[download[i].location:download[i+1].location])
    def __process(self, data):
        liz=difference_list(data)
        degs=[math.degrees(math.atan(i)) for i in liz]
        def t(x):
            angles=1.0-(x*(0.5/45))
            if angles<0:
                angles=angles=1.0-((180-x)*(0.5/45))
            return angles
        return [[t(abs(degs[i+1]-degs[i])) for i in range(len(degs)-1)],degs]
    def dict_process(self, data):
        liz=difference_list(data)
        degs=[math.degrees(math.atan(i)) for i in liz]
        def t(x):
            angles=1.0-(x*(0.5/45))
            if angles<0:
                angles=angles=1.0-((180-x)*(0.5/45))
            return angles
        return degs
    def t(self, x):
            angles=1.0-(x*(0.5/45))
            if angles<0:
                angles=angles=1.0-((180-x)*(0.5/45))
            return angles
            return degs
    def features_present(self, othertmpft):

       processed=self.dict_process(othertmpft)
       features=list()
       for i in self.outline:
           if type(i)==Feature:features.append(i)
           
       print(len(processed))
       sendback=list()
       for i in features:
           currindx=i.loc#/len(self.data)
           #currindx=round(currindx*len(processed))
           print(currindx)
           important=processed[currindx-2:currindx+2]
           print(len(important))
           sendback.append(self.t(abs(statistics.mean(important)-i.lo)))
       print(sendback)
       return sendback
    def runit(self, data):
        ge=list()
        rep=list()
        present=self.features_present(data)
        count=0
        lim=0
        def t(x):
            angles=1.0-(x*(0.5/45))
            if angles<0:
                angles=angles=1.0-((180-x)*(0.5/45))
            return angles
        for i in range(len(self.outline)-1):
            ge.append(self.dict_process(data[self.outline[i].loc:self.outline[i+1].loc]))
        ge.append(self.dict_process(data[self.outline[-1].loc:len(data)-1]))
        print(ge)
        ge=filter(lambda x:bool(not len(x)==0), ge)
        ge=list(ge)
        print(ge)
        #print(self.outline)
        sumo=0
        slopes=filter(lambda x:bool(type(x)==Slope),self.outline)
        slopes=list(slopes)
        for i in range(len(ge)):
            curr=ge[i]
            currcomp=slopes[i]
            su=0
            for r in curr:
                su+=t(abs(r-currcomp.dire))
            sumo+=(su/len(curr))
        for i in present:
            sumo+=i
        sumo=sumo/(len(ge)+len(present))
        return sumo        
##        print(ge)
##        print(self.outline)
##        for i in self.outline:
##           if ge[count] in i.dire:lim+=1;print(ge[count])
##           count+=1
##        print(lim)
##        return (len(self.outline)*0.8)<=lim
##            
##            
    def scan(self):
        dre=list()
        final=list()
        dre=self.dict_process(self.data)
        pol=[]
        oo=list()
        for d in self.listy:
            r=self.__process(d)
            if len(r[1])<2 and not len(r[1])==0:pol.append(statistics.mean(r[1]))
            elif len(r[1])==0:pass
            else:pol.append(statistics.mean(r[1]))
            print(pol)
        for i in range(len(pol)):
            final.append(Slope(self.download[i].location, pol[i]))
            print(final)
        del self.download[0]
        del self.download[-1]
        last=1
        for i in range(len(self.download)):
            final.insert(i+last, Feature(self.download[i].location, statistics.mean(dre[self.download[i].location-2:self.download[i].location+2])))
            last+=1
            print(final)
        self.outline=final
        print(self.outline)
class FeatureFinder:
    def __init__(self):
        self.similarity_percentage=float()
        self.similarity_percentage_area=Area(0,0)
    def train(self, trainer):
        #Here, we initialize values for the ff
        mylin=self.__process(trainer)
        self.similarity_percentage_area=Area(statistics.mean(mylin[0:4]), statistics.stdev(mylin))
        print(self.similarity_percentage_area)
        self.similarity_percentage_area.maxy=1.0 #Force acceptance
        return self.similarity_percentage_area
    def __process(self, data):
        liz=difference_list(data)
        degs=[math.degrees(math.atan(i)) for i in liz]
        def t(x):
            angles=1.0-(x*(0.5/45))
            if angles<0:
                angles=angles=1.0-((180-x)*(0.5/45))
            return angles
        return [t(abs(degs[i+1]-degs[i])) for i in range(len(degs)-1)]
    def scan_data(self, data):
        bh=self.__process(data)
        count=0
        j=list([TempFeature(0,data)])
        feature_watch=bool(False)
        for i in bh:
            if i in self.similarity_percentage_area and feature_watch:
                print("Feature", count)
                print("Remember:", data[count])
                j.append(TempFeature(count,data))
                feature_watch=False
                count+=1
                continue
            elif not i in self.similarity_percentage_area and feature_watch:
                print("Outliar", count)
                print("Remember:", data[count])
               # data[count]=statistics.mean(data[count-2:count+2])
                feature_watch=False
                count+=1
                continue
            elif not i in self.similarity_percentage_area and not feature_watch:
                feature_watch=True
                print('feature watch',count)
                count+=1
                continue
            else:
                count+=1
                continue
        j.append(TempFeature(len(data)-1,data))
        return j
class FeatureTester:
    def __init__(self):
        self.my=FeatureFinder()
        self.my.train([90.37764633360645, 91.014555470066, 91.721352379002,
                     92.42960343758679, 93.1270701625897, 93.83838282891722,
                     94.61756769951398, 95.62545876818837, 96.7447585417242,
                     97.7838836655262, 98.66583077945143, 99.35386506293614,
                     99.82108980552063, 100.0453546435296, 100.02926641061357,
                     99.88353380337247, 99.65276313158463, 99.20857016079242, 98.5202096519103, 97.58587741736116,
                     96.41784563807974, 95.04112717584547,
                     93.50302041301316, 91.884516870911, 90.31773467696574])
        self.data=[90.37764633360645, 91.014555470066, 91.721352379002,
                     92.42960343758679, 93.1270701625897, 93.83838282891722,
                     94.61756769951398, 95.62545876818837, 96.7447585417242,
                     97.7838836655262, 98.66583077945143, 99.35386506293614,
                     99.82108980552063, 100.0453546435296, 100.02926641061357,
                     99.88353380337247, 99.65276313158463, 99.20857016079242, 98.5202096519103, 97.58587741736116,
                     96.41784563807974, 95.04112717584547,
                     93.50302041301316, 91.884516870911, 90.31773467696574]
    def run(self):
        j=self.my.scan_data([90.37764633360645, 91.014555470066, 91.721352379002,
                     92.42960343758679, 93.1270701625897, 93.83838282891722,
                     94.61756769951398, 95.62545876818837, 96.7447585417242,
                     97.7838836655262, 98.66583077945143, 99.35386506293614,
                     99.82108980552063, 100.0453546435296, 100.02926641061357,
                     99.88353380337247, 99.65276313158463, 99.20857016079242, 98.5202096519103, 97.58587741736116,
                     96.41784563807974, 95.04112717584547,
                     93.50302041301316, 91.884516870911, 90.31773467696574])
        print(j)
        rt=DataOutline(j, self.data)
        self.g=rt.scan()
        print(self.g)
        self.data=[90.37764633360645, 91.014555470066, 91.721352379002,
                     92.42960343758679, 93.1270701625897, 93.83838282891722,
                     94.61756769951398, 95.62545876818837, 96.7447585417242,
                     97.7838836655262, 98.66583077945143, 99.35386506293614,
                     99.82108980552063, 100.0453546435296, 100.02926641061357,
                     99.88353380337247, 99.65276313158463, 99.20857016079242, 98.5202096519103, 97.58587741736116,
                     96.41784563807974, 95.04112717584547,
                     93.50302041301316, 91.884516870911, 90.31773467696574]
class SliceTrainer:
    def __init__(self):
        self.data=list()
        self.myclassifiers=list()
    def train(self, data):
        if len(self.myclassifiers)==0:
            for i in self.__split_into(data):
                j=iClassifier()
                j.train(data)
                self.myclassifiers.append(j)
        else:
            for i in self.myclassifiers:
                i.train(data)
    def classify(self, other):
        for i in range(len(self.__split_into(other))-1):pass            
    def __split_into(self, listy):
        g=list(range(0, len(listy), 4))
        newlist=list()
        g.append(len(listy))
        for i in range(len(g)-1):
            newlist.append(listy[g[i]:g[i+1]])
        return newlist
class Area:
    def __init__(self, base, plusorminus):
        self.miny=base-plusorminus
        self.maxy=base+plusorminus
    def __contains__(self, item):
        return bool(item>=self.miny and self.maxy>=item)
    def __repr__(self):
        return str("Area between "+str(self.miny)+" and "+str(self.maxy)+" ,inclusive")
class FeaturesTrainer:
    pass
##def find_pattern(liz):
##	blap=[]
##	degs=[math.degrees(math.atan(i)) for i in liz]
##	counter=0
##	prev=0
##	for i in liz:
##		blap.append(i)
##		if counter>=2:
##			myarea=Area(prev,22.5)
##			if not i in myarea:
##				print("Hi")
##		prev=i
##		print(i)
##		counter+=1
def find_pattern(liz):
    blap=[]
    watch=True
    degs=[math.degrees(math.atan(i)) for i in liz]
    counter=0
    tmp=[]
    prev=0
    for i in degs:
            blap.append(i)
            if counter>=2:
                myarea=Area(statistics.mean(blap), statistics.stdev(blap))
                print(myarea)
                print(i)
                if not i in myarea:
                        rt=degs[counter:counter+4]
                        if not statistics.mean(rt) in myarea:print("feature")
                        else:print("j")
            prev=i
            counter+=1
    print(degs)
def find_pattern_no_degreez(liz):
    blap=[]
    watch=True
    degs=liz
    counter=0
    tmp=[]
    prev=0
    for i in degs:
            blap.append(i)
            if counter>=2:
                myarea=Area(statistics.mean(blap), statistics.stdev(blap))
                print(myarea)
                print(i)
                if not i in myarea:
                        rt=degs[counter:counter+4]
                        if not statistics.mean(rt) in myarea:print("feature")
                        else:print("j")
            prev=i
            counter+=1
    print(degs)
def percent_based(liz):
    degs=[math.degrees(math.atan(i)) for i in liz]
    t=lambda x: 1.0-(x*(-0.5/45))
    hhh=[t(abs(u[i+1]-u[i])) for i in range(len(u)-1)]
    return degs
def highpass(signal):
        iir_tc=0.98
        background=signal[0]
        hp=list()
        hp.append(0)
        for i in range(1, len(signal)):
            signal[i]=float(signal[i])
            background=(iir_tc*background)+(1-iir_tc)*signal[i]
            hp.append(signal[i]-background)
        return hp
def difference_list(listu):
    return [listu[i+1]-listu[i] for i in range(len(listu)-1)]
class iClassifier:
    def __init__(self):
        self.data=list()
        self.tree=tuple()
        self.index=0
    def __with_angle_line(self,data):
        dat=[data[i]-data[i+1] for i in range(len(data)-1)]
        angles=[math.degrees(math.atan(i)) for i in dat]
        avangles=statistics.mean(angles)
        std=statistics.stdev(angles)
        return [angles, avangles, std]                
    def find_metric(self):
        self.tree=list([self.__with_angle_line(self.data)[0],self.__with_angle_line(self.data)[1], self.__with_angle_line(self.data)[2]])
    def overall_angle(self, data):
        slope1=data[0]-data[len(data)-1]
        angle1=math.degrees(math.atan(slope))
    def cmp_with(self, other):
        tree=self.__with_angle_line(other)
        counter=0
        results=list()
        for i in self.tree[0]:
            feasiblearea=Area(i, 45)
            print(feasiblearea.maxy, feasiblearea.miny)
            results.append(tree[0][counter] in feasiblearea)
            counter+=1
        if False not in results:
            return True
        else:return False
    
    def train(self, myint, indx):
        if not self.data:
            self.data=myint
            self.find_metric()
            self.indexarea=Area(indx, 1)
            
        else:
            self.data=[statistics.mean([myint[i], self.data[i]]) for i in range(len(myint)-1)]
            self.find_metric()
            index=statistics.mean([index, indx])
            tolerance=statistics.stdev([index, indx])
            self.indexarea=Area(index, tolerance)
    def classify(self, other , indexof):
        if indexof in self.indexarea:return self.cmp_with(other)       
if __name__=='__main__':
    a=ClassifierTester()
    a.run()


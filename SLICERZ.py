import statistics
import tkinter 
import math
import numpy
import matplotlib.pyplot as plt
global SENSOROFINTEREST
SENSOROFINTEREST=["F3", "F4", "T7","T8"]
class Modulator:
    def __init__(self):
        self.register_and_potentiate=list()
    def register(self,what):
        self.register_and_potentiate.append(what)
    def feature_present_penalize(self, data, features):
        j=list()
        for i in data.outline:
            if(type(features)==type(i)):
                j.append(i)
        a=min(j, key=lambda x:(abs(data.loc-x.loc)))
        penalize_by=abs(a.loc-features.loc)
    
    def scan_for_potentiate(self, data, percentage, outline):
        """This is slightly difficult"""
        for  i in self.register_and_potentiate:
            pass
            #todo/t self.feature_present_or_not(data,
class UniformInterfaceLiveRunClassifier:
    def __init__(self):
        self.data=dict({"F3":[], "F4":[], "T7":[], "T8":[]})
        self.myclassifs={}
        for i in SENSOROFINTEREST:
            self.myclassifs[i]=Classifier()
    def enhance_results(self, data):
        penalize_by=0
        promote_by=0
        for i in data:
            if i <= 0.6:
                penalize_by+=0.1
            elif i>=0.8:
                promote_by+=0.1
        am=statistics.mean(data)
        am+=promote_by
        am-=penalize_by
        return am
    def enhance_results(self, data):
        data1=list()
        percent=1
        me=float()
        percent2=1
        for i in data:
            if i <= 0.6:
                percent+=((0.6-i)/float(statistics.mean(data)))
                #penalize_by+=0.1
            elif i>=0.8: 
                percent2+=((i-0.8)/float(statistics.mean(data)))
                #data1.append(i)
        me=statistics.mean(data)
        me-=percent
        me+=percent2
        return me
    def enhance_results(self, data):
        data1=list()
        penalize_by=0
        promote_by=0
        g=Area(statistics.mean(data), statistics.stdev(data))
        for i in data:
            if not i in g and (i< statistics.mean(data)):
                penalize_by+=((statistics.mean(data)-statistics.stdev(data))-i)/float(statistics.mean(data))
            
            elif not i in g and (i>statistics.mean(data)):
                promote_by+=(i-(statistics.mean(data)-statistics.stdev(data)))/float(statistics.mean(data))

        me=statistics.median(data)
        me=penalize_by
        me*=promote_by
        return me
    def train(self,data):
        """Just give a dictionary that follows:
                 {"FC5":[s1,s2,s3,s4...sN], ....}
                 """
        for i in self.myclassifs:
            self.myclassifs[i].train(data[i])
    def enhance_results_special(self, dat):
        low25=numpy.percentile(dat, 25)
        high75=numpy.percentile(dat, 75)
        if ((statistics.mean(dat)-low25)>(high75-statistics.mean(dat))):
            return (statistics.mean(dat)-low25)+statistics.mean(dat)
        else:
            return statistics.mean(dat)-(high75-statistics.mean(dat))
##    def enhance_results_special(self, dat):
##        low25=numpy.percentile(dat, 25)
##        high75=numpy.percentile(dat, 75)
##        if ((statistics.mean(dat)-low25)>(high75-statistics.mean(dat))):
##            dat.append(float(max(dat)+(statistics.mean(dat)-low25)))
##        else:
##            dat.append(float(min(dat)-(high75-statistics.mean(dat))))
##        return statistics.mean(dat)
    def test_classifiers(self, frozen, indx, indx1):
        toret=list()
        for i in self.myclassifs:
            toret.append(self.myclassifs[i].classify(frozen[i][2][indx:indx1])[1])
        root=tkinter.Tk()
        root.title("SLICERZ Monitor")
        #label=tkinter.Label(text=statistics.mean((toret)))
        label=tkinter.Label(text=self.enhance_results(toret))
        label.pack()
    def classify(self, frozen):
        toret=list()
        for i in self.myclassifs:
            toret.append(self.myclassifs[i].classify(frozen[i])[1])
        #root=tkinter.Tk()
        #root.title("SLICERZ Monitor")
        #label=tkinter.Label(text=statistics.mean((toret)))
        #label=tkinter.Label(text=self.enhance_results(toret))
        #label.pack()
        return self.enhance_results_special(toret)   
class LiveRunClassifier:
    def __init__(self):
        self.data=dict({"F3":[], "F4":[], "T7":[], "T8":[]})
        self.myclassifs={}
        for i in SENSOROFINTEREST:
            self.myclassifs[i]=Classifier()
    def enhance_results(self, data):
        penalize_by=0
        promote_by=0
        for i in data:
            if i <= 0.6:
                penalize_by+=0.1
            elif i>=0.8:
                promote_by+=0.1
        am=statistics.mean(data)
        am+=promote_by
        am-=penalize_by
        return am
    def enhance_results(self, data):
        data1=list()
        percent=1
        me=float()
        percent2=1
        for i in data:
            if i <= 0.6:
                percent+=((0.6-i)/float(statistics.mean(data)))
                #penalize_by+=0.1
            elif i>=0.8: 
                percent2+=((i-0.8)/float(statistics.mean(data)))
                #data1.append(i)
        me=statistics.mean(data)
        me-=percent
        me+=percent2
        return me
    def enhance_results(self, data):
        data1=list()
        penalize_by=0
        promote_by=0
        g=Area(statistics.mean(data), statistics.stdev(data))
        for i in data:
            if not i in g and (i< statistics.mean(data)):
                penalize_by+=((statistics.mean(data)-statistics.stdev(data))-i)/float(statistics.mean(data))
            
            elif not i in g and (i>statistics.mean(data)):
                promote_by+=(i-(statistics.mean(data)-statistics.stdev(data)))/float(statistics.mean(data))

        me=statistics.median(data)
        me=penalize_by
        me*=promote_by
        return me
    def run_train(self,data):
        """Just give a dictionary that follows:
                 {"FC5":[s1,s2,s3,s4...sN], ....}
                 """
        for i in self.myclassifs:
            self.myclassifs[i].train(data[i])
    def enhance_results_special(self, dat):
        low25=numpy.percentile(dat, 25)
        high75=numpy.percentile(dat, 75)
        if ((statistics.mean(dat)-low25)>(high75-statistics.mean(dat))):
            return (statistics.mean(dat)-low25)+statistics.mean(dat)
        else:
            return statistics.mean(dat)-(high75-statistics.mean(dat))
##    def enhance_results_special(self, dat):
##        low25=numpy.percentile(dat, 25)
##        high75=numpy.percentile(dat, 75)
##        if ((statistics.mean(dat)-low25)>(high75-statistics.mean(dat))):
##            dat.append(float(max(dat)+(statistics.mean(dat)-low25)))
##        else:
##            dat.append(float(min(dat)-(high75-statistics.mean(dat))))
##        return statistics.mean(dat)
    def test_classifiers(self, frozen, indx, indx1):
        toret=list()
        for i in self.myclassifs:
            toret.append(self.myclassifs[i].classify(frozen[i][2][indx:indx1])[1])
        root=tkinter.Tk()
        root.title("SLICERZ Monitor")
        #label=tkinter.Label(text=statistics.mean((toret)))
        label=tkinter.Label(text=self.enhance_results(toret))
        label.pack()
    def test_classifiers_ret(self, frozen):
        toret=list()
        for i in self.myclassifs:
            toret.append(self.myclassifs[i].classify(frozen[i])[1])
        #root=tkinter.Tk()
        #root.title("SLICERZ Monitor")
        #label=tkinter.Label(text=statistics.mean((toret)))
        #label=tkinter.Label(text=self.enhance_results(toret))
        #label.pack()
        return self.enhance_results_special(toret)   
class RunThroughClassifier:
    def __init__(self, frozen):
        self.data=frozen
        self.myclassifs={}
        for i in self.data:
            self.myclassifs[i]=Classifier()
        
    def enhance_results(self, data):
        penalize_by=0
        promote_by=0
        for i in data:
            if i <= 0.6:
                penalize_by+=0.1
            elif i>=0.8:
                promote_by+=0.1
        am=statistics.mean(data)
        am+=promote_by
        am-=penalize_by
        return am
    def enhance_results(self, data):
        data1=list()
        percent=1
        me=float()
        percent2=1
        for i in data:
            if i <= 0.6:
                percent+=((0.6-i)/float(statistics.mean(data)))
                #penalize_by+=0.1
            elif i>=0.8: 
                percent2+=((i-0.8)/float(statistics.mean(data)))
                #data1.append(i)
        me=statistics.mean(data)
        me-=percent
        me+=percent2
        return me
    def enhance_results(self, data):
        data1=list()
        penalize_by=0
        promote_by=0
        g=Area(statistics.mean(data), statistics.stdev(data))
        for i in data:
            if not i in g and (i< statistics.mean(data)):
                penalize_by+=((statistics.mean(data)-statistics.stdev(data))-i)/float(statistics.mean(data))
            
            elif not i in g and (i>statistics.mean(data)):
                promote_by+=(i-(statistics.mean(data)-statistics.stdev(data)))/float(statistics.mean(data))

        me=statistics.median(data)
        me=penalize_by
        me*=promote_by
        return me
    def run_train(self,indx, indx1):
        for i in self.myclassifs:
            self.myclassifs[i].train(self.data[i][2][indx:indx1])
    def enhance_results_special(self, dat):
        low25=numpy.percentile(dat, 25)
        high75=numpy.percentile(dat, 75)
        if ((statistics.mean(dat)-low25)>(high75-statistics.mean(dat))):
            return (statistics.mean(dat)-low25)+statistics.mean(dat)
        else:
            return statistics.mean(dat)-(high75-statistics.mean(dat))
##    def enhance_results_special(self, dat):
##        low25=numpy.percentile(dat, 25)
##        high75=numpy.percentile(dat, 75)
##        if ((statistics.mean(dat)-low25)>(high75-statistics.mean(dat))):
##            dat.append(float(max(dat)+(statistics.mean(dat)-low25)))
##        else:
##            dat.append(float(min(dat)-(high75-statistics.mean(dat))))
##        return statistics.mean(dat)
    def test_classifiers(self, frozen, indx, indx1):
        toret=list()
        for i in self.myclassifs:
            toret.append(self.myclassifs[i].classify(frozen[i][2][indx:indx1])[1])
        root=tkinter.Tk()
        root.title("SLICERZ Monitor")
        #label=tkinter.Label(text=statistics.mean((toret)))
        label=tkinter.Label(text=self.enhance_results(toret))
        label.pack()
    def test_classifiers_ret(self, frozen, indx, indx1):
        toret=list()
        for i in self.myclassifs:
            toret.append(self.myclassifs[i].classify(frozen[i][2][indx:indx1])[1])
        #root=tkinter.Tk()
        #root.title("SLICERZ Monitor")
        #label=tkinter.Label(text=statistics.mean((toret)))
        #label=tkinter.Label(text=self.enhance_results(toret))
        #label.pack()
        return self.enhance_results_special(toret)   
class Slope:
    def __init__(self, location, dire):
        self.loc=location
        self.dire=dire
    def __repr__(self):
        return "Slope @ "+str(self.loc)+" "+str(self.dire)
    def __eq__(self, other):
        if type(other)==Slope:
            return self.loc==other.loc and self.dire==other.dire
        elif type(other) in [list, tuple, set, bool,dict]:
            return self.loc==other[0].loc and self.dire==other[0].dire
    def __hash__(self):
        """I am implementing this in order to allow slopes to be dict keys"""
        return hash(tuple((self.loc, self.dire)))
    def tupelize(self):
        return tuple((self.loc,self.dire))
class TrainingNotCompatible(Exception):
    pass
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
    def __eq__(self, other):
        if type(other)==Feature:
            return self.loc==other.loc and self.dire==other.dire
        elif type(other) in [list, tuple, set, bool,dict]:
            return self.loc==other[0].loc and self.dire==other[0].dire
    def __hash__(self):
        """I am implementing this in order to allow Features to be dict keys"""
        return hash(tuple((self.loc, self.lo)))
    def tupelize(self):
        return tuple((self.loc, self.lo))
class Trainer:
    def __init__(self, dataoutline, secondordermodel):
        self.secondorder=secondordermodel
        self.dat=dataoutline
    def train(self, data):
        finder=FeatureFinder()
        self.len=len(data)
        tolerance=finder.train(data)
        tree=finder.scan_data(data)
        outline=DataOutline(tree, data, Modulator())
        outline.scan()
#        if self.features_present1(self.dat.outline, outline.outline)<0.5:
  #          raise TrainingNotCompatible("The data trained and this new are not related significantly in shape. Please retrain, or check your EEG system for problems")
        myl=self.tag_both(self.dat.outline, outline.outline)
        self.calculate_adjustment(myl)
    def calculate_adjustment(self, arg):
        #print("whole"+str(arg))
        for i in arg:
            ##print("arg"+str(arg[i]))
            for j in arg[i]:
                weight_factor=(self.len-j[1])/self.len
                #print(weight_factor)
               # print(self.dat.outline)
                myindx=self.dat.outline.index(i)
                if type(j[0]) is Feature:
                    self.dat.outline[myindx].loc=numpy.average([self.dat.outline[myindx].loc, j[0].loc], weights=[1,weight_factor])
                    self.dat.outline[myindx].lo=weighted_average_of_two_arrays(self.dat.outline[myindx].lo, j[0].lo ,weighted=[1,weight_factor])
                    #self.secondorder.add(j[0])
                elif  type(j[0]) is Slope:
                    print("Slope before: \t"+str(self.dat.outline[myindx]))
                    self.dat.outline[myindx].loc=numpy.average([self.dat.outline[myindx].loc, j[0].loc], weights=[1,weight_factor])
                    print("Intervening Slope : \t"+str(j[0]))
                    self.dat.outline[myindx].dire=numpy.average([self.dat.outline[myindx].dire, j[0].dire], weights=[1,weight_factor])
                    print("Slope after: \t"+str(self.dat.outline[myindx]))
                    #self.secondorder.add(j[0])
    def weighted_average_of_two_arrays(self,avg1, avg2, weighted=[2,1]):
        toreturn=list()
        for i in range(len(avg2)-1):
            toreturn.append(np.average([avg1[i], avg2[i]], weights=weighted))
        return toreturn
    def tag_both(self, myout, theirout):
        """Tag the newlist onto the old one. Tagged dictionary"""
        features1=list()
        slopes1=list()
        features2=list()
        slopes2=list()
        for i in myout:
            if type(i)==Slope:
                slopes1.append(i)
            else:
                features1.append(i)
        for j in theirout:
            if type(j)==Slope:
                slopes2.append(j)
            else:
                features2.append(j)
        tagdict=dict()
        for i in myout:
            tagdict[i]=[]
        for i in features2:
            j=min(features1, key=lambda x:abs(features2[i].loc-features1[x].loc))
            tagdict[features1[j.index()]].append(tuple((i, abs(i.loc-j.loc))))
        for i in slopes2:
            j=min(slopes1, key=lambda x:abs(slopes2[slopes2.index(i)].loc-slopes1[slopes1.index(x)].loc))
            tagdict[slopes1[slopes1.index(j)]].append(tuple((i, abs(i.loc-j.loc))))
        return tagdict
    def __process(self, data):
        liz=difference_list(data)
        degs=[math.degrees(math.atan(i)) for i in liz]
        def t(x):
            angles=1.0-(x*(0.5/45))
            if angles<0:
                angles=angles=1.0-((180-x)*(0.5/45))
            return angles
        return [[t(abs(degs[i+1]-degs[i])) for i in range(len(degs)-1)],degs]
    def features_present1(self, myoutiline, othertmpft):
        a=FeatureFinder()
        a.train(othertmpft)
        j=a.scan_data(othertmpft)
        features=list()
        dre=self.dict_process(othertmpft)
        sendback=list()
        final_list=list()
        del j[0]
        del j[len(j)-1]
        for i in j:
            #print(i.location)
            if i.location<2:
                final_list.append(Feature(i.location, statistics.mean(dre[i.location-1:i.location+3])))
            else:
                final_list.append(Feature(i.location, statistics.mean(dre[i.location-2:i.location+2])))
        for i in myoutline:
           if type(i)==Feature:features.append(i)
        for i in features:
            if len(final_list)>0:l=min(final_list, key=lambda x: abs(i.loc-x.loc))
            else:return [0]*len(myoutline)
            dis=len(othertmpft)-abs(i.loc-l.loc)
            penalize_by=dis/len(othertmpft)
            #print(penalize_by)
            sendback.append(statistics.mean([penalize_by, self.t(abs(i.lo-l.lo))]))
        #print(sendback)
        return sendback    
class Classifier:
    def __init__(self):
        self.train1=[]
    def train(self, data):
        self.finder=FeatureFinder()
        deftolerance=self.finder.train(data)
        tree=self.finder.scan_data(data)
        #print(tree)
        self.a=Modulator()
        self.outline=DataOutline(tree, data, self.a)
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
        self.dat1=numpy.add(self.dat, numpy.random.normal(0,1,25))
        #self.dat1=[0]*25
        self.classif=Classifier()
        plt.ion()
        plt.plot(self.dat)
        plt.plot(self.dat1)
    def run(self):
       #g=FeatureFinder()
        #g.train(self.dat1)
        #print(g.scan_data(self.dat1))
        self.classif.train(self.dat)
        #print(self.classif.classify(self.dat1))
        ##self.train()
    def train(self):
        b=Trainer(self.classif.outline, Modulator())
        b.train([1]*25)
class DataOutline:
    def __init__(self,download,data, modulator=None):
        self.listy=[]
        self.outline=[]
        self.mod=modulator
        self.download=download
        self.data=data
        if download:
            for i in range(len(download)-1):
                self.listy.append(data[download[i].location:download[i+1].location])
    @classmethod
    def from_feature_set(cls, ftrset):
        ret_cls=cls(None, None)
        ret_cls.outline=ftrset
        return ret_cls
    def absolute_similarity(self, data, ref):
        liz=difference_list(data)
        degs=[math.degrees(math.atan(i)) for i in liz]
        perm=degs[ref]
        def t(x):
            angles=1.0-(x*(0.5/45))
            if angles<0:
                angles=angles=1.0-((180-x)*(0.5/45))
            return angles
        return [[[t(abs(degs[ref]-degs[ref-s])) for s in range(ref)]], [[t(abs(degs[ref]-degs[ref+i])) for i in range(int(len(degs)-ref))]]]
    def check_stuff(self, otheroutline):
        buildlist1=list()
        buildlist2=list()
        for i in self.outline:
            buildlist1.append(i.loc)
        for j in otheroutline:
            buildlist2.append(j.loc)
        for i in buildlist1:
            pass
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
    def adjust(self, data):
        buildmap=list()
        for i in outline:
            buildmap.append(i.loc)
            
    def features_present1(self, othertmpft):
        a=FeatureFinder()
        a.train(othertmpft)
        j=a.scan_data(othertmpft)
        features=list()
        dre=self.dict_process(othertmpft)
        sendback=list()
        final_list=list()
        del j[0]
        del j[len(j)-1]
        for i in j:
            #print(i.location)
            if i.location<2:
                final_list.append(Feature(i.location, statistics.mean(dre[i.location-1:i.location+3])))
            else:
                final_list.append(Feature(i.location, statistics.mean(dre[i.location-2:i.location+2])))
        for i in self.outline:
           if type(i)==Feature:features.append(i)
        for i in features:
            if len(final_list)>0:l=min(final_list, key=lambda x: abs(i.loc-x.loc))
            else:return [0]*len(self.outline)
            dis=len(othertmpft)-abs(i.loc-l.loc)
            penalize_by=dis/len(othertmpft)
            #print(penalize_by)
            sendback.append(statistics.mean([penalize_by, self.t(abs(i.lo-l.lo))]))
      #  print(sendback)
        #print("I am features1")
        return self.find_outliar(sendback)            
    def features_present(self, othertmpft):

       processed=self.dict_process(othertmpft)
       features=list()
       for i in self.outline:
           
           if type(i)==Feature:features.append(i)
           
    #   print(len(processed))
       sendback=list()
       for i in features:
           currindx=i.loc#/len(self.data)
           #currindx=round(currindx*len(processed))
      #     print(currindx)
           important=processed[currindx-self.ihatethis:currindx+self.ihatethis]
       #    print(len(important))
           sendback.append(self.t(abs(statistics.mean(important)-i.lo)))           
       #print(sendback)
       return sendback
    def find_outliar(self, data):
        if not len(data)>=2: myarea=Area(data, 0)
        else:myarea=Area(statistics.mean(data), statistics.stdev(data)*2)
        return list(filter(lambda x:bool(x in myarea), data))    
    def runit(self, data):
        ge=list()
        rep=list()
        present=self.features_present1(data)
        #print(present)
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
      #  print(ge)
        ge=filter(lambda x:bool(not len(x)==0), ge)
        ge=list(ge)
        #print(ge)
        #print(self.outline)
        sumo=0
        slopes=filter(lambda x:bool(type(x)==Slope),self.outline)
        slopes=list(slopes)
        medianthis=list()
        ind=[]
        for i in range(len(ge)):
            curr=ge[i]
            #print(slopes)
            currcomp=slopes[i]
            su=0
            for r in curr:
                ind.append(t(abs(r-currcomp.dire)))
            medianthis.append(statistics.mean(self.find_outliar(ind)))
        for i in present: 
            medianthis.append(i)
        #print(medianthis)
        #print(self.find_outliar(medianthis))
        #print("######################################"+str([statistics.mean(medianthis),statistics.median(medianthis)]))
        return list([statistics.mean(medianthis),statistics.median(medianthis)])
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
          #  print(pol)
        for i in range(len(pol)):
            final.append(Slope(self.download[i].location, pol[i]))
           ## print(final)
        del self.download[0]
        del self.download[-1]
        last=1
        for i in range(len(self.download)):
            try:
                final.insert(i+last, Feature(self.download[i].location, statistics.mean(dre[self.download[i].location-2:self.download[i].location+2])))
            except statistics.StatisticsError:
                #del  final[i-1]
                pass
            last+=1
          #  print(final)
        self.outline=final
      #  print(self.outline)
class FeatureFinder:
    def __init__(self):
        self.similarity_percentage=float()
        self.similarity_percentage_area=Area(0,0)
    def train(self, trainer):
        #Here, we initialize values for the ff
        mylin=self.__process(trainer)
        #print(mylin)
        #print("\n\n out"+str(mylin))
        a=list(filter(lambda x:bool(x>=numpy.percentile(mylin,75)), mylin))
        self.similarity_percentage_area=Area(statistics.median(mylin), statistics.variance(mylin))
        #print((statistics.median_grouped(mylin),  statistics.variance(mylin)))
        #print(self.similarity_percentage_area)
        self.similarity_percentage_area.maxy=1.0 #100 will work.
        return self.similarity_percentage_area
    def __process(self, data):
        #print("In"+str(data))
        liz=difference_list(data)
        #print("liz"+str(liz))
        degs=[math.degrees(math.atan(i)) for i in liz]
        #print(degs)
        def t(x):
            angles=1.0-(x*(0.5/45))
            if angles<0:
                angles=angles=1.0-((180-x)*(0.5/45))
            return angles
        #print("Hi"+str([t(abs(degs[i+1]-degs[i])) for i in range(len(degs)-1)]))
        return [t(abs(degs[i+1]-degs[i])) for i in range(len(degs)-1)]
    
    def scan_data(self, data):
        bh=self.__process(data)
        count=0
        previous=0
        j=list([TempFeature(0,data)])
        feature_watch=bool(False)
        for i in bh:
            if feature_watch and(i in self.similarity_percentage_area or i>previous) :
                #print("Feature", count)
                #print("Remember:", data[count])
                j.append(TempFeature(count,data))
                feature_watch=False
                count+=1
                continue
            elif feature_watch and  (not i in self.similarity_percentage_area  or i<previous):
                #print("Outliar", count)
                #print("Remember:", data[count])
               # data[count]=statistics.mean(data[count-2:count+2])
                feature_watch=False
                count+=1
                continue
            elif not i in self.similarity_percentage_area and not feature_watch:
                feature_watch=True
              #  print('feature watch',count)
                count+=1
                previous=i
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
      #  print(j)
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
        if type(base)==list and len(base)<=1:
            base=base[0] if len(base)==1 else 0
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
##    for i in range(1):
##        a=ClassifierTester()
##        a.run()
    pass

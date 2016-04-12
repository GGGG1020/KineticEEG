import ClassifyUtils
import statistics
import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/")
from SLICERZ import Area


"""
A little documentation needed here.
Here is the detector.It recieves live data from the processer and checks for an EEG MU desync. It will then spawn another process/invoke a function to do classification"""
class SensorDetection:
    
    def __init__(self, dict1, sensor):
        self.train=dict1[sensor]
        self.data=None
        self.alldis=list()
    def run_detection(self):
        """Given a window of data this sets a threshold"""
        TC_CONSTANT=2
        Null=int()
        detected=int()
        for i in self.train:
            trainset=copy.copy(i)
            trainset=list(trainset)
            del trainset[-1]
            dis=ClassifyUtils.euclideandistance(self.data, trainset, len(trainset))
            dis1=tuple((i[-1], dis))
            self.alldis.append(dis1)
            self.alldis.sort(key=lambda tup:tup[1], reverse=False)
            #Now do some vote gettingi
        consideration=self.alldis[0:TC_CONSTANT-1]
        for i in consideration:
            if i[0]=="NULL":
                Null+=1
            else:
                detected+=1
        if Null>detected:print("NULL")
        else:print("Got a bite!")
    def update(self, data):
        self.data=data
def load(file):
    """Value building"""
    a=open(file, "r")
    end_dict=dict()
    bod=a.readlines()
    if not bod[0][0]=="#":
        raise RuntimeError("Improper File")
    num_of_decls=int()
    for i in bod:
        if i[0]=="#":
            num_of_decls+=1
    for i in range(num_of_decls):
        currsens=bod[0].split(sep=",")[1]
        classoftrain=bod[0].split(sep=",")[2]
        legnthoftrain=bod[0].split(sep=",")[3]
        del bod[0]
        if not currsens in end_dict.keys():
            end_dict[currsens]=[]
        tree=bod[0:int(legnthoftrain)]
        tree=list(map(float, tree))
        tree.append(classoftrain)
        tree=tuple(tree)
        end_dict[currsens].append(tree)
        del bod[0:int(legnthoftrain)]
    return end_dict
        
class DetectionEvent:
    def __init__(self, code, indx):
        self.code=code
        self.indx=int()
        
class AverageBasedDetector:
    def __init__(self, num):
        """src must be a method-bearing object"""
        self.data=dict()
        self.num=num
    def __getdirection(self, listy):
        iir_tc=0.98
        background=signal[0]
        hp=list()
        hp.append(0)
        for i in range(1, len(signal)):
            signal[i]=float(signal[i])
            background=(iir_tc*background)+(1-iir_tc)*signal[i]
            hp.append(signal[i]-background)
        return hp
    def update(self, data):
        """Add some data into the detector for detection"""
        self.data.update(data)
    def detect(self):
        self.diffs={"FC5":[], "FC6":[], "F4":[], "F3":[]}
        points=0
        for i in ["FC5","FC6", "F4", "F3"]:
            self.diffs[i]=self.__getdirection(self.data[i])
        for i in self.diffs.keys():
            points1=0
            for k in self.diffs[i]:
                if k<0 and not points1==self.num:
                    points1+=1
                elif points1==self.num:
                    points+=1
                    break
                else:
                    points1=0
        return [(points/4)]
class DesynchronisationDetector:
    def __init__(self):
        self.data_tree=list()
        self.baseline=float()
        self.accept=None
    def calibrate(self, data):
        self.baseline=statistics.mean(data)
        self.accept=Area(self.baseline,statistics.stdev(data))
    def detect(self,data, uname=DetectionEvent(0,0)):
        prev=data[0]
        detects=[]
        detectb=False
        count=0
        pending=0
        for i in data:
            if count==0:count+=1;continue
            elif (i-prev)<0 and not detectb:detectb=True;pending=count;print("Pending @"+str(pending)+"\t"+str(data[count]))
            elif(i-prev)<0 and detectb and not i in self.accept:detectb=False;print("Detected @"+str(pending)+"\t"+str(data[count]));detects.append(DetectionEvent(2, pending))
            elif (i-prev)>=0 and detectb and not i in self.accept:detectb=False;print("Cancelled @"+str(pending)+"\t"+str(data[count]))
            count+=1
        if detects:
            return [True]+detects
        else:
            return [False]
class ClassifyPackage:
    
class DesyncDetectionApp:
    def streamandqueuefriendly(self, dataInterface):
        """Data interface is a stream, queue, or file. Anything that can be read from. Additionally it is important that one supply a get method which will hand out samples"""
        while not datainterface.empty():
            j=datainterface.get()
                if self.detect[0]==True:
                    
                    
                    
            
            
class DataInterface:
    pass
        
        
        
        
        
        
class DesyncTester:
    def __init__(self):
        self.Detector=DesynchronisationDetector()
        self.data=eval(input("Put the data in list format:   "))
    def run(self):
        self.Detector.calibrate(self.data)
        self.Detector.detect(self.data)
if __name__=='__main__':
    a=DesyncTester()
    a.run()
    print(a.data)
    
                
                    
                    
                    
        
        
        
        
        
        
            
            
                
                
        
                           
                
                
            

    
        
        
       
        
        

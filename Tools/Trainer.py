"""Training Data Getter"""
import sys
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/KineticEEG")
import Preprocessers
import CSV_Extractor
import statistics
import CSVProc
class NoMovementError(Exception):
    pass
class DataProblem(Exception):
    pass
class NeutralNotTrained(Exception):
    pass
class CSVTrainer:
    def __init__(self, csv):
        self. SENSORS_OF_INTEREST=["F3", "F4", "FC5", "FC6"]
        self.a=CSVProc.CSVProc(CSV_Extractor.CSVExtractor(csv))
        self.neures={"FC5":{2:[], 3:[]}, "F3":{2:[], 3:[]}, "F4":{2:[], 3:[]}, "FC6":{2:[], 3:[]}}
        self.neureseq={"FC5":{2:[], 3:[]}, "F3":{2:[], 3:[]}, "F4":{2:[], 3:[]}, "FC6":{2:[], 3:[]}}
        self.armres={"FC5":{2:[], 3:[]}, "F3":{2:[], 3:[]}, "F4":{2:[], 3:[]}, "FC6":{2:[], 3:[]}}
        self.DEFAULT_NUMBER=5
        self.neutral_trained=bool(False)
    def __get_with_resolution(self, focuspoints, lis, clustersize):
        pts=int(len(lis)/focuspoints)
        indices=list(range(0, len(lis), pts))
        del indices[0]
        templist=list()
        for i in indices:
            templist.append(lis[i])
        return templist
    def smooth(self, signal):
        iir_tc=0.98
        background=signal[0]
        hp=list()
        hp.append(0)
        for i in range(1, len(signal)):
            signal[i]=float(signal[i])
            background=(iir_tc*background)+(1-iir_tc)*signal[i]
            hp.append(background)
        return hp
    def is_going_down(self, dat, time, sensor):
        """Look for downwardness. Since we are pretty certain that the """
        numberofvotes=int()
        start, end=time
        finalvote=int()
##        for i in ["FC5", "F3", "F4", "FC6"]:
        lowerbound, upperbound=(self.neures[sensor][2][0]-self.neures[sensor][2][1], self.neures[sensor][2][0]+self.neures[sensor][2][1])
        dat=dat[sensor][2][(start-4)*8:(end-4)*8]
        prev=dat[0]
        minimum=float()
        for i in dat:
                if i==prev:
                    continue
                if i>lowerbound:
                    if i<prev:
                        vote+=1
                    else:
                        vote-=1
                else:
                    return False
                if vote>=(float(0.9)*len(dat)):
                    finalvote+=1
        return finalvote, 
    def return_startingpoint(self, dat, time):
        j=self.a.get_with_settings(["FC5", "F3", "F4", "FC6"], ["Beta", "Mu"])
        for i in ["FC5", "F3", "F4", "FC6"]:
            for b in [2,3]:
                for r in j[i][b]:
                    pass
    def train_neutral(self,  time):
        """8 seconds"""
        j=self.a.get_with_settings(["FC5", "F3", "F4", "FC6"], ["Beta", "Mu"])
        start, end=time
        for i in ["FC5", "F3", "F4", "FC6"]:
            for b in [2, 3]:
                self.neures[i][b].append(statistics.mean(j[i][b][(start-4)*8:(end-4)*8]))
                self.neures[i][b].append(statistics.stdev(j[i][b][(start-4)*8:(end-4)*8]))
                self.neures[i][b].append(statistics.pvariance(j[i][b][(start-4)*8:(end-4)*8]))
                self.neureseq[i][b].append(self.__get_with_resolution(self.DEFAULT_NUMBER, j[i][b][(start-4)*8:(end-4)*8], 1))
    def train_arm(self, time):
        j=self.a.get_with_settings(["FC5", "F3", "F4", "FC6"], ["Beta", "Mu"])
        start, end=time
        for i in ["FC5", "F3", "F4", "FC6"]:
                for b in [2, 3]:
                    self.armres[i][b].append(self.__get_with_resolution(self.DEFAULT_NUMBER, j[i][b][(start-4)*8:(end-4)*8],1))
    def findit(self, time, sensor):
        j=self.a.get_with_settings(["FC5", "F3", "F4", "FC6"], ["Beta", "Mu"])
        start, end=time
        indx=0
        checknumber=5
        iout=False
        foundindex=None
        samelist=list()
        isfound=False
        if not self.neutral_trained:
            raise NeutralNotTrained("The neutral state must be trained for this to work")
        dat=j[sensor][2][(start-4)*8:(end-4)*8]
        number=len(dat)
        while not isfound and indx<number:
            samelist.append(dat[indx])
            if (dat[indx]>self.neures[sensor][2][0]-self.neures[sensor][2][1]) and iout:    ###and dat[indx]<self.neures[sensor][2][0]+self.neures[sensor][2][1]
                iout=False
            elif not (dat[indx]>self.neures[sensor][2][0]-self.neures[sensor][2][1]) and not iout:
                iout=True
                foundindex=indx
            elif not (dat[indx]>self.neures[sensor][2][0]-self.neures[sensor][2][1]) and iout and (dat[indx+1]<dat[indx]):
                if (indx-foundindex)>checknumber:
                    break
            indx+=1
        if foundindex is None:
            return -1
        else:
            return foundindex
        def findint(self, time, sensor):
            j=self.a.get_with_settings(["FC5", "F3", "F4", "FC6"], ["Beta", "Mu"])
            start, end=time
            indx=0
            data=j[sensor][2]
            checknumber=5
            sensor1=sensor
            iout=False
            foundindex=None
            samelist=list()
            found=False
            lit=list()
            for i in data:
                samelist.append(i)
                lit.append(statistics.mean(samelist))
            avg=0
            indx=0
            iout=False
            while not iout and indx<len(lit):
                if lit[indx+1]<lit[indx] and not iout:
                    iout=True
                    for i in range(indx, indx+5):
                        if lit[i+1]<lit[i]:
                            iout=True
                        else:
                            iout=False
                else:
                    i+=1
                if iout:
                    return avg
                else:
                    raise NoMovementError("No Movement found")
                
                    
    
                
                
                
        
        
            
        
                
                
            
            
            
        
        
        
        
        
        

                    
                    
                    
        
                               
        
        
                

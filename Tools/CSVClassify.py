"CSVClassifier.py"
import sys
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/Tools")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG")
import CSV_Proc
import statistics
import SLICERZ
import math
##import mscvrt



class TryClassifier:
    def __init__(self, file, otherfile):
        self.csv_proc_myfile=CSV_Proc.CSVProc(CSV_Proc.CSV_Extractor.CSVExtractor(file))
        self.csv_proc_otherfile=CSV_Proc.CSVProc(CSV_Proc.CSV_Extractor.CSVExtractor(otherfile))
    def train_and_run(self, indx1, indx2, sensors=["FC5"], bands=["Mu"]):
        assert type(indx1)==tuple and type(indx2)==tuple
        assert type(sensors)==list
        getdata=self.csv_proc_myfile.get_with_settings(sensors, bands)
        putdata=self.csv_proc_otherfile.get_with_settings(sensors, bands)
        self.classifier=SLICERZ.RunThroughClassifier(getdata)
        self.classifier.run_train(indx1[0], indx1[1])
        return (self.classifier.test_classifiers_ret(putdata, indx2 [0], indx2[1]))
        
        
if __name__=="__main__":
    import sys
    try:
        c=TryClassifier("C:/Users/Gaurav/Desktop/Gaurav_TIMED_4-4-13.03.16.15.57.05.CSV","C:/Users/Gaurav/Desktop/Gaurav_TIMED_4-4-13.03.16.15.57.05.CSV")
        g=[0,0,0,0]
        for i in range(4, 133):
            j=c.train_and_run(tuple((8*(29-4), 8*(31-4))), tuple((8*(i-4), 8*(i-2))), ["F3", "F4", "T7","T8"],["Mu"]) #89-91
            g.append(j)
        co=0
        for p in g:
            print(str(p*g[co+1])+"/t"+str(co))
##            if p==0:
##                co+=1
##                continue
            #print(str(abs((statistics.mean([p*g[co+1]]))))+"/t"+str(co)) #/abs((statistics.stdev([p, g[co+1]]))))))
            #print(str(p)+"/t"+str(co)) #/abs((statistics.stdev([p, g[co+1]]))))))
            co+=1
        #c.train_and_run(tuple((8*(62-4), 8*(64-4))), tuple((8*(89-4), 8*(91-4))), [ "T7",
                                                                                   #"T8", "F3", "F4"],["Mu"]) #89-91
    except:
        input("Click to exit")


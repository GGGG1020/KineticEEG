"""Training Data Getter"""
import sys
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/KineticEEG")
import Preprocessers
import CSV_Extractor
import statistics
import CSVProc
class CSVTrainer:
    def __init__(self, csv):
        self. SENSORS_OF_INTEREST=["F3", "F4", "FC5", "FC6"]
        self.a=CSVProc.CSVProc(CSV_Extractor.CSVExtractor(csv))
        self.neures={"FC5":{2:[], 3:[]}, "F3":{2:[], 3:[]}, "F4":{2:[], 3:[]}, "FC6":{2:[], 3:[]}}
        self.armres={"FC5":{2:[], 3:[]}, "F3":{2:[], 3:[]}, "F4":{2:[], 3:[]}, "FC6":{2:[], 3:[]}}
    def train_neutral(self,  time):
        """8 seconds"""
        j=self.a.get_with_settings(["FC5", "F3", "F4", "FC6"], ["Beta", "Mu"])
        start, end=time
        
        for i in ["FC5", "F3", "F4", "FC6"]:
            for b in [2, 3]:
                self.neures[i][b].append(statistics.mean(j[i][b][(start-4)*8:(end-4)*8]))
                self.neures[i][b].append(statistics.stdev(j[i][b][(start-4)*8:(end-4)*8]))
                self.neures[i][b].append(statistics.pvariance(j[i][b][(start-4)*8:(end-4)*8]))
    def train_arm(self, time):
        j=self.a.get_with_settings(["FC5", "F3", "F4", "FC6"], ["Beta", "Mu"])
        start, end=time
            for i in ["FC5", "F3", "F4", "FC6"]:
                for b in [2, 3]:
                    
                    
                    
        
                               
        
        
                

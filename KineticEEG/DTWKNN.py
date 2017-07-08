####DTAKNN

import ClassifyUtils
import fastdtw

class Sample:
    def __init__(self, data, label,sensor):
        self.data=data
        self.label=label
        self.sensors

class DTW_kNN:
    def __init__(self, k, actions):
        self.k=k
        self.actions=actions
        self.trset=list()
    def train(self, data:dict,label:str)->None:
        self.trset.append(Sample(data, label))
    def classify(self, data:dict)->str:
            
        
        

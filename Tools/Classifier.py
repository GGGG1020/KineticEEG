__author__="Gaurav Ghosal"
__version__="0.0.1"
import sys
sys.path.append("C:/Users/Gaurav/Documents/GitHub/KineticEEG/KineticEEG")
import pickle
import ClassifyUtils
class Classifier:
    Neutral=1
    Arm=2
    Kick=3
    def __init__(self, file):
        self.previous_state=Classifier.Neutral
        self.data_tree=dict()
        self.loadbasedata=open(file, "rb")
        self.training=pickle.loads(self.loadbasedata.read())
    def update(self, data):
        self.data_tree.update(data)
    def update_add(self, dictu):
        for i in other.keys():
            self.data_tree[i]=self.data_tree[i]+other[i]
    def classify(self):
        for i in self.data_tree.keys():
            current=self.training[i]
            
                
        
            




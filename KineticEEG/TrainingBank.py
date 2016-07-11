import pickle
import ClassifyUtils, statistics
class TrainingBank:
    def __init__(self, data_dict=None):
        """Data_dict is list of tuples like so:
              [('arm', {data_dict})]"""
        self.data_dict=data_dict or []
    @classmethod    
    def fromfile(cls, filename):
        f=open(filename, "rb")
        lst_of_dct=pickle.loads(f.read())
        return cls(data_dict=dct)
    def add_to_bank(self,action, data):
        self.data_dict.append(tuple((action, data)))
    def get_data_iter(self):
        return self.data_dict
    def filter_action(self, action):
        training_list=list()
        for i in self.data_dict:
            if i[0]==action:
                training_list.append(i)
        return training_list
class kNearest:
    """Distance function should be a function capable of taking in whatever data type the trainingbank consists of. No type checking is implemented.(Trainingbanktuple[0] should= movement type)"""
    def __init__(self, TBank, distancefunction:callable, high, k):
        self.TBank=TBank
        self.high=high
        self.distance_function=distancefunction
        self.k=k
    def get_classify_for_next_point(self, dpoint):
        sortd=sorted(self.TBank.get_data_iter(),key=lambda x:self.distance_function(dpoint, x), reverse=self.high)
        a=list()
        for i in range(self.k):
            a.append(sortd[i][0])
        try:
            j=statistics.mode(a)
        except statistics.StatisticsError:
            j="Neutral"
        return j

if __name__=='__main__':
    a=TrainingBank()
    a.add_to_bank("Arm", [1,2,3,4])
    a.add_to_bank("Kick", [1,3,5,7])
    a. add_to_bank("neutral", [1,2,2,-1])
    a.add_to_bank("Arm", [1,2,3,3.5])
    a.add_to_bank('Kick', [1,3.5, 5,7])
    a. add_to_bank("neutral", [1,2,2,-2])
    def modded_euclidean(inst1, inst2):
        return ClassifyUtils.euclideandistance(inst1, inst2[1], len(inst1))
    b=kNearest(a, modded_euclidean, False, 2)
    print(b.get_classify_for_next_point([1,2,4,5]))
        
            
        
        
        
        
        
        
    
                
        
        

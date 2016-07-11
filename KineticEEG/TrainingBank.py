import pickle

class TrainingBank:
    def __init__(self, data_dict=None):
        """Data_dict is list of tuples like so:
              [('arm', {data_dict})]"""
        self.data_dict=data_dict
    @classmethod    
    def fromfile(cls, filename):
        f=open(filename, "rb")
        lst_of_dct=pickle.loads(f.read())
        return cls(data_dict=dct)
    def filter_action(self, action):
        training_list=list()
        for i in self.data_dict:
            if i[0]==action:
                
        
        

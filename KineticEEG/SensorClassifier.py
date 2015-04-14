import ClassifyUtils
"""What we will get is a list/array containing the computed spectrum information.
The list will be like this:
>>>data=[delta, theta, alpha, beta, "class"]
trainingdata is a list of lists
"""
class SensorClassifier:
    """This classifies the sensor's information in a binary form"""
    def __init__(self,sensor,sensordata, trainingdata):
        "Initializer!"
        self. sensordatalegnth=len(sensordata)
        self.trainingdata=trainingdata[sensor]
        self.sensordata=sensordata
        self.delta_val=float(self.sensordata[0])
        self.theta_val=float(self.sensordata[1])
        self.alpha_val=float(self.sensordata[2])
        self.beta_val=float(self.sensordata[3])
        self.inst=list([self.delta_val, self.theta_val, self.alpha_val, self.beta_val])
    def get_neighbors(self,num):
        self.ds=list()
        leng=len(self.trainingdata)-1
        for i in range(len(self.trainingdata)):
            distance=ClassifyUtils.euclideandistance(self.inst, self.trainingdata[i],leng)
            self.ds.append((self.trainingdata[i], distance))
        self.ds.sort(key=lambda tup:tup[1])
        self.neighbors=list()
        for i in range(num):
            self.neighbors.append(self.ds[i][0])
    def get_responses(self):
        self.votes=dict()
        for i in range(len(self.neighbors)):
            vote=self.neighbors[i][-1]
            if vote in self.votes.keys():
                self.votes[vote]+=1
            else:
                self.votes.update({vote:1})
                
            
        
    
        
    
        
        
        
        
        

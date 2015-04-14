import ClassifyUtils
"""What we will get is a list/array containing the computed spectrum information.
The list will be like this:
>>>data=[delta, theta, alpha, beta, "class"]
trainingdata is a list of lists
"""



class SensorClassifier:
    """This classifies the sensor's information in a binary form"""
    def __init__(self,sensor,sensordata, trainingdata):
        self. sensordatalegnth=len(sensordata)
        self.sensordata=sensordata
        self.trainingdata=trainingdata
        self.delta_val=self.sensordata[0]
        self.theta_val=self.sensordata[1]
        self.alpha_val=self.sensordata[2]
        self.beta_val=self.sensordata[3]
    def get_neighbors(self, allneighbors, inst, num):
        ds=list()
        leng=len(allneighbors)-1
        for i in range(len(allneighbors)):
            distance=ClassifyUtils.euclideandistance((inst, allneighbors[i],leng))
            ds.append(allneighbors[i], distance)
        ds.sort(key=lambda tup:tup[1])
        neighbors=list()
        for i in range(num):
            neighbors.append(ds[x][0])
        return neighbors
        
    
        
        
        
        
        

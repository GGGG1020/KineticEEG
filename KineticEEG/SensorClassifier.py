import ClassifyUtils
"""What we will get is a list/array containing the computed spectrum information.
The list will be like this:
>>>data=[delta, theta, alpha, beta]
trainingdata is a list of lists
"""


class SensorClassifier:
    """This classifies the sensor's information in a binary form"""

    def __init__(self,sensor,sensordata, trainingdata):
        self. sensordatalegnth=len(sensordata)
        self.sensordata=sensordata
        self.delta_val=self.sensordata[0]
        self.theta_val=self.sensordata[1]
        self.alpha_val=self.sensordata[2]
        self.beta_val=self.sensordata[3]
        
        

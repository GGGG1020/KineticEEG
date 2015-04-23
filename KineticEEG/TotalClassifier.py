import SensorClassifier
import ClassifyUtils


class TotalClassifier:
    """This classifies ALL of the data"""
    def __init__(self):
        self.sensorclassifierlist=list()
        self.last_state=str("Nuetral")
        self.trainingdata=ClassifyUtils.load_trainingdata("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/Tests/testdata.dat")
        self.data=dict()
    def update_new_data(self, new_data):pass

    propert

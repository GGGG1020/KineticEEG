import SensorClassifier
import ClassifyUtils
class TotalClassifier:
    """This classifies ALL of the data
    Specifications for TotalClassifier:
    _____________________________

    (1)The dict of data given shall be a dict of the following format
    data={"AF3":[delta, theta, alpha, beta], FC5:[delta, theta, alpha, beta], ect.....}
    (2)A threshold is recommended to prevent slowness
    (3)......"""
    def __init__(self):
        self.sensorclassifierlist=list()
        self.last_state=str("Nuetral")
        self.trainingdata=ClassifyUtils.load_trainingdata("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/Tests/testdata.dat")
        self.data=dict()
        self.allvotes=list()
        self.vote_counts=dict()
        self.curr_state=str()
    def classify(self):
        self.sensorclassifierlist.clear()
        for i in self.data.keys():
            self.sensorclassifierlist.append(SensorClassifier(i, self.data[i], self.trainingdata))
        for i in self.sensorclassifierlist:
            i.getneighbors()
            r=i.get_responses()
            for b in r.keys():
                val=r[b]
                del r[b]
                r.update({val:b})
            vote=r[max(r.keys())]
            self.allvotes.append(vote)
        for k in ["Kick", "Arm", "Nuetral"]:
            self.vote_counts[k]=self.allvotes.count(k)
        self.vote_counts=dict((value, key) for key, value in self.vote_counts.iteritems())
        self.curr_state=self.vote_counts[max(self.vote_counts.keys())]
    def update_new_data(self, new_data):
        self.data=new_data
        


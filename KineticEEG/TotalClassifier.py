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
        self.vote_counts1=dict()
        self.vote_counts=dict()
        self.allvotes=list()
        for i in self.data.keys():
            self.sensorclassifierlist.append(SensorClassifier.SensorClassifier(i, self.data[i], self.trainingdata))
        for i in self.sensorclassifierlist:
            i.get_neighbors(1)
            i.get_responses()
            self.r=i.votes
            for b in self.r.keys():
                val=self.r[b]
                del self.r[b]
                self.r.update({val:b})
            vote=self.r[max(self.r.keys())]
            self.allvotes.append(vote)
        for k in ["kick\n", "arm\n", "nuetral\n"]:
            self.vote_counts[k]=self.allvotes.count(k)
        self.vote_counts1=dict((value, key) for key, value in iter(self.vote_counts.items()))
        self.curr_state=self.vote_counts1[max(self.vote_counts1.keys())]
        #if not self.curr_state=="Nuetral" and self.last_state=="Nuetral":
            #return "Nuetral"
            #self.last_state==self.curr_state
        #if# self.
        return self.curr_state
    def update_new_data(self, new_data):
        self.data=new_data
        

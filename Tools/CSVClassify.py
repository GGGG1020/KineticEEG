"CSVClassifier.py"
import sys
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/KineticEEG")
sys.path.append("C:/Users/Gaurav/My Documents/GitHub/KineticEEG/Tools")
import CSV_Extractor
import Preprocessers
class CSV_Classifier:
    """Takes data from CSV and classifier"""
    def __init__(self, file):
        self.extract=CSV_Extractor.CSVExtractor(file)
        self.processor=Preprocessers.DataProcessor()
        self.listolist=dict()
    def getwindow(self, sizeofwindow):
        for i in self.extract.sensor2column:
            graf=self.extract.get_data_from_sensor(i, sizeofwindow)
            self.listolist[i]=graf
    def preprocess(self):
        self.processor.update_data(self.listolist)
        self.processor.do_highpass()
        self.processor.do_hanning_wndow()
        self.processor.do_bin_power()
        self.processor.
        
class CSV_Trainer:
    """Gathers the nessecary data for doing the classification"""
    def __init__(self):pass

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
class CSV_Trainer:
    """Gathers the nessecary data for doing the classification"""
    def __init__(self):pass

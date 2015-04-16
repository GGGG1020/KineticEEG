import csv



class CSVExtractor:
    def __init__(self, file):
        self.sensor2column={"AF3":2, "F7":3, "F3":4,"FC5":5, "T7":6,"P7":7,"O1":8,"O2":9,"P8":10, "T8":11, "FC6":12,"F4":13,"F8":14,"AF4":15}
        self.fileob=open(file, "r")
        self.csv_read=csv.reader(self.fileob)
        
    def get_data_from_sensor(self, sensor, length):
        indx=self.sensor2column[sensor]
        list_of_vals=list()
        for i in range(length+1):
            curr_line=next(self.csv_read)
            if curr_line[0][0]=="t":
                pass
            else:
                list_of_vals.append(float(curr_line[indx])

                                    )
        return list_of_vals
    
        
                        

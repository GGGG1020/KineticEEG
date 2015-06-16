import csv
"""This is a tool to extract sensor reading data from the CSVs the the Emotiv Testbench Software provides"""
class CSVExtractor:
    def __init__(self, file):
        self.sensor2column={"AF3":2, "F7":3, "F3":4,"FC5":5, "T7":6,"P7":7,"O1":8,"O2":9,"P8":10, "T8":11, "FC6":12,"F4":13,"F8":14,"AF4":15}
        self.fileob=open(file, "r")
        self.csv_read=csv.reader(self.fileob)
        self.large_list=list()
        for i in self.csv_read:
            self.large_list.append(i)
        print(len(self.large_list))
        if self.large_list[0][0][0]=="t":
            del self.large_list[0]
            
##    def get_data_from_sensor(self, sensor, length):
##        indx=self.sensor2column[sensor]
##        list_of_vals=list()
##        for i in range(length+1):
##            curr_line=next(self.csv_read)
##            if curr_line[0][0]=="t":
##                pass
##            else:
##                list_of_vals.append(float(curr_line[indx]))
##        return list_of_vals
    def get256more(self,sensor):
        indx=self.sensor2column[sensor]
        listylist=list()
        for i in range(256):
            listylist.append(float(self.large_list[i][indx]))
            del self.large_list[i][indx]
        return listylist

        
        
    
        
                        

import csv
"""This is a tool to extract sensor reading data from the CSVs the the Emotiv Testbench Software provides"""
class CSVExtractor:
    def __init__(self, file):
        self.sensor2column={"AF3":2, "F7":3, "F3":4,"FC5":5, "T7":6,"P7":7,"O1":8,"O2":9,"P8":10, "T8":11, "FC6":12,"F4":13,"F8":14,"AF4":15}
        self.fileob=open(file, "r")
        self.file=file
        self.nicethingy=dict({'F3': [], 'FC5': [], 'T7': [], 'F7': [], 'P7': [], 'P8': [], 'AF4': [], 'O2': [], 'O1': [], 'T8': [], 'AF3': [], 'FC6': [], 'F4': [], 'F8': []})
        self.csv_read=csv.reader(self.fileob)
        self.large_list=list()
        indx=int(0)
        for i in self.csv_read:
            self.large_list.append(i)
        print(len(self.large_list))
        if self.large_list[0][0][0]=="t":
            del self.large_list[0]
        self.lennylen=len(self.large_list)
        #Now be nice to our friend at 0x058A18B0
        for i in self.large_list:
            for j in self.sensor2column:
                self.nicethingy[j].append(self.large_list[indx][self.sensor2column[j]])
            indx+=1
    def get_with_constraints(self,sensor, startpos, endpos):
        return self.nicethingy[sensor][startpos:endpos]
    
    def get_data_from_sensor(self, sensor, length):
        newfileob=open(self.file,"r")
        csv_read=csv.reader(newfileob)
        indx=self.sensor2column[sensor]
        list_of_vals=list()
        for i in range(length+1):
            ##print(i)
            curr_line=next(csv_read)
            if curr_line[0][0]=="t":
                pass
            else:
                list_of_vals.append(float(curr_line[indx]))
        return list_of_vals
    def get128more(self,sensor):
        indx=self.sensor2column[sensor]
        listylist=list()
        for i in range(128):
            listylist.append(float(self.nicethingy[sensor][0]))
            del self.nicethingy[sensor][0]
        return listylist 
    def get16more(self, sensor):
        listylist=list()
        for i in range(16):
            listylist.append(self.nicethingy[sensor][0])
            del self.nicethingy[sensor][0]
        return listylist
    
        
                        
